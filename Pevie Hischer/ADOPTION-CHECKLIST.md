# Pevie Hischer Adoption Checklist

Use this checklist to install and operationalize `Pevie Hischer` in a target repository.

## 1) Copy Package

- [ ] Copy the full `Pevie Hischer` directory into the target repo root.
- [ ] Confirm these exist:
  - [ ] `Pevie Hischer/build-system/`
  - [ ] `Pevie Hischer/tools/`
  - [ ] `Pevie Hischer/tests/`
  - [ ] `Pevie Hischer/.github/workflows/pevie-quality.yml`

## 2) Define Team Conventions

- [ ] Pick canonical ticket path (example: `docs/tickets/current.md`).
- [ ] Pick canonical planning brief path (example: `docs/tickets/current-planning-brief.md`).
- [ ] Document these paths in team docs or repo README.

## 3) Wire Agent Workflow

- [ ] Implementation agent uses:
  - [ ] `Pevie Hischer/build-system/agents/frontend-implementation-agent.md`
- [ ] Reviewer agent uses:
  - [ ] `Pevie Hischer/build-system/agents/frontend-staff-reviewer.md`
- [ ] Team references:
  - [ ] `Pevie Hischer/AGENTS.md`
  - [ ] `Pevie Hischer/build-system/README.md`

## 4) Enable Local Commands

Run and confirm:

- [ ] `make -f "Pevie Hischer/Makefile" test`
- [ ] `make -f "Pevie Hischer/Makefile" review-packet`
- [ ] `make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=<ticket> PLAN=<planning-brief>`

For trivial tickets:

- [ ] `make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=<ticket>`

## 5) CI Integration

- [ ] Ensure GitHub Actions is enabled for the repository.
- [ ] Confirm workflow appears in Actions tab:
  - [ ] `pevie-quality`
- [ ] Open a PR touching `Pevie Hischer/**` and verify workflow passes.

## 6) Project-Specific Hardening

- [ ] Extend `test` target with host repo checks (lint/typecheck/unit/e2e/storybook, as applicable).
- [ ] Define performance budget thresholds for your app/surface.
- [ ] Define accessibility verification standard (automated + manual).
- [ ] Define release rollout/rollback policy for risky frontend changes.

## 7) Operational Governance

- [ ] Require planning brief for non-trivial tickets.
- [ ] Require PR notes with risk + QA evidence.
- [ ] Run weekly garbage collection:
  - [ ] use `Pevie Hischer/build-system/templates/garbage-collection.md`
  - [ ] convert repeated review findings into rules/tests/tooling

## 8) Done Criteria

Adoption is complete when:

- [ ] The workflow runs in active PRs.
- [ ] Non-trivial tickets consistently include planning briefs.
- [ ] Review packets are generated for meaningful frontend changes.
- [ ] Accessibility/performance evidence is visible in PR notes.
- [ ] At least one repeated review issue has been promoted into a durable guardrail.
