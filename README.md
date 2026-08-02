# Pjario Staltman

[![Quality](https://github.com/ChristFollower873461/pjario-staltman/actions/workflows/quality.yml/badge.svg)](https://github.com/ChristFollower873461/pjario-staltman/actions/workflows/quality.yml)

An open-source operating system for building software with agents.

Pjario Staltman turns agent work into a repeatable loop: tickets define intent, agents implement scoped changes, proof is captured, staff-level review checks the work, and repeated friction becomes durable guardrails instead of repeated comments.

The package is intentionally small, local-first, and auditable. It does not deploy code or call an LLM for you; it makes the surrounding engineering work explicit enough for humans and agents to review.

## Current Status

- Visibility: public open source
- Public-readiness: verified with [`PUBLICATION-CHECKLIST.md`](PUBLICATION-CHECKLIST.md) and the [`public release audit`](docs/public-release-audit.md)
- License: [MIT](LICENSE), including the bundled Pevie Hischer profile and exported Agent Skill artifacts

## Trust Path

If you are evaluating this package cold, start with [`docs/trust-contract.md`](docs/trust-contract.md). It explains what the package does, what it does not do, which commands write files, which commands read git state, which command path uses network, and the exact cold-start proof command sequence.

Runtime requirements are listed in [`docs/prerequisites.md`](docs/prerequisites.md).

The license and reuse posture is documented in [`docs/license-posture.md`](docs/license-posture.md). Security issues can be reported privately through [GitHub Security Advisories](https://github.com/ChristFollower873461/pjario-staltman/security/advisories/new).

External tool and dependency posture is documented in [`docs/supply-chain.md`](docs/supply-chain.md).

The public-readiness gate is:

```bash
make public-ready
```

That target runs the package tests, examples, Pevie design linting, doctor checks, skill export budget checks, review packet generation, and generated-artifact cleanup. For a local-only preflight that avoids npm/network access, run `make local-ready` first.

The repository quality workflow runs the same `make public-ready` gate on pushes and pull requests.

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

### Quiet Aggregate

A recovered review-learning loop in [`docs/quiet-aggregate.md`](docs/quiet-aggregate.md). It accepts verified findings from a maintained autoreview helper, human review, or CI; records them in a private local ledger; and proposes a consolidated guardrail only after the same failure class repeats across independent reviews. It never rewrites policy automatically.

## Quick Start

1. Write work using [`build-system/templates/ticket.md`](build-system/templates/ticket.md) and set `Level: trivial` or `Level: non-trivial`.
2. For non-trivial work, draft [`build-system/templates/planning-brief.md`](build-system/templates/planning-brief.md) before implementation.
3. For build or release coordination, fill [`build-system/templates/build-request.md`](build-system/templates/build-request.md) and use [`build-system/agents/build-coordinator.md`](build-system/agents/build-coordinator.md).
4. Give the task plus [`AGENTS.md`](AGENTS.md) and [`build-system/agents/implementation-agent.md`](build-system/agents/implementation-agent.md) to an implementation agent.
5. Capture QA and risk evidence with [`build-system/templates/pr.md`](build-system/templates/pr.md), [`build-system/templates/qa-plan.md`](build-system/templates/qa-plan.md), and [`build-system/templates/completion-report.md`](build-system/templates/completion-report.md).
6. Check proof coverage with `make check-proof`.
7. Generate a review packet with `make review-packet`.
8. Review with [`build-system/agents/software-engineer-reviewer.md`](build-system/agents/software-engineer-reviewer.md).
9. Record verified findings with `python3 tools/quiet-aggregate.py record` when review history matters.
10. Promote repeated review feedback with a reviewed Quiet Aggregate proposal and [`build-system/templates/garbage-collection.md`](build-system/templates/garbage-collection.md).

For first-time adoption, follow [`docs/adopt-in-15-minutes.md`](docs/adopt-in-15-minutes.md). For rollback or removal from a target repo, use [`docs/remove-from-target-repo.md`](docs/remove-from-target-repo.md).

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
python3 tools/quiet-aggregate.py --help
python3 tools/quiet-aggregate.py report
make export-skill
make export-skill SKILL_MODE=caveman
make skill-budget
make local-ready
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
│   └── quiet-aggregate.md
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
- [`docs/prerequisites.md`](docs/prerequisites.md) documents required local tools and the npm-only lint path.
- [`docs/supply-chain.md`](docs/supply-chain.md) documents external tool pins and network touchpoints.
- Review packets exclude likely sensitive untracked files by default.
- The tracked diff is mandatory context; packet generation fails rather than silently dropping it.
- `make doctor` checks required files, root workflow placement, generated-artifact ignores, and tracked-file privacy markers.
- `make local-ready` provides an offline/local preflight before running npm-based design linting.
- `make check-proof` checks that active ticket risks are represented in QA/PR/completion evidence.
- Quiet Aggregate keeps verified review history local, rejects likely secrets and host paths, and requires independent sources before promotion.
- `make skill-budget` keeps the exported skill small enough for agent context.
- `SKILL_MODE=caveman` exports the lowest-context loop for agents that only need the operating pattern.
- Oh Shucksenburg requires accepted debt to have an owner, trigger, and removal path.
- Non-trivial work should not start without scope, proof, and rollout thinking.
- Review findings should block only when tied to correctness, user risk, production risk, security, privacy, scale, or maintainability.

## Philosophy

Keep the system small. Add a rule, template field, test, lint, or tool only when it prevents a real recurring failure.
