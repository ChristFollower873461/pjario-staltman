import importlib.util
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "triage-review-finding.py"
    spec = importlib.util.spec_from_file_location("triage_review_finding", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/triage-review-finding.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


triage = load_module()


class TriageReviewFindingTests(unittest.TestCase):
    def test_build_record_turns_finding_into_garbage_collection(self):
        record = triage.build_record(
            "[P2] Missing rollback proof\n\nThe PR note did not name a rollback path.",
            "template",
        )

        self.assertIn("# Garbage Collection", record)
        self.assertIn("P2 Missing rollback proof", record)
        self.assertIn("Decision: template", record)
        self.assertIn("Missing template field", record)
        self.assertIn("tools/quiet-aggregate.py", record)

    def test_accepted_non_rule_has_explicit_rationale(self):
        record = triage.build_record("Cosmetic suggestion only.", "accepted-non-rule")
        self.assertIn("accepted-non-rule", record)
        self.assertIn("No durable rule added", record)


if __name__ == "__main__":
    unittest.main()
