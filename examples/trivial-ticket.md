# Ticket

## Outcome

The README command list mentions the validated examples check so adopters can verify the package after copying it.

## Context

This is a documentation-only change with no runtime behavior.

## Implementation Complexity

Level: trivial

Rationale:

- The change is small, local, reversible, and does not touch production behavior.

## Scope

In:

- Update the command list.

Out:

- Change package tooling.
- Change adoption policy.

## Risk Surfaces

Mark any that apply and add notes:

- Data writes or migrations: None.
- Authn/authz: None.
- Multi-tenancy: None.
- External calls: None.
- Async/background work: None.
- LLM/AI: None.
- PII/privacy: None.
- Billing/cost: None.
- Rollout/rollback: Revert the documentation commit.

## Acceptance Criteria

- README includes the relevant command.
- `make validate-examples` still passes.

## Required Proof

Commands, tests, screenshots, logs, load test, runbook, migration plan, or manual QA expected before review.

- `make validate-examples`
