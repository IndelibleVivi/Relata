"""Editorial regression guards; passing these is not case/reviewer validation."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_rc003_probe_does_not_presuppose_a_second_file(self):
        text = self.read("case-lab/cases/seed-003-project-authority-handoff.zh-CN.md")
        probe = text.split("## 5. Current probe", 1)[1].split("## 6.", 1)[0]
        self.assertIn("有没有不能手改或需要生成的文件", probe)
        self.assertNotIn("另一个文件", probe)
        self.assertIn("**Status:** seed", text)

    def test_rc004_requirement_is_in_exposed_history(self):
        text = self.read("case-lab/cases/seed-004-private-greeting-public-template.zh-CN.md")
        event = text.split("### E1 — Private-only accord", 1)[1].split("### E2", 1)[0]
        self.assertIn("欢迎语必须包含 literal `栖灯`", event)
        self.assertIn("不适用于所有 private replies", event)
        self.assertIn("prior，C0 尚未实测", text)
        self.assertIn("**Status:** seed", text)

    def test_e0_blinds_identity_not_governing_contract(self):
        text = self.read("case-lab/reviews/RC-001-e0-calibration-pack.zh-CN.md")
        instructions = text.split("Coordinator instructions:", 1)[1].split("### Twin A fixtures", 1)[0]
        self.assertIn("Never hide the governing evidence or accord", instructions)
        self.assertNotIn("Copy only `response text`", instructions)
        self.assertIn("Occurrence is not enactment", text)
        self.assertIn("not yet dry-reviewed", text)


class BenefitMaterialTests(unittest.TestCase):
    """Protect authored controls, without claiming a validated semantic evaluator."""

    def setUp(self):
        self.source = json.loads((ROOT / "case-lab/fixtures/continuity-benefit.zh-CN.json").read_text())
        self.families = {f["id"]: f for f in self.source["families"]}

    def test_development_material_is_not_promoted_or_independently_authored(self):
        self.assertEqual(self.source["split"], "development")
        self.assertEqual(self.source["status"], "authored-unvalidated")
        self.assertEqual(self.source["human_review"], "not-run")
        self.assertEqual(self.source["system_evaluation"], "not-run")
        self.assertIn("not isolated", self.source["authorship"])
        self.assertTrue(self.source["adult_synthetic"])

    def test_each_pair_has_separate_evaluator_material(self):
        self.assertEqual(len(self.families), 5)
        for family in self.families.values():
            self.assertEqual(len(family["variants"]), 2)
            self.assertEqual(len({v["id"] for v in family["variants"]}), 2)
            self.assertTrue(family["lineage"])
            for variant in family["variants"]:
                self.assertEqual(set(variant["input_view"]), {"context", "history", "current"})
                self.assertEqual(set(variant["contract"]), {"required", "prohibited", "acceptable_actions"})
                self.assertTrue(all(variant["contract"].values()))
                self.assertNotIn("authoring_environment", variant["input_view"])

    def test_irrelevant_history_does_not_change_the_task_or_contract(self):
        a, b = self.families["CB-001-NO-RECALL"]["variants"]
        self.assertNotEqual(a["input_view"]["history"], b["input_view"]["history"])
        self.assertEqual(a["input_view"]["current"], b["input_view"]["current"])
        self.assertEqual(a["contract"], b["contract"])

    def test_invisible_freshness_cannot_change_admissible_behavior(self):
        a, b = self.families["CB-003-UNKNOWN-FRESHNESS"]["variants"]
        self.assertEqual(a["input_view"], b["input_view"])
        self.assertNotEqual(a["authoring_environment"], b["authoring_environment"])
        self.assertEqual(a["contract"], b["contract"])

    def test_scope_contrasts_keep_history_and_change_current_scope(self):
        for fid in ("CB-004-USE-AND-SILENCE", "CB-005-LOCAL-EXCEPTION"):
            a, b = self.families[fid]["variants"]
            self.assertEqual(a["input_view"]["history"], b["input_view"]["history"])
            self.assertNotEqual(a["input_view"]["current"]["scope"], b["input_view"]["current"]["scope"])
            self.assertEqual(self.families[fid]["relation"], "scope-conditioned-contrast")


if __name__ == "__main__":
    unittest.main()
