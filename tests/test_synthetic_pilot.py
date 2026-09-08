"""All data is public synthetic; deny network and arbitrary process creation in rehearsals."""
import ast
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import synthetic_pilot as p
from tools.synthetic_subject import ScriptedSubject


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.output = self.root / "run"

    def tearDown(self):
        self.temp.cleanup()

    def run_bundle(self):
        with patch("socket.socket", side_effect=AssertionError("network forbidden")), \
             patch("subprocess.Popen", side_effect=AssertionError("process forbidden")):
            return p.run(self.output, seed=7)

    def trials(self):
        manifest = p.read_json(self.output / "run.json")
        return [(self.output / "trials" / (identity + ".json")) for identity in manifest["planned_ids"]]

    def test_complete_matrix_without_network_or_processes(self):
        self.assertEqual(self.run_bundle()["status"], "completed")
        result = p.verify(self.output)
        self.assertEqual(result["trial_statuses"], {"completed": 10})
        self.assertIsNone(result["score"])
        for path in self.trials():
            trial = p.read_json(path)
            should_know = trial["condition"] not in {"current-only", "no-memory"}
            self.assertEqual(trial["checks"]["expected_location_present"], should_know)
            self.assertFalse(trial["checks"]["other_location_present"])
            self.assertEqual(trial["checks"]["case_decision"], "unreviewed")

    def test_identical_no_history_and_probe_views(self):
        a, b = p.fixture("A"), p.fixture("B")
        self.assertEqual(p.input_tape(a, "current-only"), p.input_tape(b, "current-only"))
        for condition in p.CONDITIONS:
            self.assertEqual(p.input_tape(a, condition)[-1], p.input_tape(b, condition)[-1])
        a["history"][0]["text"] = b["history"][0]["text"]
        self.assertEqual(a["history"], b["history"])

    def test_gold_metadata_does_not_reach_subject(self):
        case = p.fixture("A")
        before = p.input_tape(case, "scripted-native")
        case["world"] = "HIDDEN-WORLD"
        case["evidence_contract"] = {"gold": "EVALUATOR-ONLY-CANARY"}
        case["secret"] = "EVALUATOR-ONLY-CANARY"
        self.assertEqual(before, p.input_tape(case, "scripted-native"))
        for entry in before:
            self.assertEqual(set(entry), {"operation", "text"})
        with self.assertRaises(ValueError):
            ScriptedSubject().receive({"operation": "probe", "text": p.PROBE, "gold": "x"})

    def test_history_is_not_shared_between_instances(self):
        a, b = ScriptedSubject(), ScriptedSubject()
        a.receive({"operation": "observe", "text": p.fixture("A")["history"][0]["text"]})
        self.assertIn(p.LOCATIONS["A"], a.receive({"operation": "probe", "text": p.PROBE}))
        self.assertNotIn(p.LOCATIONS["A"], b.receive({"operation": "probe", "text": p.PROBE}))

    def test_session_reset_and_no_memory(self):
        for retain in (True, False):
            subject = ScriptedSubject(retain=retain)
            for message in p.input_tape(p.fixture("A"), "scripted-native"):
                response = subject.receive(message)
            self.assertEqual(p.LOCATIONS["A"] in response, retain)

    def test_review_retains_contract_but_hides_identity_and_expected_label(self):
        self.run_bundle()
        packet = p.read_json(self.output / "review-packet.json")
        self.assertEqual(len(packet), 10)
        for entry in packet:
            self.assertIn("evidence_contract", entry)
            self.assertEqual(len(entry["event_evidence"]), 6)
            self.assertEqual(entry["probe"], p.PROBE)
            for hidden in ("condition", "world", "case_id", "subject", "checks", "expected_label"):
                self.assertNotIn(hidden, entry)
            self.assertIsNone(entry["decision"])

    def test_fixture_quote_is_only_literal_not_semantic_success(self):
        case = p.fixture("A")
        checks = p.literal_checks("绝对不是" + p.LOCATIONS["A"], case)
        self.assertTrue(checks["expected_location_present"])
        self.assertIsNone(checks["capability_claim"])
        self.assertEqual(checks["case_decision"], "unreviewed")

    def test_existing_output_is_not_overwritten(self):
        self.output.mkdir()
        sentinel = self.output / "sentinel"
        sentinel.write_text("unchanged")
        with self.assertRaises(FileExistsError):
            p.run(self.output)
        self.assertEqual(sentinel.read_text(), "unchanged")

    def test_symlink_output_and_parent_are_rejected(self):
        target = self.root / "target"
        target.mkdir()
        link = self.root / "link"
        link.symlink_to(target, target_is_directory=True)
        for output in (link, link / "child"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                p.run(output)
        self.assertEqual(list(target.iterdir()), [])

    def test_missing_parent_is_not_created(self):
        with self.assertRaises(ValueError):
            p.run(self.root / "missing" / "run")
        self.assertFalse((self.root / "missing").exists())

    def test_error_preserved_and_other_trials_continue(self):
        original = ScriptedSubject.receive
        seen = False
        def fail_once(subject, message):
            nonlocal seen
            if message["operation"] == "probe" and not seen:
                seen = True
                raise RuntimeError("not logged: private exception canary")
            return original(subject, message)
        with patch.object(ScriptedSubject, "receive", fail_once):
            manifest = self.run_bundle()
        self.assertEqual(manifest["status"], "complete-with-errors")
        self.assertEqual(p.verify(self.output)["trial_statuses"], {"error": 1, "completed": 9})
        contents = "".join(path.read_text() for path in self.trials())
        self.assertNotIn("private exception canary", contents)
        errored = next(p.read_json(path) for path in self.trials() if p.read_json(path)["status"] == "error")
        self.assertIsNone(errored["checks"])
        self.assertEqual(errored["observations"][-1]["status"], "attempted")

    def test_invalid_response_is_execution_error_not_low_score(self):
        original = ScriptedSubject.receive
        def invalid(subject, message):
            return {"answer": "bad type"} if message["operation"] == "probe" else original(subject, message)
        with patch.object(ScriptedSubject, "receive", invalid):
            self.run_bundle()
        self.assertEqual(p.verify(self.output)["trial_statuses"], {"error": 10})
        self.assertEqual(p.read_json(self.output / "review-packet.json"), [])

    def test_interruption_is_not_fabricated_as_completion(self):
        with patch.object(ScriptedSubject, "receive", side_effect=KeyboardInterrupt):
            manifest = self.run_bundle()
        self.assertEqual(manifest["status"], "interrupted")
        result = p.verify(self.output)
        self.assertEqual(result["trial_statuses"], {"interrupted": 1, "not-run": 9})
        self.assertEqual(result["semantic_reviews_pending"], 0)

    def test_unsealed_crash_is_rejected(self):
        self.run_bundle()
        (self.output / "integrity.json").unlink()
        with self.assertRaises(ValueError):
            p.verify(self.output)

    def test_byte_tamper_is_rejected(self):
        self.run_bundle()
        path = self.trials()[0]
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            p.verify(self.output)

    def mutate_and_reseal(self, mutate):
        self.run_bundle()
        path = self.trials()[0]
        trial = p.read_json(path)
        mutate(trial)
        p.atomic_json(path, trial)
        p.seal(self.output)
        with self.assertRaises(ValueError):
            p.verify(self.output)

    def test_reordered_steps_fail_even_with_new_hashes(self):
        self.mutate_and_reseal(lambda t: t["observations"].reverse())

    def test_wrong_trial_id_fails_even_with_new_hashes(self):
        self.mutate_and_reseal(lambda t: t.update(id="0" * 32))

    def test_missing_probe_fails_even_with_new_hashes(self):
        self.mutate_and_reseal(lambda t: t["observations"].pop())

    def test_tampered_diagnostic_fails_even_with_new_hashes(self):
        self.mutate_and_reseal(lambda t: t["checks"].update(case_decision="pass"))

    def test_injected_gold_field_fails_even_with_new_hashes(self):
        self.mutate_and_reseal(lambda t: t["observations"][0]["input"].update(gold="A"))

    def test_changed_source_evidence_fails_even_with_new_hashes(self):
        self.mutate_and_reseal(lambda t: t["case"]["history"][0].update(text="changed"))

    def test_duplicate_cells_fail_even_with_new_hashes(self):
        self.run_bundle()
        paths = self.trials()
        first = p.read_json(paths[0])
        other = p.read_json(paths[1])
        first["case"], first["condition"] = other["case"], other["condition"]
        p.atomic_json(paths[0], first)
        p.seal(self.output)
        with self.assertRaises(ValueError):
            p.verify(self.output)

    def test_review_identity_leak_is_rejected(self):
        self.run_bundle()
        path = self.output / "review-packet.json"
        packet = p.read_json(path)
        packet[0]["condition"] = "scripted-native"
        p.atomic_json(path, packet)
        p.seal(self.output)
        with self.assertRaises(ValueError):
            p.verify(self.output)

    def test_extra_or_missing_files_are_rejected(self):
        self.run_bundle()
        extra = self.output / "private.md"
        extra.write_text("do not inspect")
        with self.assertRaises(ValueError):
            p.verify(self.output)
        extra.unlink()
        self.trials()[0].unlink()
        with self.assertRaises(ValueError):
            p.verify(self.output)

    def test_manifest_path_traversal_is_rejected_before_read(self):
        self.run_bundle()
        path = self.output / "integrity.json"
        integrity = p.read_json(path)
        name = next(n for n in integrity["files"] if n.startswith("trials/"))
        integrity["files"]["../private.txt"] = integrity["files"].pop(name)
        p.atomic_json(path, integrity)
        with self.assertRaisesRegex(ValueError, "invalid evidence path"):
            p.verify(self.output)

    def test_symlink_evidence_is_not_read(self):
        self.run_bundle()
        target = self.root / "synthetic-private.json"
        target.write_text('{"canary":"should not read"}')
        path = self.trials()[0]
        path.unlink()
        path.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "invalid evidence file"):
            p.verify(self.output)

    def test_duplicate_json_keys_are_rejected(self):
        path = self.root / "bad.json"
        path.write_text('{"id":1,"id":2}')
        with self.assertRaisesRegex(ValueError, "duplicate JSON"):
            p.read_json(path)

    def test_subject_imports_have_no_io_modules(self):
        tree = ast.parse((p.ROOT / "tools/synthetic_subject.py").read_text())
        imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        imports += [alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names]
        self.assertEqual(set(imports), {"__future__", "re"})


if __name__ == "__main__":
    unittest.main()
