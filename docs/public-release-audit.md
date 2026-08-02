# Public Release Audit

Release baseline: `0.3.0`

Reviewed: 2026-08-02

## Outcome

Pjario Staltman is safe to publish as a small, MIT-licensed operating system for agent-assisted engineering. One versioned Work Packet now carries the core workflow from intent through proof and review; Pevie Hischer and Quiet Aggregate share the same adoption, privacy, and removal boundaries.

## Scope

This audit covers the current release tree, reachable repository history, executable quality gates, public documentation, licensing, security reporting, external tool pins, and the optional structured-autoreview boundary. It does not claim that Pjario validates a host application's correctness or that a model-generated finding is correct; adopters must still verify findings and run their own product, security, accessibility, performance, and release checks.

## Privacy And Secret Proof

- Gitleaks `8.30.1` scanned the full reachable history with `--all`: zero findings.
- Gitleaks `8.30.1` scanned the current working tree: zero findings.
- `make doctor` scanned tracked text for credentials, private paths, private organization markers, and generated review artifacts: zero findings.
- The package contains no screenshots, customer exports, runtime credentials, or telemetry.
- Work Packets and Quiet Aggregate reject common credential shapes and local absolute paths before writing; private runtime state stays ignored while `.pjario/work/*.md` remains reviewable.

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

The public-ready gate runs 82 Python tests across both profiles. Coverage includes Work Packet parsing, stable risk/proof mapping, success and accepted-gap completion, incomplete-review rejection, path and secret rejection, exported-command execution, bundled-helper integrity, idempotent adoption inventory, mandatory review context, legacy proof compatibility, deterministic skill-behavior fixtures, and Quiet Aggregate success, rejection, corruption, identity-integrity, idempotency, resource-limit, and promotion cases. It validates both Work Packet examples and the legacy golden workflows, builds both skill export modes with their MIT notice and within their context budgets, generates review packets without silently dropping the Work Packet or diff, and lints all three bundled design contracts with `@google/design.md@0.4.0`.

The standard exported skill is 200 words in `SKILL.md` and 682 Markdown words total, down from the 0.2.0 baseline of 259 and 969. Its generated OpenAI interface metadata matches the official generator, and the official Agent Skills validator reports `Skill is valid!`.

The maintained OpenClaw autoreview compatibility reference was audited separately at commit `55816c47d133d00bf0b6306881589975505338a9`: 271 hardening tests passed with 3 environment-specific skips, and its deterministic `--dry-run` succeeded against Pjario. That external suite is evidence for the adapter boundary, not part of Pjario's public-ready test count.

## Supply Chain

- Core Python tooling uses only the standard library.
- The `pjario` CLI and exported command helpers add no runtime dependency or network call.
- GitHub Actions are pinned to immutable commits and restricted to read-only repository contents.
- The only package fetched by the normal public-ready gate is the exact `@google/design.md@0.4.0` validator.
- Dependabot checks GitHub Actions weekly.
- Quiet Aggregate uses only the Python standard library and does not download or invoke the optional autoreview helper.

## Known Limits

- Pjario is workflow tooling, not a hosted service, autonomous deployment system, or substitute for host-repository tests.
- Behavioral fixtures are deterministic contract tests, not claims about every model response; maintainers should rerun representative agent evaluations when prompts or routing change materially.
- Quiet Aggregate does not infer semantic equivalence, verify findings, invoke a model, or apply policy. The main agent or human owns those decisions.
- `make public-ready` requires npm/network access for the design validator; `make local-ready` provides the offline preflight.
- No GitHub Release tag should be created until the workflow has been exercised in a real target repository and the resulting adoption evidence has been reviewed.

## Launch Verification

- Public repository: `https://github.com/ChristFollower873461/pjario-staltman`
- The default-branch quality badge runs the same `make public-ready` contract documented above.
- Anonymous GitHub API and raw `README.md` requests returned the public repository and MIT license metadata.
- GitHub private vulnerability reporting, secret scanning, and push protection are enabled.
