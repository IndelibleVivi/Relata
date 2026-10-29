"""Author an interpretation, preserve its revisions and inspect its public boundary."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from relata_lab.application import Application
from relata_lab.core import Lab


class AnalysisBrowserTests(unittest.TestCase):
    def test_authored_analysis_to_public_claim(self):
        check = subprocess.run(['node', '-e', "try{require.resolve('playwright')}catch{process.exit(42)}"], cwd=ROOT)
        if check.returncode == 42:
            self.skipTest('Playwright unavailable; set NODE_PATH to bundled runtime packages')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            output = Path(os.environ.get('RELATA_ANALYSIS_QA_OUTPUT', str(root / 'screenshots')))
            output.mkdir(parents=True, exist_ok=True)
            workspace = root / 'workspace'
            app = Application(workspace)
            def command(name, **payload):
                return app.command(name, payload, name + str(len(app.lab.get_state()['objects'])) + str(counter.pop()))
            counter = list(range(30))
            study = command('object.create', kind='study', title='经验适用性 · 作者示例', body={'text':'表面相同，用途是否相同？'})
            def new_run(title):
                return command('run.create', title=title, study={'id':study['id'],'revision':1}, trajectories=[{'id':'history','label':'同一合成历史'}], positions=[{'id':'p1','trajectory_id':'history','condition':'purpose changed','checkpoint':'1'},{'id':'p2','trajectory_id':'history','condition':'empty','checkpoint':'2'}])
            run = new_run('已有观察的运行')
            other = new_run('尚无观察的另一运行')
            observation = command('observation.record', run_id=run['id'], position_ids=['p1'], content={'transport':'completed','shape':'text','text':'这次仍沿用了旧的语气。','input':'这次只取事实，不沿用上次的口吻。','governing_history':'先前用于共同创作，现在用于事实整理。'}, provenance={'kind':'authored synthetic acceptance'})
            empty = command('observation.record', run_id=run['id'], position_ids=['p2'], content={'transport':'completed','shape':'empty','text':'','input':'继续检查空返回。','governing_history':'作者合成历史'}, provenance={'kind':'authored synthetic acceptance'})
            review_round = command('round.create', title='作者测试首评', protocol='delivered-input-2', observation_ids=[observation['id'],empty['id']], contract={'question':'当前材料允许怎样解释？'}, **{'pass':'first'})
            review = command('review.submit', round_id=review_round['id'], observation_id=observation['id'], reviewer='synthetic-reviewer', judgment={'response_act':'answer','mapping':'unmapped','rationale':'旧方法可能被过度沿用，当前尚不能确定。'})
            seed = root / 'seed.json'
            seed.write_text(json.dumps({'study':study['id'],'run':run['id'],'otherRun':other['id'],'observation':observation['id'],'empty':empty['id'],'review':review['id']}))
            app.close()
            process = subprocess.Popen([sys.executable,'-B',str(ROOT/'tools/relata_lab.py'),'--workspace',str(workspace),'serve','--port','0'], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                line = process.stdout.readline().strip()
                if not line:
                    _, errors = process.communicate(timeout=10)
                    self.fail('Studio did not start: ' + errors)
                base = line.split(' ',2)[-1]
                result = subprocess.run(['node','tests/analysis_browser.cjs',base,str(output),str(seed)], cwd=ROOT, capture_output=True,text=True,timeout=120)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            finally:
                process.terminate()
                process.communicate(timeout=10)
            receipt = json.loads((output/'analysis-result.json').read_text())
            restored = Lab.restore(output/'analysis-transfer.zip',root/'restored')
            try:
                first = restored.get_object(receipt['analysisId'],1)
                latest = restored.get_object(receipt['analysisId'])
                self.assertEqual(latest['revision'],2)
                self.assertIn('当前目的已经改变',first['body']['text'])
                self.assertEqual(len(first['body']['limits']),2)
                self.assertIn('无法区分',latest['body']['text'])
                self.assertEqual(len(restored.get_state()['reviews']),2)
                self.assertEqual(len(restored.get_state()['runs']),1)
                self.assertEqual(restored.get_state()['working'],[])
            finally:
                restored.close()


if __name__ == '__main__':
    unittest.main()
