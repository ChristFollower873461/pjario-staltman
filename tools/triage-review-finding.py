#!/usr/bin/env python3
"""Convert a review finding into a garbage-collection decision record."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DECISIONS = [
    "rule",
    "template",
    "test",
    "lint",
    "runtime-guardrail",
    "tooling",
    "accepted-non-rule",
]


def read_finding(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    if not path.is_file():
        raise SystemExit(f"Expected finding file path: {path}")
    return path.read_text(encoding="utf-8")


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def infer_failure_class(decision: str) -> str:
    return {
        "rule": "Missing rule",
        "template": "Missing template field",
        "test": "Missing test",
        "lint": "Missing lint/source check",
        "runtime-guardrail": "Missing runtime guardrail",
        "tooling": "Slow/flaky workflow",
        "accepted-non-rule": "Accepted non-rule",
    }[decision]


def extract_title(text: str) -> str:
    match = re.search(r"\[(P[0-3])\]\s+(.+)", text)
    if match:
        return f"{match.group(1)} {match.group(2).strip()}"
    first = next((line.strip("# ").strip() for line in text.splitlines() if line.strip()), "Review finding")
    return first[:90]


def build_record(finding: str, decision: str) -> str:
    title = extract_title(finding)
    body = compact(finding)
    failure_class = infer_failure_class(decision)
    durable_fix = "No durable rule added; record the rationale and revisit if it repeats."
    if decision != "accepted-non-rule":
        durable_fix = f"Add or update a {decision.replace('-', ' ')} so this failure is caught earlier."

    return f"""# Garbage Collection

## Repeated Friction

- {title}

## Quiet Aggregate Evidence

- Not recorded by this single-finding helper. Use `tools/quiet-aggregate.py` when recurrence across independent reviews needs an auditable ledger.

## Failure Class

- {failure_class}

## Root Cause

The review found a gap that the current workflow did not prevent before review.

## Durable Fix

- Decision: {decision}
- Action: {durable_fix}

## Source Finding

```text
{body}
```

## Acceptance Criteria

- Future similar work is caught before staff review, or the accepted non-rule rationale is explicit.

## Owner

- Coordinator
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finding", type=Path, help="Finding text file. Reads stdin if omitted.")
    parser.add_argument("--decision", choices=DECISIONS, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    record = build_record(read_finding(args.finding), args.decision)
    if args.output:
        args.output.write_text(record, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(record, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
