# Build Request

Use this when a coordinator hands a concrete build, release, or verification task to an implementation agent.

## Outcome

What should exist when this is done?

- The package has a private GitHub-ready quality pass with passing tests, validated examples, and green CI.

## Target

- Repo path: `/path/to/pjario-staltman`
- Branch: `main`
- Platform or surface: GitHub repository package
- App/package/bundle ID: Not applicable.
- Version/build number: Not applicable.
- Release track or destination: Private repository, public-ready posture.

## Current State

Paste the exact failing command, error text, console page state, CI link, screenshot note, or user-visible behavior.

- Review found Pevie packet trimming, weak planning validation, and unclear nested workflow adoption.

## Scope And Non-Goals

In:

- Fix review findings.
- Add regression coverage.
- Run package checks and privacy scan.

Out:

- Change repository visibility.
- Add a public license decision.

## Constraints

- Signing or credentials: Not applicable.
- Environment variables: Not applicable.
- Feature flags: Not applicable.
- External services: GitHub Actions only.
- Deadline or sequencing: Keep the private repository clean and ready.

## Risk Surfaces

Mark any that apply and add notes:

- Data writes or migrations: None.
- Authn/authz: None.
- Multi-tenancy: None.
- External calls: GitHub push and Actions status only.
- Async/background work: CI runs after push.
- LLM/AI: Review packets feed agent review.
- PII/privacy: Run privacy scan before push.
- Billing/cost: None.
- Store/release review: None.
- Rollout/rollback: Revert commit if package checks fail.

## Required Proof

Commands, builds, tests, screenshots, logs, artifact paths, store-page status, or manual QA expected before handoff.

- `make test-all`
- `make review-packet`
- `make pevie-review-packet`
- privacy scan
- GitHub Actions success

## Coordinator Follow-Up Needed

What should the coordinator do after the implementation agent reports back?

- Merge or open PR: Direct private `main` push is acceptable for this package pass.
- Rerun CI: Confirm GitHub Actions passes.
- Upload artifact: Not applicable.
- Submit for review: Not applicable.
- Collect missing access: Not applicable.
- Other: Keep repository private until public-license and visibility decisions are made.
