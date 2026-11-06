import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
from continuation_core import (validate_bundle, episode_text, writer_payload,
    rank_episodes, reader_payload, judge_payload, validate_judgment)


def bundle():
    h = {"id": "D01", "split": "development", "coverage": "creative", "title": "TITLE_SENTINEL",
         "episodes": [{"id": f"E{i}", "day": f"第{i}天", "messages": [
             {"role": "user", "text": f"这是第{i}段原话。"},
             {"role": "assistant", "text": f"这是第{i}次我的看法，不代表你的感觉。"}]} for i in range(1, 7)]}
    ps = [{"id": f"D01-P{i}", "history_id": "D01", "kind": kind,
           "messages": [{"role": "user", "text": f"FUTURE_SENTINEL_{i}现在请继续。"}]}
          for i, kind in enumerate(("continue", "reconnect", "historical"), 1)]
    os = [{"probe_id": p["id"], "rationale": "ORACLE_SENTINEL", "evidence": [{"episode_id": "E1", "quote": "第1段原话"}],
           "criteria": [{"id": "C1", "dimension": "progress", "expectation": "具体完成当前工作。"},
                        {"id": "C2", "dimension": "fidelity", "expectation": "不把看法当成用户的感觉。"},
                        {"id": "C3", "dimension": "intrusion", "expectation": "不编造新约定。"}],
           "allowed_alternatives": ["可以直接续写。", "有必要时可以说明不确定。"]} for p in ps]
    return ({"schema": "relata.continuation-histories/v1", "histories": [h]},
            {"schema": "relata.continuation-probes/v1", "probes": ps},
            {"schema": "relata.continuation-oracles/v1", "oracles": os})


