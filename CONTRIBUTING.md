# Contributing

Pjario Staltman welcomes focused issues and pull requests that make agent-assisted engineering easier to trust, adopt, or remove.

## Quality Bar

Every meaningful change should preserve the operating loop:

1. Ticket.
2. Planning brief for non-trivial work.
3. Scoped implementation.
4. Proof.
5. Staff-level review.
6. Durable rule, test, template, or tool when friction repeats.

## Local Checks

Run the package checks before proposing a change:

```bash
make local-ready
make public-ready
```

For template or example changes, also run:

```bash
make validate-examples
make pevie-validate-examples
```

## Pull Request Expectations

- Keep changes scoped to one quality improvement.
- Update examples when changing template requirements.
- Add regression tests when fixing tool behavior.
- Explain risk, proof, and follow-ups in the PR note.
- Do not include private company names, credentials, screenshots, customer data, personal paths, or generated review packets.

## Security And License

Do not open a public issue for a suspected vulnerability or accidentally exposed secret. Follow [`SECURITY.md`](SECURITY.md) instead.

Contributions are accepted under the repository's [MIT License](LICENSE).
