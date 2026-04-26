# Ticket

## Outcome

Review packets must always include the tracked diff or fail with a clear error, so reviewers never receive a packet without the changes under review.

## Context

The review packet is used as the handoff to a staff-style review agent. If optional instructions or rules crowd out the diff, the review becomes low signal and can miss real defects.

## Implementation Complexity

Level: non-trivial

Rationale:

- The change affects review tooling and the trustworthiness of review evidence.
- It needs regression coverage for tight packet-size budgets.

## Scope

In:

- Make the diff mandatory packet context.
- Omit optional rules before omitting the diff.
- Add regression tests for budget handling.

Out:

- Add hosted review automation.
- Change the review severity model.

## Risk Surfaces

Mark any that apply and add notes:

- Data writes or migrations: None.
- Authn/authz: None.
- Multi-tenancy: None.
- External calls: None.
- Async/background work: None.
- LLM/AI: Review packet content feeds an LLM or agent reviewer, so missing diff context is a correctness risk.
- PII/privacy: Review packets can include diffs; keep sensitive untracked filtering intact.
- Billing/cost: None.
- Rollout/rollback: Revert the tooling change if packet generation breaks.

## Acceptance Criteria

- Packet generation includes `# Changes To Review` under tight optional-context budgets.
- Packet generation fails when the diff cannot fit.
- Unit tests cover both behaviors.

## Required Proof

Commands, tests, screenshots, logs, load test, runbook, migration plan, or manual QA expected before review.

- `make test`
- `make review-packet`
