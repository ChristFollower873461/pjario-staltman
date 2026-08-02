# Public Release Audit

Release baseline: `0.2.0`

Reviewed: 2026-08-02

## Outcome

Pjario Staltman is safe to publish as a small, MIT-licensed operating system for agent-assisted engineering. The core workflow, Pevie Hischer frontend profile, and Quiet Aggregate review-learning loop share adoption, proof, review, privacy, and removal conventions.

## Scope

This audit covers the current release tree, reachable repository history, executable quality gates, public documentation, licensing, security reporting, external tool pins, and the optional structured-autoreview boundary. It does not claim that Pjario validates a host application's correctness or that a model-generated finding is correct; adopters must still verify findings and run their own product, security, accessibility, performance, and release checks.

## Privacy And Secret Proof

- Gitleaks `8.30.1` scanned the full reachable history with `--all`: zero findings.
- Gitleaks `8.30.1` scanned the current working tree: zero findings.
- `make doctor` scanned tracked text for credentials, private paths, private organization markers, and generated review artifacts: zero findings.
- The package contains no screenshots, customer exports, runtime credentials, or telemetry.
- Quiet Aggregate rejects common credential shapes and local absolute paths before writing its ignored local ledger.

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

The public-ready gate runs 64 Python tests across both profiles, including Quiet Aggregate success, rejection, corruption, identity-integrity, idempotency, path-confinement, resource-limit, and promotion cases. It validates the golden workflows, builds both skill export modes with their MIT notice and within their context budgets, generates both review packets without silently dropping the diff, and lints all three bundled design contracts with `@google/design.md@0.4.0`.

The maintained OpenClaw autoreview compatibility reference was audited separately at commit `55816c47d133d00bf0b6306881589975505338a9`: 271 hardening tests passed with 3 environment-specific skips, and its deterministic `--dry-run` succeeded against Pjario. That external suite is evidence for the adapter boundary, not part of Pjario's public-ready test count.

## Supply Chain

- Core Python tooling uses only the standard library.
- GitHub Actions are pinned to immutable commits and restricted to read-only repository contents.
- The only package fetched by the normal public-ready gate is the exact `@google/design.md@0.4.0` validator.
- Dependabot checks GitHub Actions weekly.
- Quiet Aggregate uses only the Python standard library and does not download or invoke the optional autoreview helper.

## Known Limits

- Pjario is workflow tooling, not a hosted service, autonomous deployment system, or substitute for host-repository tests.
- Quiet Aggregate does not infer semantic equivalence, verify findings, invoke a model, or apply policy. The main agent or human owns those decisions.
- `make public-ready` requires npm/network access for the design validator; `make local-ready` provides the offline preflight.
- No GitHub Release tag should be created until the workflow has been exercised in a real target repository and the resulting adoption evidence has been reviewed.

## Launch Verification

- Public repository: `https://github.com/ChristFollower873461/pjario-staltman`
- The default-branch quality badge runs the same `make public-ready` contract documented above.
- Anonymous GitHub API and raw `README.md` requests returned the public repository and MIT license metadata.
- GitHub private vulnerability reporting, secret scanning, and push protection are enabled.
