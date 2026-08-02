import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "export-skill.py"
    spec = importlib.util.spec_from_file_location("export_skill", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/export-skill.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


export_skill = load_module()


class ExportSkillTests(unittest.TestCase):
    def test_export_fails_without_reuse_terms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "source"
            root.mkdir()
            output = Path(tmp) / "export"

            with self.assertRaisesRegex(SystemExit, "missing LICENSE"):
                export_skill.export_skill(root, output)
            self.assertFalse(output.exists())

    def test_export_skill_has_minimal_skill_shape(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pjario-staltman"
            export_skill.export_skill(source_root, output)

            self.assertTrue((output / "SKILL.md").is_file())
            self.assertEqual(
                (output / "LICENSE").read_text(encoding="utf-8"),
                (source_root / "LICENSE").read_text(encoding="utf-8"),
            )
            self.assertTrue((output / "references" / "core-workflow.md").is_file())
            self.assertTrue((output / "references" / "completion-contract.md").is_file())
            self.assertTrue((output / "references" / "technical-debt.md").is_file())
            self.assertTrue((output / "references" / "quiet-aggregate.md").is_file())
            self.assertTrue((output / "references" / "pevie-hischer.md").is_file())
            self.assertTrue((output / "references" / "proof-matrix.md").is_file())
            quiet_aggregate = output / "scripts" / "quiet-aggregate"
            self.assertTrue(quiet_aggregate.is_file())
            self.assertTrue(quiet_aggregate.stat().st_mode & 0o111)
            self.assertIn("quiet-aggregate.finding/v1", quiet_aggregate.read_text(encoding="utf-8"))
            self.assertTrue((output / "agents" / "openai.yaml").is_file())
            self.assertFalse((output / "README.md").exists())
            self.assertIn("name: pjario-staltman", (output / "SKILL.md").read_text(encoding="utf-8"))

    def test_caveman_export_has_no_references(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pjario-staltman-caveman"
            export_skill.export_skill(source_root, output, mode="caveman")

            skill_text = (output / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue((output / "SKILL.md").is_file())
            self.assertEqual(
                (output / "LICENSE").read_text(encoding="utf-8"),
                (source_root / "LICENSE").read_text(encoding="utf-8"),
            )
            self.assertTrue((output / "agents" / "openai.yaml").is_file())
            self.assertFalse((output / "references").exists())
            self.assertFalse((output / "scripts").exists())
            self.assertIn("Caveman Mode", skill_text)
            self.assertLessEqual(len(skill_text.split()), 140)


if __name__ == "__main__":
    unittest.main()
