import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "check-proof.py"
    spec = importlib.util.spec_from_file_location("check_proof", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/check-proof.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_proof = load_module()


class CheckProofTests(unittest.TestCase):
    def write(self, root: Path, rel: str, text: str) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def ticket(self) -> str:
        return """# Ticket

## Risk Surfaces

- Data writes or migrations: None.
- Authn/authz: None.
- Multi-tenancy: None.
- External calls: None.
- Async/background work: None.
- LLM/AI: Prompt context affects reviewer accuracy.
- PII/privacy: Privacy scan is required.
- Billing/cost: None.
- Rollout/rollback: Revert commit if checks fail.

## Required Proof

- `make public-ready`
"""

    def test_passes_when_evidence_covers_active_risks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(root, "ticket.md", self.ticket())
            qa = self.write(root, "qa.md", "Automated Checks\n- make public-ready\n- LLM prompt smoke\n")
            pr = self.write(root, "pr.md", "Privacy scan passed. Rollback path is revert commit.\n")
            check_proof.validate(ticket, qa, pr, None)

    def test_fails_when_active_risk_lacks_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(root, "ticket.md", self.ticket())
            qa = self.write(root, "qa.md", "Automated Checks\n- make public-ready\n")
            pr = self.write(root, "pr.md", "Privacy scan passed.\n")
            with self.assertRaises(SystemExit) as exc:
                check_proof.validate(ticket, qa, pr, None)
            self.assertIn("Rollout/rollback", str(exc.exception))

    def test_fails_for_empty_required_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(root, "ticket.md", self.ticket().replace("- `make public-ready`", ""))
            qa = self.write(root, "qa.md", "LLM privacy rollback\n")
            pr = self.write(root, "pr.md", "LLM privacy rollback\n")
            with self.assertRaises(SystemExit) as exc:
                check_proof.validate(ticket, qa, pr, None)
            self.assertIn("Required Proof", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
