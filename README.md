# Pjario Staltman

[![Quality](https://github.com/ChristFollower873461/pjario-staltman/actions/workflows/quality.yml/badge.svg)](https://github.com/ChristFollower873461/pjario-staltman/actions/workflows/quality.yml)

An open-source operating system for building software with agents.

Pjario Staltman turns agent work into a repeatable loop: one Work Packet carries intent, scope, risks, proof, review, and handoff; repeated friction becomes durable guardrails instead of repeated comments.

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

- one versioned Work Packet for outcome, scope, risks, plan, stable proof IDs, evidence, review, gaps, and next action
- progressive planning that stays minimal for trivial work and becomes mandatory for non-trivial work
- implementation-agent handoffs
- build-request handoffs for coordinated build/release work
- staff-level review prompts
- structural proof checks that map stable risk IDs to evidence
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

1. Create one Work Packet with `python3 tools/pjario.py start --help`.
2. Fill Scope. For non-trivial work, fill Plan and map each active `RISK-xx` to a `PROOF-xx` requirement.
3. Run `python3 tools/pjario.py check --packet .pjario/work/WORK-ID.md` before implementation.
4. Implement the scoped change and attach real evidence to every proof ID.
5. Run `python3 tools/pjario.py review --packet .pjario/work/WORK-ID.md --base origin/main`.
6. Record the review decision, then run `python3 tools/pjario.py finish --packet .pjario/work/WORK-ID.md`.
7. When the same verified failure class repeats across independent reviews, use `python3 tools/pjario.py learn ...` to route it through Quiet Aggregate.

For first-time adoption, follow [`docs/adopt-in-15-minutes.md`](docs/adopt-in-15-minutes.md). For rollback or removal from a target repo, use [`docs/remove-from-target-repo.md`](docs/remove-from-target-repo.md).

## Commands

```bash
python3 tools/pjario.py start --help
python3 tools/pjario.py check --packet .pjario/work/WORK-ID.md
python3 tools/pjario.py review --packet .pjario/work/WORK-ID.md --base origin/main
python3 tools/pjario.py finish --packet .pjario/work/WORK-ID.md
python3 tools/pjario.py adopt --profile core --dry-run
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

The ticket, planning-brief, QA, PR, and completion commands below are compatibility paths for existing adopters; new work should use one Work Packet.

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

Validated examples live in [`examples/`](examples/) and [`Pevie Hischer/examples/`](Pevie%20Hischer/examples/). They are intentionally small, but show how trivial and non-trivial work use the same packet with different planning depth.

Complete Work Packet examples live in [`examples/work-packets/`](examples/work-packets/). The legacy multi-artifact reference flow remains in [`examples/golden-workflow/`](examples/golden-workflow/).

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
├── evals/
│   └── skill-behavior.json
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
- Work Packets use stable risk and proof IDs, so evidence is checked structurally instead of by copied prose.
- Review packets exclude likely sensitive untracked files by default.
- The tracked diff is mandatory context; packet generation fails rather than silently dropping it.
- `make doctor` checks required files, root workflow placement, generated-artifact ignores, and tracked-file privacy markers.
- `make local-ready` provides an offline/local preflight before running npm-based design linting.
- `make check-proof PACKET=.pjario/work/WORK-ID.md` checks stable proof IDs, terminal evidence, and active-risk coverage; the legacy multi-file form remains supported.
- Quiet Aggregate keeps verified review history local, rejects likely secrets and host paths, and requires independent sources before promotion.
- `make skill-budget` keeps the exported skill small enough for agent context.
- `SKILL_MODE=caveman` exports the lowest-context loop for agents that only need the operating pattern.
- Oh Shucksenburg requires accepted debt to have an owner, trigger, and removal path.
- Non-trivial work should not start without scope, proof, and rollout thinking.
- Review findings should block only when tied to correctness, user risk, production risk, security, privacy, scale, or maintainability.

## Philosophy

Keep the system small. Add a rule, template field, test, lint, or tool only when it prevents a real recurring failure.
