import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[2]
    script = root / "Pevie Hischer" / "tools" / "check-design-context.py"
    spec = importlib.util.spec_from_file_location("pevie_check_design_context", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Pevie Hischer check-design-context.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_design_context = load_module()


class PevieDesignContextTests(unittest.TestCase):
    def valid_design(self) -> str:
        return '''---
name: Ledger Desk
colors:
  primary: "#111827"
typography:
  body-md:
    fontFamily: Inter
    fontSize: 1rem
rounded:
  md: 8px
spacing:
  md: 16px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
---

## Overview

Quiet operational product.

## Colors

High-contrast neutral system.

## Typography

Inter for all UI text.

## Layout

Dense but readable.

## Elevation & Depth

Flat by default.

## Shapes

Use restrained radii.

## Components

Use canonical buttons.

## Do's and Don'ts

Do use tokens.
'''

    def write(self, root: Path, rel: str, content: str) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_design_context_passes(self):
        check_design_context.validate_design_context(self.valid_design())

    def test_missing_front_matter_fails(self):
        with self.assertRaises(SystemExit) as exc:
            check_design_context.validate_design_context("## Overview\n")
        self.assertIn("front matter", str(exc.exception))

    def test_missing_token_group_fails(self):
        with self.assertRaises(SystemExit) as exc:
            check_design_context.validate_design_context(
                self.valid_design().replace("components:\n", "componentz:\n")
            )
        self.assertIn("components", str(exc.exception))

    def test_missing_section_fails(self):
        with self.assertRaises(SystemExit) as exc:
            check_design_context.validate_design_context(
                self.valid_design().replace("## Components", "## Component Patterns")
            )
        self.assertIn("Components", str(exc.exception))

    def test_sections_must_be_in_order(self):
        design = self.valid_design().replace(
            "## Colors\n\nHigh-contrast neutral system.\n\n## Typography",
            "## Typography\n\nInter for all UI text.\n\n## Colors",
        )
        with self.assertRaises(SystemExit) as exc:
            check_design_context.validate_design_context(design)
        self.assertIn("out of order", str(exc.exception))

    def test_main_reads_design_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            design = self.write(root, "DESIGN.md", self.valid_design())
            exit_code = check_design_context.main(["--design", str(design)])
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
