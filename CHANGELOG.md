# Changelog

All notable changes to this package should be documented here.

## Unreleased

- Added a target-repo removal guide so adoption has a documented backout path.
- Added `make local-ready` as a local-only preflight before npm-based Pevie design linting.
- Updated GitHub Actions to run the same `make public-ready` gate documented for public evaluation.
- Added a trust contract documenting command behavior, file writes, git-state reads, network use, cold-start proof, and the public-release gate.
- Added `SKILL_MODE=caveman` and `make skill-budget` to keep exported agent context intentionally small.
- Added Oh Shucksenburg technical-debt control across core and Pevie templates, proof matrices, exported skill references, and doctor-required files.
- Added a complete core golden workflow example with ticket, build request, planning brief, QA plan, PR note, completion report, and garbage collection.
- Added `make check-proof`, `make kickoff-build`, and `make triage-review-finding` for core proof enforcement, build-request handoff generation, and review-finding garbage collection.
- Added `build-system/templates/completion-report.md` so implementation-agent closeouts have a stable shape.
- Added `make doctor`, `make kickoff`, `make export-skill`, and `make public-ready` so package adoption, implementation handoff, skill packaging, and publication checks are deterministic.
- Added core and Pevie proof matrices to make required evidence explicit by work type.
- Added root research notes for current Agent Skills, DESIGN.md, GitHub workflow placement, and secret-protection conventions.
- Added pinned official `@google/design.md` linting for Pevie `DESIGN.md` examples and CI.
- Added a 15-minute adoption guide and a complete Pevie golden workflow example.
- Added a Stitch-compatible `DESIGN.md` contract to the Pevie frontend profile.
- Added Pevie design-context validation and wired `DESIGN.md` into planning, implementation, review, PR notes, and QA plans.
- Hardened Pevie review packets so the diff is mandatory context and optional rules cannot crowd it out.
- Hardened Pevie planning-brief validation to reject empty required sections and stale ready gates.
- Clarified Pevie GitHub Actions adoption when using the nested companion profile by itself.
- Updated GitHub Actions workflow dependencies to current major versions.
- Added validated examples for core and frontend workflows.
- Added public-facing contribution and security docs while keeping the repository private.

## 0.1.0-private

- Added the core Pjario Staltman workflow package.
- Added the Pevie Hischer frontend quality profile.
- Added review-packet generation, planning-brief validation, tests, and GitHub Actions.
