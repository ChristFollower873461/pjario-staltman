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

## Release Safety

Before making the repository public:

- Run the privacy scan from `PUBLICATION-CHECKLIST.md`.
- Confirm generated `.review-packet.md` files are ignored and absent from the tracked tree.
- Confirm the chosen license and disclosure channel match the intended audience.