class ContinuationCoreTest(unittest.TestCase):
    def test_authored_bundle_has_full_comparison_and_literal_source_evidence(self):
        root = Path(__file__).resolve().parents[1] / "research" / "continuation-use"
        values = [json.loads((root / name).read_text()) for name in ("histories.json", "probes.json", "oracles.json")]
        result = validate_bundle(*values)
        self.assertEqual((result["histories"], result["probes"], result["oracles"]), (60, 180, 180))
        self.assertTrue(result["full_bundle"])

    def setUp(self):
        self.values = bundle()
        self.h = self.values[0]["histories"][0]
        self.p = self.values[1]["probes"][0]
        self.o = self.values[2]["oracles"][0]
        self.ranking = [{"episode_id": f"E{i}", "dense": 0, "lexical": 0, "rrf": 1/i} for i in range(1, 7)]

    def test_small_development_bundle_does_not_pass_formal_gate(self):
        self.assertEqual(validate_bundle(*self.values, require_full=False)["probes"], 3)
        with self.assertRaisesRegex(ValueError, "12 development"):
            validate_bundle(*self.values)

    def test_quote_must_belong_to_named_source_not_other_episode_or_probe(self):
        self.o["evidence"][0]["quote"] = "第2段原话"
        with self.assertRaisesRegex(ValueError, "literal"):
            validate_bundle(*self.values, require_full=False)
        self.o["evidence"][0]["quote"] = self.p["messages"][0]["text"]
        with self.assertRaisesRegex(ValueError, "literal"):
            validate_bundle(*self.values, require_full=False)

    def test_missing_episode_and_duplicate_probe_rejected(self):
        self.h["episodes"].pop()
        with self.assertRaisesRegex(ValueError, "six episodes"):
            validate_bundle(*self.values, require_full=False)
        values = bundle()
        values[1]["probes"].append(copy.deepcopy(values[1]["probes"][0]))
        with self.assertRaises(ValueError):
            validate_bundle(*values, require_full=False)

    def test_original_role_and_unicode_text_survive(self):
        text = episode_text(self.h["episodes"][0])
        self.assertIn("user: 这是第1段原话。", text)
        self.assertIn("assistant: 这是第1次我的看法，不代表你的感觉。", text)

    def test_writer_sees_only_current_episode_and_previous_actual_memory(self):
        self.h["oracle"] = "HIDDEN_AUTHOR_LABEL"
        for condition in ("summary", "notes"):
            value = writer_payload(self.h, 1, "先前生成的记忆", condition)
            data = json.loads(value["input"])
            self.assertIn("第2段原话", data["new_episode"])
            self.assertEqual(data["prior_memory"], "先前生成的记忆")
            for forbidden in ("第1段原话", "第3段原话", "TITLE_SENTINEL", "HIDDEN_AUTHOR_LABEL", "FUTURE_SENTINEL", "ORACLE_SENTINEL"):
                self.assertNotIn(forbidden, json.dumps(value, ensure_ascii=False))

    def test_current_only_contains_no_historical_text(self):
        value = reader_payload(self.h, self.p, "current", "历史不该出现", self.ranking)
        self.assertEqual(value["exposure"]["episode_ids"], [])
        self.assertEqual(json.loads(value["input"])["retained_memory"], "")
        self.assertNotIn("第1段原话", value["input"])
        self.assertIn("FUTURE_SENTINEL", value["input"])

    def test_search_selection_and_reader_instruction_are_shared(self):
        values = [reader_payload(self.h, self.p, c, "实际记忆", self.ranking) for c in ("search", "summary", "notes")]
        self.assertEqual([v["exposure"]["episode_ids"] for v in values], [["E1", "E2", "E3"]] * 3)
        self.assertEqual(len({v["instructions"] for v in values}), 1)
        self.assertEqual(len({json.dumps(v["exposure"]["quoted_sources"]) for v in values}), 1)
        for value in values:
            self.assertNotIn("TITLE_SENTINEL", value["input"])
            self.assertNotIn("ORACLE_SENTINEL", value["input"])
            self.assertFalse(value["exposure"]["token_matched"])

    def test_full_reference_preserves_all_originals(self):
        value = reader_payload(self.h, self.p, "full", "ignored", [])
        self.assertEqual(len(value["exposure"]["episode_ids"]), 6)
        self.assertIn("第6次我的看法", value["input"])
        self.assertNotIn("ignored", value["input"])

    def test_budget_failure_never_silently_truncates(self):
        with self.assertRaisesRegex(ValueError, "memory exposure"):
            reader_payload(self.h, self.p, "notes", "猫" * 2001, self.ranking)
        self.h["episodes"][0]["messages"][0]["text"] = "猫" * 4001
        with self.assertRaisesRegex(ValueError, "no silent truncation"):
            reader_payload(self.h, self.p, "search", "", self.ranking)

    def test_dense_and_lexical_relevance_reach_expected_episode(self):
        self.h["episodes"][3]["messages"][0]["text"] = "蓝色木偶需要两下船板声。"
        self.p["messages"][0]["text"] = "木偶的船板声怎么处理？"
        vectors = {e["id"]: [0.0, 1.0] for e in self.h["episodes"]}
        vectors["E4"] = [1.0, 0.0]
        ranked = rank_episodes(self.h, self.p, vectors, [1.0, 0.0])
        self.assertEqual(ranked[0]["episode_id"], "E4")
        self.assertGreater(ranked[0]["lexical"], 0)
        for invalid in ([0, 0], [float("nan"), 1], [1]):
            with self.assertRaises(ValueError):
                rank_episodes(self.h, self.p, vectors, invalid)

    def test_judge_view_is_blind_to_model_and_condition_metadata(self):
        self.h.update({"condition": "SECRET_ARM", "requested_model": "SECRET_MODEL"})
        self.p["arbitrary"] = "SECRET_EXTRA"
        value = judge_payload(self.h, self.p, self.o, "候选回答")
        for forbidden in ("SECRET_ARM", "SECRET_MODEL", "SECRET_EXTRA", "TITLE_SENTINEL", "D01-P1"):
            self.assertNotIn(forbidden, value["input"])
        self.assertIn("第6段原话", value["input"])
        self.assertIn("可以直接续写", value["input"])

    def judgment(self):
        return {"criteria": [{"id": f"C{i}", "judgment": "met", "answer_quote": "已有文字", "evidence_episode_ids": ["E1"], "reason": "原文中有可核查的回应。"} for i in range(1, 4)], "overall_note": "保留解释边界。"}

    def test_judgment_coverage_quotes_and_source_ids_are_bound(self):
        good = self.judgment()
        self.assertEqual(validate_judgment(good, self.o, "这是已有文字。", self.h), good)
        for field, bad in (("answer_quote", "不存在的引文"), ("evidence_episode_ids", ["E7"]), ("id", "C4"), ("judgment", "pass")):
            value = self.judgment()
            value["criteria"][0][field] = bad
            with self.assertRaises(ValueError):
                validate_judgment(value, self.o, "这是已有文字。", self.h)
        value = self.judgment()
        value["criteria"].pop()
        with self.assertRaises(ValueError):
            validate_judgment(value, self.o, "这是已有文字。", self.h)

    def test_missing_behavior_can_be_reviewed_without_fabricated_quote(self):
        value = self.judgment()
        value["criteria"][0].update(judgment="not_met", answer_quote="", reason="答案缺少具体可执行安排。")
        validate_judgment(value, self.o, "这是已有文字。", self.h)
        value["criteria"][0]["reason"] = "这样比较好。"
        with self.assertRaisesRegex(ValueError, "omission"):
            validate_judgment(value, self.o, "这是已有文字。", self.h)


if __name__ == "__main__":
    unittest.main()
