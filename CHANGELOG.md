# Changelog

All notable changes to this package should be documented here.

## Unreleased

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
