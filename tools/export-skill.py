#!/usr/bin/env python3
"""Export a minimal Agent Skills-compatible Pjario Staltman skill."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


STANDARD_SKILL_MD = """---
name: pjario-staltman
description: Use when a repository explicitly adopts Pjario Staltman or the user requests Pjario Work Packets, ticket-to-proof workflow, staff review packets, Quiet Aggregate learning, Pevie Hischer frontend quality checks, or Pjario adoption/removal. Do not trigger merely because ordinary software work involves planning, implementation, or review.
---

# Pjario Staltman

Use one tracked Work Packet as the task, plan, proof ledger, review state, and handoff.

## Flow

1. Inspect the target repo and its `AGENTS.md` before editing.
2. Run `python3 scripts/pjario start --help`; create one packet under `.pjario/work/`.
3. Keep trivial work small. For non-trivial work, complete Plan and map every active `RISK-xx` to a `PROOF-xx` requirement.
4. Run `python3 scripts/pjario check --packet <path>` before implementation.
5. Implement the scoped change and replace each proof's pending evidence with a terminal result.
6. Run `python3 scripts/pjario review --packet <path>` and then `python3 scripts/pjario finish --packet <path>`.

## Route Context

- UI/UX work: read `references/pevie-hischer.md`; require Design Context.
- Proof selection: read `references/proof-matrix.md`.
- Accepted debt: read `references/technical-debt.md`.
- The same verified failure across independent reviews: read `references/quiet-aggregate.md`, then use `pjario learn`.
- Adoption, review command details, or legacy artifact compatibility: read `references/core-workflow.md`.

Never invent evidence, activate Quiet Aggregate from one review, expose private ledger contents, or mutate policy automatically.
"""

CORE_WORKFLOW_MD = """# Core Workflow

Prefer the versioned `pjario.work/v1` Work Packet. Legacy ticket, plan, QA, PR, and completion files remain supported for existing adopters.

```bash
python3 scripts/pjario start --help
python3 scripts/pjario check --packet .pjario/work/WORK-ID.md
python3 scripts/pjario review --packet .pjario/work/WORK-ID.md --base origin/main
python3 scripts/pjario finish --packet .pjario/work/WORK-ID.md
python3 scripts/pjario adopt --profile core --dry-run
```

`review` always includes the Work Packet and tracked diff. `adopt` is dry-run-only. Use host-repo checks in addition to Pjario validation.
"""

TECHNICAL_DEBT_MD = """# Oh Shucksenburg

Use when work adds shortcuts, duplication, coupling, stale TODOs, or future cleanup.

- Name debt explicitly in the Work Packet.
- Accepted debt requires owner, trigger, and removal path.
- Paid-down debt requires behavior proof.
- Add abstractions only when they remove real duplication, risk, or cognitive load.
- For frontend work, include token bypasses, missing states, accessibility, and performance debt.
"""

QUIET_AGGREGATE_MD = """# Quiet Aggregate

Use only after a finding is verified and the same explicit failure class repeats across independent source references.

```bash
python3 scripts/pjario learn record ...
python3 scripts/pjario learn report
python3 scripts/pjario learn propose ...
```

Only actionable records count. The private ledger stays ignored. The tool never invokes a model or applies policy; review each proposal.
"""

PEVIE_MD = """# Pevie Hischer

Use for user-facing UI, UX, design systems, accessibility, frontend performance, observability, or polish.

- `DESIGN.md` or `docs/product/DESIGN.md`.
- A frontend Work Packet with concrete Design Context.
- Screenshots or viewport evidence for visible changes.
- Accessibility, failure-state, performance, and production QA proportional to risk.

Block on broken flows, inaccessible UI, unmanaged design drift, performance regressions, missing failure states, or unproved rollout risk. Do not block on subjective taste unless it contradicts `DESIGN.md` or the product quality bar.
"""

PROOF_MATRIX_MD = """# Proof Selection

Choose the smallest credible proof and map active risks to its `PROOF-xx` ID.

