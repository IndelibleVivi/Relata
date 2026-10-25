"""Offline tests for the bounded RC-005 review workspace."""
from copy import deepcopy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import rc005_review as review

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "case-lab" / "reviews" / "workbench" / "demo.json"


class WorkspaceCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.workspace = self.root / "workspace"
        review.prepare_practice(DEMO, self.workspace)
        self.packet_raw = (self.workspace / "review-packet.json").read_bytes()
        self.packet = json.loads(self.packet_raw)
        self.items = {item["review_id"]: item for item in self.packet["items"]}
        self.contract, _, self.contract_sha = review.load_contract()

    def tearDown(self):
        self.temp.cleanup()

    def judgment(self, review_id, *, judgment_id=None, reviewer="reviewer-a",
                 supersedes=None, amendment_reason="", **changes):
        item = self.items[review_id]
        response = item["response"]
        id_value = judgment_id or hashlib.sha256(
            f"judgment:{review_id}:{reviewer}:{supersedes}".encode()).hexdigest()[:32]
        claims = []
        if response:
            claims = [{
                "quote": response,
                "kind": "fact",
                "attribution": "练习归属：原文字句用于检查判断依据。",
                "support": "underdetermined",
                "evidence_refs": ["current"],
                "rationale": "练习判断只检查历史是否支持具体字句。",
            }]
        value = {
            "judgment_id": id_value,
            "review_id": review_id,
            "supersedes": supersedes,
            "amendment_reason": amendment_reason,
            "created_at": "2026-10-25T12:00:00Z",
            "claims": claims,
            "current_action": "unresolved",
            "clarification": "none",
            "selective_use": "unresolved",
            "confidence_limits": "unresolved",
            "guessability": "cannot-tell",
            "guess_confidence": "unsure",
            "guess_cue": "",
            "rationale": "合成回归判断，不是研究结果。",
            "notes": "",
        }
        value.update(changes)
        return value

    def batch(self, records, *, reviewer=None, practice=True, **changes):
        value = {
            "format": "rc005-review-batch-1",
            "packet_sha256": hashlib.sha256(self.packet_raw).hexdigest(),
            "contract_sha256": self.contract_sha,
            "rubric_revision": self.contract["revision"],
            "review_pass": "blind",
            "reviewer_id": reviewer or "reviewer-a",
            "practice_only": practice,
            "records": records,
        }
        value.update(changes)
        return value

    def import_value(self, value, name):
        path = self.root / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return review.import_review(self.workspace, path)

    def complete_item(self):
        return next(item for item in self.packet["items"]
                    if item["response_state"] == "complete" and item["response"])

    def empty_item(self):
        return next(item for item in self.packet["items"] if item["response"] == "")

    def failure_item(self):
        return next(item for item in self.packet["items"]
                    if item["response_state"] == "technical-failure")

    def add_packet_item(self, *, response="", state="complete", review_id="f" * 32):
        item = deepcopy(self.items[self.complete_item()["review_id"]])
        item.update(response=response, response_state=state, review_id=review_id)
        self.items[review_id] = item
        self.packet["items"].append(item)
        packet_raw = (json.dumps(self.packet, ensure_ascii=False, indent=2,
                                 allow_nan=False) + "\n").encode("utf-8")
        (self.workspace / "review-packet.json").write_bytes(packet_raw)
        snapshot = json.loads((self.workspace / "source-snapshot.json").read_text())
        snapshot["packet_sha256"] = hashlib.sha256(packet_raw).hexdigest()
        snapshot["items"][review_id] = {"body": item, "response_state": state}
        (self.workspace / "source-snapshot.json").write_text(
            json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
        binding_path = self.workspace / "private-binding.json"
        binding = json.loads(binding_path.read_text())
        binding["packet_sha256"] = hashlib.sha256(packet_raw).hexdigest()
        binding["source_snapshot_sha256"] = hashlib.sha256(
            review.canonical(snapshot)).hexdigest()
        binding_path.write_text(json.dumps(binding, ensure_ascii=False), encoding="utf-8")
        self.packet_raw = packet_raw


class PreparationTests(WorkspaceCase):
    def test_practice_prepare_binds_exact_serialized_packet_bytes(self):
        wrapper = json.loads(DEMO.read_text(encoding="utf-8"))
        expected = (json.dumps(wrapper["packet"], ensure_ascii=False, indent=2,
                               allow_nan=False) + "\n").encode("utf-8")
        self.assertEqual(expected, self.packet_raw)
        result = review.verify(self.workspace)
        self.assertTrue(result["practice_only"])
        binding = json.loads((self.workspace / "private-binding.json").read_text())
        self.assertIsNone(binding["run"])
        self.assertEqual(binding["packet_sha256"], hashlib.sha256(expected).hexdigest())

    def test_practice_is_clearly_labeled_and_contains_required_states(self):
        wrapper = json.loads(DEMO.read_text(encoding="utf-8"))
        self.assertIs(wrapper["practice_only"], True)
        items = wrapper["packet"]["items"]
        self.assertEqual(len(items), 7)
        self.assertTrue(any(item["response"] == "" for item in items))
        self.assertTrue(any(item["response"] is None and
                            item["response_state"] == "technical-failure" for item in items))
        self.assertTrue(any("提议" in item["response"] for item in items if item["response"]))
        self.assertTrue(any("已经" in item["response"] for item in items if item["response"]))
        for item in items:
            self.assertRegex(item["review_id"], r"^[0-9a-f]{32}$")
            self.assertNotIn("condition", item)
            self.assertNotIn("variant", item)
            self.assertNotIn("required_meanings", item)

    def test_prepare_rejects_existing_output_and_symlink(self):
        with self.assertRaisesRegex(ValueError, "already exists"):
            review.prepare_practice(DEMO, self.workspace)
        link = self.root / "link"
        link.symlink_to(self.root / "target")
        with self.assertRaisesRegex(ValueError, "symlink"):
            review.prepare_practice(DEMO, link / "workspace")
        self.assertFalse((self.root / "target").exists())

    def test_prepare_practice_rejects_non_practice_wrapper(self):
        wrapper = json.loads(DEMO.read_text())
        wrapper["practice_only"] = False
        source = self.root / "bad-wrapper.json"
        source.write_text(json.dumps(wrapper, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "practice-only"):
            review.prepare_practice(source, self.root / "bad-output")
        self.assertFalse((self.root / "bad-output").exists())

    def test_saved_copy_rejects_contract_and_packet_tampering(self):
        packet_path = self.workspace / "review-packet.json"
        original = packet_path.read_bytes()
        packet_path.write_bytes(original + b" ")
        with self.assertRaisesRegex(ValueError, "private binding packet"):
            review.verify(self.workspace)
        packet_path.write_bytes(original)
        contract_path = self.workspace / "contract.json"
        original_contract = contract_path.read_bytes()
        contract_path.write_bytes(original_contract + b" ")
        with self.assertRaisesRegex(ValueError, "workspace contract"):
            review.verify(self.workspace)

    def test_saved_copy_rejects_snapshot_body_even_with_resealed_binding(self):
        snapshot_path = self.workspace / "source-snapshot.json"
        binding_path = self.workspace / "private-binding.json"
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        identifier = next(iter(snapshot["items"]))
        snapshot["items"][identifier]["body"]["response"] = "tampered"
        snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False),
                                 encoding="utf-8")
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
        binding["source_snapshot_sha256"] = hashlib.sha256(
            review.canonical(snapshot)).hexdigest()
        binding_path.write_text(json.dumps(binding, ensure_ascii=False),
                                encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source snapshot"):
            review.verify(self.workspace)


class ImportTests(WorkspaceCase):
    def chain_record(self, identifier, supersedes=None, reviewer="reviewer-a"):
        return {
            "judgment_id": identifier, "review_id": "1" * 32,
            "supersedes": supersedes, "reviewer_id": reviewer,
            "amendment_reason": "" if supersedes is None else "练习修订。",
            "rubric_revision": self.contract["revision"], "review_pass": "blind",
        }

    def test_chain_validator_rejects_disconnected_cycle_after_rooted_chain(self):
        # Close the cycle before the validator sees it, after a valid rooted component.
        d = self.chain_record("d" * 32, "c" * 32)
        records = [
            self.chain_record("a" * 32),
            self.chain_record("b" * 32, "a" * 32),
            d,
            self.chain_record("c" * 32, "d" * 32),
        ]
        with self.assertRaisesRegex(ValueError, "no root|disconnected head"):
            review.validate_chains(records)

    def test_cumulative_prefix_then_new_record_then_identical_retry(self):
        first = self.judgment(self.complete_item()["review_id"],
                              judgment_id="a" * 32, reviewer="reviewer-a")
        second = self.judgment(self.empty_item()["review_id"],
                               judgment_id="b" * 32, reviewer="reviewer-a", claims=[])
        self.import_value(self.batch([first], reviewer="reviewer-a"), "partial.json")
        cumulative = self.batch([first, second], reviewer="reviewer-a")
        result = self.import_value(cumulative, "cumulative.json")
        self.assertEqual(result["status"], "imported")
        self.assertEqual(result["records"], 1)
        self.assertEqual(result["batch"], "000002.json")
        stored = json.loads((self.workspace / "judgments" / "000002.json").read_text())
        self.assertEqual(stored["records"], [second])
        retry = self.import_value(cumulative, "retry.json")
        self.assertEqual(retry["status"], "already-imported")
        self.assertEqual(retry["records"], 0)
        self.assertIsNone(retry["batch"])
        self.assertEqual(len(list((self.workspace / "judgments").glob("[0-9]*.json"))), 2)
        self.assertEqual(review.verify(self.workspace)["judgments"], 2)

    def test_known_id_changed_content_or_owner_fails(self):
        rid = self.complete_item()["review_id"]
        first = self.judgment(rid, judgment_id="a" * 32, reviewer="reviewer-a")
        self.import_value(self.batch([first]), "first.json")
        changed = dict(first, rationale="changed content")
        with self.assertRaisesRegex(ValueError, "changed content or owner"):
            self.import_value(self.batch([changed]), "changed.json")
        value = self.batch([first], reviewer="reviewer-b")
        with self.assertRaisesRegex(ValueError, "changed content or owner"):
            self.import_value(value, "other-owner.json")
        duplicated = self.batch([first, first])
        with self.assertRaisesRegex(ValueError, "duplicated in import"):
            self.import_value(duplicated, "duplicate.json")

    def test_cumulative_journal_can_amend_an_earlier_item_after_later_item_import(self):
        first = self.judgment(self.complete_item()["review_id"], judgment_id="a" * 32)
        later = self.judgment(self.empty_item()["review_id"], judgment_id="b" * 32)
        self.import_value(self.batch([first, later]), "two-items.json")
        amendment = self.judgment(first["review_id"], judgment_id="c" * 32,
                                  supersedes=first["judgment_id"],
                                  amendment_reason="返回先前回答补充判断。")
        # The browser keeps each item's history together; it does not reorder
        # the entire journal whenever another item is amended.
        cumulative = self.batch([first, amendment, later])
        result = self.import_value(cumulative, "amend-earlier.json")
        self.assertEqual(result["records"], 1)
        self.assertEqual(review.verify(self.workspace)["judgments"], 3)
        self.assertEqual(self.import_value(cumulative, "amend-earlier-retry.json")["status"],
                         "already-imported")

    def test_cumulative_journal_amendments_append_only_new_suffix(self):
        rid = self.complete_item()["review_id"]
        root = self.judgment(rid, judgment_id="a" * 32, reviewer="reviewer-a")
        self.import_value(self.batch([root]), "root.json")
        amendment = self.judgment(
            rid, judgment_id="b" * 32, reviewer="reviewer-a",
            supersedes="a" * 32, amendment_reason="练习修订：补充来源。",
            current_action="within")
        first_cumulative = self.batch([root, amendment], reviewer="reviewer-a")
        result = self.import_value(first_cumulative, "amendment.json")
        self.assertEqual(result["records"], 1)
        second_amendment = self.judgment(
            rid, judgment_id="c" * 32, reviewer="reviewer-a",
            supersedes="b" * 32, amendment_reason="练习修订：再次核对。",
            current_action="outside")
        second_cumulative = self.batch(
            [root, amendment, second_amendment], reviewer="reviewer-a")
        result = self.import_value(second_cumulative, "amendment-2.json")
        self.assertEqual(result["records"], 1)
        retry = self.import_value(second_cumulative, "amendment-retry.json")
        self.assertEqual(retry["status"], "already-imported")
        self.assertEqual(retry["recognized_records"], 3)
        report_value, _ = review.report(self.workspace, "json")
        self.assertEqual(report_value["counts"]["historical_judgments"], 3)
        self.assertEqual(report_value["counts"]["current_judgments"], 1)
        self.assertEqual(len(report_value["historical_judgments"]), 3)
        current = report_value["current_judgments"][0]
        self.assertEqual(current["judgment_id"], "c" * 32)
        self.assertEqual(current["amendment_reason"], "练习修订：再次核对。")

    def test_valid_review_round_trip_and_deterministic_report(self):
        item = self.complete_item()
        value = self.batch([self.judgment(item["review_id"])])
        imported = self.import_value(value, "review.json")
        self.assertEqual(imported["records"], 1)
        first = review.verify(self.workspace)
        second = review.verify(self.workspace)
        self.assertEqual(first, second)
        report, fmt = review.report(self.workspace, "json")
        self.assertEqual(fmt, "json")
        self.assertEqual(report["counts"]["reviewed_current"], 1)
        self.assertEqual(report["counts"]["unreviewed_current"],
                         report["counts"]["reviewable"] - 1)
        again, _ = review.report(self.workspace, "json")
        self.assertEqual(report, again)

    def test_technical_failure_and_noncomplete_items_are_not_reviewable(self):
        failed = self.failure_item()
        with self.assertRaisesRegex(ValueError, "not reviewable"):
            self.import_value(self.batch([self.judgment(failed["review_id"])]), "failure.json")
        self.assertEqual(review.verify(self.workspace)["judgments"], 0)

    def test_empty_response_is_reviewable_only_with_zero_claims(self):
        item = self.empty_item()
        record = self.judgment(item["review_id"], claims=[])
        self.import_value(self.batch([record]), "empty-valid.json")
        self.assertEqual(review.verify(self.workspace)["judgments"], 1)
        bad = self.judgment(item["review_id"], reviewer="reviewer-b", claims=[{
            "quote": "not in the response", "kind": "fact", "attribution": "x",
            "support": "unsupported", "evidence_refs": ["current"],
            "rationale": "x",
        }])
        with self.assertRaisesRegex(ValueError, "blank response must have no claims"):
            self.import_value(self.batch([bad], reviewer="reviewer-b"), "bad-claim.json")

    def test_nonempty_response_requires_claim_and_exact_quote(self):
        item = self.complete_item()
        with self.assertRaisesRegex(ValueError, "needs at least one claim"):
            self.import_value(self.batch([self.judgment(item["review_id"], claims=[])]),
                              "no-claim.json")
        bad = self.judgment(item["review_id"])
        bad["claims"][0]["quote"] = "not an exact substring"
        with self.assertRaisesRegex(ValueError, "exact response substring"):
            self.import_value(self.batch([bad]), "bad-quote.json")

    def test_evidence_refs_and_positive_guess_cue_are_enforced(self):
        item = self.complete_item()
        bad = self.judgment(item["review_id"])
        bad["claims"][0]["evidence_refs"] = ["H999"]
        with self.assertRaisesRegex(ValueError, "evidence refs"):
            self.import_value(self.batch([bad]), "bad-ref.json")
        bad = self.judgment(item["review_id"], guessability="full-history", guess_cue="")
        with self.assertRaisesRegex(ValueError, "needs a cue"):
            self.import_value(self.batch([bad]), "bad-cue.json")

    def test_evidence_refs_may_be_empty_for_unsupported_and_required_for_supported(self):
        rid = self.complete_item()["review_id"]
        unsupported = self.judgment(rid)
        unsupported["claims"][0]["support"] = "unsupported"
        unsupported["claims"][0]["evidence_refs"] = []
        self.import_value(self.batch([unsupported]), "unsupported-no-ref.json")
        supported = self.judgment(rid, reviewer="reviewer-b",
                                  judgment_id="9" * 32)
        supported["claims"][0]["support"] = "supported"
        supported["claims"][0]["evidence_refs"] = []
        with self.assertRaisesRegex(ValueError, "requires evidence refs"):
            self.import_value(self.batch([supported], reviewer="reviewer-b"),
                              "supported-no-ref.json")

    def test_whitespace_complete_response_needs_no_impossible_quote(self):
        rid = "c" * 32
        self.add_packet_item(response="  \n\t", review_id=rid)
        value = self.judgment(rid, claims=[])
        self.import_value(self.batch([value]), "whitespace.json")
        self.assertEqual(review.verify(self.workspace)["judgments"], 1)
        report, _ = review.report(self.workspace, "json")
        self.assertEqual(report["counts"]["empty_completed"], 1)
        self.assertEqual(report["counts"]["whitespace_completed"], 1)
        self.assertEqual(report["counts"]["reviewable"], 7)

    def test_malformed_types_raise_value_error_cleanly(self):
        rid = self.complete_item()["review_id"]
        cases = (
            ("claims", [{"quote": 1}]),
            ("claims", [{"quote": "x", "kind": [], "attribution": "x",
                         "support": "unsupported", "evidence_refs": [],
                         "rationale": "x"}]),
            ("claims", [{"quote": "x", "kind": "fact", "attribution": "x",
                         "support": "unsupported", "evidence_refs": [1],
                         "rationale": "x"}]),
            ("claims", [{"quote": "x", "kind": "fact", "attribution": "x",
                         "support": "unsupported", "evidence_refs": [],
                         "rationale": "x"}], "current_action"),
        )
        for index, case in enumerate(cases):
            value = self.judgment(rid)
            value["claims"] = case[1]
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.import_value(self.batch([value]), f"malformed-{index}.json")

    def test_field_limits_count_characters_not_utf8_bytes(self):
        rid = self.complete_item()["review_id"]
        reviewer = "界" * 120
        record = self.judgment(rid, reviewer=reviewer)
        self.import_value(self.batch([record], reviewer=reviewer), "unicode-limit.json")
        too_long = self.judgment(rid, reviewer="reviewer-b",
                                 judgment_id="8" * 32)
        with self.assertRaisesRegex(ValueError, "character limit"):
            self.import_value(self.batch([too_long], reviewer="界" * 121),
                              "unicode-too-long.json")

    def test_packet_root_rejects_private_extras(self):
        packet = json.loads((self.workspace / "review-packet.json").read_text())
        packet["review-map.private"] = {"condition": "private"}
        with self.assertRaisesRegex(ValueError, "review packet has unknown"):
            review.validate_packet(packet, self.contract, practice=True)

    def test_strict_types_and_unknown_fields_are_rejected(self):
        item = self.complete_item()
        record = self.judgment(item["review_id"])
        record["practice_only"] = True
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.import_value(self.batch([record]), "unknown-record.json")
        record = self.judgment(item["review_id"])
        record["current_action"] = 1
        with self.assertRaisesRegex(ValueError, "not an allowed option"):
            self.import_value(self.batch([record]), "int-option.json")
        value = self.batch([self.judgment(item["review_id"])])
        value["practice_only"] = 1
        with self.assertRaisesRegex(ValueError, "practice flag"):
            self.import_value(value, "int-practice.json")

    def test_packet_and_contract_digest_mismatch_rejected(self):
        item = self.complete_item()
        for field in ("packet_sha256", "contract_sha256"):
            value = self.batch([self.judgment(item["review_id"])])
            value[field] = "0" * 64
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.import_value(value, f"bad-{field}.json")

    def test_small_batches_amendments_and_reviewer_disagreement(self):
        item = self.complete_item()
        rid = item["review_id"]
        first = self.judgment(rid, judgment_id="1" * 32, reviewer="reviewer-a")
        self.import_value(self.batch([first]), "batch-1.json")
        amendment = self.judgment(rid, judgment_id="2" * 32, reviewer="reviewer-b",
                                  supersedes="1" * 32,
                                  amendment_reason="First chain cannot be amended by another reviewer.")
        with self.assertRaisesRegex(ValueError, "across item|zero or multiple"):
            self.import_value(self.batch([amendment], reviewer="reviewer-b"), "batch-bad.json")
        second = self.judgment(rid, judgment_id="3" * 32, reviewer="reviewer-b",
                               current_action="outside")
        self.import_value(self.batch([second], reviewer="reviewer-b"), "batch-2.json")
        amendment = self.judgment(rid, judgment_id="4" * 32, reviewer="reviewer-a",
                                  supersedes="1" * 32,
                                  amendment_reason="练习修订：重新依据完整历史。",
                                  current_action="within")
        self.import_value(self.batch([first, amendment], reviewer="reviewer-a"),
                          "batch-3.json")
        result = review.verify(self.workspace)
        self.assertEqual(result["judgments"], 3)
        self.assertEqual(result["current_heads"], 2)
        report, _ = review.report(self.workspace, "json")
        self.assertEqual(report["counts"]["historical_judgments"], 3)
        self.assertEqual(report["counts"]["current_judgments"], 2)
        self.assertEqual(len(report["multi_reviewer_differences"]), 1)
        self.assertEqual(report["distributions"]["current_action"]["within"], 1)
        self.assertEqual(report["distributions"]["current_action"]["outside"], 1)

    def test_stale_fork_rejected_and_identical_retry_recognized(self):
        rid = self.complete_item()["review_id"]
        first = self.judgment(rid, judgment_id="a" * 32, reviewer="reviewer-a")
        batch_path = self.root / "first.json"
        batch_path.write_text(json.dumps(self.batch([first]), ensure_ascii=False))
        review.import_review(self.workspace, batch_path)
        retry = review.import_review(self.workspace, batch_path)
        self.assertEqual(retry["status"], "already-imported")
        self.assertEqual(retry["records"], 0)
        fork_one = self.judgment(rid, judgment_id="b" * 32, reviewer="reviewer-a",
                                 supersedes="a" * 32, amendment_reason="练习修订一。")
        self.import_value(self.batch([first, fork_one], reviewer="reviewer-a"),
                          "fork-one.json")
        fork_two = self.judgment(rid, judgment_id="c" * 32, reviewer="reviewer-a",
                                 supersedes="a" * 32, amendment_reason="练习修订二。")
        with self.assertRaisesRegex(ValueError, "stale or disconnected head"):
            self.import_value(self.batch([first, fork_one, fork_two],
                                         reviewer="reviewer-a"),
                              "fork-two.json")
        self.assertEqual(review.verify(self.workspace)["judgments"], 2)

    def test_batch_atomicity_keeps_all_validation_before_write(self):
        first = self.judgment(self.complete_item()["review_id"], judgment_id="d" * 32,
                              reviewer="reviewer-a")
        second = self.judgment(self.complete_item()["review_id"], judgment_id="e" * 32,
                               reviewer="reviewer-a")
        second["current_action"] = "not allowed"
        before = sorted((self.workspace / "judgments").iterdir())
        with self.assertRaises(ValueError):
            self.import_value(self.batch([first, second], reviewer="reviewer-a"),
                              "partially-invalid.json")
        self.assertEqual(before, sorted((self.workspace / "judgments").iterdir()))
        self.assertEqual(review.verify(self.workspace)["judgments"], 0)

    def test_interrupted_temp_residue_is_ignored_and_retry_succeeds(self):
        folder = self.workspace / "judgments"
        residue = folder / ".000001.interrupted.tmp"
        residue.write_text('{"partial":', encoding="utf-8")
        rid = self.complete_item()["review_id"]
        record = self.judgment(rid, judgment_id="7" * 32)
        result = self.import_value(self.batch([record]), "retry-after-interrupt.json")
        self.assertEqual(result["status"], "imported")
        self.assertEqual(result["batch"], "000001.json")
        self.assertTrue(residue.exists())
        self.assertEqual(review.verify(self.workspace)["judgments"], 1)

    def test_promotion_failure_leaves_no_trusted_record_and_temp_is_removed(self):
        rid = self.complete_item()["review_id"]
        record = self.judgment(rid, judgment_id="6" * 32)
        source = self.root / "promote-fail.json"
        source.write_text(json.dumps(self.batch([record]), ensure_ascii=False),
                          encoding="utf-8")
        with patch("os.link", side_effect=OSError("promotion failed")):
            with self.assertRaisesRegex(OSError, "promotion failed"):
                review.import_review(self.workspace, source)
        self.assertFalse((self.workspace / "judgments" / "000001.json").exists())
        self.assertFalse(any((self.workspace / "judgments").glob(".*.tmp")))
        self.assertEqual(review.verify(self.workspace)["judgments"], 0)

    def test_exact_interrupted_candidate_name_does_not_block_its_retry(self):
        record = self.judgment(self.complete_item()["review_id"], judgment_id="d" * 32)
        batch = self.batch([record])
        # Simulate the exact name left by the original deterministic temp path.
        candidate = review.canonical(batch)
        residue = self.workspace / "judgments" / f".000001.{review.digest(candidate)[:16]}.tmp"
        residue.write_bytes(b'{"partial":')
        result = self.import_value(batch, "same-candidate-retry.json")
        self.assertEqual(result["records"], 1)
        self.assertTrue(residue.exists())
        self.assertEqual(review.verify(self.workspace)["judgments"], 1)

    def test_filename_contention_does_not_overwrite_numbered_batch(self):
        rid = self.complete_item()["review_id"]
        root = self.judgment(rid, judgment_id="5" * 32)
        self.import_value(self.batch([root]), "root-before-contention.json")
        first_batch = (self.workspace / "judgments" / "000001.json").read_bytes()
        record = self.judgment(rid, judgment_id="6" * 32, supersedes="5" * 32,
                               amendment_reason="练习修订。")
        source = self.root / "contended.json"
        source.write_text(json.dumps(self.batch([root, record]), ensure_ascii=False),
                          encoding="utf-8")
        with patch("os.link", side_effect=FileExistsError("contended")):
            with self.assertRaisesRegex(ValueError, "already exists"):
                review.import_review(self.workspace, source)
        self.assertEqual((self.workspace / "judgments" / "000001.json").read_bytes(),
                         first_batch)
        self.assertFalse((self.workspace / "judgments" / "000002.json").exists())
        self.assertFalse(any((self.workspace / "judgments").glob(".*.tmp")))

    def test_no_network_process_or_runtime_initialization(self):
        with patch("socket.socket", side_effect=AssertionError("network used")), \
             patch("subprocess.Popen", side_effect=AssertionError("process used")), \
             patch.object(review.study.Study, "__init__",
                          side_effect=AssertionError("runtime initialized")):
            item = self.complete_item()
            self.import_value(self.batch([self.judgment(item["review_id"])]),
                              "offline.json")
            review.verify(self.workspace)
            review.report(self.workspace, "json")
            review.report(self.workspace, "markdown")

    def test_report_markdown_and_json_are_operator_readable(self):
        rid = self.complete_item()["review_id"]
        self.import_value(self.batch([self.judgment(rid)]), "report.json")
        value, fmt = review.report(self.workspace, "json")
        self.assertEqual(fmt, "json")
        self.assertIn("no accuracy", " ".join(value["limits"]))
        text, fmt = review.report(self.workspace, "markdown")
        self.assertEqual(fmt, "markdown")
        self.assertIn("# RC-005", text)
        self.assertIn("开发工作表", text)
        self.assertIn("technical failures", " ".join(value["limits"]))

    def test_markdown_reports_keep_notes_and_aliases_literal(self):
        payload = '<img src="https://invalid.example/image"> ![x](https://invalid.example/x)\n|break|'
        alias = 'reviewer|`literal`'
        record = self.judgment(self.complete_item()["review_id"], reviewer=alias,
                               rationale=payload, notes=payload)
        self.import_value(self.batch([record], reviewer=alias), "literal-notes.json")
        text, _ = review.report(self.workspace, "markdown")
        self.assertNotIn('<img src=', text)
        self.assertNotIn('![x](', text)
        self.assertIn('&lt;img src=', text)
        self.assertIn(r'reviewer\|\`literal\`', text)
        self.assertIn(r'<br>\|break\|', text)
        value, _ = review.report(self.workspace, "json")
        self.assertEqual(value["current_judgments"][0]["notes"], payload)
        self.assertEqual(value["current_judgments"][0]["reviewer_id"], alias)

    def test_report_retains_claim_disagreement_without_dimension_difference(self):
        rid = self.complete_item()["review_id"]
        first = self.judgment(rid, judgment_id="d" * 32, reviewer="reviewer-a")
        second = self.judgment(rid, judgment_id="e" * 32, reviewer="reviewer-b")
        second["claims"][0]["support"] = "unsupported"
        second["claims"][0]["attribution"] = "另一名评审者的归属解释。"
        second["claims"][0]["evidence_refs"] = []
        self.import_value(self.batch([first], reviewer="reviewer-a"), "claim-a.json")
        self.import_value(self.batch([second], reviewer="reviewer-b"), "claim-b.json")
        value, _ = review.report(self.workspace, "json")
        self.assertEqual(value["multi_reviewer_differences"], [])
        self.assertEqual(len(value["claim_interpretation_differences"]), 1)
        difference = value["claim_interpretation_differences"][0]
        self.assertEqual(set(difference["by_reviewer"]), {"reviewer-a", "reviewer-b"})
        self.assertIn("attribution", difference["by_reviewer"]["reviewer-b"][0])
        self.assertEqual(len(value["current_judgments"]), 2)
        self.assertEqual(len(value["historical_judgments"]), 2)
        text, _ = review.report(self.workspace, "markdown")
        self.assertIn("论断解释差异", text)
        self.assertIn("当前完整判断", text)
        self.assertIn("另一名评审者的归属解释", text)

    def test_report_cli_writes_json_and_markdown_to_new_files(self):
        rid = self.complete_item()["review_id"]
        self.import_value(self.batch([self.judgment(rid)]), "cli-report.json")
        json_output = self.root / "report.json"
        markdown_output = self.root / "report.md"
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(review.main([
                "report", "--workspace", str(self.workspace),
                "--format", "json", "--output", str(json_output),
            ]), 0)
            self.assertEqual(review.main([
                "report", "--workspace", str(self.workspace),
                "--format", "markdown", "--output", str(markdown_output),
            ]), 0)
        self.assertIn("report-written", output.getvalue())
        report_value = json.loads(json_output.read_text(encoding="utf-8"))
        self.assertEqual(report_value["format"], "rc005-review-report-1")
        self.assertTrue(report_value["practice_only"])
        self.assertIn("RC-005", markdown_output.read_text(encoding="utf-8"))
        with contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertEqual(review.main([
                "report", "--workspace", str(self.workspace),
                "--format", "json", "--output", str(json_output),
            ]), 1)
        self.assertIn("File exists", error.getvalue())


class NativeBindingTests(WorkspaceCase):
    def test_prepare_requires_existing_export_and_keeps_run_private(self):
        from tests.test_rc005_native import RC005Tests
        helper = RC005Tests()
        run = helper.review_sources(self.root, failure=True)
        with self.assertRaisesRegex(ValueError, "no existing review packet"):
            review.prepare(run, self.root / "without-export")
        review.study.Study.export_review(run)
        output = self.root / "native-workspace"
        result = review.prepare(run, output)
        self.assertFalse(result["practice_only"])
        binding = json.loads((output / "private-binding.json").read_text())
        self.assertEqual(binding["run"], str(run.resolve()))
        self.assertNotIn(str(run.resolve()),
                         (output / "review-packet.json").read_text())
        self.assertEqual(review.verify(output)["positions"], 144)

    def test_source_operation_change_fails_visibly(self):
        from tests.test_rc005_native import RC005Tests
        helper = RC005Tests()
        run = helper.review_sources(self.root, failure=True)
        review.study.Study.export_review(run)
        output = self.root / "native-workspace"
        review.prepare(run, output)
        operation = run / "operations" / "P-A-p1-1-full-history.json"
        value = json.loads(operation.read_text())
        value["result"]["response"]["choices"][0]["message"]["content"] = "changed"
        review.study.save(operation, value)
        with self.assertRaisesRegex(ValueError, "native run verification failed"):
            review.verify(output)

    def test_native_private_map_and_saved_snapshot_must_match(self):
        from tests.test_rc005_native import RC005Tests
        helper = RC005Tests()
        run = helper.review_sources(self.root, failure=True)
        review.study.Study.export_review(run)
        output = self.root / "native-workspace"
        review.prepare(run, output)
        snapshot_path = output / "source-snapshot.json"
        binding_path = output / "private-binding.json"
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        identifier = next(iter(snapshot["items"]))
        snapshot["items"][identifier]["body"]["response"] = "tampered"
        snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False),
                                 encoding="utf-8")
        binding = json.loads(binding_path.read_text(encoding="utf-8"))
        binding["source_snapshot_sha256"] = hashlib.sha256(
            review.canonical(snapshot)).hexdigest()
        binding_path.write_text(json.dumps(binding, ensure_ascii=False),
                                encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source snapshot body differs"):
            review.verify(output)

    def test_copied_workspace_still_needs_original_run_for_verify(self):
        from tests.test_rc005_native import RC005Tests
        helper = RC005Tests()
        run = helper.review_sources(self.root, failure=True)
        review.study.Study.export_review(run)
        output = self.root / "native-workspace"
        review.prepare(run, output)
        moved = self.root / "copied"
        moved.mkdir()
        for part in ("drafts", "judgments"):
            (moved / part).mkdir()
        for name in ("review-packet.json", "contract.json", "source-snapshot.json",
                     "private-binding.json"):
            (moved / name).write_bytes((output / name).read_bytes())
        binding = json.loads((moved / "private-binding.json").read_text())
        binding["run"] = str(self.root / "missing-run")
        (moved / "private-binding.json").write_text(json.dumps(binding), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "bound native run is missing"):
            review.verify(moved)


if __name__ == "__main__":
    unittest.main()
