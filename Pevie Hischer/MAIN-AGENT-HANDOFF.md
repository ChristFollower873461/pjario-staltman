# Main Agent Handoff: Pevie Hischer

`Pevie Hischer` is a frontend-focused companion package to `Pjario Staltman`.

It is designed for teams that want high UI taste and production scalability with enforceable agent workflows.

## Package Contents

- `AGENTS.md`
  - Frontend-oriented operating constraints.
- `build-system/README.md`
  - Workflow loop and severity model.
- `build-system/agents/`
  - `frontend-implementation-agent.md`
  - `frontend-staff-reviewer.md`
- `build-system/rules/`
  - `frontend-taste-and-review-standards.md`
  - `frontend-production-readiness.md`
- `build-system/templates/`
  - `DESIGN.md`
  - `ticket.md`
  - `planning-brief.md`
  - `pr.md`
  - `qa-plan.md`
  - `garbage-collection.md`
- `examples/`
  - Validated sample trivial ticket, non-trivial ticket, and planning brief.
- `tools/`
  - `review-packet.py`
  - `check-planning-brief.py`
  - `check-design-context.py`
- `tests/`
  - unit coverage for both tools
- `Pevie Hischer/.github/workflows/pevie-quality.yml`
  - sample package-scoped CI checks; copy this file into the target repo's root `.github/workflows/` directory if adopting Pevie by itself
- `RESEARCH-NOTES.md`
  - external reference synthesis

## Baseline Commands

- `make -f "Pevie Hischer/Makefile" test`
- `make -f "Pevie Hischer/Makefile" validate-examples`
- `make -f "Pevie Hischer/Makefile" review-packet`
- `make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md`
- `make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md`

For trivial tickets, `PLAN` is optional.

## Recommended Adoption Path

1. Copy `Pevie Hischer` into your target repo.
2. Decide canonical ticket, plan, and `DESIGN.md` paths for your team.
3. Create or update `DESIGN.md` from `Pevie Hischer/build-system/templates/DESIGN.md` before non-trivial UI implementation.
4. Wire the agent prompts into your implementation/review workflow.
5. Copy `Pevie Hischer/.github/workflows/pevie-quality.yml` to the target repo's root `.github/workflows/` directory, or fold the Pevie jobs into existing CI.
6. Start with one product surface, then expand.

## Non-Negotiables To Keep

- Accessibility verification for changed user flows.
- `DESIGN.md` review for non-trivial user-facing UI work.
- Performance and runtime impact notes for user-facing changes.
- Planning brief requirement for non-trivial tickets.
- Review feedback tied to risk and user impact.

## First Follow-Ups For Main Agent

- Add project-specific frontend checks (lint/test/storybook/playwright) to the `test` target.
- Add stack-specific performance budgets and threshold policy.
- Add design-system ownership and change governance process.
