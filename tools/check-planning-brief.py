#!/usr/bin/env python3
"""Enforce planning brief presence for non-trivial tickets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PLAN_SECTIONS = [
    "## Ticket Restatement",
    "## Scope And Non-Goals",
    "## Proposed Approach",
    "## Dependencies And Unknowns",
    "## Risk-To-Proof Map",
    "## Test And QA Plan",
    "## Rollout And Rollback Plan",
    "## Ready-To-Implement Gate",
]

READY_GATE_CHECKS = [
    "- [ ] Outcome and non-goals are unambiguous.",
    "- [ ] Relevant risk surfaces are mapped to proof.",
    "- [ ] Required tests and manual QA are defined.",
    "- [ ] Rollout and rollback are concrete.",
    "- [ ] Open unknowns are resolved or explicitly tracked.",
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")
    if not path.is_file():
        raise SystemExit(f"Expected a file path, got: {path}")
    return path.read_text(encoding="utf-8")


def detect_ticket_complexity(ticket_text: str) -> str:
    match = re.search(
        r"^Level:\s*(trivial|non-trivial)\s*$",
        ticket_text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        raise SystemExit(
            "Ticket is missing implementation complexity. Add `Level: trivial` or "
            "`Level: non-trivial` under `## Implementation Complexity`."
        )
    return match.group(1).lower()


def require_non_placeholder(plan_text: str, section_header: str) -> None:
    next_section_match = re.search(
        rf"^{re.escape(section_header)}\n(.*?)(?=^## |\Z)",
        plan_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not next_section_match:
        raise SystemExit(f"Planning brief is missing section: {section_header}")
    body = next_section_match.group(1)
    meaningful_lines = [
        line.strip()
        for line in body.splitlines()
        if line.strip() and line.strip() not in {"-", "In:", "Out:"}
    ]
    if not meaningful_lines:
        raise SystemExit(f"Planning brief section is empty: {section_header}")


def validate_planning_brief(plan_text: str) -> None:
    for section in REQUIRED_PLAN_SECTIONS:
        require_non_placeholder(plan_text, section)

    missing_gate_lines = [line for line in READY_GATE_CHECKS if line not in plan_text]
    if missing_gate_lines:
        raise SystemExit(
            "Planning brief checklist appears out of date. Restore the required "
            "ready-to-implement gate items from the template."
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket", type=Path, required=True, help="Path to filled ticket markdown")
    parser.add_argument(
        "--planning-brief",
        type=Path,
        required=False,
        help="Path to filled planning brief markdown",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    ticket_text = read_text(args.ticket)
    complexity = detect_ticket_complexity(ticket_text)

    if complexity == "trivial":
        print("PASS: Ticket marked trivial; planning brief not required.")
        return 0

    if not args.planning_brief:
        raise SystemExit(
            "Ticket is non-trivial, but --planning-brief was not provided."
        )
    plan_text = read_text(args.planning_brief)
    validate_planning_brief(plan_text)
    print("PASS: Non-trivial ticket includes a valid planning brief.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