| Work | Minimum proof |
| --- | --- |
| Copy/docs | Targeted diff plus render or link check |
| Core logic | Happy path and one meaningful failure test |
| Refactor | Existing tests plus named behavior equivalence |
| API/contract | Schema or contract fixture and compatibility note |
| Data/migration | Forward, rollback, and data-loss proof |
| Auth/privacy | Allowed and denied access tests |
| External call | Timeout and error-path proof |
| Release/package | Artifact identity and clean install/run smoke test |
| UI | Viewport screenshot, accessibility, and failure state |
| Performance | Before/after measurement against a budget |
| Observability | Event name and emitted sample |
| Agent tooling | Unit test plus real command invocation |

Evidence must name the command, artifact, measurement, or observation. Use `accepted-gap` only with a concrete Known Gaps entry and next action.
"""

CAVEMAN_SKILL_MD = """---
name: pjario-staltman
description: Use when the user explicitly requests Pjario's smallest Work Packet loop for scoped implementation, proof, review, debt, or cleanup.
---

# Pjario Staltman: Caveman Mode

Do the smallest durable loop:

1. Create one Work Packet: outcome, scope, risks, proof IDs.
2. Add a plan only when non-trivial.
3. Build the scoped change.
4. Attach real evidence to every proof ID.
5. Review the packet and diff.
6. Name accepted debt: owner, trigger, removal path.
7. Promote only independently repeated, verified friction.

For frontend work, establish `DESIGN.md` before implementation.
"""

OPENAI_YAML = """interface:
  display_name: "Pjario Staltman"
  short_description: "One Work Packet from intent through proof"
  default_prompt: "Use $pjario-staltman to run this change through one scoped Work Packet, proof, and review."
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_executable(path: Path, text: str) -> None:
    write(path, text)
    path.chmod(0o755)


def read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def export_skill(root: Path, output: Path, force: bool = False, mode: str = "standard") -> None:
    license_text = read_optional(root / "LICENSE")
    if not license_text:
        raise SystemExit("Source package is missing LICENSE; exported skills must carry reuse terms.")

    if output.exists():
        if not force:
            raise SystemExit(f"Output already exists: {output}. Rerun with --force to replace it.")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    write(output / "LICENSE", license_text)

    if mode == "caveman":
        write(output / "SKILL.md", CAVEMAN_SKILL_MD)
        write(output / "agents" / "openai.yaml", OPENAI_YAML)
        return

    write(output / "SKILL.md", STANDARD_SKILL_MD)
    write(output / "references" / "core-workflow.md", CORE_WORKFLOW_MD)
    write(output / "references" / "technical-debt.md", TECHNICAL_DEBT_MD)
    write(output / "references" / "quiet-aggregate.md", QUIET_AGGREGATE_MD)
    write(output / "references" / "proof-matrix.md", PROOF_MATRIX_MD)
    write(output / "references" / "pevie-hischer.md", PEVIE_MD)
    work_packet = read_optional(root / "build-system" / "templates" / "work-packet.md")
    if not work_packet:
        raise SystemExit("Source package is missing the Work Packet template.")
    write(output / "assets" / "work-packet.md", work_packet)
    pjario = read_optional(root / "tools" / "pjario.py")
    if not pjario:
        raise SystemExit("Source package is missing tools/pjario.py.")
    write_executable(output / "scripts" / "pjario", pjario)
    quiet_aggregate = read_optional(root / "tools" / "quiet-aggregate.py")
    if not quiet_aggregate:
        raise SystemExit("Source package is missing tools/quiet-aggregate.py.")
    write_executable(output / "scripts" / "quiet-aggregate", quiet_aggregate)
    review_packet = read_optional(root / "tools" / "review-packet.py")
    if not review_packet:
        raise SystemExit("Source package is missing tools/review-packet.py.")
    write_executable(output / "scripts" / "review-packet", review_packet)
    write(output / "agents" / "openai.yaml", OPENAI_YAML)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Source package root.")
    parser.add_argument("--output", type=Path, required=True, help="Output skill directory.")
    parser.add_argument("--force", action="store_true", help="Replace the output directory if it exists.")
    parser.add_argument("--mode", choices=["standard", "caveman"], default="standard")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    export_skill(args.root.resolve(), args.output.resolve(), force=args.force, mode=args.mode)
    print(f"Exported skill to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
