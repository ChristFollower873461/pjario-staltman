# Public Release Audit

Release baseline: `0.1.0`

Reviewed: 2026-08-01

## Outcome

Pjario Staltman is safe to publish as a small, MIT-licensed operating system for agent-assisted engineering. The core workflow and the Pevie Hischer frontend profile remain bundled because they share adoption, proof, review, and removal conventions.

## Scope

This audit covers the current tracked tree, all 16 commits in the repository history, executable quality gates, public documentation, licensing, security reporting, and external tool pins. It does not claim that Pjario validates a host application's correctness; adopters must still run their own product, security, accessibility, performance, and release checks.

## Privacy And Secret Proof

- Gitleaks `8.30.1` scanned all 16 commits with `--all`: zero findings.
- Gitleaks `8.30.1` scanned the current working tree: zero findings.
- `make doctor` scanned tracked text for credentials, private paths, private organization markers, and generated review artifacts: zero findings.
- The package contains no screenshots, customer exports, runtime credentials, or telemetry.

## Reproducible Quality Proof

```bash
make test-all
make validate-examples
make kickoff-build REQUEST=examples/golden-workflow/build-request.md
make doctor
make skill-budget
make local-ready
make public-ready
```

The public-ready gate runs 53 Python tests across both profiles, validates the golden workflows, builds both skill export modes with their MIT notice and within their context budgets, generates both review packets without silently dropping the diff, and lints all three bundled design contracts with `@google/design.md@0.4.0`.

## Supply Chain

- Core Python tooling uses only the standard library.
- GitHub Actions are pinned to immutable commits and restricted to read-only repository contents.
- The only package fetched by the normal public-ready gate is the exact `@google/design.md@0.4.0` validator.
- Dependabot checks GitHub Actions weekly.

## Known Limits

- Pjario is workflow tooling, not a hosted service, autonomous deployment system, or substitute for host-repository tests.
- `make public-ready` requires npm/network access for the design validator; `make local-ready` provides the offline preflight.
- No GitHub Release tag should be created until the workflow has been exercised in a real target repository and the resulting adoption evidence has been reviewed.

## Launch Verification

- Public repository: `https://github.com/ChristFollower873461/pjario-staltman`
- Default-branch quality run: `https://github.com/ChristFollower873461/pjario-staltman/actions/runs/30730184308` (`fccdd393de0e5d4012c767374387be1bc6d95679`, passed)
- Anonymous GitHub API and raw `README.md` requests returned the public repository and MIT license metadata.
- GitHub private vulnerability reporting, secret scanning, and push protection are enabled.
