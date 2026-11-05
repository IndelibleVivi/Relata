"""Preserve the fixed diagnostic's computation and recorded-byte boundary."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


STUDY = Path(__file__).resolve().parents[1] / 'research' / 'authorization-continuity'
FILES = ('diagnose.py', 'fixtures.json', 'results.json', 'receipt.json')


class AuthorizationDiagnosticTests(unittest.TestCase):
    def run_check(self, study):
        return subprocess.run(
            [sys.executable, '-B', str(study / 'diagnose.py')],
            capture_output=True, text=True, timeout=15,
        )

    def test_saved_computation_and_receipt_are_current_and_read_only(self):
        before = {name: (STUDY / name).read_bytes() for name in FILES}
        result = self.run_check(STUDY)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['expected'], {'allow': 13, 'deny': 15, 'unknown': 4})
        self.assertTrue(all(report['checks'].values()))
        self.assertEqual(before, {name: (STUDY / name).read_bytes() for name in FILES})

    def test_changed_input_script_result_and_receipt_are_rejected(self):
        for target in FILES:
            with self.subTest(target=target), tempfile.TemporaryDirectory() as temp:
                study = Path(temp)
                for name in FILES:
                    shutil.copyfile(STUDY / name, study / name)
                path = study / target
                if target == 'diagnose.py':
                    path.write_text(path.read_text() + '\n# changed bytes, unchanged computation\n')
                elif target == 'fixtures.json':
                    value = json.loads(path.read_text())
                    value['evidence_boundary'] += ' Changed author metadata.'
                    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
                elif target == 'results.json':
                    path.write_text(path.read_text() + '\n')
                else:
                    value = json.loads(path.read_text())
                    value['all_invariants_passed'] = False
                    path.write_text(json.dumps(value, indent=2) + '\n')
                changed = path.read_bytes()
                result = self.run_check(study)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertRegex(result.stderr, 'Recorded results differ|Receipt integrity mismatch|Receipt metadata')
                self.assertEqual(path.read_bytes(), changed)


if __name__ == '__main__':
    unittest.main()
