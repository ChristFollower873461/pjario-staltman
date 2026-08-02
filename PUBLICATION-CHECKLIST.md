# Publication Checklist

Use this before making the repository public.

Release audit: [`docs/public-release-audit.md`](docs/public-release-audit.md)

## Privacy And Provenance

- [x] Confirm there are no personal paths, private company names, credentials, tokens, keys, screenshots, or customer data.
- [x] Confirm package docs describe generic agent workflows, not private internal operations.
- [x] Resolve `docs/license-posture.md` with the MIT License.
- [x] Keep `Pevie Hischer/` bundled as the intentionally related frontend profile.
- [x] Point `SECURITY.md` to GitHub private vulnerability reporting.

## Repository Polish

- [x] Review `docs/trust-contract.md` from the perspective of a cold outside evaluator.
- [x] Review `docs/license-posture.md` and confirm the current visibility/reuse stance is intentional.
- [x] Review `docs/prerequisites.md` against the current GitHub Actions toolchain.
- [x] Review `docs/supply-chain.md` against current external tool versions.
- [x] Review `docs/quiet-aggregate.md` against the tested autoreview schema and local privacy boundary.
- [x] Review `docs/adopt-in-15-minutes.md` and `docs/remove-from-target-repo.md` for reversible adoption.
- [x] Validate both complete Work Packet examples with `pjario finish`.
- [x] Run deterministic skill-behavior fixtures for triggering, routing, and learning boundaries.
- [x] Run `make test-all`.
- [x] Run `make validate-examples`.
- [x] Run `make kickoff-build REQUEST=examples/golden-workflow/build-request.md`.
- [x] Run `make pevie-validate-examples`.
- [x] Run `make pevie-design-lint`.
- [x] Run `make doctor`.
- [x] Run `make export-skill OUT="$(mktemp -d)/pjario-staltman"`.
- [x] Execute `scripts/pjario start` from a clean exported skill.
- [x] Validate the exported skill with the Agent Skills validator and generated OpenAI interface metadata.
- [x] Run `make export-skill SKILL_MODE=caveman OUT="$(mktemp -d)/pjario-staltman-caveman"`.
- [x] Run `make skill-budget`.
- [x] Run `make local-ready`.
- [x] Run `make public-ready`.
- [x] Run `make review-packet`.
- [x] Run `make pevie-review-packet`.
- [x] Confirm generated `.review-packet.md` files are ignored.
- [x] Confirm the public-release commit passes GitHub Actions on the default branch.
- [x] Review `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `ADOPTION-CHECKLIST.md`, `MAIN-AGENT-HANDOFF.md`, and `docs/trust-contract.md` for public clarity.

## Public Launch

- [x] Add the MIT License for public reuse.
- [x] Confirm the repository description, homepage, and topics fit the intended public audience.
- [x] Set the repository visibility to public and verify unauthenticated API and raw-source access.
- [x] Enable and verify GitHub private vulnerability reporting.
- [ ] Create a first release tag only after the workflow has been used in at least one real target repo.
