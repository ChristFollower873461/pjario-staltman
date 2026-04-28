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
3. Create or update the host repo's `DESIGN.md` from `build-system/templates/DESIGN.md` before UI implementation.
4. Implement with `build-system/agents/frontend-implementation-agent.md`.
5. Attach QA and risk evidence via:
   - `build-system/templates/pr.md`
   - `build-system/templates/qa-plan.md`
6. Generate a packet for review:
   - `python3 tools/review-packet.py --base main --output .review-packet.md`
7. Review with `build-system/agents/frontend-staff-reviewer.md`.
8. Promote repeated review friction with `build-system/templates/garbage-collection.md`.
9. Run `make -f "Pevie Hischer/Makefile" test`.
10. Validate examples with `make -f "Pevie Hischer/Makefile" validate-examples`.

## Opinionated Frontend Quality Bar

- Visual/UI consistency with design tokens and canonical components
- A current `DESIGN.md` that captures brand, UX principles, design tokens, references, and forbidden patterns
- WCAG-aligned accessibility checks for changed surfaces
- Core Web Vitals and runtime error regressions treated as release risk
- Tests cover the happy path and one important failure path
- Risky launches include rollback/kill-switch details

## `DESIGN.md` Contract

Every adopted frontend repo should maintain a top-level `DESIGN.md` or an agreed equivalent such as `docs/product/DESIGN.md`.

Pevie treats this file as the source of truth for product taste. Implementation agents read it before UI work; reviewers block when a patch violates it without a documented reason.

Use `build-system/templates/DESIGN.md` as the starter template.

## Commands

- `make -f "Pevie Hischer/Makefile" test`
- `make -f "Pevie Hischer/Makefile" validate-examples`
- `make -f "Pevie Hischer/Makefile" review-packet`
- `make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md`
- `make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md`

## Examples

Validated examples live in [`examples/`](examples/). They show the minimum acceptable shape for trivial frontend work and for non-trivial frontend work that needs a planning brief.
