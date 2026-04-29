# Planning Brief

Use this before implementation for non-trivial changes. Keep it short and specific.

## Ticket Restatement

What outcome are we delivering, in plain language?

## Scope And Non-Goals

In:

- 

Out:

- 

## Proposed Approach

- 

## Dependencies And Unknowns

Dependencies (services, APIs, migrations, flags, teams):

- 

Unknowns to resolve before coding:

- 

## Risk-To-Proof Map

Map each relevant risk surface to concrete evidence required before review.

- Data writes/migrations -> 
- Authn/authz -> 
- Multi-tenancy -> 
- External calls/timeouts -> 
- Async/background work -> 
- LLM/AI validation -> 
- PII/privacy -> 
- Billing/cost -> 
- Technical debt/maintainability ->
- Rollout/rollback -> 

## Test And QA Plan

Automated checks:

- 

Manual checks:

- 

Failure-path checks:

- 

## Rollout And Rollback Plan

- Feature flag strategy:
- Rollout stages:
- Rollback trigger:
- Rollback steps:

## Ready-To-Implement Gate

Mark done before writing code:

- [ ] Outcome and non-goals are unambiguous.
- [ ] Relevant risk surfaces are mapped to proof.
- [ ] Required tests and manual QA are defined.
- [ ] Rollout and rollback are concrete.
- [ ] Open unknowns are resolved or explicitly tracked.
