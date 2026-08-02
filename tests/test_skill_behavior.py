import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_export_module():
    path = ROOT / "tools" / "export-skill.py"
    spec = importlib.util.spec_from_file_location("export_skill_behavior", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/export-skill.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


export_skill = load_export_module()


class SkillBehaviorTests(unittest.TestCase):
    def test_behavior_fixture_covers_routing_and_learning_boundaries(self):
        payload = json.loads((ROOT / "evals" / "skill-behavior.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], "pjario.skill-evals/v1")
        cases = {case["id"]: case for case in payload["cases"]}
        self.assertEqual(
            set(cases),
            {
                "trivial-copy",
                "non-trivial-migration",
                "frontend-flow",
                "single-review-finding",
                "independent-repeat",
            },
        )
        self.assertFalse(cases["trivial-copy"]["expected"]["plan_required"])
        self.assertEqual(
            cases["non-trivial-migration"]["expected"]["required_risks"],
            ["RISK-01", "RISK-10"],
        )
        self.assertEqual(cases["frontend-flow"]["expected"]["profile"], "frontend")
        self.assertTrue(cases["frontend-flow"]["expected"]["design_context_required"])
        self.assertFalse(cases["single-review-finding"]["expected"]["quiet_aggregate"])
        self.assertTrue(cases["independent-repeat"]["expected"]["quiet_aggregate"])
        self.assertFalse(cases["independent-repeat"]["expected"]["policy_mutation"])

    def test_exported_skill_encodes_the_behavior_contract_concisely(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "skill"
            export_skill.export_skill(ROOT, output)
            skill = (output / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Keep trivial work small", skill)
            self.assertIn("UI/UX work: read `references/pevie-hischer.md`", skill)
            self.assertIn("same verified failure across independent reviews", skill)
            self.assertIn("Never invent evidence", skill)
            self.assertIn("Do not trigger merely because ordinary software work", skill)
            self.assertLessEqual(len(skill.split()), 220)
            self.assertIn(
                "$pjario-staltman",
                (output / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
