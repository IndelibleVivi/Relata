"""Plumbing-only tests for the fixed future-question response/review packet.

Every response and review below is synthetic and exists only to exercise
import, binding, append-only storage and descriptive counters. None is a
subject, model, human-reviewer or research result.
"""
from copy import deepcopy
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import future_question_review as review

class FutureQuestionReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.packet = self.root / "packet"
        review.prepare(self.packet)
        self.manifest = review.read_json(self.packet / "hidden" / "review-manifest.json")
        self.by_cell = {
            (row["family"], row["question"], row["world_id"]): row
            for row in self.manifest["records"]
        }

    def tearDown(self):
        self.temp.cleanup()

    def write_batch(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def response_batch(self, response_rows, name="responses.json"):
        return self.write_batch(name, {
            "format": review.RESPONSE_FORMAT,
            "provenance": "synthetic plumbing fixture; not a subject run",
            "records": response_rows,
        })

    def response(self, family="A-AUTHORSHIP", question="later", world="A",
                 status="completed", text="Synthetic response only.", failure=None,
                 attempt_id=None, previous_attempt=None, version=1):
        row = self.by_cell[(family, question, world)]
        record = {"input_id": row["input_id"], "status": status,
                  "response": text if status == "completed" else None,
                  "failure": failure if status == "technical_failure" else None}
        if version == 2:
            record.update(attempt_id=attempt_id, previous_attempt=previous_attempt)
        return record

    def response_batch_v2(self, response_rows, name="responses-v2.json"):
        return self.write_batch(name, {
            "format": review.RESPONSE_FORMAT_V2,
            "provenance": "synthetic v2 plumbing fixture; not a subject run",
            "records": response_rows,
        })

    def export(self):
        out = self.root / "blind"
        review.export_review(self.packet, out)
        key = review.read_json(out / "hidden" / "review-key.json")
        item = review.read_json(out / "items" / f"{key['records'][0]['alias']}.json")
        return out, key, item

    def review_batch(self, rows, name="reviews.json"):
        return self.write_batch(name, {"format": review.REVIEW_FORMAT, "records": rows})

    def test_v1_pending_can_continue_in_v2_and_mixed_completed_export(self):
        pending = self.response(status="pending")
        completed = self.response("B-CONDITIONAL-USE", world="A")
        review.import_responses(self.packet, self.response_batch([pending, completed]))
        original = (self.packet / "responses" / "000001.json").read_bytes()
        old_export, old_key, _ = self.export()
        answer = self.response(version=2, attempt_id="A-" + "8" * 32,
                               previous_attempt="legacy-v1", text="")
        review.import_responses(self.packet, self.response_batch_v2([answer]))
        mixed = self.root / "mixed-v2"
        review.export_review(self.packet, mixed)
        key = review.read_json(mixed / "hidden" / "review-key.json")
        self.assertEqual(key["format"], review.REVIEW_KEY_FORMAT_V2)
        self.assertEqual({r["attempt_id"] for r in key["records"]},
                         {"legacy-v1", "A-" + "8" * 32})
        batch = self.write_batch("mixed-reviews.json", {
            "format": review.REVIEW_FORMAT_V2,
            "records": [{"alias": r["alias"], "reviewer_id": "synthetic",
                         "response_act": "empty" if r["input_id"] == pending["input_id"] else "answer",
                         "mapping": "unmapped", "decision": None,
                         "reason": "Mixed-version plumbing only.",
                         "evidence_refs": ["current"]} for r in key["records"]]})
        review.import_reviews(self.packet, mixed, batch)
        self.assertEqual(review.verify(self.packet)["responses"], 2)
        self.assertEqual((self.packet / "responses" / "000001.json").read_bytes(), original)
        self.assertEqual(review.read_json(old_export / "hidden" / "review-key.json"), old_key)

    def test_empty_packet_is_pending_not_a_zero_score(self):
        result = review.recompute(self.packet)
        overall = result["overall"]
        self.assertEqual(overall["total"], 224)
        self.assertEqual(overall["pending"], 224)
        self.assertEqual(overall["attempted"], 0)
        self.assertIsNone(overall["answer_coverage"])
        self.assertIsNone(overall["judgment_contract_mismatch_rate"])
        self.assertIsNone(overall["judgment_contract_match_rate"])
        self.assertEqual(result["families"]["G-GLOBAL-INTERSECTION"]["total"], 42)
        with self.assertRaisesRegex(ValueError, "no completed responses"):
            review.export_review(self.packet, self.root / "empty-review")

    def test_input_export_and_hidden_manifest_are_separate(self):
        self.assertEqual(len(self.manifest["records"]), 224)
        for path in (self.packet / "inputs").iterdir():
            body = review.read_json(path)
            self.assertEqual(set(body), set(review.inputs.INPUT_VIEW_FIELDS))
            serialized = path.read_text(encoding="utf-8")
            for canary in ("authoring_world", "family", "condition", "answer_region",
                           "reviewer_id", "reason", "evidence_refs"):
                self.assertNotIn(canary, serialized)
        self.assertTrue((self.packet / "hidden" / "review-manifest.json").is_file())

    def test_full_packet_contains_every_fixed_projection_and_world(self):
        self.assertEqual(len(self.manifest["conditions"]), len(review.inputs.CONDITIONS))
        self.assertEqual({row["family"] for row in self.manifest["records"]},
                         set(review.inputs.FAMILY_IDS))

    def test_wrong_missing_and_duplicate_response_ids_are_rejected(self):
        wrong = self.response()
        wrong["input_id"] = "I-" + "0" * 32
        with self.assertRaisesRegex(ValueError, "unknown"):
            review.import_responses(self.packet, self.response_batch([wrong], "wrong.json"))
        missing = self.response()
        del missing["status"]
        with self.assertRaisesRegex(ValueError, "response fields"):
            review.import_responses(self.packet, self.response_batch([missing], "missing.json"))
        duplicate = self.response()
        with self.assertRaisesRegex(ValueError, "duplicated in the import"):
            review.import_responses(self.packet, self.response_batch(
                [duplicate, deepcopy(duplicate)], "duplicate.json"))

    def test_response_is_append_only_even_across_separate_batches(self):
        row = self.response()
        review.import_responses(self.packet, self.response_batch([row], "first.json"))
        with self.assertRaisesRegex(ValueError, "already used"):
            review.import_responses(self.packet, self.response_batch([row], "second.json"))
        self.assertEqual(review.verify(self.packet)["responses"], 1)

    def test_statuses_bind_output_and_failure_separately(self):
        for record in (
            {**self.response(), "status": "pending", "response": "must not survive"},
            {**self.response(), "status": "technical_failure",
             "response": "must not survive", "failure": "transport unavailable"},
            self.response(status="completed", text="", failure=None),
        ):
            with self.subTest(record=record), self.assertRaises(ValueError):
                review.import_responses(
                    self.packet, self.response_batch([record], "bad-status.json"))

        empty = self.response(status="completed", text="", failure=None,
                              attempt_id="A-" + "1" * 32, version=2)
        whitespace = self.response("B-CONDITIONAL-USE", world="A",
                                   status="completed", text="  \n", failure=None,
                                   attempt_id="A-" + "2" * 32, version=2)
        review.import_responses(
            self.packet, self.response_batch_v2([empty, whitespace]))
        result = review.recompute(self.packet)["overall"]
        self.assertEqual(result["completed"], 2)
        self.assertEqual(result["attempts"], 2)

    def test_technical_and_semantic_failures_have_distinct_denominators(self):
        rows = [
            self.response("A-AUTHORSHIP", world="A"),
            self.response("A-AUTHORSHIP", world="B", status="technical_failure",
                          failure="synthetic transport failure"),
            self.response("B-CONDITIONAL-USE", world="A"),
        ]
        review.import_responses(self.packet, self.response_batch(rows))
        result = review.recompute(self.packet)
        a = result["families"]["A-AUTHORSHIP"]
        self.assertEqual((a["attempted"], a["completed"], a["technical_failure"]),
                         (2, 1, 1))
        self.assertEqual(a["answer_coverage"], "1/2")
        self.assertEqual(a["judgment_contract_mismatch_rate"], None)
        self.assertEqual(result["overall"]["pending"], 221)
        self.assertEqual(result["overall"]["attempts"], 3)

    def test_v2_pending_and_failure_can_gain_an_explicit_completed_attempt(self):
        pending_id = "A-" + "1" * 32
        completed_id = "A-" + "2" * 32
        review.import_responses(self.packet, self.response_batch_v2([
            self.response(status="pending", attempt_id=pending_id, version=2),
        ], "pending-v2.json"))
        review.import_responses(self.packet, self.response_batch_v2([
            self.response(status="completed", attempt_id=completed_id,
                          previous_attempt=pending_id, version=2),
        ], "completed-v2.json"))
        packet = review.inspect_packet(self.packet)
        self.assertEqual([row["status"] for row in
                          packet["attempt_histories"][self.response()["input_id"]]],
                         ["pending", "completed"])
        result = review.recompute(self.packet)["overall"]
        self.assertEqual((result["completed"], result["attempts"],
                          result["positions_with_multiple_attempts"],
                          result["positions_with_completed_history"],
                          result["total"]), (1, 2, 1, 1, 224))

        failed = self.response("B-CONDITIONAL-USE", world="A",
                               status="technical_failure", failure="offline failure",
                               attempt_id="A-" + "3" * 32, version=2)
        review.import_responses(self.packet, self.response_batch_v2(
            [failed], "failure-v2.json"))
        review.import_responses(self.packet, self.response_batch_v2([
            self.response("B-CONDITIONAL-USE", world="A", status="completed",
                          attempt_id="A-" + "4" * 32,
                          previous_attempt=failed["attempt_id"], version=2),
        ], "retry-v2.json"))
        result = review.recompute(self.packet)["overall"]
        self.assertEqual((result["attempts"],
                          result["positions_with_completed_history"]), (4, 2))

    def test_v2_completed_history_is_immutable_and_attempt_ids_are_unique(self):
        first_id, second_id = "A-" + "5" * 32, "A-" + "6" * 32
        first = self.response(attempt_id=first_id, version=2)
        review.import_responses(self.packet, self.response_batch_v2(
            [first], "first-v2.json"))
        with self.assertRaisesRegex(ValueError, "cannot be silently replaced"):
            review.import_responses(self.packet, self.response_batch_v2([
                self.response(text="Different replacement", attempt_id=second_id,
                              previous_attempt=first_id, version=2),
            ], "replace-v2.json"))
        with self.assertRaisesRegex(ValueError, "already used|predecessor"):
            review.import_responses(self.packet, self.response_batch_v2([
                self.response("B-CONDITIONAL-USE", world="A", attempt_id=first_id,
                              version=2),
            ], "reuse-v2.json"))
        self.assertEqual(review.verify(self.packet)["attempts"], 1)

    def test_v2_empty_exports_and_unmapped_review_skips_contract_decision(self):
        empty = self.response(text="", attempt_id="A-" + "7" * 32, version=2)
        review.import_responses(self.packet, self.response_batch_v2(
            [empty], "empty-v2.json"))
        out = self.root / "blind-v2"
        review.export_review(self.packet, out)
        key = review.read_json(out / "hidden" / "review-key.json")
        item = review.read_json(
            out / "items" / f"{key['records'][0]['alias']}.json")
        self.assertEqual((key["format"], item["response"], item["response_state"]),
                         (review.REVIEW_KEY_FORMAT_V2, "",
                          "completed"))
        self.assertEqual(set(item["mapping_options"]), set(review.MAPPING_OPTIONS))
        base = {"alias": item["alias"], "reviewer_id": "reviewer-v2",
                "response_act": "empty", "mapping": "ambiguous",
                "decision": None, "reason": "The empty response has no finite map.",
                "evidence_refs": ["current"]}
        with self.assertRaisesRegex(ValueError, "must not carry a decision"):
            review.import_reviews(self.packet, out, self.write_batch(
                "bad-v2-review.json", {
                    "format": review.REVIEW_FORMAT_V2,
                    "records": [base | {"decision": "title-yuanting"}],
                }))
        imported = review.import_reviews(self.packet, out, self.write_batch(
            "good-v2-review.json",
            {"format": review.REVIEW_FORMAT_V2, "records": [base]}))
        self.assertEqual(imported["records"], 1)
        review.import_reviews(self.packet, out, self.write_batch(
            "second-v2-review.json",
            {"format": review.REVIEW_FORMAT_V2,
             "records": [base | {"reviewer_id": "reviewer-v2-b"}]}))
        summary = review.recompute(self.packet)["overall"]
        self.assertEqual(summary["unmapped_judgments"], 2)
        self.assertEqual(summary["multi_reviewer_disagreements"], 0)
        self.assertEqual(summary["judgments"], {"correct": 0, "incorrect": 0,
                                                "total": 0})

    def test_blind_export_hides_identity_and_requires_completed_response(self):
        review.import_responses(self.packet, self.response_batch([
            self.response(),
            self.response("A-AUTHORSHIP", world="B", status="technical_failure",
                          failure="synthetic transport failure"),
        ]))
        out, key, item = self.export()
        self.assertEqual(len(key["records"]), 1)
        self.assertEqual(set(item), set(review.REVIEW_ITEM_FIELDS))
        serialized = (out / "items" / f"{item['alias']}.json").read_text()
        for hidden in ("A-AUTHORSHIP", "world_id", "answer_region", "projection",
                       "archive_access", "failure"):
            self.assertNotIn(hidden, serialized)

    def test_review_requires_reason_evidence_and_known_alias(self):
        review.import_responses(self.packet, self.response_batch([self.response()]))
        out, _, item = self.export()
        base = {"alias": item["alias"], "reviewer_id": "synthetic-reviewer-1",
                "decision": "title-yuanting", "reason": "synthetic evidence",
                "evidence_refs": ["current"]}
        for change in ({"reason": ""}, {"evidence_refs": []},
                       {"evidence_refs": ["memory[999]"]},
                       {"alias": "V-" + "0" * 32}):
            bad = deepcopy(base)
            bad.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                review.import_reviews(self.packet, out,
                                      self.review_batch([bad], "bad-review.json"))

    def test_new_review_options_are_family_wide_not_world_or_question_keys(self):
        review.import_responses(self.packet, self.response_batch([self.response()]))
        _, _, item = self.export()
        self.assertEqual(set(item["decision_options"]), {
            "title-yuanting", "originator-human", "originator-companion"})
        self.assertIn("请根据", item["instructions"])
        self.assertIn("Judge", item["instructions"])
        self.assertNotIn("A-AUTHORSHIP", json.dumps(item))

    def test_new_review_rejects_an_unrelated_family_option(self):
        review.import_responses(self.packet, self.response_batch([self.response()]))
        out, _, item = self.export()
        with self.assertRaisesRegex(ValueError, "exported item options"):
            review.import_reviews(self.packet, out, self.review_batch([{
                "alias": item["alias"], "reviewer_id": "synthetic-reviewer",
                "decision": "blue", "reason": "Synthetic off-task option.",
                "evidence_refs": ["current"],
            }]))
        self.assertEqual(review.verify(self.packet)["reviews"], 0)

    def test_old_global_vocabulary_exports_remain_replayable(self):
        review.import_responses(self.packet, self.response_batch([self.response()]))
        with patch.object(review, "REVIEW_INSTRUCTIONS", review.LEGACY_REVIEW_INSTRUCTIONS), \
             patch.object(review, "decision_options_for",
                          side_effect=lambda record, contracts: deepcopy(contracts["decisions"])):
            out, _, item = self.export()
        review.import_reviews(self.packet, out, self.review_batch([{
            "alias": item["alias"], "reviewer_id": "synthetic-legacy-reviewer",
            "decision": "blue", "reason": "Synthetic legacy mismatch retained.",
            "evidence_refs": ["current"],
        }]))
        self.assertEqual(review.verify(self.packet)["reviews"], 1)
        self.assertEqual(review.recompute(self.packet)["overall"]["judgments"]["incorrect"], 1)

    def test_persisted_new_review_cannot_switch_to_an_off_family_decision(self):
        review.import_responses(self.packet, self.response_batch([self.response()]))
        out, _, item = self.export()
        review.import_reviews(self.packet, out, self.review_batch([{
            "alias": item["alias"], "reviewer_id": "synthetic-reviewer",
            "decision": "originator-human", "reason": "Synthetic disagreement.",
            "evidence_refs": ["current"],
        }]))
        # Verification must not read the external reviewer folder again.
        with patch.object(review, "_load_review_packet", side_effect=AssertionError("external folder read")):
            self.assertEqual(review.verify(self.packet)["reviews"], 1)
        path = self.packet / "reviews" / "000001.json"
        body = review.read_json(path)
        body["records"][0]["decision"] = "blue"
        path.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "exported item options"):
            review.verify(self.packet)

    def test_review_is_append_only_and_retains_disagreement(self):
        review.import_responses(self.packet, self.response_batch([
            self.response(),
        ]))
        second = self.root / "blind-two"
        review.export_review(self.packet, second)
        key = review.read_json(second / "hidden" / "review-key.json")
        reason = "Synthetic reviewer 1 cites current task text only."
        rows = []
        first_alias = None
        for key_record in key["records"]:
            alias = key_record["alias"]
            first_alias = first_alias or alias
            rows.append({"alias": alias, "reviewer_id": "synthetic-reviewer-1",
                         "decision": "title-yuanting", "reason": reason,
                         "evidence_refs": ["current"]})
        review.import_reviews(self.packet, second,
                              self.review_batch(rows, "first-review.json"))
        review.import_reviews(self.packet, second, self.review_batch([{
            "alias": first_alias, "reviewer_id": "synthetic-reviewer-2",
            "decision": "originator-human",
            "reason": "Synthetic reviewer 2 records disagreement.",
            "evidence_refs": ["current"],
        }], "second-review.json"))
        self.assertEqual(review.verify(self.packet)["reviews"], 2)
        summary = review.recompute(self.packet)["overall"]
        self.assertEqual(summary["scorable"], 1)
        self.assertEqual(summary["multi_reviewer_disagreements"], 1)
        self.assertEqual(summary["judgments"]["total"], 2)
        with self.assertRaisesRegex(ValueError, "already reviewed"):
            review.import_reviews(self.packet, second, self.review_batch([
                {"alias": first_alias, "reviewer_id": "synthetic-reviewer-1",
                 "decision": "title-yuanting", "reason": "Replacement attempt.",
                 "evidence_refs": ["current"]},
            ], "repeat.json"))

    def test_review_rejects_packet_from_another_preparation(self):
        review.import_responses(self.packet, self.response_batch([self.response()]))
        out, _, item = self.export()
        other = self.root / "other"
        review.prepare(other)
        with self.assertRaises(ValueError):
            review.import_reviews(other, out, self.review_batch([
                {"alias": item["alias"], "reviewer_id": "synthetic-reviewer-1",
                 "decision": "title-yuanting", "reason": "wrong packet",
                 "evidence_refs": ["current"]},
            ]))

    def test_same_reviewer_cannot_replay_response_under_another_alias(self):
        review.import_responses(self.packet, self.response_batch([self.response()]))
        out, key, item = self.export()
        review.import_reviews(self.packet, out, self.review_batch([{
            "alias": item["alias"], "reviewer_id": "synthetic-reviewer-1",
            "decision": "title-yuanting", "reason": "Synthetic first review.",
            "evidence_refs": ["current"],
        }]))
        second = self.root / "blind-second"
        review.export_review(self.packet, second)
        second_key = review.read_json(second / "hidden" / "review-key.json")
        with self.assertRaisesRegex(ValueError, "reviewer already reviewed"):
            review.import_reviews(self.packet, second, self.review_batch([{
                "alias": second_key["records"][0]["alias"],
                "reviewer_id": "synthetic-reviewer-1",
                "decision": "title-yuanting", "reason": "Replay attempt.",
                "evidence_refs": ["current"],
            }], "replay.json"))

    def test_review_alias_is_bound_to_its_exported_response(self):
        first = self.response()
        second = self.response("B-CONDITIONAL-USE", world="A")
        review.import_responses(self.packet, self.response_batch([first, second]))
        out, _, item = self.export()
        for key_record in review.read_json(out / "hidden" / "review-key.json")["records"]:
            item_path = out / "items" / f"{key_record['alias']}.json"
            body = review.read_json(item_path)
            if key_record["input_id"] == second["input_id"]:
                body["response"] = first["response"]
            item_path.write_text(json.dumps(body, ensure_ascii=False),
                                 encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            review.import_reviews(self.packet, out, self.review_batch([{
                "alias": item["alias"], "reviewer_id": "synthetic-reviewer-1",
                "decision": "title-yuanting", "reason": "changed response",
                "evidence_refs": ["current"],
            }, {
                "alias": next(row["alias"] for row in review.read_json(
                    out / "hidden" / "review-key.json")["records"]
                    if row["input_id"] == second["input_id"]),
                "reviewer_id": "synthetic-reviewer-2",
                "decision": "title-yuanting", "reason": "changed response",
                "evidence_refs": ["current"],
            }]))

    def test_persisted_review_replay_rejects_changed_binding_and_payload(self):
        first = self.response()
        second = self.response("B-CONDITIONAL-USE", world="A")
        review.import_responses(self.packet, self.response_batch([first, second]))
        out, key, item = self.export()
        rows = []
        for key_record in key["records"]:
            exported = review.read_json(out / "items" / f"{key_record['alias']}.json")
            rows.append({"alias": key_record["alias"],
                         "reviewer_id": "synthetic-reviewer-1",
                         "decision": next(iter(exported["decision_options"])),
                         "reason": "Synthetic valid persisted review.",
                         "evidence_refs": ["current"]})
        review.import_reviews(self.packet, out, self.review_batch(rows))
        batch_path = self.packet / "reviews" / "000001.json"
        valid = review.read_json(batch_path)
        pending_id = self.by_cell[("C-DISCARDED-RATIONALE", "later", "A")]["input_id"]
        second_key_record = next(record for record in key["records"]
                                 if record["input_id"] == second["input_id"])
        changes = (
            lambda record: record.update(input_id=pending_id),
            lambda record: record.update(alias="V-" + "0" * 32),
            lambda record: record.update(reason=" "),
            lambda record: record.update(evidence_refs=["memory[999]"]),
            lambda record: record.update(input_id=second["input_id"],
                                         alias=second_key_record["alias"]),
        )
        for change in changes:
            body = deepcopy(valid)
            change(body["records"][0])
            batch_path.write_text(json.dumps(body, ensure_ascii=False),
                                  encoding="utf-8")
            with self.subTest(change=change), self.assertRaises(ValueError):
                review.verify(self.packet)
        batch_path.write_text(json.dumps(valid, ensure_ascii=False), encoding="utf-8")

        response_batch = self.packet / "responses" / "000001.json"
        response_body = review.read_json(response_batch)
        response_body["records"][0]["response"] = "Changed persisted response."
        response_batch.write_text(json.dumps(response_body, ensure_ascii=False),
                                  encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "response digest mismatch"):
            review.verify(self.packet)

    def test_judgment_level_rates_retain_two_scorable_responses(self):
        review.import_responses(self.packet, self.response_batch([
            self.response(),
            self.response("B-CONDITIONAL-USE", world="A"),
        ]))
        out, key, item = self.export()
        first_alias, second_alias = [row["alias"] for row in key["records"]]
        review.import_reviews(self.packet, out, self.review_batch([
            {"alias": first_alias, "reviewer_id": "synthetic-reviewer-1",
             "decision": "originator-companion",
             "reason": "Synthetic legal decision for A.",
             "evidence_refs": ["current"]},
            {"alias": first_alias, "reviewer_id": "synthetic-reviewer-2",
             "decision": "originator-human",
             "reason": "Synthetic legal decision for A.",
             "evidence_refs": ["current"]},
            {"alias": second_alias, "reviewer_id": "synthetic-reviewer-1",
             "decision": "do-not-lend-until-sunday",
             "reason": "Synthetic illegal decision for B.",
             "evidence_refs": ["current"]},
        ]))
        summary = review.recompute(self.packet)
        overall = summary["overall"]
        self.assertEqual(overall["scorable"], 2)
        self.assertEqual(overall["judgments"], {
            "correct": 2, "incorrect": 1, "total": 3,
        })
        self.assertEqual(overall["judgment_contract_match_rate"], "2/3")
        self.assertEqual(overall["judgment_contract_mismatch_rate"], "1/3")

    def test_contract_drift_and_input_tamper_are_rejected(self):
        path = self.packet / "hidden" / "review-manifest.json"
        body = review.read_json(path)
        body["contract_sha256"] = "0" * 64
        path.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "contract revision"):
            review.verify(self.packet)
        self.assertEqual(len(self.manifest["records"]), 224)
        self.assertTrue((self.packet / "inputs").is_dir())

    def test_self_consistent_manifest_cannot_drop_one_cell(self):
        path = self.packet / "hidden" / "review-manifest.json"
        body = review.read_json(path)
        dropped = body["records"].pop()
        (self.packet / "inputs" / f"{dropped['input_id']}.json").unlink()
        path.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "every fixed cell"):
            review.verify(self.packet)

    def test_input_tamper_and_label_leak_are_rejected(self):
        row = self.manifest["records"][0]
        path = self.packet / "inputs" / f"{row['input_id']}.json"
        body = review.read_json(path)
        body["authoring_world"] = "LEAK"
        path.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs"):
            review.verify(self.packet)

    def test_symlink_paths_are_rejected(self):
        target = self.root / "target"
        target.mkdir()
        link = self.root / "link"
        link.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            review.prepare(link / "packet")
        self.assertFalse((target / "packet").exists())

    def test_prepare_rejects_retired_condition_filters(self):
        # A fixed full-matrix command must not silently ignore a requested subset.
        destination = self.root / "filtered"
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                review.main(["prepare", str(destination), "--projection", "retained",
                             "--access", "closed"])
        self.assertFalse(destination.exists())

    def test_existing_packet_is_not_overwritten(self):
        sentinel = self.packet / "sentinel"
        sentinel.write_text("unchanged")
        with self.assertRaises(FileExistsError):
            review.prepare(self.packet)
        self.assertEqual(sentinel.read_text(), "unchanged")

    def test_cli_plumbing_round_trip_uses_no_network_or_processes(self):
        response_file = self.response_batch([self.response()])
        with patch("socket.socket", side_effect=AssertionError("network forbidden")), \
             patch("subprocess.Popen", side_effect=AssertionError("process forbidden")):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(review.main(["verify", str(self.packet)]), 0)
                self.assertEqual(review.main([
                    "import-responses", str(self.packet), "--input", str(response_file)
                ]), 0)
                review.export_review(self.packet, self.root / "blind")
                key = review.read_json(self.root / "blind" / "hidden" / "review-key.json")
                alias = key["records"][0]["alias"]
                review_file = self.review_batch([{
                    "alias": alias, "reviewer_id": "synthetic-reviewer-1",
                    "decision": "title-yuanting",
                    "reason": "Synthetic CLI plumbing only.",
                    "evidence_refs": ["current"],
                }])
                self.assertEqual(review.main([
                    "import-review", str(self.packet), "--review-packet",
                    str(self.root / "blind"), "--input", str(review_file)
                ]), 0)
                self.assertEqual(review.main(["recompute", str(self.packet)]), 0)
        self.assertIn("relata-future-question-review-summary-1", output.getvalue())

if __name__ == "__main__":
    unittest.main()
