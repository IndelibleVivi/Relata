"""Editorial regression guards; passing these is not case/reviewer validation."""
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
