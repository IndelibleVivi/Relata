"""Application, fixed instruments and actual loopback transport acceptance."""
import base64
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from relata_lab.application import Application
from relata_lab.core import Lab, LabError
from relata_lab.instruments import compute


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.app = Application(self.root / 'work')

    def tearDown(self):
        self.app.close()
        self.temp.cleanup()

    def test_three_instruments_persist_restart_replay_and_transfer(self):
        runs = []
        for suite, count in [('measurement', 7), ('applicability', 80), ('opportunity', 35)]:
            result = self.app.command('instrument.run', {'suite': suite}, suite)
            self.assertEqual(result['events'], count)
            self.assertEqual(result, self.app.command('instrument.run', {'suite': suite}, suite))
            self.assertEqual(self.app.lab.coverage(result['run']['id'])['counts']['returned'], count)
            runs.append(result['run'])
        before = self.app.state()
        self.assertEqual(len(before['observations']), 122)
        self.assertEqual(len(before['attempts']), 122)
        actions = [o for o in before['observations'] if o['content']['shape'] == 'action']
        self.assertTrue(actions)
        self.assertTrue(all(isinstance(o['content']['actions'], list) for o in actions))
        self.assertTrue(any(len(json.loads(o['content']['governing_history'])) > 3 for o in actions))
        self.assertNotIn('run_id', self.app.lab.public_projection([{'id': o['id'], 'revision': 1} for o in before['objects'] if o['kind'] == 'analysis'])['objects'][0]['body'])
        bundle = self.app.command('workspace.export', {'profile': 'research-transfer', 'selected': [{'id': runs[1]['id'], 'revision': 1}]}, 'transfer')
        archive = self.root / 'transfer.zip'
        archive.write_bytes(base64.b64decode(bundle['base64']))
        other = Lab.restore(archive, self.root / 'restored')
        try:
            self.assertEqual(other.coverage(runs[1]['id'])['planned'], 80)
            self.assertEqual(len(other.get_state()['observations']), 80)
        finally:
            other.close()
        self.app.close()
        self.app = Application(self.root / 'work')
        self.assertEqual(before, self.app.state())

    def test_strong_current_control_and_three_retirement_failures(self):
        app = compute('applicability')['analysis']['comparisons']
        for mode in ('formation', 'consumption'):
            scores = {r['policy']: r['matches'] for r in app if r['mode'] == mode}
            self.assertEqual(scores['current-only'], 7)
            self.assertGreater(scores['current-only'], scores['surface-rule'])
            self.assertGreater(scores['human-rule'], scores['global-disable'])
        opportunity = compute('opportunity')['analysis']
        reaccess = {r['reason']: r for r in opportunity['source_reaccess']}
        self.assertTrue(reaccess['allowed']['task_completed'])
        self.assertEqual(reaccess['budget']['read_count'], 0)
        self.assertEqual(reaccess['deadline']['read_count'], 0)
        self.assertEqual(reaccess['stale']['action'], 'clarify')
        results = {r['policy']: r for r in opportunity['opportunities']}
        self.assertEqual(results['task-ledger']['completed'], ['draft'])
        self.assertEqual(results['task-ledger']['invalid_attempts'], 0)
        self.assertEqual(results['surface-reminder']['invalid_attempts'], 3)
        self.assertEqual(len(set(results['surface-reminder']['invalid_events'])), 3)
        self.assertEqual(results['current-only']['completed'], [])
        global_event = next(e for e in compute('measurement')['events'] if e['operation'] == 'intersect')
        self.assertTrue(all('碰面' in text for text in global_event['input']['originals']))
        self.assertNotIn('a', global_event['input']['originals'])

    def test_selected_public_reader_has_saved_sources_but_no_private_dependency(self):
        source = self.app.command('source.capture', {'title': 'Public source', 'text': '<script>alert(1)</script> exact source', 'visibility': 'public'}, 'source')
        hidden = self.app.command('object.create', {'kind': 'source', 'title': 'SECRET-TITLE', 'body': {'text': 'SECRET-BODY'}}, 'hidden')
        claim = self.app.command('object.create', {'kind': 'claim', 'title': 'Conditional claim', 'body': {'text': 'A claim', 'limits': ['Unreviewed']}, 'visibility': 'public', 'refs': [{'id': source['id'], 'revision': 1, 'relation': 'supports'}, {'id': hidden['id'], 'revision': 1, 'relation': 'challenges'}]}, 'claim')
        result = self.app.command('publication.preview', {'selected': [{'id': claim['id'], 'revision': 1}], 'title': 'Reading edition'}, 'preview')
        self.assertEqual(len(result['inventory']), 2)
        self.assertIn('&lt;script&gt;', result['html'])
        self.assertNotIn('<script>', result['html'])
        self.assertIn('exact source', result['html'])
        for secret in ('SECRET-TITLE', 'SECRET-BODY', hidden['id']):
            self.assertNotIn(secret, json.dumps(result))
        self.app.command('object.revise', {'id': source['id'], 'expected_revision': 1, 'body': {'text': 'new version'}}, 'source-update')
        self.assertEqual(result, self.app.command('publication.preview', {'selected': [{'id': claim['id'], 'revision': 1}], 'title': 'Reading edition'}, 'preview-again'))
        with self.assertRaises(LabError):
            self.app.command('publication.preview', {'selected': [{'id': hidden['id'], 'revision': 1}], 'title': 'Denied'}, 'deny')

    def test_private_legacy_source_cannot_be_relabelled_public(self):
        source = self.app.command('object.create', {'kind': 'source', 'title': 'Legacy',
            'body': {'format': 'relata-legacy-compat-source-1'}, 'visibility': 'public'}, 'legacy')
        with self.assertRaisesRegex(LabError, 'private bindings'):
            self.app.lab.public_projection([{'id': source['id'], 'revision': 1}])

    def test_catalog_snapshots_survive_imported_model_and_reopen(self):
        catalog = self.app.command('catalog.install', {}, 'catalog')
        self.assertEqual(len(catalog['snapshots']), 10)
        first = catalog['snapshots'][0]
        raw = self.app.lab.read_artifact(first['body']['artifact_digest'])
        model = json.loads(raw)['models'][0]
        model['summary'] += ' Synthetic revision for restoration check.'
        other = self.app.command('snapshot.import', {'model': model}, 'import')
        self.assertEqual(other['visibility'], 'private')
        self.assertNotEqual(first['body']['artifact_digest'], other['body']['artifact_digest'])
        self.assertEqual(self.app.lab.read_artifact(first['body']['artifact_digest']), raw)
        self.assertEqual(len(self.app.state()['snapshot_versions']), 11)

    def test_articles_are_revisioned_author_objects(self):
        result = self.app.command('library.examples', {}, 'articles')
        self.assertEqual(len(result['articles']), 2)
        again = self.app.command('library.examples', {}, 'articles-2')
        self.assertEqual(result, again)
        self.assertTrue(all('text' in a['body'] and a['visibility'] == 'public' for a in result['articles']))


