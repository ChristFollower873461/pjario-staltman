# Completeness Review

This package is complete enough to use as a first working harness for agentic software building.

## Covered

- Repo-wide agent rules in `AGENTS.md`.
- A build loop for ticket, implementation, proof, review, human steering, and rule promotion.
- An implementation-agent prompt for end-to-end patch ownership.
- A staff software engineer review-agent prompt with severity levels and hard blocks.
- A build-coordinator prompt for handing concrete build and release work to an implementation agent.
- Scale-readiness rules derived from the supplied PDF.
- Review standards that separate blocking risk from taste.
- Ticket, PR note, QA plan, and garbage-collection templates.
- A planning-brief template to force pre-implementation scope, risk-to-proof mapping, and rollout planning.
- A build-request template for repo path, target platform, current state, constraints, required proof, and coordinator follow-up.
- A local `review-packet.py` tool that packages repo rules and diffs for review.
- A `make review-packet` shortcut.
- A `check-planning-brief.py` validator and `make check-planning-brief` guard for non-trivial tickets.
- A frontend-focused `Pevie Hischer/` profile with frontend implementation and review prompts.
- Repository-level GitHub Actions quality workflow.
- Private-to-public publication checklist.

## Intentionally Not Included Yet

- Language-specific linters, because there is no app stack in this repo yet.
- Stack-specific CI integrations, because target host app platforms are not known yet.
- Project-specific runbooks, because there is no deployed service yet.
- Actual reviewer automation in GitHub, because this package is tool-agnostic until a host repo exists.

## First Additions Once App Code Exists

- Host-repo CI jobs that run app-specific lint, typecheck, unit, e2e, and package review checks.
- One bespoke lint or source test for the first repeated agent failure.
- A project `RUNBOOK.md`.
- A small `docs/critical-user-journeys.md` file for QA-plan generation.
