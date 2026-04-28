# Golden Workflow: Frontend Status Panel

This folder shows a complete Pevie Hischer flow for a small but non-trivial UI change.

Use it as the reference path for frontend-heavy work:

1. Start with `ticket.md`.
2. Establish `DESIGN.md` before implementation.
3. Complete `planning-brief.md`.
4. Implement the scoped UI change.
5. Record evidence in `qa-plan.md` and `pr-note.md`.
6. Generate a review packet.
7. Review against `DESIGN.md`, accessibility, performance, failure states, and rollout proof.

Validate this example with:

```bash
make -f "Pevie Hischer/Makefile" validate-examples
make -f "Pevie Hischer/Makefile" design-lint DESIGN="Pevie Hischer/examples/golden-workflow/DESIGN.md"
```
