# Adoption Checklist

Use this checklist when installing Pjario Staltman into a target repository.

## 1. Copy Core Package

- [ ] Copy `AGENTS.md`.
- [ ] Copy `build-system/`.
- [ ] Copy `examples/`.
- [ ] Copy `tools/`.
- [ ] Copy `tests/`.
- [ ] Copy `.github/workflows/quality.yml` into the target repo root workflow directory, or fold equivalent checks into existing CI.
- [ ] Copy the relevant `Makefile` targets.

## 2. Define Local Conventions

- [ ] Pick the canonical ticket path.
- [ ] Pick the canonical planning-brief path.
- [ ] Pick where build requests live.
- [ ] Pick where QA plans, PR notes, and completion reports live.
- [ ] Decide whether planning briefs are mandatory in CI or soft-gated.

## 3. Wire Agent Workflow

- [ ] Implementation agents read `AGENTS.md`.
- [ ] Implementation agents read `build-system/agents/implementation-agent.md`.
- [ ] Review agents read `build-system/agents/software-engineer-reviewer.md`.
- [ ] Coordinators use `build-system/templates/build-request.md`.

## 4. Enable Local Checks

Run and confirm:

- [ ] `make test`
- [ ] `make validate-examples`
- [ ] `make doctor MODE=adopted PROFILE=core`
- [ ] `make review-packet`
- [ ] `make kickoff TICKET=<ticket> PLAN=<planning-brief>`
- [ ] `make kickoff-build REQUEST=<build-request>`
- [ ] `make check-proof TICKET=<ticket> QA=<qa-plan> PR=<pr-note> COMPLETION=<completion-report>`
- [ ] `make check-planning-brief TICKET=<ticket> PLAN=<planning-brief>`

For trivial tickets:

- [ ] `make check-planning-brief TICKET=<ticket>`

## 5. Add Frontend Profile When Needed

Use `Pevie Hischer/` when a target repo needs higher frontend discipline.

- [ ] Copy `Pevie Hischer/`.
- [ ] Run `make -f "Pevie Hischer/Makefile" test`.
- [ ] Run `make -f "Pevie Hischer/Makefile" validate-examples`.
- [ ] Run `make -f "Pevie Hischer/Makefile" design-lint-examples`.
- [ ] After creating `DESIGN.md`, run `make doctor MODE=adopted PROFILE=pevie`.
- [ ] Wire `frontend-implementation-agent.md` into implementation handoffs.
- [ ] Wire `frontend-staff-reviewer.md` into frontend review.
- [ ] Define accessibility and performance proof expectations.

## 6. Add CI

- [ ] Run package tests.
- [ ] Run planning-brief checks for non-trivial work.
- [ ] Build review packets as a sanity check.
- [ ] Add host app checks: lint, typecheck, unit, e2e, Storybook, Playwright, or platform-specific builds.

## 7. Start Small

- [ ] Adopt the workflow on one product surface first.
- [ ] Hold weekly garbage collection.
- [ ] Use `make triage-review-finding FINDING=<finding> DECISION=<rule|template|test|lint|tooling|accepted-non-rule>` after repeated review friction.
- [ ] Promote one repeated issue at a time into a durable rule, template, test, lint, or tool.

## Done Criteria

Adoption is complete when:

- [ ] Non-trivial work consistently starts with a planning brief.
- [ ] PR notes include risk and QA evidence.
- [ ] Completion reports include changed files, commands, proof status, known gaps, and next coordinator action.
- [ ] Review packets are used for meaningful changes.
- [ ] At least one repeated review issue has been converted into a durable guardrail.
