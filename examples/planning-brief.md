# Planning Brief

Use this before implementation for non-trivial changes. Keep it short and specific.

## Ticket Restatement

Review packets must always include the diff under review, even when optional rules context is too large for the packet budget.

## Scope And Non-Goals

In:

- Preserve the diff as mandatory packet context.
- Omit optional rules context when the packet budget is tight.
- Add regression tests for tight budgets and oversized diffs.

Out:

- No hosted automation.
- No change to reviewer severity rules.

## Proposed Approach

- Split the packet into header, optional rules, and mandatory diff sections.
- Calculate byte budgets before assembling the final packet.
- Fail loudly if the mandatory header and diff cannot fit.

## Dependencies And Unknowns

Dependencies (services, APIs, migrations, flags, teams):

- Local Git is available.
- Existing unit test structure remains in place.

Unknowns to resolve before coding:

- None.

## Risk-To-Proof Map

Map each relevant risk surface to concrete evidence required before review.

- Data writes/migrations -> Not applicable.
- Authn/authz -> Not applicable.
- Multi-tenancy -> Not applicable.
- External calls/timeouts -> Not applicable.
- Async/background work -> Not applicable.
- LLM/AI validation -> Add tests proving diff context is retained for review-agent input.
- PII/privacy -> Preserve sensitive untracked-file filtering.
- Billing/cost -> Not applicable.
- Rollout/rollback -> Revert the tooling change if packet generation regresses.

## Test And QA Plan

Automated checks:

- `make test`
- `make review-packet`

Manual checks:

- Inspect a generated packet and confirm the diff section is present.

Failure-path checks:

- Run a test where the diff exceeds `--max-bytes` and confirm it fails with a clear error.

## Rollout And Rollback Plan

- Feature flag strategy: Not needed.
- Rollout stages: Local package change only.
- Rollback trigger: Packet generation fails in normal use.
- Rollback steps: Revert the tooling commit.

## Ready-To-Implement Gate

Mark done before writing code:

- [ ] Outcome and non-goals are unambiguous.
- [ ] Relevant risk surfaces are mapped to proof.
- [ ] Required tests and manual QA are defined.
- [ ] Rollout and rollback are concrete.
- [ ] Open unknowns are resolved or explicitly tracked.
