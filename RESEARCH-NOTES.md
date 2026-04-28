# Research Notes

These notes capture external conventions that shape this package.

## Agent Skills

- Source: https://developers.openai.com/codex/skills
- Skills are folders with `SKILL.md` plus optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`.
- Skills rely on progressive disclosure: concise metadata first, full instructions only when the skill is selected.
- For this package, the repo is the full operating system; `make export-skill` emits the smaller reusable skill artifact.

## DESIGN.md

- Source: https://github.com/google-labs-code/design.md
- `DESIGN.md` combines YAML design tokens with Markdown rationale.
- The official CLI supports `lint`, `diff`, `export`, and `spec`.
- Pevie uses pinned `@google/design.md` linting so UI agents cannot silently drift from the design contract.

## GitHub Workflows

- Source: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- GitHub workflow files must live under the repository root `.github/workflows` directory.
- Nested workflow files can be included as package templates, but adopters must copy active workflows to the host repo root.

## Secret Protection

- Source: https://github.com/security/advanced-security/secret-protection
- GitHub Secret Protection and push protection can block many credential leaks during pushes.
- This package still keeps a local tracked-file privacy scan in `make doctor` because local checks catch public-readiness problems before a push.
