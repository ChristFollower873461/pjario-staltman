#!/usr/bin/env python3
"""Require planning briefs for non-trivial frontend tickets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "## Ticket Restatement",
    "## Scope And Non-Goals",
    "## Approach",
    "## Dependencies And Unknowns",
    "## Risk-To-Proof Mapping",
    "## QA Strategy",
    "## Rollout And Rollback",
    "## Ready-To-Implement Gate",
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")
    if not path.is_file():
        raise SystemExit(f"Expected file path, got: {path}")
    return path.read_text(encoding="utf-8")


def detect_level(ticket_text: str) -> str:
    match = re.search(r"^Level:\s*(trivial|non-trivial)\s*$", ticket_text, re.IGNORECASE | re.MULTILINE)
    if not match:
        raise SystemExit("Ticket must declare complexity: `Level: trivial` or `Level: non-trivial`.")
    return match.group(1).lower()


def validate_plan(plan_text: str) -> None:
    for section in REQUIRED_SECTIONS:
        if section not in plan_text:
            raise SystemExit(f"Planning brief missing required section: {section}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket", type=Path, required=True, help="Ticket markdown path")
    parser.add_argument("--planning-brief", type=Path, help="Planning brief markdown path")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    level = detect_level(read_text(args.ticket))
    if level == "trivial":
        print("PASS: trivial ticket; planning brief optional.")
        return 0
    if not args.planning_brief:
        raise SystemExit("Non-trivial ticket requires --planning-brief.")
    validate_plan(read_text(args.planning_brief))
    print("PASS: non-trivial ticket includes planning brief.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
