# Main Agent Handoff

Pjario Staltman is a portable engineering loop for agents. The preferred path uses one tracked Work Packet from intent through proof and review. The older ticket, plan, QA, PR, and completion artifacts remain supported for incremental adoption.

## What Is Included

- `build-system/templates/work-packet.md`: canonical `pjario.work/v1` contract.
- `tools/pjario.py`: start, check, review, finish, learn, and adoption-preview commands.
- `build-system/agents/`: implementation, staff review, and build coordination prompts.
- `build-system/rules/`: review, proof, scale-readiness, and technical-debt rules.
- `tools/review-packet.py`: bounded review context with mandatory Work Packet and diff support.
- `tools/quiet-aggregate.py`: private, deterministic recurrence ledger and non-mutating guardrail proposals.
- `evals/skill-behavior.json`: deterministic routing and promotion-boundary fixtures.
- `Pevie Hischer/`: optional frontend profile for design context, accessibility, performance, observability, and production QA. When adopted alone, copy its workflow into the target repo root `.github/workflows/` directory.
- `examples/work-packets/`: complete trivial and non-trivial reference packets.
- Legacy templates, tools, and examples for existing adopters.

## Preferred Commands

```bash
python3 tools/pjario.py start --help
python3 tools/pjario.py check --packet .pjario/work/WORK-ID.md
python3 tools/pjario.py review --packet .pjario/work/WORK-ID.md --base origin/main
python3 tools/pjario.py finish --packet .pjario/work/WORK-ID.md
python3 tools/pjario.py learn --help
python3 tools/pjario.py adopt --target . --profile core --dry-run
make test-all
make doctor
make local-ready
make public-ready
```

The adoption command is intentionally dry-run-only. It reports the files and policy choices a target repository needs without silently modifying that repository.

## Working Contract

1. Create one Work Packet under `.pjario/work/`.
2. Keep trivial work concise. For non-trivial work, complete Plan and map every active `RISK-xx` to one or more `PROOF-xx` requirements.
3. Run `pjario check` before implementation.
4. Implement only the stated Scope; treat Non-Goals as binding.
5. Replace pending evidence with real commands, artifacts, measurements, or observations.
6. Run `pjario review`; record the decision and findings in the packet.
7. Run `pjario finish`. Use `accepted-gap` only with a named gap and concrete next action.
8. Route only independently repeated, verified failure classes through Quiet Aggregate. Never mutate policy automatically.

For UI work, use `Profile: frontend`, provide Design Context, and apply the Pevie Hischer rules. For accepted technical debt, record owner, trigger, and removal path in the packet.

## Adoption In A Target Repository

1. Run `python3 tools/pjario.py adopt --target <repo> --profile <core|frontend> --dry-run` from this package.
2. Review the preview and copy only the selected package files through the target repository's normal change process.
3. Preserve `.pjario/work/*.md` as reviewable project history; keep the rest of `.pjario/` ignored as private runtime state.
4. Run `make doctor MODE=adopted PROFILE=<core|pevie>` and the target application's own checks.
5. Add Pjario checks to CI only after the local flow works.

## Legacy Compatibility

Existing adopters may continue to use:

```bash
make kickoff TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md
make check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md
make check-proof TICKET=path/to/ticket.md QA=path/to/qa-plan.md PR=path/to/pr-note.md COMPLETION=path/to/completion-report.md
make kickoff-build REQUEST=path/to/build-request.md
make triage-review-finding FINDING=path/to/finding.md DECISION=test
```

Do not convert active legacy work merely for cosmetic consistency. Start new work with a Work Packet and migrate old artifacts only when useful.

## Completion Evidence

Before proposing completion, report:

- Work Packet ID and achieved outcome.
- Files changed.
- Proof IDs and their actual evidence.
- Review decision.
- Known gaps and next action.

`make public-ready` is the package release gate. It runs both profile suites, examples, doctor checks, export budgets, review-packet generation, whitespace checks, and the pinned Pevie design validator.
