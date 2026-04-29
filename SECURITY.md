# Security

Pjario Staltman is currently private. Treat it as public-bound: do not commit secrets, private customer data, screenshots containing sensitive information, or personal machine paths.

## Reporting

While this repository is private, report security issues through the existing private maintainer channel.

If the repository is made public, enable GitHub private vulnerability reporting or GitHub Security Advisories before accepting outside reports.

## Sensitive Files

The review-packet tooling excludes likely sensitive untracked files by default. Do not override that behavior unless the reviewer explicitly needs the file contents and the contents have been checked for secrets.

Examples of files that must not be committed:

- `.env` and `.env.*`
- private keys and certificates
- API tokens or service credentials
- customer data exports
- screenshots with account, billing, credential, or personal data

## Command Behavior

Core Pjario tooling is local. It validates files, reads git state, generates review packets, exports skills, and writes explicit output files. Use `make local-ready` for a local-only preflight before any npm-based linting.

Pevie design linting can use network because it runs:

```bash
npx -y @google/design.md@0.1.1 lint DESIGN.md
```

Use `make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md` when an offline check is required.

The normal workflow does not push commits, deploy code, change remote repository settings, collect telemetry, or intentionally read secrets.

## Release Safety

Before making the repository public:

- Run the privacy scan from `PUBLICATION-CHECKLIST.md`.
- Review `docs/trust-contract.md`.
- Run `make local-ready`.
- Confirm generated `.review-packet.md` files are ignored and absent from the tracked tree.
- Confirm the chosen license and disclosure channel match the intended audience.
