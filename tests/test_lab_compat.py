"""Synthetic, practice-only tests for frozen legacy compatibility reading."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from relata_lab import Lab, LabError
from relata_lab import compat
from tools import future_question_review as future_review
from tools import rc005_review as rc005_review


class LegacyCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.lab = Lab(self.root / "lab")

    def tearDown(self):
        self.lab.close()
        self.temp.cleanup()

    def practice(self):
        workspace = self.root / "practice"
        rc005_review.prepare_practice(
            ROOT / "case-lab" / "reviews" / "workbench" / "demo.json",
            workspace)
        return workspace

    def future(self):
        workspace = self.root / "future"
        future_review.prepare(workspace)
        return workspace

    def register(self, path, format_id, name):
        return compat.register_legacy(
            self.lab, path, format_id, name, native_run=None)

    def test_practice_is_frozen_across_current_fixture_and_contract_changes(self):
        workspace = self.practice()
        packet_path = workspace / "review-packet.json"
        original = packet_path.read_bytes()
        source = self.register(workspace, compat.FORMAT_PRACTICE, "practice")

        changed = json.loads(original)
        changed["items"][0]["response"] = "fixture changed after freeze"
        packet_path.write_text(
            json.dumps(changed, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        current_contract = workspace / "contract.json"
        current_contract.write_text(current_contract.read_text() + " ",
                                    encoding="utf-8")

        frozen = compat.read_legacy(self.lab, source["id"])
        self.assertEqual(frozen["files"]["review-packet.json"].encode("utf-8"),
                         original)
        self.assertEqual(frozen["verification"]["source_binding"], "verified-now")
        self.assertEqual(frozen["verification"]["review_verifier"],
                         "tools.rc005_review.load_reviews")
        self.assertTrue(frozen["frozen_verification"]["practice_only"])

    def test_frozen_reader_never_consults_current_canonical_material(self):
        from unittest.mock import patch
        source = self.register(self.practice(), compat.FORMAT_PRACTICE, "frozen-no-current")
        before = compat.read_legacy(self.lab, source["id"])
        with patch.object(rc005_review, "load_workspace", side_effect=AssertionError("current source read")), patch.object(future_review, "inspect_packet", side_effect=AssertionError("current contract read")):
            self.assertEqual(compat.read_legacy(self.lab, source["id"]), before)

    def test_future_question_workspace_is_read_from_frozen_members(self):
        workspace = self.future()
        original_packet = (workspace / "hidden" / "review-manifest.json").read_bytes()
        original_input = next((workspace / "inputs").iterdir()).read_bytes()
        source = self.register(workspace, compat.FORMAT_FUTURE, "future")
        for name in ("history_sha256", "contract_sha256"):
            self.assertEqual(len(source["body"]["frozen_verification"][name]), 64)
        frozen = compat.read_legacy(self.lab, source["id"])
        self.assertEqual(
            frozen["files"]["hidden/review-manifest.json"].encode("utf-8"),
            original_packet)
        self.assertTrue(any(value.encode("utf-8") == original_input
                            for name, value in frozen["files"].items()
                            if name.startswith("inputs/")))
        self.assertEqual(source["body"]["verification"]["source_binding"],
                         "verified-now")

    def test_future_reader_uses_frozen_inputs_without_current_bundle(self):
        workspace = self.future()
        first = sorted((workspace / "inputs").iterdir())[0]
        original = first.read_bytes()
        source = self.register(workspace, compat.FORMAT_FUTURE, "future-frozen")
        frozen = compat.read_legacy(self.lab, source["id"])
        frozen_name = "inputs/" + first.name
        self.assertEqual(frozen["files"][frozen_name].encode("utf-8"), original)
        self.assertEqual(frozen["verification"]["canonical_verifier"],
                         "tools.future_question_review.inspect_packet")

    def test_future_registration_rejects_broken_review_batch(self):
        workspace = self.future()
        (workspace / "reviews" / "000001.json").write_text(
            json.dumps({"format": "not-a-review-batch"}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "review batch"):
            self.register(
                workspace, compat.FORMAT_FUTURE, "future-broken-review")

    def test_practice_inventory_cannot_be_mislabeled_as_native(self):
        workspace = self.practice()
        binding = workspace / "private-binding.json"
        value = json.loads(binding.read_text())
        value["practice_only"] = False
        value["run"] = str(self.root / "missing-native-run")
        binding.write_text(json.dumps(value, ensure_ascii=False) + "\n",
                           encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "exactly 144"):
            self.register(workspace, compat.FORMAT_NATIVE, "native")

    def test_native_does_not_call_workspace_verify_in_place_of_native_verifier(self):
        workspace = self.practice()
        with patch.object(rc005_review, "verify",
                          side_effect=AssertionError("workspace verifier called")):
            with self.assertRaisesRegex(LabError, "non-practice binding"):
                compat.register_legacy(
                    self.lab, workspace, compat.FORMAT_NATIVE, "wrong-helper")

    def test_native_run_identity_must_match_private_binding(self):
        workspace = self.practice()
        loaded = rc005_review.load_workspace(workspace)
        bound = self.root / "bound-run"
        selected = self.root / "selected-run"
        bound.mkdir()
        selected.mkdir()
        loaded["binding"]["run"] = str(bound)
        loaded["practice_only"] = False
        with patch.object(rc005_review, "load_workspace", return_value=loaded), \
             patch.object(rc005_review, "verify_native_source") as native:
            with self.assertRaisesRegex(LabError, "selected run differs"):
                compat.register_legacy(
                    self.lab, workspace, compat.FORMAT_NATIVE,
                    "identity-mismatch", native_run=selected)
            native.assert_not_called()

    def test_native_stub_receives_exact_packet_and_contract(self):
        workspace = self.practice()
        loaded = rc005_review.load_workspace(workspace)
        run = self.root / "same-run"
        run.mkdir()
        loaded["binding"]["run"] = str(run)
        loaded["practice_only"] = False
        packet_path = workspace / "review-packet.json"
        contract_sha = rc005_review.load_contract()[2]

        def stub(native_run, review_workspace):
            self.assertEqual(native_run, run)
            self.assertEqual(review_workspace, workspace)
            return packet_path, contract_sha

        with patch.object(rc005_review, "load_workspace", return_value=loaded), \
             patch.object(rc005_review, "verify_native_source",
                          side_effect=stub) as native:
            source = compat.register_legacy(
                self.lab, workspace, compat.FORMAT_NATIVE,
                "canonical-stub", native_run=run)
        native.assert_called_once_with(run, workspace)
        self.assertEqual(source["body"]["verification"]["source_binding"],
                         "verified-now")
        self.assertEqual(source["body"]["verification"]["native_run"], str(run))
        self.assertTrue(source["body"]["verification"]["native_run_reverified"])
        self.assertEqual(source["body"]["verification"]["native_verifier"],
                         "tools.rc005_review.verify_native_source")

    def test_native_requires_explicit_original_run(self):
        workspace = self.practice()
        loaded = rc005_review.load_workspace(workspace)
        loaded["practice_only"] = False
        with patch.object(rc005_review, "load_workspace", return_value=loaded), \
             patch.object(rc005_review, "verify_native_source") as native:
            with self.assertRaisesRegex(LabError, "requires its original run"):
                compat.register_legacy(
                    self.lab, workspace, compat.FORMAT_NATIVE, "missing-run")
            native.assert_not_called()

    def test_native_invalid_frozen_judgment_chain_is_rejected(self):
        workspace = self.practice()
        loaded = rc005_review.load_workspace(workspace)
        run = self.root / "chain-run"
        run.mkdir()
        loaded["binding"]["run"] = str(run)
        loaded["practice_only"] = False
        item = next(row for row in loaded["packet"]["items"]
                    if row["response_state"] == "complete" and row["response"])
        contract = loaded["contract"]
        record = {
            "judgment_id": "a" * 32, "review_id": item["review_id"],
            "supersedes": "b" * 32,
            "amendment_reason": "synthetic broken chain",
            "created_at": "2026-10-25T12:00:00Z",
            "claims": [{
                "quote": item["response"], "kind": "fact",
                "attribution": "synthetic", "support": "underdetermined",
                "evidence_refs": ["current"], "rationale": "synthetic"}],
            "current_action": "unresolved", "clarification": "none",
            "selective_use": "unresolved",
            "confidence_limits": "unresolved",
            "guessability": "cannot-tell", "guess_confidence": "unsure",
            "guess_cue": "", "rationale": "synthetic", "notes": "",
        }
        batch = {
            "format": contract["batch_format"],
            "packet_sha256": loaded["packet_sha256"],
            "contract_sha256": loaded["contract_sha256"],
            "rubric_revision": contract["revision"],
            "review_pass": "blind", "reviewer_id": "synthetic",
            "practice_only": loaded["practice_only"], "records": [record],
        }
        (workspace / "judgments" / "000001.json").write_text(
            json.dumps(batch, ensure_ascii=False), encoding="utf-8")

        def stub(native_run, review_workspace):
            return workspace / "review-packet.json", rc005_review.load_contract()[2]

        with patch.object(rc005_review, "load_workspace", return_value=loaded), \
             patch.object(rc005_review, "verify_native_source",
                          side_effect=stub):
            with self.assertRaisesRegex(ValueError, "unknown ID"):
                compat.register_legacy(
                    self.lab, workspace, compat.FORMAT_NATIVE,
                    "bad-judgments", native_run=run)

    def test_missing_artifact_and_inventory_tamper_fail_closed(self):
        workspace = self.practice()
        source = self.register(workspace, compat.FORMAT_PRACTICE, "broken")
        manifest_digest = source["body"]["artifact_digest"]
        (self.lab.blobs / manifest_digest).unlink()
        with self.assertRaises(LabError) as missing:
            compat.read_legacy(self.lab, source["id"])
        self.assertEqual(missing.exception.code, "missing_artifact")

        workspace2 = self.root / "practice-two"
        rc005_review.prepare_practice(
            ROOT / "case-lab" / "reviews" / "workbench" / "demo.json",
            workspace2)
        source2 = self.register(workspace2, compat.FORMAT_PRACTICE, "tamper")
        self.lab.command("object.revise", {
            "id": source2["id"], "expected_revision": 1,
            "body": source2["body"] | {
                "inventory": source2["body"]["inventory"][:-1]},
        }, "tamper-object")
        with self.assertRaises(LabError):
            compat.read_legacy(self.lab, source2["id"])

    def test_source_body_tamper_fails_against_frozen_metadata(self):
        workspace = self.practice()
        source = self.register(workspace, compat.FORMAT_PRACTICE, "body-tamper")
        changed = source["body"] | {
            "verification": source["body"]["verification"] |
            {"source_binding": "rewritten"}}
        self.lab.command("object.revise", {
            "id": source["id"], "expected_revision": 1, "body": changed,
        }, "body-tamper-revise")
        with self.assertRaisesRegex(LabError, "frozen metadata"):
            compat.read_legacy(self.lab, source["id"])

    def test_unknown_format_and_symlink_inventory_are_rejected(self):
        workspace = self.practice()
        with self.assertRaises(LabError):
            compat.register_legacy(self.lab, workspace, "unknown-format", "bad")
        link = self.root / "link"
        link.symlink_to(workspace, target_is_directory=True)
        with self.assertRaises(LabError):
            self.register(link, compat.FORMAT_PRACTICE, "symlink")

    def test_command_id_is_idempotent_without_fixed_object_id_collision(self):
        workspace = self.practice()
        first = self.register(workspace, compat.FORMAT_PRACTICE, "same-command")
        second = compat.register_legacy(
            self.lab, workspace, compat.FORMAT_PRACTICE, "same-command")
        self.assertEqual(first, second)

    def test_frozen_material_survives_backup_restore(self):
        workspace = self.practice()
        source = self.register(workspace, compat.FORMAT_PRACTICE, "backup-source")
        before = compat.read_legacy(self.lab, source["id"])
        archive = self.root / "compat-backup.zip"
        self.lab.backup(archive)
        restored = Lab.restore(archive, self.root / "restored")
        try:
            self.assertEqual(compat.read_legacy(restored, source["id"]), before)
        finally:
            restored.close()

    def test_frozen_material_survives_research_transfer(self):
        workspace = self.practice()
        source = self.register(workspace, compat.FORMAT_PRACTICE, "transfer-source")
        before = compat.read_legacy(self.lab, source["id"])
        archive = self.root / "compat-transfer.zip"
        self.lab.export_bundle(
            archive, "research-transfer",
            [{"id": source["id"], "revision": 1}])
        restored = Lab.restore(archive, self.root / "transferred")
        try:
            self.assertEqual(compat.read_legacy(restored, source["id"]), before)
        finally:
            restored.close()


if __name__ == "__main__":
    unittest.main()
