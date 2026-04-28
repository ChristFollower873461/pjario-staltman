# Core Golden Workflow

This folder shows a complete core Pjario Staltman flow for non-frontend agent work.

Use it as the reference when adopting the base package without Pevie:

1. `ticket.md` defines the outcome, scope, active risks, and required proof.
2. `planning-brief.md` maps scope and risks to proof before implementation.
3. `build-request.md` shows the coordinator handoff shape.
4. `qa-plan.md` names automated, manual, and failure-path evidence.
5. `pr-note.md` records risk, rollout, and proof for review.
6. `completion-report.md` is the implementation-agent closeout.
7. `garbage-collection.md` shows how review friction becomes a durable guardrail.

Validate with:

```bash
make validate-examples
make check-proof TICKET=examples/golden-workflow/ticket.md QA=examples/golden-workflow/qa-plan.md PR=examples/golden-workflow/pr-note.md COMPLETION=examples/golden-workflow/completion-report.md
make kickoff-build REQUEST=examples/golden-workflow/build-request.md
```
