# Planning Brief

Use this before implementation for non-trivial changes. Keep it short and specific.

## Ticket Restatement

Add a complete core Pjario workflow example and proof validation so implementation handoffs are easier to generate and harder to under-prove.

## Scope And Non-Goals

In:

- Golden workflow fixture.
- Proof checker for active risk surfaces.
- Build-request kickoff support.
- Completion-report template.
- Garbage-collection triage helper.

Out:

- Stack-specific host app CI.
- Public release automation.

## Proposed Approach

- Add example files under `examples/golden-workflow/`.
- Add `tools/check-proof.py` to validate ticket risk evidence in QA, PR, and completion reports.
- Extend `tools/kickoff.py` so build requests can generate implementation prompts.
- Add `tools/triage-review-finding.py` for review-finding garbage collection.
- Wire the commands into `Makefile`, docs, tests, and CI.

## Dependencies And Unknowns

Dependencies (services, APIs, migrations, flags, teams):

- Local Python and Git.
- Existing package Makefile.

Unknowns to resolve before coding:

- None.

## Risk-To-Proof Map

Map each relevant risk surface to concrete evidence required before review.

- Data writes/migrations -> Not applicable.
- Authn/authz -> Not applicable.
- Multi-tenancy -> Not applicable.
- External calls/timeouts -> Not applicable.
- Async/background work -> Not applicable.
- LLM/AI validation -> `make kickoff-build`, review packet generation, and proof checker tests.
- PII/privacy -> `make doctor` privacy scan inside `make public-ready`.
- Billing/cost -> Not applicable.
- Rollout/rollback -> GitHub Actions success and revertable package commit.

## Test And QA Plan

Automated checks:

- `make test`
- `make validate-examples`
- `make public-ready`

Manual checks:

- Inspect generated kickoff-build output.
- Inspect the golden workflow for copy/paste clarity.

Failure-path checks:

- Unit test missing proof for an active risk surface.
- Unit test non-trivial kickoff still requires a planning brief.

## Rollout And Rollback Plan

- Feature flag strategy: Not needed.
- Rollout stages: Private package commit and CI validation.
- Rollback trigger: `make public-ready` or GitHub Actions fails.
- Rollback steps: Revert the package commit.

## Ready-To-Implement Gate

Mark done before writing code:

- [ ] Outcome and non-goals are unambiguous.
- [ ] Relevant risk surfaces are mapped to proof.
- [ ] Required tests and manual QA are defined.
- [ ] Rollout and rollback are concrete.
- [ ] Open unknowns are resolved or explicitly tracked.
