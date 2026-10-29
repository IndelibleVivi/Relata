"""Three complete local user journeys using an isolated bundled Chromium profile."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from relata_lab.core import Lab
from tools import future_question_review as future_review


class StudioBrowserTests(unittest.TestCase):
    def test_research_review_publication_and_restore(self):
        available = subprocess.run(['node', '-e', "try{require.resolve('playwright')}catch{process.exit(42)}"], cwd=ROOT)
        if available.returncode == 42:
            self.skipTest('Playwright unavailable; set NODE_PATH to bundled runtime packages')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            # An explicit output path can retain screenshots for visual QA; research stays temporary.
            output = Path(os.environ.get('RELATA_QA_OUTPUT', str(root / 'evidence')))
            output.mkdir(parents=True, exist_ok=True)
            workspace = root / 'workspace'
            def start():
                process = subprocess.Popen([sys.executable, '-B', str(ROOT / 'tools/relata_lab.py'), '--workspace', str(workspace), 'serve', '--port', '0'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                line = process.stdout.readline().strip()
                if not line:
                    _, errors = process.communicate(timeout=10)
                    self.fail('Studio did not start: ' + errors)
                return process, line.split(' ', 2)[-1]
            future = root / 'future'
            future_review.prepare(future)
            input_id = next(iter(future_review.inspect_packet(future)['by_id']))
            responses = root / 'responses.json'
            responses.write_text(json.dumps({'format': 'relata-future-question-responses-2', 'provenance': 'synthetic browser acceptance', 'records': [{'input_id': input_id, 'attempt_id': 'A-' + '1' * 32, 'previous_attempt': None, 'status': 'completed', 'response': '', 'failure': None}]}))
            future_review.import_responses(future, responses)
            future_export = root / 'future-export'
            future_review.export_review(future, future_export)
            item = next((future_export / 'items').glob('*.json'))
            process, base = start()
            try:
                result = subprocess.run(['node', 'tests/studio_browser.cjs', base, str(output), str(item)], cwd=ROOT, text=True, capture_output=True, timeout=180)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('"status":"pass"', result.stdout)
            finally:
                process.terminate()
                process.communicate(timeout=10)
            future_review.import_reviews(future, future_export, output / 'future-question-reviews.json')
            self.assertEqual(len(future_review.inspect_packet(future)['reviews']), 1)
            # The process is genuinely closed before reading and restoring canonical data.
            lab = Lab(workspace)
            before = lab.get_state()
            lab.close()
            backup = Lab.restore(output / 'workspace-backup.zip', root / 'backup-restored')
            try:
                # Backup may precede the final reading-position autosave; evidence is identical.
                for key in ('objects', 'observations', 'reviews', 'attempts'):
                    self.assertEqual(before[key], backup.get_state()[key])
            finally:
                backup.close()
            transfer = Lab.restore(output / 'research-transfer.zip', root / 'transfer-restored')
            try:
                self.assertEqual(len(transfer.get_state()['runs']), 1)
                self.assertEqual(len(transfer.get_state()['observations']), 1)
                run = transfer.get_state()['runs'][0]
                self.assertEqual(run['body']['study']['revision'], 1)
                self.assertEqual(transfer.get_object(run['body']['study']['id'])['revision'], 2)
                self.assertEqual(transfer.coverage(run['id'])['counts']['returned'], 3)
                self.assertTrue(any(a['state'] == 'uncertain' for a in transfer.get_state()['attempts']))
            finally:
                transfer.close()
            process, base = start()
            try:
                smoke = r"""
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({headless:true});try{const p=await b.newPage();await p.goto(process.argv[1]+'/#desk');await p.locator('.thread-row').first().click();await p.locator('#thread-text').waitFor();if(!(await p.locator('#thread-text').inputValue()).includes('观察与解释'))throw Error('draft did not survive restart');}finally{await b.close();}})().catch(e=>{console.error(e);process.exitCode=1});
"""
                check = subprocess.run(['node', '-e', smoke, base], cwd=ROOT, text=True, capture_output=True, timeout=45)
                self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            finally:
                process.terminate()
                process.communicate(timeout=10)


if __name__ == '__main__':
    unittest.main()
