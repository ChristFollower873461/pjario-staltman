# Publication Checklist

Use this before making the repository public.

## Privacy And Provenance

- [ ] Confirm there are no personal paths, private company names, credentials, tokens, keys, screenshots, or customer data.
- [ ] Confirm package docs describe generic agent workflows, not private internal operations.
- [ ] Decide whether to include a license. Until then, keep the repository private.
- [ ] Decide whether to keep `Pevie Hischer/` in this repository or split it into a separate package later.

## Repository Polish

- [ ] Run `make test-all`.
- [ ] Run `make review-packet`.
- [ ] Run `make pevie-review-packet`.
- [ ] Confirm generated `.review-packet.md` files are ignored.
- [ ] Confirm GitHub Actions passes on the default branch.
- [ ] Review `README.md`, `ADOPTION-CHECKLIST.md`, and `MAIN-AGENT-HANDOFF.md` for public clarity.

## Public Launch

- [ ] Add a license if public reuse is intended.
- [ ] Add repository description and topics.
- [ ] Set the repository visibility to public.
- [ ] Create a first release tag only after the workflow has been used in at least one real target repo.
