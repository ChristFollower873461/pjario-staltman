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

    def test_stack_hints_warn_without_failing(self):
        report = doctor.Report()
        doctor.add_stack_hints("web", report)
        self.assertFalse(report.failures)
        self.assertTrue(report.warnings)
        self.assertIn("lint", report.warnings[0])

    def test_publication_docs_require_trust_contract_and_public_ready_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Package\n", encoding="utf-8")
            (root / "PUBLICATION-CHECKLIST.md").write_text("# Checklist\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")

            report = doctor.Report(passes=[], warnings=[], failures=[])
            doctor.check_publication_docs(root, report)
            self.assertTrue(report.failures)
            self.assertIn("docs/trust-contract.md", report.failures[0])

            (root / "docs").mkdir()
            (root / "docs" / "trust-contract.md").write_text("Run make public-ready.\n", encoding="utf-8")
            report = doctor.Report(passes=[], warnings=[], failures=[])
            doctor.check_publication_docs(root, report)
            self.assertTrue(report.failures)
            self.assertIn("public-ready gate", report.failures[0])

            (root / "README.md").write_text("Run make public-ready.\n", encoding="utf-8")
            report = doctor.Report(passes=[], warnings=[], failures=[])
            doctor.check_publication_docs(root, report)
            self.assertFalse(report.failures)


if __name__ == "__main__":
    unittest.main()
