import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "check-planning-brief.py"
    spec = importlib.util.spec_from_file_location("check_planning_brief", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/check-planning-brief.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_planning_brief = load_module()


class PlanningBriefCheckTests(unittest.TestCase):
    def write(self, root: Path, rel: str, content: str) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def full_plan_text(self) -> str:
        return """# Planning Brief

## Ticket Restatement
Ship safer release checks.

## Scope And Non-Goals
In:
- Enforcement and tests.
Out:
- CI integration for external repos.

## Proposed Approach
- Add a script and make target.

## Dependencies And Unknowns
Dependencies:
- None.
Unknowns:
- None.

## Risk-To-Proof Map
- Data writes/migrations -> Not applicable.
- Authn/authz -> Not applicable.
- Multi-tenancy -> Not applicable.
- External calls/timeouts -> Not applicable.
- Async/background work -> Not applicable.
- LLM/AI validation -> Not applicable.
- PII/privacy -> Not applicable.
- Billing/cost -> Not applicable.
- Rollout/rollback -> Manual rollback to previous commit.

## Test And QA Plan
Automated checks:
- make test
Manual checks:
- Run checker with sample files.
Failure-path checks:
- Missing plan should fail.

## Rollout And Rollback Plan
- Feature flag strategy: Not needed.
- Rollout stages: Internal only.
- Rollback trigger: Tooling breaks.
- Rollback steps: Revert commit.

## Ready-To-Implement Gate
- [ ] Outcome and non-goals are unambiguous.
- [ ] Relevant risk surfaces are mapped to proof.
- [ ] Required tests and manual QA are defined.
- [ ] Rollout and rollback are concrete.
- [ ] Open unknowns are resolved or explicitly tracked.
"""

    def test_detect_complexity_requires_field(self):
        with self.assertRaises(SystemExit) as exc:
            check_planning_brief.detect_ticket_complexity("# Ticket\n")
        self.assertIn("missing implementation complexity", str(exc.exception).lower())

    def test_trivial_ticket_passes_without_planning_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: trivial\n",
            )
            exit_code = check_planning_brief.main(["--ticket", str(ticket)])
            self.assertEqual(exit_code, 0)

    def test_non_trivial_ticket_requires_planning_brief_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: non-trivial\n",
            )
            with self.assertRaises(SystemExit) as exc:
                check_planning_brief.main(["--ticket", str(ticket)])
            self.assertIn("non-trivial", str(exc.exception))

    def test_non_trivial_ticket_passes_with_valid_planning_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: non-trivial\n",
            )
            plan = self.write(root, "planning-brief.md", self.full_plan_text())
            exit_code = check_planning_brief.main(
                ["--ticket", str(ticket), "--planning-brief", str(plan)]
            )
            self.assertEqual(exit_code, 0)

    def test_non_trivial_ticket_fails_for_empty_required_plan_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: non-trivial\n",
            )
            plan_text = self.full_plan_text().replace(
                "## Proposed Approach\n- Add a script and make target.\n",
                "## Proposed Approach\n\n",
            )
            plan = self.write(root, "planning-brief.md", plan_text)
            with self.assertRaises(SystemExit) as exc:
                check_planning_brief.main(
                    ["--ticket", str(ticket), "--planning-brief", str(plan)]
                )
            self.assertIn("section is empty", str(exc.exception))

    def test_planning_brief_path_must_be_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: non-trivial\n",
            )
            with self.assertRaises(SystemExit) as exc:
                check_planning_brief.main(
                    ["--ticket", str(ticket), "--planning-brief", str(root)]
                )
            self.assertIn("Expected a file path", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
