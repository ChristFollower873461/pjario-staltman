# Ticket

## Outcome

Frontend planning briefs must reject empty required sections so non-trivial UI work starts with real scope, risk, QA, and rollout thinking.

## Context

The Pevie profile is intended to hold frontend work to a higher quality bar than generic implementation. A planning brief that contains only section headings does not provide enough implementation or review context.

## Implementation Complexity

Level: non-trivial

Rationale:

- The checker gates non-trivial frontend work.
- The change needs regression tests for empty sections and stale ready-gate checklists.

## Scope

In:

- Reject empty required planning sections.
- Require the ready-to-implement gate from the template.
- Add regression tests.

Out:

- Add stack-specific frontend linting.
- Change the ticket template.

## Risk Surfaces

- Accessibility: Planning must map accessibility proof before implementation.
- Performance: Planning must name performance evidence for user-facing changes.
- Data/API correctness: Planning must map API-state proof where relevant.
- External dependencies: Planning must name fallback behavior where relevant.
- Privacy/PII: Planning must include safe logging and data handling notes where relevant.
- Rollout/rollback: Planning must define a realistic rollback path.

## Acceptance Criteria

- A non-trivial ticket with empty planning sections fails validation.
- A planning brief missing required ready-gate items fails validation.
- Existing valid planning brief examples pass.

## Required Proof

Commands, checks, screenshots, videos, logs, or manual QA required before review.

- `make -f "Pevie Hischer/Makefile" test`
- `make -f "Pevie Hischer/Makefile" validate-examples`
