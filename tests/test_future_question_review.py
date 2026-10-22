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
                 status="completed", text="Synthetic response only.", failure=None):
        row = self.by_cell[(family, question, world)]
        return {"input_id": row["input_id"], "status": status,
                "response": text if status == "completed" else None,
                "failure": failure if status == "technical_failure" else None}

    def export(self):
        out = self.root / "blind"
        review.export_review(self.packet, out)
        key = review.read_json(out / "hidden" / "review-key.json")
        item = review.read_json(out / "items" / f"{key['records'][0]['alias']}.json")
        return out, key, item

    def review_batch(self, rows, name="reviews.json"):
        return self.write_batch(name, {"format": review.REVIEW_FORMAT, "records": rows})

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
            "decision": "request-production-record",
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
            rows.append({"alias": key_record["alias"],
                         "reviewer_id": "synthetic-reviewer-1",
                         "decision": "title-yuanting",
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
