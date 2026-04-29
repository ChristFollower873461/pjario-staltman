# Prerequisites

Pjario Staltman is intentionally light. Core commands use the local shell, Git, Make, and Python standard library.

## Supported Baseline

- macOS or Linux shell environment.
- Git available as `git`.
- Make available as `make`.
- Python 3.11 or newer available as `python3`.
- Node.js 24 and npm/npx for Pevie `DESIGN.md` linting and the full `make public-ready` gate.

The GitHub Actions quality workflow uses Python 3.11 and Node 24.

## Local-Only Use

For a local-only preflight that avoids npm and network access, run:

```bash
make local-ready
```

This path exercises the Python tooling, examples, doctor checks, skill exports, skill budget, and review-packet generation.

## Full Public-Ready Use

For full package proof, run:

```bash
make public-ready
```

This includes `make local-ready` plus Pevie `DESIGN.md` linting through:

```bash
npx -y @google/design.md@0.1.1 lint DESIGN.md
```

## No Core Package Install

The core package has no Python dependency install step. If a command requires installing app-specific dependencies, that dependency belongs to the host repository, not this package.
