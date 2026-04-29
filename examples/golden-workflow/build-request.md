# Build Request

Use this when a coordinator hands a concrete build, release, or verification task to an implementation agent.

## Outcome

What should exist when this is done?

- Core Pjario has a complete golden workflow and commands that generate proofable implementation handoffs.

## Target

- Repo path: `./`
- Branch: `main`
- Platform or surface: Agent workflow package
- App/package/bundle ID: Not applicable.
- Version/build number: Not applicable.
- Release track or destination: Private repository main branch.

## Current State

Paste the exact failing command, error text, console page state, CI link, screenshot note, or user-visible behavior.

- Core guidance exists, but Pevie has a stronger golden workflow than the base package.

## Scope And Non-Goals

In:

- Add core golden workflow files.
- Add proof checker and build-request kickoff.
- Add completion-report and garbage-collection examples.

Out:

- Public visibility.
- Host app stack CI.

## Constraints

- Signing or credentials: Not applicable.
- Environment variables: Not applicable.
- Feature flags: Not applicable.
- External services: GitHub Actions after push.
- Deadline or sequencing: Keep the package private and public-ready.

## Risk Surfaces

Mark any that apply and add notes:

- Data writes or migrations: None.
- Authn/authz: None.
- Multi-tenancy: None.
- External calls: GitHub Actions status only.
- Async/background work: CI runs after push.
- LLM/AI: Kickoff and review packet prompts feed agent work.
- PII/privacy: Run package doctor privacy scan.
- Billing/cost: None.
- Technical debt/maintainability: Keep the workflow lightweight and backed by validation.
- Store/release review: None.
- Rollout/rollback: Revert commit if package checks fail.

## Required Proof

Commands, builds, tests, screenshots, logs, artifact paths, store-page status, or manual QA expected before handoff.

- `make validate-examples`
- `make kickoff-build REQUEST=examples/golden-workflow/build-request.md`
- `make public-ready`
- GitHub Actions success

## Coordinator Follow-Up Needed

What should the coordinator do after the implementation agent reports back?

- Merge or open PR: Direct private `main` push is acceptable.
- Rerun CI: Confirm GitHub Actions passes.
- Upload artifact: Not applicable.
- Submit for review: Not applicable.
- Collect missing access: Not applicable.
- Other: Keep private until license and visibility decisions are made.
