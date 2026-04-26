# Contributing

Pjario Staltman is private while it is being refined. This guide exists so the repository is ready for outside collaborators later.

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
make test-all
make review-packet
make pevie-review-packet
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

## Public Release Note

Do not change repository visibility until `PUBLICATION-CHECKLIST.md` is complete and the license posture is intentionally chosen.
