# Pjario Staltman

[![Quality](https://github.com/ChristFollower873461/pjario-staltman/actions/workflows/quality.yml/badge.svg)](https://github.com/ChristFollower873461/pjario-staltman/actions/workflows/quality.yml)

A small operating system for building software with agents.

Pjario Staltman turns agent work into a repeatable loop: tickets define intent, agents implement scoped changes, proof is captured, staff-level review checks the work, and repeated friction becomes durable guardrails instead of repeated comments.

This repository is private while the system is being refined. It is structured so it can be made public later with minimal cleanup.

## Current Status

- Visibility: private
- Public-readiness: staged for later review with [`PUBLICATION-CHECKLIST.md`](PUBLICATION-CHECKLIST.md)
- License: intentionally undecided until public reuse is approved

## Trust Path

If you are evaluating this package cold, start with [`docs/trust-contract.md`](docs/trust-contract.md). It explains what the package does, what it does not do, which commands write files, which commands read git state, which command path uses network, and the exact cold-start proof command sequence.

The public-readiness gate is:

```bash
make public-ready
```

That target runs the package tests, examples, Pevie design linting, doctor checks, skill export budget checks, review packet generation, and generated-artifact cleanup.

## Profiles

### Pjario Staltman

The core workflow for agentic engineering:

- ticketed work with explicit outcome, scope, risk, acceptance criteria, and proof
- planning briefs for non-trivial changes
- implementation-agent handoffs
- build-request handoffs for coordinated build/release work
- staff-level review prompts
- proof checks that map ticket risks to QA/PR evidence
- Oh Shucksenburg technical-debt control for shortcuts, coupling, duplication, and accepted cleanup debt
- review packet generation
- rule promotion when review feedback repeats

### Pevie Hischer

A frontend-focused companion profile in [`Pevie Hischer/`](Pevie%20Hischer/README.md). Use it when the work needs high-taste UI delivery, Stitch-compatible `DESIGN.md` discipline, accessibility, performance review, frontend observability, and production-grade QA evidence.

### Oh Shucksenburg

A technical-debt control profile in [`build-system/rules/oh-shucksenburg-technical-debt.md`](build-system/rules/oh-shucksenburg-technical-debt.md). Use it when work risks adding shortcuts, duplicated logic, hidden coupling, stale TODOs, or future maintenance cost.

## Quick Start

1. Write work using [`build-system/templates/ticket.md`](build-system/templates/ticket.md) and set `Level: trivial` or `Level: non-trivial`.
2. For non-trivial work, draft [`build-system/templates/planning-brief.md`](build-system/templates/planning-brief.md) before implementation.
3. For build or release coordination, fill [`build-system/templates/build-request.md`](build-system/templates/build-request.md) and use [`build-system/agents/build-coordinator.md`](build-system/agents/build-coordinator.md).
4. Give the task plus [`AGENTS.md`](AGENTS.md) and [`build-system/agents/implementation-agent.md`](build-system/agents/implementation-agent.md) to an implementation agent.
5. Capture QA and risk evidence with [`build-system/templates/pr.md`](build-system/templates/pr.md), [`build-system/templates/qa-plan.md`](build-system/templates/qa-plan.md), and [`build-system/templates/completion-report.md`](build-system/templates/completion-report.md).
6. Check proof coverage with `make check-proof`.
7. Generate a review packet with `make review-packet`.
8. Review with [`build-system/agents/software-engineer-reviewer.md`](build-system/agents/software-engineer-reviewer.md).
9. Promote repeated review feedback with [`build-system/templates/garbage-collection.md`](build-system/templates/garbage-collection.md).

For first-time adoption, follow [`docs/adopt-in-15-minutes.md`](docs/adopt-in-15-minutes.md).

## Commands

```bash
make test
make validate-examples
make doctor
make review-packet
make check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md
make check-proof TICKET=path/to/ticket.md QA=path/to/qa-plan.md PR=path/to/pr-note.md COMPLETION=path/to/completion-report.md
make kickoff TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md
make kickoff-build REQUEST=path/to/build-request.md
make triage-review-finding FINDING=path/to/finding.md DECISION=test
make export-skill
make export-skill SKILL_MODE=caveman
make skill-budget
make public-ready
make test-all
```

For trivial tickets, `PLAN` is optional:

```bash
make check-planning-brief TICKET=path/to/ticket.md
```

Frontend profile checks:

```bash
make pevie-test
make pevie-validate-examples
make pevie-design-lint
make kickoff PROFILE=pevie TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md DESIGN=DESIGN.md
make pevie-review-packet
```

## Examples

Validated examples live in [`examples/`](examples/) and [`Pevie Hischer/examples/`](Pevie%20Hischer/examples/). They are intentionally small, but they show the expected difference between trivial work and non-trivial work that needs a planning brief.

The complete core reference flow lives in [`examples/golden-workflow/`](examples/golden-workflow/).

The complete frontend reference flow lives in [`Pevie Hischer/examples/golden-workflow/`](Pevie%20Hischer/examples/golden-workflow/).

Run:

```bash
make validate-examples
make pevie-validate-examples
make pevie-design-lint
```

## Repository Layout

```text
.
├── AGENTS.md
├── build-system/
│   ├── agents/
│   ├── rules/
│   └── templates/
├── docs/
├── examples/
├── tools/
├── tests/
├── Pevie Hischer/
│   ├── build-system/
│   ├── examples/
│   ├── tools/
│   └── tests/
├── ADOPTION-CHECKLIST.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── MAIN-AGENT-HANDOFF.md
├── PUBLICATION-CHECKLIST.md
└── SECURITY.md
```

## Safety Defaults

- [`docs/trust-contract.md`](docs/trust-contract.md) documents the local command behavior and public-release gate.
- Review packets exclude likely sensitive untracked files by default.
- The tracked diff is mandatory context; packet generation fails rather than silently dropping it.
- `make doctor` checks required files, root workflow placement, generated-artifact ignores, and tracked-file privacy markers.
- `make check-proof` checks that active ticket risks are represented in QA/PR/completion evidence.
- `make skill-budget` keeps the exported skill small enough for agent context.
- `SKILL_MODE=caveman` exports the lowest-context loop for agents that only need the operating pattern.
- Oh Shucksenburg requires accepted debt to have an owner, trigger, and removal path.
- Non-trivial work should not start without scope, proof, and rollout thinking.
- Review findings should block only when tied to correctness, user risk, production risk, security, privacy, scale, or maintainability.

## Philosophy

Keep the system small. Add a rule, template field, test, lint, or tool only when it prevents a real recurring failure.
