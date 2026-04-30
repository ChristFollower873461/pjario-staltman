# Supply Chain

Pjario Staltman is intentionally low-dependency.

## Core Package

- Core Python tools use the Python standard library.
- There is no core Python dependency install step.
- There is no vendored third-party code.
- Generated review packets and skill exports are local artifacts and are ignored by default.

## External Runtime Touchpoints

| Surface | Purpose | Pinning |
| --- | --- | --- |
| `actions/checkout` | GitHub Actions checkout | Major version in `.github/workflows/quality.yml` |
| `actions/setup-python` | GitHub Actions Python runtime | Major version plus Python `3.11` |
| `actions/setup-node` | GitHub Actions Node runtime | Major version plus Node `24` |
| `@google/design.md` | Pevie `DESIGN.md` linting | Exact version through `DESIGN_MD_VERSION ?= 0.1.1` |

## Network Use

Core Pjario commands are local. Network is expected only for:

- GitHub Actions dependency/action resolution.
- Pevie design linting through `npx -y @google/design.md@0.1.1`.

Use `make local-ready` when a local-only validation path is needed.

## Review Rule

Before changing an external tool, update this document, keep the version pinned, and run:

```bash
make public-ready
```

For a stricter public release, consider pinning GitHub Actions by commit SHA. The current package uses major-version pins for maintainability while the repository remains private.
