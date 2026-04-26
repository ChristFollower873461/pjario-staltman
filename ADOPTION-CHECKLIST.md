# Adoption Checklist

Use this checklist when installing Pjario Staltman into a target repository.

## 1. Copy Core Package

- [ ] Copy `AGENTS.md`.
- [ ] Copy `build-system/`.
- [ ] Copy `tools/`.
- [ ] Copy `tests/`.
- [ ] Copy the relevant `Makefile` targets.

## 2. Define Local Conventions

- [ ] Pick the canonical ticket path.
- [ ] Pick the canonical planning-brief path.
- [ ] Pick where build requests live.
- [ ] Decide whether planning briefs are mandatory in CI or soft-gated.

## 3. Wire Agent Workflow

- [ ] Implementation agents read `AGENTS.md`.
- [ ] Implementation agents read `build-system/agents/implementation-agent.md`.
- [ ] Review agents read `build-system/agents/software-engineer-reviewer.md`.
- [ ] Coordinators use `build-system/templates/build-request.md`.

## 4. Enable Local Checks

Run and confirm:

- [ ] `make test`
- [ ] `make review-packet`
- [ ] `make check-planning-brief TICKET=<ticket> PLAN=<planning-brief>`

For trivial tickets:

- [ ] `make check-planning-brief TICKET=<ticket>`

## 5. Add Frontend Profile When Needed

Use `Pevie Hischer/` when a target repo needs higher frontend discipline.

- [ ] Copy `Pevie Hischer/`.
- [ ] Run `make -f "Pevie Hischer/Makefile" test`.
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
- [ ] Promote one repeated issue at a time into a durable rule, template, test, lint, or tool.

## Done Criteria

Adoption is complete when:

- [ ] Non-trivial work consistently starts with a planning brief.
- [ ] PR notes include risk and QA evidence.
- [ ] Review packets are used for meaningful changes.
- [ ] At least one repeated review issue has been converted into a durable guardrail.
