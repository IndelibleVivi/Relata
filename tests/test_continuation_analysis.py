import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
from continuation_analysis import comparisons, Evidence, review_payload, review_schema, decode_review
from continuation_api import StudyAPI, MODELS, output_text
from continuation_core import reader_payload
from test_continuation_core import bundle


class ContinuationAnalysisTest(unittest.TestCase):
    def test_review_selects_literal_lines_without_model_authored_quotation(self):
        roots = bundle()
        h, p, oracle = roots[0]["histories"][0], roots[1]["probes"][0], roots[2]["oracles"][0]
        answer = "**标题**\n\n原文第二段，标点也保留。"
        payload = review_payload(h, p, oracle, answer)
        visible = json.loads(payload["input"])
        self.assertEqual(visible["candidate_answer_lines"][2], {"line": 3, "text": "原文第二段，标点也保留。"})
        self.assertNotIn("D01-P1", payload["input"])
        raw = {"criteria": {c["id"]: {"judgment": "met", "answer_line": 3,
                "evidence_episode_ids": ["E1"], "reason": "所选内容符合当前任务。"}
                for c in oracle["criteria"]}, "overall_note": "仅校验定位，不证明判断正确。"}
        decoded = decode_review(raw, oracle, answer, h)
        self.assertEqual(decoded["criteria"][0]["answer_quote"], answer.splitlines()[2])
        self.assertEqual(review_schema(oracle, answer)["properties"]["criteria"]["required"], ["C1", "C2", "C3"])
        for line in (-1, 4, True, "3"):
            bad = copy.deepcopy(raw)
            bad["criteria"]["C1"]["answer_line"] = line
            with self.assertRaises(ValueError):
                decode_review(bad, oracle, answer, h)
        raw["criteria"]["C1"].update(answer_line=0, judgment="not_met", reason="回答没有完成当前任务。")
        self.assertEqual(decode_review(raw, oracle, answer, h)["criteria"][0]["answer_quote"], "")

    def rows(self):
        return [{"history_id": hid, "probe_id": hid + f"-P{p}", "criterion_id": f"C{c}",
                 "model": MODELS[0], "condition": arm, "dimension": "progress",
                 "kind": ("continue", "reconnect", "historical")[p-1], "verdict": "met"}
                for hid in ("D01", "D03") for p in range(1, 4)
                for c in range(1, 4 if p == 1 else 2) for arm in ("notes", "search")]

    def contrast(self, rows):
        return next(x for x in comparisons(rows) if x["left"] == "notes" and x["right"] == "search"
                    and x["dimension"] == "progress" and x["kind"] == "all" and x["model"] == MODELS[0])

    def test_missing_or_uncertain_is_not_zero_and_excludes_whole_paired_history(self):
        for outcome in ("uncertain", "not_applicable", "review_missing", "answer_unavailable"):
            rows = self.rows()
            rows[0]["verdict"] = outcome
            result = self.contrast(rows)
            self.assertEqual((result["planned_histories"], result["paired_histories"], result["excluded_histories"]), (2, 1, 1))
            self.assertEqual(result["mean_difference"], 0)

    def test_tasks_have_equal_weight_despite_different_criterion_counts(self):
        rows = self.rows()
        for row in rows:
            if row["history_id"] == "D01" and row["probe_id"] == "D01-P1" and row["condition"] == "search":
                row["verdict"] = "not_met"
        result = self.contrast(rows)
        self.assertAlmostEqual(result["mean_difference"], 1/6)
        self.assertEqual((result["better"], result["tie"], result["worse"]), (1, 1, 0))
        self.assertEqual(result["paired_histories"], 2)  # Not ten independent criterion rows.

    def test_empty_common_evidence_is_not_reported_as_zero_effect(self):
        rows = self.rows()
        for row in rows:
            row["verdict"] = "review_missing"
        result = self.contrast(rows)
        self.assertEqual(result["paired_histories"], 0)
        self.assertIsNone(result["mean_difference"])

    def test_missing_counterpart_criterion_excludes_history(self):
        rows = self.rows()
        rows.pop(0)
        self.assertEqual(self.contrast(rows)["paired_histories"], 1)

    def test_formulation_comparison_uses_its_own_common_histories(self):
        rows = self.rows()
        for row in rows:
            if row["condition"] == "search":
                row["condition"] = "summary"
        rows[0]["verdict"] = "uncertain"
        result = next(x for x in comparisons(rows) if x["left"] == "notes" and x["right"] == "summary"
                      and x["dimension"] == "progress" and x["kind"] == "all" and x["model"] == MODELS[0])
        self.assertEqual(result["contrast_role"], "secondary_formulation")
        self.assertEqual((result["paired_histories"], result["planned_histories"]), (1, 2))
        self.assertEqual(result["mean_difference"], 0)

    def test_answer_receipt_rejects_rewritten_text_and_source_binding(self):
        roots = bundle()
        values = (roots[0]["histories"], roots[1]["probes"], roots[2]["oracles"])
        h, p = values[0][0], values[1][0]
        with tempfile.TemporaryDirectory() as directory:
            def transport(*_):
                return 200, json.dumps({"status": "completed", "model": MODELS[0], "id": "response-1",
                    "usage": {"input_tokens": 1, "output_tokens": 1},
                    "output": [{"type": "message", "content": [{"type": "output_text", "text": "原始回答"}]}]})
            api = StudyAPI(directory, "/unused", transport=transport)
            api.bind("source-v1:development", roots)
            ranking = [{"episode_id": f"E{i}", "dense": 0.1, "lexical": 0.0, "rrf": 0.01} for i in range(1, 7)]
            payload = reader_payload(h, p, "current", "", ranking)
            response = api.response(f"reader/v1/{p['id']}/current/{MODELS[0]}", MODELS[0], payload)
            record = {"history_id": h["id"], "probe_id": p["id"], "condition": "current", "requested_model": MODELS[0],
                      "returned_model": response["model"], "response_id": response["id"], "state": "completed",
                      "answer": output_text(response), "usage": response["usage"], "exposure": payload["exposure"], "ranking": ranking}
            path = Path(directory) / "answers" / p["id"] / "current" / (MODELS[0] + ".json")
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(record))
            evidence = Evidence(directory, values, "development")
            self.assertEqual(evidence.answer(h, p, "current", MODELS[0])[1], "completed")
            record["answer"] = "后来改写"
            path.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, "literal provider"):
                evidence.answer(h, p, "current", MODELS[0])
            changed = copy.deepcopy(values)
            changed[0][0]["title"] = "改过的来源"
            with self.assertRaisesRegex(ValueError, "frozen run"):
                Evidence(directory, changed, "development")


if __name__ == "__main__":
    unittest.main()
