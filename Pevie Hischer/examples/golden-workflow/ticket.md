# Ticket

## Outcome

Finance operators can scan account health from a status panel that shows loading, empty, error, and healthy states without drifting from `DESIGN.md`.

## Context

The target surface is a recurring operational dashboard. Agents often build generic dashboards unless product taste, state behavior, and proof requirements are established before implementation.

## Implementation Complexity

Level: non-trivial

Rationale:

- The change is user-facing UI.
- It has design-system, accessibility, state-handling, and review-proof requirements.
- It should establish a reusable pattern for later status panels.

## Scope

In:

- Add or update one account health status panel.
- Use tokens and component rules from `DESIGN.md`.
- Cover loading, empty, error, and healthy states.
- Add focused automated or manual proof.

Out:

- Rebuild the dashboard layout.
- Add new analytics endpoints.
- Change account-health scoring logic.

## Risk Surfaces

- Design coherence: Must follow `DESIGN.md`; deviations require PR-note justification.
- Accessibility: State labels and recovery actions must be keyboard and screen-reader usable.
- Performance: Panel must not block the dashboard shell or cause layout shift.
- Data/API correctness: State text must reflect API result shape accurately.
- External dependencies: API timeout/error state must be visible and recoverable.
- Privacy/PII: Do not log customer account details in frontend telemetry.
- Rollout/rollback: Revert panel change or hide behind an existing dashboard flag.

## Acceptance Criteria

- Panel follows `DESIGN.md` tokens and component rules.
- Loading, empty, error, and healthy states are implemented or explicitly mocked for QA.
- Primary recovery action is keyboard accessible.
- QA evidence includes screenshots or notes for all states.
- PR note names any design deviations.

## Required Proof

Commands, checks, screenshots, videos, logs, or manual QA required before review.

- `make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md`
- Relevant app test command.
- Manual QA notes for loading, empty, error, and healthy states.
- Screenshot or visual review note comparing the panel to `DESIGN.md`.
