# Main Agent Handoff

This package is a portable release-quality workflow for agentic engineering:

- Ticketed work with explicit risk surfaces and proof requirements
- Pre-implementation planning for non-trivial tasks
- Implementation and QA evidence templates
- Staff-level review agent rubric and severity model
- Review packet generation for LLM/agent review
- Enforcement checks and tests for core guardrails
- A frontend-focused companion profile in `Pevie Hischer/`

## What Is Included

- `AGENTS.md`
  - Repo operating rules and completion bar.
- `build-system/README.md`
  - Full workflow loop and review posture.
- `build-system/rules/`
  - `review-standards.md`
  - `scale-readiness.md`
  - `proof-matrix.md`
- `build-system/agents/`
  - `implementation-agent.md`
  - `software-engineer-reviewer.md`
  - `build-coordinator.md`
- `build-system/templates/`
  - `build-request.md`
  - `ticket.md`
  - `planning-brief.md`
  - `qa-plan.md`
  - `pr.md`
  - `garbage-collection.md`
- `examples/`
  - Validated sample trivial ticket, non-trivial ticket, planning brief, and build request.
- `docs/adopt-in-15-minutes.md`
  - Fast target-repo adoption path.
- `tools/review-packet.py`
  - Builds `.review-packet.md` for review-agent context.
  - Includes sensitive untracked-file filtering by default.
- `tools/check-planning-brief.py`
  - Enforces planning brief for non-trivial tickets.
- `tools/check-proof.py`
  - Checks that QA/PR/completion evidence covers active ticket risks.
- `tools/doctor.py`, `tools/kickoff.py`, `tools/export-skill.py`
  - Validate package/adoption shape, generate implementation-agent prompts, and export a compact Agent Skills artifact.
- `tools/triage-review-finding.py`
  - Converts review findings into garbage-collection records.
- `tests/`
  - Unit tests for package tool scripts.
- `Pevie Hischer/`
  - Frontend-focused profile for UI taste, Stitch-compatible `DESIGN.md`, accessibility, performance, observability, and frontend QA.
  - If adopting its nested workflow file, copy it into the host repo root `.github/workflows/` directory.
- `.github/workflows/quality.yml`
  - Repository-level smoke and package checks.
- `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`
  - Public-facing maintainer and release-readiness docs.

## Baseline Commands

- `make test`
- `make test-all`
- `make validate-examples`
- `make review-packet`
- `make doctor`
- `make kickoff TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md`
- `make kickoff-build REQUEST=path/to/build-request.md`
- `make check-proof TICKET=path/to/ticket.md QA=path/to/qa-plan.md PR=path/to/pr-note.md COMPLETION=path/to/completion-report.md`
- `make triage-review-finding FINDING=path/to/finding.md DECISION=test`
- `make export-skill`
- `make public-ready`
- `make pevie-test`
- `make pevie-validate-examples`
- `make pevie-design-lint`
- `make pevie-review-packet`
- `make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md`
- `make check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md`

Notes:

- For trivial tickets, `PLAN` is optional:
  - `make check-planning-brief TICKET=path/to/ticket.md`
- If using `review-packet.py --base <ref>`, ensure the base ref exists locally.

## Expected Working Contract

1. Fill `build-system/templates/ticket.md` and set `Level: trivial` or `Level: non-trivial`.
2. For non-trivial work, fill `build-system/templates/planning-brief.md`.
3. For coordinated build work, fill `build-system/templates/build-request.md` and use `build-system/agents/build-coordinator.md`.
4. For frontend-heavy work, use `Pevie Hischer/MAIN-AGENT-HANDOFF.md`.
5. Implement with `build-system/agents/implementation-agent.md`.
6. Attach evidence using `build-system/templates/pr.md` and `build-system/templates/qa-plan.md`.
7. Generate packet with `make review-packet`.
8. Review with `build-system/agents/software-engineer-reviewer.md`.
9. Promote repeated failures using `build-system/templates/garbage-collection.md`.

## Adoption Steps In A Target Repo

1. Copy `AGENTS.md`, `build-system/`, `tools/`, `tests/`, `Makefile` targets.
2. Run `make test` and confirm all checks pass.
3. Run `make doctor MODE=adopted` after copying the workflow into the host repo.
4. Pick canonical ticket and planning-brief paths in the target repo.
5. Optionally add CI to run:
   - `make test`
   - `make pevie-test`
   - `make check-planning-brief ...` on changed tickets
   - `make review-packet` sanity step
6. Start with one team/project path and tune rules via weekly garbage collection.

## Known Integration Decisions For Main Agent

- Decide canonical paths for active ticket + planning brief in the host repo.
- Decide where build requests live in the host repo.
- Decide whether planning-brief enforcement should be mandatory in CI or soft-gated.
- Decide whether to keep `scale-readiness.md` as-is or split by stack (web/backend/data/AI).
- Decide whether `Pevie Hischer/` should be adopted as the default frontend profile.
- For frontend-heavy repos, decide where the canonical `DESIGN.md` lives before implementation begins.
- Add host-repo specific runbooks once deployed services exist.

## QA Snapshot

- `make test-all` currently passes in this repository.
- `make validate-examples` and `make pevie-validate-examples` currently pass.
- `make doctor` checks package shape, public-readiness docs, root workflow placement, generated artifacts, and tracked privacy markers.
- `make check-proof` validates the core golden workflow proof evidence.
- `make review-packet` currently generates `.review-packet.md`.
- Planning checker passes on valid non-trivial ticket + planning brief.
- Pevie `DESIGN.md` template and example currently pass design-context validation.
