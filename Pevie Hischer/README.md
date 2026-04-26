# Pevie Hischer

A frontend-first quality system for high-taste, production-grade software delivery with agents.

This package is based on `Pjario Staltman`, with a tighter focus on:

- UI taste and consistency at scale
- Design-system discipline
- Performance and accessibility as merge gates
- Production observability for frontend releases

## Start Here

1. Write a ticket using `build-system/templates/ticket.md`.
2. For non-trivial work, complete `build-system/templates/planning-brief.md`.
3. Implement with `build-system/agents/frontend-implementation-agent.md`.
4. Attach QA and risk evidence via:
   - `build-system/templates/pr.md`
   - `build-system/templates/qa-plan.md`
5. Generate a packet for review:
   - `python3 tools/review-packet.py --base main --output .review-packet.md`
6. Review with `build-system/agents/frontend-staff-reviewer.md`.
7. Promote repeated review friction with `build-system/templates/garbage-collection.md`.
8. Run `make -f "Pevie Hischer/Makefile" test`.

## Opinionated Frontend Quality Bar

- Visual/UI consistency with design tokens and canonical components
- WCAG-aligned accessibility checks for changed surfaces
- Core Web Vitals and runtime error regressions treated as release risk
- Tests cover the happy path and one important failure path
- Risky launches include rollback/kill-switch details

## Commands

- `make -f "Pevie Hischer/Makefile" test`
- `make -f "Pevie Hischer/Makefile" review-packet`
- `make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md`
