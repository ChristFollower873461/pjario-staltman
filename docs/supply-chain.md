# Supply Chain

Pjario Staltman is intentionally low-dependency.

## Core Package

- Core Python tools use the Python standard library.
- The `pjario` Work Packet CLI, dry-run adopter, and stable proof validator add no runtime dependency.
- There is no core Python dependency install step.
- There is no vendored third-party code.
- Generated review packets and skill exports are local artifacts and are ignored by default.

## External Runtime Touchpoints

| Surface | Purpose | Pinning |
| --- | --- | --- |
| `actions/checkout` | GitHub Actions checkout | `v7.0.1` commit `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `actions/setup-python` | GitHub Actions Python runtime | `v7.0.0` commit `5fda3b95a4ea91299a34e894583c3862153e4b97`, Python `3.11` |
| `actions/setup-node` | GitHub Actions Node runtime | `v7.0.0` commit `820762786026740c76f36085b0efc47a31fe5020`, Node `24` |
| `@google/design.md` | Pevie `DESIGN.md` linting | Exact package version `@google/design.md@0.4.0` through `DESIGN_MD_VERSION` |

## Optional Review Integration

Quiet Aggregate can consume the structured JSON produced by OpenClaw's maintained `autoreview` skill. The compatibility contract was tested against `openclaw/openclaw` commit `55816c47d133d00bf0b6306881589975505338a9`.

Pjario does not vendor, download, install, or invoke that helper. The commit is a tested schema reference, not a runtime dependency. Operators independently choose the reviewer engine, model provider, credentials, network boundary, and cost posture before producing a report for Quiet Aggregate.

## Network Use

Core Pjario commands are local. Network is expected only for:

- GitHub Actions dependency/action resolution.
- Pevie design linting through `npx -y @google/design.md@0.4.0`.

Quiet Aggregate itself does not use the network. Running an external autoreview helper may submit a bounded change bundle to the selected model provider; review that helper's isolation, privacy, and cost contract separately.

Use `make local-ready` when a local-only validation path is needed.

## Review Rule

Before changing an external tool, update this document, keep the version pinned, and run:

```bash
make public-ready
```

The active root workflow and bundled Pevie workflow template both use immutable commit SHAs with reviewed release tags in comments. Dependabot checks those action pins weekly. `make doctor` fails when action pins are mutable or the documented design validator version drifts from the executable Makefile pin.