class LoopbackTests(unittest.TestCase):
    def test_host_origin_token_and_literal_artifact_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            process = subprocess.Popen([sys.executable, '-B', str(ROOT / 'tools/relata_lab.py'), '--workspace', str(Path(temp) / 'work'), 'serve', '--port', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                line = process.stdout.readline().strip()
                self.assertIn('http://127.0.0.1:', line, process.stderr.read() if process.poll() is not None else 'startup did not return its address')
                base = line.split(' ', 2)[-1]
                def call(path, data=None, headers=None):
                    req = urllib.request.Request(base + path, data=data, headers=headers or {})
                    try:
                        response = urllib.request.urlopen(req, timeout=10)
                    except urllib.error.HTTPError as err:
                        response = err
                    return response.status, response.headers, response.read()
                code, headers, body = call('/')
                self.assertEqual(code, 200)
                token = re.search(r'name="relata-token" content="([^"]+)"', body.decode())[1]
                self.assertEqual(call('/api/state')[0], 403)
                self.assertEqual(call('/api/state', headers={'X-Relata-Token': token, 'Origin': 'https://example.invalid'})[0], 403)
                self.assertEqual(call('/', headers={'Host': 'evil.invalid'})[0], 403)
                self.assertEqual(call('/api/state', headers={'X-Relata-Token': token})[0], 200)
                payload = json.dumps({'name': 'artifact.put', 'payload': {'text': '<svg onload="alert(1)"></svg>', 'media_type': 'image/svg+xml'}, 'command_id': 'blob'}).encode()
                code, _, data = call('/api/command', payload, {'X-Relata-Token': token, 'Content-Type': 'application/json'})
                self.assertEqual(code, 200)
                digest = json.loads(data)['digest']
                code, hdr, raw = call('/api/artifact/' + digest, headers={'X-Relata-Token': token})
                self.assertEqual(hdr.get_content_type(), 'text/plain')
                self.assertEqual(hdr['X-Content-Type-Options'], 'nosniff')
                self.assertIn(b'<svg', raw)
                self.assertEqual(call('/../../AGENTS.md')[0], 404)
                self.assertEqual(call('/legacy-clinic.html')[1].get_content_type(), 'application/octet-stream')
            finally:
                process.terminate()
                process.communicate(timeout=10)


if __name__ == '__main__':
    unittest.main()
