# Ticket

## Outcome

Implementation agents can prove core workflow changes consistently, so coordinators get a complete handoff instead of loose notes.

## Context

The package already validates planning briefs and review packets. The next core gap is evidence discipline: agents need one reference flow that shows ticket, planning, QA, PR, completion, and garbage collection working together.

## Implementation Complexity

Level: non-trivial

Rationale:

- The work changes package workflow, examples, and validation.
- It should prove LLM/AI review context, privacy scanning, and rollback evidence.

## Scope

In:

- Add a golden workflow fixture.
- Add proof checking for ticket risk surfaces.
- Add kickoff support for build requests.
- Add completion-report and garbage-collection evidence.

Out:

- Host-app-specific tests.
- Public repository visibility.

## Risk Surfaces

Mark any that apply and add notes:

- Data writes or migrations: None.
- Authn/authz: None.
- Multi-tenancy: None.
- External calls: None.
- Async/background work: None.
- LLM/AI: Review packet and kickoff prompts feed agent work, so missing evidence weakens reviewer accuracy.
- PII/privacy: Package publication needs privacy scanning before handoff.
- Billing/cost: None.
- Technical debt/maintainability: The new workflow should not add process weight without mechanical enforcement.
- Rollout/rollback: Revert the package commit if validation or CI fails.

## Acceptance Criteria

- Golden workflow files validate locally.
- Proof checker rejects missing active risk evidence.
- Build-request kickoff prompt names the request and required proof posture.
- Completion report captures changed files, proof status, artifacts, gaps, and next coordinator action.
- Technical debt impact is explicitly recorded.

## Required Proof

Commands, tests, screenshots, logs, load test, runbook, migration plan, or manual QA expected before review.

- `make validate-examples`
- `make check-proof TICKET=examples/golden-workflow/ticket.md QA=examples/golden-workflow/qa-plan.md PR=examples/golden-workflow/pr-note.md COMPLETION=examples/golden-workflow/completion-report.md`
- `make kickoff-build REQUEST=examples/golden-workflow/build-request.md`
- `make public-ready`
