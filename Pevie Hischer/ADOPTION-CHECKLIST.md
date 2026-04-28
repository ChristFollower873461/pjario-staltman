# Pevie Hischer Adoption Checklist

Use this checklist to install and operationalize `Pevie Hischer` in a target repository.

## 1) Copy Package

- [ ] Copy the full `Pevie Hischer` directory into the target repo root.
- [ ] Confirm these exist:
  - [ ] `Pevie Hischer/build-system/`
  - [ ] `Pevie Hischer/examples/`
  - [ ] `Pevie Hischer/tools/`
  - [ ] `Pevie Hischer/tests/`
  - [ ] `Pevie Hischer/.github/workflows/pevie-quality.yml`
- [ ] If using the Pevie workflow by itself, copy `Pevie Hischer/.github/workflows/pevie-quality.yml` into the target repo's root `.github/workflows/` directory.

## 2) Define Team Conventions

- [ ] Pick canonical ticket path (example: `docs/tickets/current.md`).
- [ ] Pick canonical planning brief path (example: `docs/tickets/current-planning-brief.md`).
- [ ] Pick canonical design-context path (recommended: top-level `DESIGN.md`; acceptable: `docs/product/DESIGN.md`).
- [ ] Create the design-context file from `Pevie Hischer/build-system/templates/DESIGN.md`.
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
- [ ] `make -f "Pevie Hischer/Makefile" validate-examples`
- [ ] `make -f "Pevie Hischer/Makefile" design-lint-examples`
- [ ] `make doctor MODE=adopted PROFILE=pevie`
- [ ] `make kickoff PROFILE=pevie TICKET=<ticket> PLAN=<planning-brief> DESIGN=<design-file>`
- [ ] `make -f "Pevie Hischer/Makefile" review-packet`
- [ ] `make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=<ticket> PLAN=<planning-brief>`

For trivial tickets:

- [ ] `make -f "Pevie Hischer/Makefile" check-planning-brief TICKET=<ticket>`

## 5) CI Integration

- [ ] Ensure GitHub Actions is enabled for the repository.
- [ ] Confirm the Pevie workflow file lives under the target repo's root `.github/workflows/` directory, or that equivalent Pevie checks are folded into an existing workflow.
- [ ] Confirm workflow appears in Actions tab:
  - [ ] `pevie-quality`
- [ ] Open a PR touching `Pevie Hischer/**` and verify workflow passes.

## 6) Project-Specific Hardening

- [ ] Extend `test` target with host repo checks (lint/typecheck/unit/e2e/storybook, as applicable).
- [ ] Add a check, review rule, or PR template item requiring `DESIGN.md` review for user-facing UI changes.
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
- [ ] User-facing UI work consistently references `DESIGN.md` or the chosen design-context file.
- [ ] Review packets are generated for meaningful frontend changes.
- [ ] Accessibility/performance evidence is visible in PR notes.
- [ ] At least one repeated review issue has been promoted into a durable guardrail.
