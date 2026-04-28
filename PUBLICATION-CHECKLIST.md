# Publication Checklist

Use this before making the repository public.

## Privacy And Provenance

- [ ] Confirm there are no personal paths, private company names, credentials, tokens, keys, screenshots, or customer data.
- [ ] Confirm package docs describe generic agent workflows, not private internal operations.
- [ ] Decide whether to include a license. Until then, keep the repository private.
- [ ] Decide whether to keep `Pevie Hischer/` in this repository or split it into a separate package later.
- [ ] Confirm `SECURITY.md` has the right public reporting channel before opening the repo.

## Repository Polish

- [ ] Run `make test-all`.
- [ ] Run `make validate-examples`.
- [ ] Run `make kickoff-build REQUEST=examples/golden-workflow/build-request.md`.
- [ ] Run `make pevie-validate-examples`.
- [ ] Run `make pevie-design-lint`.
- [ ] Run `make doctor`.
- [ ] Run `make export-skill OUT="$(mktemp -d)/pjario-staltman"`.
- [ ] Run `make public-ready`.
- [ ] Run `make review-packet`.
- [ ] Run `make pevie-review-packet`.
- [ ] Confirm generated `.review-packet.md` files are ignored.
- [ ] Confirm GitHub Actions passes on the default branch.
- [ ] Review `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `ADOPTION-CHECKLIST.md`, and `MAIN-AGENT-HANDOFF.md` for public clarity.

## Public Launch

- [ ] Add a license if public reuse is intended.
- [ ] Confirm the repository description and topics still fit the intended public audience.
- [ ] Set the repository visibility to public.
- [ ] Create a first release tag only after the workflow has been used in at least one real target repo.
