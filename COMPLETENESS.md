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
- Oh Shucksenburg technical-debt control rules for accepted debt, coupling, duplication, and maintainability.
- Ticket, PR note, QA plan, and garbage-collection templates.
- A completion-report template for implementation-agent closeout.
- A planning-brief template to force pre-implementation scope, risk-to-proof mapping, and rollout planning.
- A build-request template for repo path, target platform, current state, constraints, required proof, and coordinator follow-up.
- Validated examples for trivial tickets, non-trivial tickets, planning briefs, and build requests.
- A complete core golden workflow example that connects ticket, build request, planning brief, QA plan, PR note, completion report, and garbage collection.
- A 15-minute adoption guide for first-time target repos.
- A target-repo removal guide for reversible adoption.
- A prerequisites guide for local tools, full public-ready tools, and the npm-only lint path.
- A license-posture guide so public-readiness does not imply public reuse rights.
- A trust contract that documents command behavior, write paths, network use, cold-start proof, and public-release gates.
- A local `review-packet.py` tool that packages repo rules and diffs for review.
- A `make review-packet` shortcut.
- A `check-planning-brief.py` validator and `make check-planning-brief` guard for non-trivial tickets.
- A `make doctor` readiness check for package/adoption shape, workflow placement, generated artifacts, and tracked privacy markers.
- A `make kickoff` prompt generator for compact implementation-agent handoffs.
- A `make kickoff-build` prompt generator for coordinator build requests.
- A `make check-proof` guard for matching QA/PR/completion evidence to active ticket risks.
- A `make triage-review-finding` helper for turning review findings into garbage-collection records.
- A `make export-skill` target that emits a minimal Agent Skills-compatible artifact, including a caveman mode for ultra-low-context installs.
- A `make skill-budget` guard that fails when exported skill context grows too large.
- A `make local-ready` gate for local-only validation before npm-based design linting.
- A `make public-ready` gate for tests, design linting, doctor checks, diff whitespace, and review packet generation.
- A proof matrix that maps work types to expected evidence.
- A frontend-focused `Pevie Hischer/` profile with frontend implementation and review prompts.
- A Stitch-compatible Pevie `DESIGN.md` template plus validation for frontend design context.
- A complete Pevie golden workflow example that connects ticket, `DESIGN.md`, planning brief, QA plan, and PR note.
- Repository-level GitHub Actions quality workflow.
- Public-facing `CONTRIBUTING.md`, `SECURITY.md`, and `CHANGELOG.md`.
- Private-to-public publication checklist.

## Intentionally Not Included Yet

- Language-specific app linters, because there is no host app stack in this repo yet.
- Stack-specific CI integrations, because target host app platforms are not known yet.
- Project-specific runbooks, because there is no deployed service yet.
- Actual reviewer automation in GitHub, because this package is tool-agnostic until a host repo exists.

## First Additions Once App Code Exists

- Host-repo CI jobs that run app-specific lint, typecheck, unit, e2e, and package review checks.
- One bespoke lint or source test for the first repeated agent failure.
- A project `RUNBOOK.md`.
- A small `docs/critical-user-journeys.md` file for QA-plan generation.
