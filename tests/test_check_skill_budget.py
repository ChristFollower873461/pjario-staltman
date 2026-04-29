import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "check-skill-budget.py"
    spec = importlib.util.spec_from_file_location("check_skill_budget", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/check-skill-budget.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_skill_budget = load_module()


class CheckSkillBudgetTests(unittest.TestCase):
    def test_budget_passes_for_small_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("# Skill\nsmall words\n", encoding="utf-8")
            check_skill_budget.validate(root, max_skill_words=10, max_total_words=10)

    def test_budget_fails_for_large_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("word " * 20, encoding="utf-8")
            with self.assertRaises(SystemExit) as exc:
                check_skill_budget.validate(root, max_skill_words=10, max_total_words=30)
            self.assertIn("SKILL.md budget exceeded", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
