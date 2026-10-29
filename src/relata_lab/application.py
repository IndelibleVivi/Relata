"""Local application actions shared by the CLI and HTTP transport."""
from __future__ import annotations

import json
import re
from pathlib import Path
import subprocess
import tempfile

from .core import Lab, LabError
from . import instruments
from .publication import preview

REPO = Path(__file__).resolve().parents[2]
ATLAS = REPO / 'systems' / 'architecture-atlas'


def install_catalog(lab, command_id):
    installed = []
    for path in sorted((ATLAS / 'models').glob('*.json')):
        model = json.loads(path.read_text())
        ident = 'catalog-' + model['id'] + '-' + model['commit'][:12]
        existing = [o for o in lab.list_objects('snapshot') if o['id'] == ident]
        process = subprocess.run(['node', str(ATLAS / 'studio-payload.cjs'), '--project', model['id']],
                                 cwd=REPO, text=True, capture_output=True, timeout=60, check=True)
        json.loads(process.stdout)
        artifact = lab.command('artifact.put', {'text': process.stdout, 'media_type': 'application/json'}, command_id + ':' + ident + ':blob')
        body = {'project': model['id'], 'commit': model['commit'], 'boundary': model['boundary'],
                     'summary': model['summary'], 'sources': model['sources'],
                     'artifact_digest': artifact['digest'], 'evidence': 'source-inspected',
                     'source_availability': 'external', 'reading_scope': 'pinned public model; upstream source not bundled'}
        if existing and existing[0]['body'] == body:
            installed += existing
            continue
        payload = {'id': ident, 'title': model['name'], 'body': body, 'visibility': 'public'}
        if existing:
            payload['expected_revision'] = existing[0]['revision']
        else:
            payload['kind'] = 'snapshot'
        obj = lab.command('object.revise' if existing else 'object.create', payload, command_id + ':' + ident)
        installed.append(obj)
    return {'snapshots': installed}


def import_snapshot(lab, model, command_id):
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / 'model.json'
        path.write_text(json.dumps(model, ensure_ascii=False))
        process = subprocess.run(['node', str(ATLAS / 'studio-payload.cjs'), '--project', model['id'],
                                  '--model-file', str(path)], cwd=REPO, text=True,
                                 capture_output=True, timeout=60, check=True)
    artifact = lab.command('artifact.put', {'text': process.stdout, 'media_type': 'application/json'}, command_id + ':blob')
    return lab.command('object.create', {'kind': 'snapshot', 'title': model['name'], 'body': {
        'project': model['id'], 'commit': model['commit'], 'summary': model['summary'],
        'boundary': model['boundary'], 'artifact_digest': artifact['digest'], 'sources': model['sources'],
        'evidence': 'source-inspected; imported author model, not independent verification',
        'reading_scope': 'validated atlas model; upstream bytes external'}, 'visibility': 'private'}, command_id + ':snapshot')


def source_capture(lab, payload, command_id):
    """No URL fetch or path read: store only text deliberately supplied by the author."""
    artifact = lab.command('artifact.put', {'text': payload['text'], 'media_type': 'text/plain'}, command_id + ':artifact')
    return lab.command('object.create', {'kind': 'source', 'title': payload['title'],
        'body': {'artifact_digest': artifact['digest'], 'origin': payload.get('origin', ''),
                 'version': payload.get('version', 'author capture'), 'reading_scope': payload.get('reading_scope', ''),
                 'capture': 'author-supplied text; identity not independently verified'},
        'visibility': payload.get('visibility', 'private')}, command_id + ':source')


