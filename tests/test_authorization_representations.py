"""Regression tests for the fixed authorization representation bundle."""

from copy import deepcopy
import importlib.util
import io
import json
import re
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "research/authorization-continuity/prepare_representations.py"
spec = importlib.util.spec_from_file_location(
    "authorization_representations", CLI)
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def patched_read(mapping):
    original = study.read_json

    def read(path):
        return mapping[path] if path in mapping else original(path)

    return read


class RepresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (cls.source, cls.histories, cls.representations,
         cls.states, cls.controls) = study.validate_bundle()
        cls.ids = [history["history_id"]
                   for history in cls.source["histories"]]

    def test_counts_complete_bundle(self):
        report = study.report()
        self.assertEqual(report["histories"], 32)
        self.assertEqual(report["faithful_representations"], 96)
        self.assertEqual(report["o_states"], 32)
        self.assertEqual(report["controls"],
                         {"goal_rebinding": 1, "flattened_marginals": 4})

    def test_P_is_plain_prose_and_S_reuses_it_with_explicit_links(self):
        for history_id in self.ids:
            p = study.show(history_id, "P")["memory_body"]
            s = study.show(history_id, "S")["memory_body"]
            for turn in self.histories[history_id]["turns"]:
                self.assertNotRegex(p, rf"\b{turn['turn_id']}\b")
            self.assertEqual(re.sub(r" \[source: [^\]]+\]", "", s), p)
            facts = self.representations[history_id]["facts"]
            for fact in facts:
                self.assertIn(fact["prose"], p)
                self.assertIn(
                    f"{fact['prose']} [source: "
                    f"{', '.join(fact['source_refs'])}]", s)

    def test_common_task_metadata_mode_and_stop_rule_match_all_conditions(self):
        for history_id in self.ids:
            items = {
                condition: study.show(history_id, condition)
                for condition in study.CONDITIONS + ("O",)
            }
            tasks = {json.dumps(item["task"], ensure_ascii=False,
                                sort_keys=True)
                     for item in items.values()}
            metadata = {json.dumps(item["task"]["metadata"], ensure_ascii=False,
                                   sort_keys=True)
                        for item in items.values()}
            self.assertEqual(len(tasks), 1)
            self.assertEqual(len(metadata), 1)
            task = next(iter(items.values()))["task"]
            self.assertEqual(task["candidate_mode"],
                             self.histories[history_id]["candidate_mode"])
            self.assertEqual(task["candidate_instruction"],
                             self.histories[history_id]
                             ["candidate_instruction"])
            expected = (
                "不要执行" if task["candidate_mode"] ==
                "independent_eligibility" else "顺序")
            self.assertIn(expected, task["candidate_instruction"])

    def test_all_P_facts_have_sources_and_capability_metadata(self):
        for history_id in self.ids:
            item = study.show(history_id, "P")
            history = self.histories[history_id]
            self.assertEqual(
                item["task"]["metadata"],
                [{"turn_id": turn["turn_id"], "speaker": turn["speaker"],
                  "role": turn["role"], "capability": turn["capability"]}
                 for turn in history["turns"]])

    def test_acceptance_and_revocation_events_do_not_masquerade_as_current_state(self):
        f6 = study.show("hist-736e9ed7b374", "R")["memory_body"]
        self.assertIn("撤销事件", f6)
        self.assertNotIn("validity=revoked", f6)
        f7 = study.show("hist-a6c594a6d4ea", "R")["memory_body"]
        self.assertIn("撤销事件", f7)
        self.assertNotIn("不再有效", f7)

    def test_required_family_facts_remain_visible(self):
        checks = {
            ("hist-d40354c35dd3", "P"): (
                "private-notes", "private-workspace", "project-note"),
            ("hist-f9778437ec02", "P"): (
                "private-notes", "public-site", "方案编号"),
            ("hist-534ecab6942d", "R"): (
                "material-a", "material-b", "spent=0"),
            ("hist-7bc52ce79d20", "R"): (
                "material-a", "material-b", "spent=5"),
            ("hist-123167c4d18b", "P"): (
                "public", "team-cleared", "draft-v1"),
            ("hist-181d811fff30", "P"): (
                "private diary", "draft-v1", "owner bridge"),
            ("hist-736e9ed7b374", "R"): (
                "授权", "撤销事件", "t02"),
            ("hist-a6c594a6d4ea", "R"): (
                "撤销事件", "t02", "此后不要再 draft 或 modify"),
            ("hist-f4373c2319d3", "R"): (
                "private-workspace", "排除 public release"),
            ("hist-79f3ad41ad1f", "R"): (
                "授权一", "授权二"),
        }
        for (history_id, condition), fragments in checks.items():
            body = study.show(history_id, condition)["memory_body"]
            for fragment in fragments:
                self.assertIn(fragment, body)

    def test_unknowns_remain_unresolved_without_certainty(self):
        for history_id in ("hist-f9778437ec02", "hist-d10e8f2ca77d",
                           "hist-895ee1b6a30f"):
            state = study.show(history_id, "O")["state"]
            self.assertTrue(state["unresolved"])
            self.assertTrue(state["environment"]["resolved_scope"].startswith(
                "absent-pending-"))
            text = json.dumps(state, ensure_ascii=False)
            self.assertIn("unknown", text)
            self.assertNotIn('"decision"', text)

    def test_authority_metadata_is_chronological_not_flattened(self):
        case = study.show("hist-895ee1b6a30f", "P")
        self.assertEqual(case["task"]["metadata"][0]["speaker"], "S")
        self.assertIn("未记录", case["task"]["metadata"][0]["capability"])
        self.assertNotIn("可授权修改", case["task"]["metadata"][0]["capability"])
        self.assertIn("U 拥有", case["task"]["background"])

    def test_all_32_faithful_arms_load_without_history_oracle(self):
        calls = []
        original = study.read_json

        def observed(path):
            calls.append(path)
            return original(path)

        with patch.object(study, "read_json", observed):
            for history_id in self.ids:
                for condition in study.CONDITIONS:
                    study.show(history_id, condition)
        self.assertFalse(any(path.name == "history-oracles.json"
                             for path in calls))
        self.assertNotIn(study.AUDIT, calls)
        self.assertNotIn(study.STATES, calls)
        self.assertNotIn(study.CONTROLS, calls)

    def test_report_computes_a_separate_O_full_input_length(self):
        report = study.report()
        item = study.show("hist-f9778437ec02", "O")
        row = next(entry for entry in report["O_sizes"]
                   if entry["history_id"] == "hist-f9778437ec02")
        self.assertEqual(
            row["memory"],
            study.length_metrics(
                study.canonical(item["state"]).decode("utf-8")))
        self.assertEqual(
            row["projection"],
            study.length_metrics(study.canonical(item).decode("utf-8")))

    def test_legal_positive_controls_remain_visible(self):
        checks = {
            ("hist-f0c9f796e64f", "R"):
                ("C 的分类事实", "接受 P3"),
            ("hist-220fb4c7c506", "R"):
                ("bridge", "preserves_label=true"),
            ("hist-aea9d6e21b29", "R"):
                ("撤销尝试事件：C", "t01 许可"),
            ("hist-b79457a4d666", "R"):
                ("持续裁量", "可自主选择", "直到 U 撤销"),
        }
        for (history_id, condition), fragments in checks.items():
            body = study.show(history_id, condition)["memory_body"]
            for fragment in fragments:
                self.assertIn(fragment, body)

    def test_O_preserves_complete_grants_and_issued_state(self):
        f1 = study.show("hist-ef80f8ff5f05", "O")["state"]
        self.assertEqual(
            [scope["verb"] for scope in f1["grants"][0]["scope"]],
            ["read", "organize"])
        f4v4 = study.show("hist-7bc52ce79d20", "O")["state"]
        self.assertEqual(
            {scope["object"] for grant in f4v4["grants"]
             for scope in grant["scope"]},
            {"material-a", "material-b"})
        f6v4 = study.show("hist-317b23b1f581", "O")["state"]
        self.assertEqual(f6v4["grants"][0]["validity"]["status"], "issued")
        self.assertEqual(f6v4["environment"]["clock"], "t05")
        self.assertNotIn('"decision"', json.dumps(f6v4))

    def test_O_does_not_import_scope_from_the_rejected_proposal(self):
        state = study.show("hist-336c786c1900", "O")["state"]
        self.assertEqual(state["acceptance"]["referent"], "P2")
        self.assertEqual(state["grants"][0]["scope"], [{
            "verb": "publish", "object": "project-note",
            "purpose": "prepare-project", "surface": "public-site",
        }])

    def test_representations_preserve_source_negations_and_bridge_scope(self):
        for history_id in ("hist-336c786c1900", "hist-a87beb01b97b"):
            for condition in ("P", "R"):
                body = study.show(history_id, condition)["memory_body"]
                self.assertTrue(any(term in body for term in (
                    "不包含公开发布", "不延伸到发布", "排除 public release",
                    "不含 publish")))
        for condition in ("P", "R"):
            body = study.show("hist-7e0b5b519abb", condition)["memory_body"]
            for term in ("draft-v2", "private diary", "project-release",
                         "public-site"):
                self.assertIn(term, body)
            self.assertTrue("来源标签继续保留" in body or
                            "preserves_label=true" in body)

    def test_controls_are_explicit_and_truthful_about_mechanism(self):
        self.assertEqual(
            self.controls["goal_rebinding"]["applicable_history_ids"],
            ["hist-ef80f8ff5f05"])
        self.assertEqual(
            self.controls["flattened_marginals"]
            ["applicable_history_ids"],
            ["hist-2c7f217a3e94", "hist-9c680d06c3b1",
             "hist-79f3ad41ad1f", "hist-a87beb01b97b"])
        with self.assertRaisesRegex(ValueError, "not applicable"):
            study.show("hist-9d77406b45d7", "goal_rebinding")
        with self.assertRaisesRegex(ValueError, "not applicable"):
            study.show("hist-ef80f8ff5f05", "flattened_marginals")

    def test_goal_rebinding_does_not_announce_intervention(self):
        body = study.show(
            "hist-ef80f8ff5f05", "goal_rebinding")["memory_body"]
        self.assertIn("private-workspace", body)
        self.assertIn("P1 明确不包含公开发布", body)
        self.assertIn("接受了同一 prepare-project 目标的 P2", body)
        self.assertNotIn("改写", body)
        self.assertNotIn("deliberate", body)

    def test_flattened_controls_have_no_complete_rows_and_match_each_source(self):
        baseline = self.controls["flattened_marginals"]["variants"]
        for history_id in self.controls[
                "flattened_marginals"]["applicable_history_ids"]:
            body = study.show(
                history_id, "flattened_marginals")["memory_body"]
            self.assertNotIn("[read |", body)
            self.assertNotIn("[publish |", body)
            if history_id != "hist-a87beb01b97b":
                self.assertNotIn("t03", body)
            self.assertEqual(body, baseline[history_id])

    def test_audit_quotes_match_named_ref_and_representation_witnesses(self):
        audit = study.read_json(study.AUDIT)
        for row in audit["histories"]:
            history = self.histories[row["history_id"]]
            facts = self.representations[row["history_id"]]["facts"]
            self.assertEqual([fact["fact_id"] for fact in row["facts"]],
                             [fact["fact_id"] for fact in facts])
            for audit_fact, fact in zip(row["facts"], facts):
                self.assertEqual(audit_fact["prose_witness"], fact["prose"])
                self.assertEqual(audit_fact["relation_witness"],
                                 fact["relation"])
                self.assertIn(
                    fact["prose"],
                    study.show(row["history_id"], "P")["memory_body"])
                self.assertIn(
                    fact["relation"],
                    study.show(row["history_id"], "R")["memory_body"])
                for witness in audit_fact["source_witnesses"]:
                    target = next(
                        turn for turn in history["turns"]
                        if turn["turn_id"] == witness["ref"])
                    self.assertEqual(target["text"], witness["quote"])

    def test_author_labels_and_decisions_are_not_exported(self):
        for history_id in self.ids:
            for condition in study.CONDITIONS + ("O",):
                text = json.dumps(
                    study.show(history_id, condition), ensure_ascii=False)
                for key in (
                    "author_decisions", "grant_interpretation", "rationale",
                    "fixture_witnesses", "expected", "coverage_claim",
                ):
                    self.assertNotIn(key, text)

    def test_report_exact_bytes_and_codepoints_for_both_layers_and_O(self):
        report = study.report()
        self.assertNotIn('"tokens"', json.dumps(report))
        for condition in study.CONDITIONS:
            self.assertEqual(len(report["sizes"][condition]), 32)
            self.assertEqual(len(report["full_projection"][condition]), 32)
            for body_row, full_row in zip(report["sizes"][condition],
                                          report["full_projection"][condition]):
                item = study.show(body_row["history_id"], condition)
                self.assertEqual(
                    body_row["memory"],
                    study.length_metrics(item["memory_body"]))
                self.assertEqual(
                    full_row["projection"],
                    study.length_metrics(
                        study.canonical(item).decode("utf-8")))
                self.assertIn("metadata", item["task"])
                self.assertEqual(set(item), {"scene", "task", "memory_body"})
        self.assertEqual(len(report["O_sizes"]), 32)
        for row in report["O_sizes"]:
            self.assertIn("memory", row)
            self.assertIn("projection", row)
        for row in report["paired_S_R_to_P"]:
            p = study.show(row["history_id"], "P")
            for condition in ("S", "R"):
                other = study.show(row["history_id"], condition)
                for layer, numerator, denominator in (
                    ("memory", other["memory_body"], p["memory_body"]),
                    ("projection", study.canonical(other).decode(),
                     study.canonical(p).decode()),
                ):
                    n = study.length_metrics(numerator)
                    d = study.length_metrics(denominator)
                    self.assertEqual(row[f"{condition}_to_P"][layer],
                                     {key: round(n[key] / d[key], 6)
                                      for key in ("bytes", "codepoints")})
        for control, rows in report["control_sizes"].items():
            for row in rows:
                item = study.show(row["history_id"], control)
                self.assertEqual(row["memory"],
                                 study.length_metrics(item["memory_body"]))
                self.assertEqual(row["projection"], study.length_metrics(
                    study.canonical(item).decode()))

    def test_source_binding_rejects_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            stale = Path(folder) / "histories.json"
            stale.write_bytes(study.HISTORIES.read_bytes() + b"\n")
            with patch.object(study, "HISTORIES", stale):
                with self.assertRaisesRegex(ValueError, "stale"):
                    study.validate_bundle()
        source = deepcopy(self.source)
        source["histories"][0]["turns"][0]["unexpected"] = "reason"
        mapping = {study.HISTORIES: source}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "fields"):
                study.validate_bundle()

    def test_wrong_ref_quote_duplicate_facts_and_bad_witnesses_rejected(self):
        original = study.read_json
        representations = original(study.REPRESENTATIONS)
        audit = original(study.AUDIT)

        wrong_quote = deepcopy(audit)
        wrong_quote["histories"][0]["facts"][1]["source_witnesses"][0][
            "quote"] = self.histories[
                "hist-ef80f8ff5f05"]["turns"][0]["text"]
        mapping = {study.AUDIT: wrong_quote}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "named source ref"):
                study.validate_bundle()

        missing_prose = deepcopy(representations)
        missing_prose["histories"][0]["facts"][0]["prose"] = ""
        mapping = {study.REPRESENTATIONS: missing_prose}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "empty P fact"):
                study.validate_bundle()

        duplicate = deepcopy(representations)
        duplicate["histories"][0]["facts"][1]["fact_id"] = "f01"
        mapping = {study.REPRESENTATIONS: duplicate}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "duplicate fact"):
                study.validate_bundle()

    def test_missing_common_O_fields_and_nested_author_keys_rejected(self):
        states = study.read_json(study.STATES)
        missing = deepcopy(states)
        missing["states"][0]["state"].pop("environment")
        mapping = {study.STATES: missing}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "incomplete"):
                study.validate_bundle()

        nested = deepcopy(states)
        nested["states"][0]["state"]["environment"]["expected"] = "allow"
        mapping = {study.STATES: nested}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "unknown fields"):
                study.validate_bundle()

    def test_nested_state_values_cannot_smuggle_author_objects(self):
        injections = [
            (0, ("acceptance", "referent")),
            (0, ("environment", "project_goal")),
            (0, ("environment", "later_proposal", "accepted")),
            (0, ("grants", 0, "conditions")),
            (0, ("grants", 0, "validity", "valid_until")),
            (0, ("unresolved",)),
            (6, ("grants", 0, "semantic_dependency", "fact")),
            (12, ("environment", "counters", "shared", "limit")),
            (16, ("environment", "artifacts", "draft-v1", "parents")),
            (18, ("environment", "bridges", 0, "source")),
            (24, ("grants", 0, "per_proposal_acceptance_required")),
            (31, ("grants", 0, "authority_capable")),
        ]
        for index, path in injections:
            with self.subTest(index=index, path=path):
                states = study.read_json(study.STATES)
                target = states["states"][index]["state"]
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = {"expected": "allow"}
                with patch.object(study, "read_json",
                                  patched_read({study.STATES: states})):
                    with self.assertRaises(ValueError):
                        study.show(self.ids[index], "O")

    def test_nonexistent_audit_witness_and_candidate_ref_rejected(self):
        for key in ("prose_witness", "relation_witness"):
            audit = study.read_json(study.AUDIT)
            audit["histories"][0]["facts"][0][key] = "absent text"
            with patch.object(study, "read_json",
                              patched_read({study.AUDIT: audit})):
                with self.assertRaisesRegex(ValueError, "witness differs"):
                    study.validate_bundle()
        reps = study.read_json(study.REPRESENTATIONS)
        reps["histories"][0]["facts"][0]["source_refs"] = ["a01"]
        with patch.object(study, "read_json",
                          patched_read({study.REPRESENTATIONS: reps})):
            with self.assertRaisesRegex(ValueError, "dangling source ref"):
                study.validate_bundle()

    def test_common_wrapper_is_complete_for_O_and_distortion_controls(self):
        for history_id in self.ids:
            baseline = study.show(history_id, "H")
            conditions = ["O"] + [
                name for name, control in self.controls.items()
                if history_id in control["applicable_history_ids"]]
            for condition in conditions:
                item = study.show(history_id, condition)
                self.assertEqual(item["scene"], baseline["scene"])
                self.assertEqual(item["task"], baseline["task"])
                self.assertEqual(set(item), {"scene", "task",
                    "state" if condition == "O" else "memory_body"})

    def test_controls_missing_arm_and_hash_tampering_rejected(self):
        controls = study.read_json(study.CONTROLS)
        missing = deepcopy(controls)
        missing["controls"][1]["variants"].pop("hist-79f3ad41ad1f")
        mapping = {study.CONTROLS: missing}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "IDs and variants"):
                study.validate_bundle()

        audit = study.read_json(study.AUDIT)
        stale = deepcopy(audit)
        stale["representation_sha256"] = "0" * 64
        mapping = {study.AUDIT: stale}
        with patch.object(study, "read_json", patched_read(mapping)):
            with self.assertRaisesRegex(ValueError, "representation binding"):
                study.validate_bundle()

    def test_commands_are_read_only(self):
        files = (study.HISTORIES, study.REPRESENTATIONS, study.STATES,
                 study.CONTROLS, study.AUDIT)
        before = {path: path.read_bytes() for path in files}
        with patch.object(study.sys, "stdout",
                          type("Out", (), {"buffer": io.BytesIO()})()):
            self.assertEqual(study.main(["check"]), 0)
            self.assertEqual(study.main(["report"]), 0)
            self.assertEqual(
                study.main(["show", "hist-f9778437ec02", "O"]), 0)
        self.assertEqual(before,
                         {path: path.read_bytes() for path in files})


if __name__ == "__main__":
    unittest.main()
