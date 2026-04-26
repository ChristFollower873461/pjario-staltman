import importlib.util
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[2]
    script = root / "Pevie Hischer" / "tools" / "check-planning-brief.py"
    spec = importlib.util.spec_from_file_location("pevie_check_planning_brief", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Pevie Hischer check-planning-brief.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_planning_brief = load_module()


class PeviePlanningBriefTests(unittest.TestCase):
    def write(self, root: Path, rel: str, content: str) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def valid_plan(self) -> str:
        return """# Planning Brief

## Ticket Restatement
Ship a frontend quality package.

## Scope And Non-Goals
In:
- Add package files.
Out:
- CI adoption in host repos.

## Approach
- Reuse proven operating loop.

## Dependencies And Unknowns
Dependencies:
- Existing agent workflow.
Unknowns:
- Host stack details.

## Risk-To-Proof Mapping
- Accessibility -> manual checks
- Performance -> budget notes
- Data/API correctness -> tests
- External dependency reliability -> fallback behavior
- Privacy/PII -> safe logging
- Rollout/rollback -> feature flag and revert

## QA Strategy
Automated:
- make test
Manual:
- smoke key flows
Failure-path:
- forced API error state

## Rollout And Rollback
- Feature flag: yes
- Rollout stages: internal, 10%, 100%
- Rollback trigger: regression
- Rollback steps: disable flag and revert

## Ready-To-Implement Gate
- [ ] Scope and non-goals are explicit.
- [ ] Key risks are mapped to proof.
- [ ] QA plan is concrete.
- [ ] Rollout/rollback is realistic.
- [ ] Unknowns are resolved or intentionally tracked.
"""

    def test_trivial_ticket_passes_without_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: trivial\n",
            )
            exit_code = check_planning_brief.main(["--ticket", str(ticket)])
            self.assertEqual(exit_code, 0)

    def test_non_trivial_ticket_requires_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: non-trivial\n",
            )
            with self.assertRaises(SystemExit) as exc:
                check_planning_brief.main(["--ticket", str(ticket)])
            self.assertIn("requires --planning-brief", str(exc.exception))

    def test_non_trivial_ticket_passes_with_valid_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: non-trivial\n",
            )
            plan = self.write(root, "plan.md", self.valid_plan())
            exit_code = check_planning_brief.main(
                ["--ticket", str(ticket), "--planning-brief", str(plan)]
            )
            self.assertEqual(exit_code, 0)

    def test_missing_required_plan_section_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = self.write(
                root,
                "ticket.md",
                "# Ticket\n\n## Implementation Complexity\n\nLevel: non-trivial\n",
            )
            plan = self.write(
                root,
                "plan.md",
                self.valid_plan().replace("## QA Strategy", "## QA Removed"),
            )
            with self.assertRaises(SystemExit) as exc:
                check_planning_brief.main(
                    ["--ticket", str(ticket), "--planning-brief", str(plan)]
                )
            self.assertIn("missing required section", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