class Application:
    def __init__(self, workspace):
        self.lab = Lab(Path(workspace))

    def command(self, name, payload, command_id):
        if name == 'legacy.read':
            from .compat import read_legacy
            return read_legacy(self.lab, payload['id'])
        if name == 'analysis.context':
            from .analysis import context
            return context(self.lab, payload['run_id'])
        if name == 'catalog.install':
            return install_catalog(self.lab, command_id)
        if name == 'source.capture':
            return source_capture(self.lab, payload, command_id)
        if name == 'snapshot.import':
            return import_snapshot(self.lab, payload['model'], command_id)
        if name == 'instrument.run':
            return instruments.run(self.lab, payload['suite'], command_id)
        if name == 'library.examples':
            results = []
            for stem in ('collection-delivery-comparison', 'finite-instrument-report'):
                path = REPO / 'research' / (stem + '.md')
                text = path.read_text()
                ident = 'article-' + stem
                existing = next((o for o in self.lab.list_objects() if o['id'] == ident), None)
                body = {'text': text, 'origin': 'research/' + path.name,
                        'evidence': 'authored source synthesis / deterministic computation; see article limits'}
                refs = []
                for link in dict.fromkeys(re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)):
                    target = link.split('#')[0]
                    if not target or '://' in target or target.startswith('#'):
                        continue
                    material = (path.parent / target).resolve()
                    if not material.is_relative_to(REPO) or material.suffix not in {'.md', '.json', '.py'}:
                        continue
                    relative = material.relative_to(REPO).as_posix()
                    # Only these authored/public source surfaces belong to the bundled works.
                    if not relative.startswith(('systems/source-studies/', 'systems/architecture-atlas/', 'research/', 'src/relata_lab/', 'tools/')):
                        continue
                    ignored = subprocess.run(['git', 'check-ignore', '-q', '--', relative], cwd=REPO)
                    if ignored.returncode == 0 or not material.is_file():
                        raise LabError('disclosure', 'Article dependency is unavailable or ignored: ' + relative)
                    artifact = self.lab.command('artifact.put', {'text': material.read_text(), 'media_type': 'text/plain'}, command_id + ':' + stem + ':' + relative + ':blob')
                    sid = 'article-source-' + re.sub(r'[^a-zA-Z0-9-]', '-', relative)
                    old = next((o for o in self.lab.list_objects() if o['id'] == sid), None)
                    source_body = {'artifact_digest': artifact['digest'], 'origin': relative,
                                   'version': 'authored source frozen at import', 'reading_scope': 'complete referenced repository file'}
                    if old and old['body'] == source_body:
                        source = old
                    else:
                        source_payload = {'id': sid, 'title': material.name, 'body': source_body, 'visibility': 'public'}
                        if old:
                            source_payload['expected_revision'] = old['revision']
                        else:
                            source_payload['kind'] = 'source'
                        source = self.lab.command('object.revise' if old else 'object.create', source_payload, command_id + ':' + stem + ':' + relative)
                    refs.append({'id': source['id'], 'revision': source['revision'], 'relation': 'source'})
                if existing and existing['body'] == body and existing['refs'] == refs:
                    results.append(existing)
                    continue
                payload = {'id': ident, 'title': text.splitlines()[0].lstrip('# '), 'body': body, 'refs': refs, 'visibility': 'public'}
                if existing:
                    payload['expected_revision'] = existing['revision']
                else:
                    payload['kind'] = 'claim'
                results.append(self.lab.command('object.revise' if existing else 'object.create', payload, command_id + ':' + stem))
            return {'articles': results}
        if name == 'publication.preview':
            return preview(self.lab, payload['selected'], payload['title'])
        if name == 'review.export':
            return self.lab.export_round(payload['round_id'])
        if name == 'review.journal':
            return self.lab.import_reviews(payload['packet'], payload['records'], command_id)
        if name == 'workspace.export':
            profile = payload['profile']
            with tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / ('publication.json' if profile == 'public-publication' else 'research.zip')
                if profile == 'workspace-backup':
                    self.lab.backup(target)
                elif profile in ('research-transfer', 'public-publication'):
                    self.lab.export_bundle(target, profile, payload.get('selected', []))
                else:
                    raise LabError('invalid', 'Unsupported workspace export profile.')
                import base64
                return {'profile': profile, 'filename': profile + ('.json' if profile == 'public-publication' else '.zip'),
                        'base64': base64.b64encode(target.read_bytes()).decode('ascii')}
        return self.lab.command(name, payload, command_id)

    def state(self):
        state = self.lab.get_state()
        state['catalog'] = [{'id': k, 'title': v[0], 'description': v[1]} for k, v in instruments.CATALOG.items()]
        state['coverage'] = {run['id']: self.lab.coverage(run['id']) for run in state['runs']}
        state['snapshot_versions'] = [self.lab.get_object(o['id'], revision)
                                      for o in state['objects'] if o['kind'] == 'snapshot'
                                      for revision in range(1, o['revision'] + 1)]
        return state

    def close(self):
        self.lab.close()
