import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PNG = ROOT / "docs" / "assets" / "github-social-preview.png"
SOURCE = ROOT / "docs" / "assets" / "github-social-preview.svg"


class SocialPreviewTests(unittest.TestCase):
    def test_github_preview_has_expected_dimensions_and_size(self):
        data = PNG.read_bytes()

        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", data[16:24]), (1280, 640))
        self.assertLess(len(data), 1_000_000)

    def test_preview_source_keeps_product_boundaries_explicit(self):
        source = SOURCE.read_text(encoding="utf-8")

        self.assertIn("One packet.", source)
        self.assertIn("Attach proof", source)
        self.assertIn("QUIET AGGREGATE", source)
        self.assertIn("HUMAN-REVIEWED GUARDRAIL", source)
        self.assertIn("Never silently changes policy.", source)


if __name__ == "__main__":
    unittest.main()
