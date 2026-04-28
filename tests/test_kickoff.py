import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "kickoff.py"
    spec = importlib.util.spec_from_file_location("kickoff", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/kickoff.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


kickoff = load_module()


class KickoffTests(unittest.TestCase):
    def write(self, root: Path, rel: str, text: str) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_non_trivial_ticket_requires_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(root, "ticket.md", "## Implementation Complexity\n\nLevel: non-trivial\n")
            with self.assertRaises(SystemExit) as exc:
                kickoff.build_prompt(root, ticket, None, None, "core", "main")
            self.assertIn("planning-brief", str(exc.exception))

    def test_pevie_prompt_includes_design_and_frontend_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "AGENTS.md", "# Rules\n")
            self.write(root, "Pevie Hischer/AGENTS.md", "# Frontend Rules\n")
            ticket = self.write(root, "ticket.md", "## Implementation Complexity\n\nLevel: non-trivial\n")
            plan = self.write(root, "planning-brief.md", "# Plan\n")
            design = self.write(root, "DESIGN.md", "# Design\n")

            prompt = kickoff.build_prompt(root, ticket, plan, design, "pevie", "main")

            self.assertIn("Profile: `pevie`", prompt)
            self.assertIn("DESIGN.md", prompt)
            self.assertIn("design-lint", prompt)
            self.assertIn("frontend", prompt.lower())


if __name__ == "__main__":
    unittest.main()
