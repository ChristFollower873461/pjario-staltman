#!/usr/bin/env python3
"""Export a minimal Agent Skills-compatible Pjario Staltman skill."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SKILL_MD = """---
name: pjario-staltman
description: Use when planning, coordinating, implementing, proving, or reviewing agent-built software with tickets, planning briefs, QA evidence, review packets, durable rule promotion, or the Pevie Hischer frontend quality profile.
---

# Pjario Staltman

Use this skill to keep agentic build work efficient and reviewable.

## Core Loop

1. Start from a ticket with outcome, scope, risks, acceptance criteria, and required proof.
2. Require a planning brief for non-trivial work before implementation.
3. Give the implementation agent a compact kickoff with repo path, ticket, plan, constraints, and proof commands.
4. Capture proof in tests, QA notes, screenshots, logs, review packets, or release artifacts.
5. Review with a staff-level bar focused on correctness, user risk, production risk, security, privacy, scale, and maintainability.
6. Promote repeated review friction into a rule, template, test, lint, or tool.

## When Frontend Work Uses Pevie Hischer

Read `references/pevie-hischer.md` when work touches UI, UX, design systems, accessibility, frontend performance, frontend observability, or user-facing polish.

For non-trivial UI work, establish `DESIGN.md` before implementation. Treat it as the design equivalent of `AGENTS.md`: implementation reads it first, planning maps it to proof, and review blocks unmanaged drift.

## Useful References

- `references/core-workflow.md` - package workflow, commands, and completion contract.
- `references/proof-matrix.md` - expected proof by work type.
- `references/pevie-hischer.md` - frontend-specific operating rules.

## Completion Contract

Return changed files, commands run, pass/fail results, artifact paths or identities, known gaps, and the next coordinator action.
"""

CORE_WORKFLOW_MD = """# Core Workflow

## Inputs

- Repo path and branch.
- Ticket with implementation complexity.
- Planning brief for non-trivial work.
- Constraints, risk surfaces, required proof, and next coordinator action.

## Commands

```bash
make doctor
make kickoff TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md
make test
make validate-examples
make review-packet
make public-ready
```

For trivial tickets, omit `PLAN`.

## Review Packet Rule

The tracked diff is mandatory review context. If the diff cannot fit, narrow the diff or increase the packet budget rather than trimming the changes under review.
"""

PEVIE_MD = """# Pevie Hischer

Use Pevie for frontend-heavy work where visual quality, design-system discipline, accessibility, performance, and QA evidence matter.

## Required Frontend Context

- `DESIGN.md` or `docs/product/DESIGN.md`.
- Ticket and planning brief for non-trivial changes.
- Frontend proof commands and manual QA notes.
- Screenshots or viewport evidence for visible changes.

## Commands

```bash
make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md
make -f "Pevie Hischer/Makefile" design-lint DESIGN=DESIGN.md
make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md
make -f "Pevie Hischer/Makefile" test
make -f "Pevie Hischer/Makefile" review-packet
```

## Review Posture

Block on broken flows, inaccessible UI, unmanaged design drift, performance regressions, missing failure states, or unproved rollout risk. Do not block on subjective taste unless it contradicts `DESIGN.md` or the product quality bar.
"""

OPENAI_YAML = """interface:
  display_name: "Pjario Staltman"
  short_description: "Agentic build workflow with tickets, proof, review, and Pevie frontend checks."
  default_prompt: "Use Pjario Staltman to structure this build, define proof, and prepare a reviewable handoff."
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def export_skill(root: Path, output: Path, force: bool = False) -> None:
    if output.exists():
        if not force:
            raise SystemExit(f"Output already exists: {output}. Rerun with --force to replace it.")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    write(output / "SKILL.md", SKILL_MD)
    write(output / "references" / "core-workflow.md", CORE_WORKFLOW_MD)
    proof_matrix = read_optional(root / "build-system" / "rules" / "proof-matrix.md")
    if proof_matrix:
        write(output / "references" / "proof-matrix.md", proof_matrix)
    write(output / "references" / "pevie-hischer.md", PEVIE_MD)
    write(output / "agents" / "openai.yaml", OPENAI_YAML)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Source package root.")
    parser.add_argument("--output", type=Path, required=True, help="Output skill directory.")
    parser.add_argument("--force", action="store_true", help="Replace the output directory if it exists.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    export_skill(args.root.resolve(), args.output.resolve(), force=args.force)
    print(f"Exported skill to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
