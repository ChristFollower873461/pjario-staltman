import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "doctor.py"
    spec = importlib.util.spec_from_file_location("doctor", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/doctor.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


doctor = load_module()


class DoctorTests(unittest.TestCase):
    def test_privacy_scan_flags_local_user_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_path = "/Users/" + "sta" + "ndley/private"
            (root / "notes.md").write_text(f"Path: {private_path}\n", encoding="utf-8")
            report = doctor.Report(passes=[], warnings=[], failures=[])
            doctor.scan_privacy(root, report)
            self.assertTrue(report.failures)
            self.assertIn("local absolute user path", report.failures[0])

    def test_require_pevie_design_in_adopted_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = doctor.Report(passes=[], warnings=[], failures=[])
            doctor.require_pevie_design(root, report, mode="adopted")
            self.assertTrue(report.failures)
            self.assertIn("DESIGN.md", report.failures[0])

            report = doctor.Report(passes=[], warnings=[], failures=[])
            (root / "docs" / "product").mkdir(parents=True)
            (root / "docs" / "product" / "DESIGN.md").write_text("# Design\n", encoding="utf-8")
            doctor.require_pevie_design(root, report, mode="adopted")
            self.assertFalse(report.failures)
            self.assertTrue(report.passes)


if __name__ == "__main__":
    unittest.main()
