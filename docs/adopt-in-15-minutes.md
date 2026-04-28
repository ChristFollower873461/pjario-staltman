# Adopt In 15 Minutes

Use this path when installing Pjario Staltman into a target repository for the first time.

## 1. Copy The Core

Copy:

- `AGENTS.md`
- `build-system/`
- `tools/`
- `tests/`
- `.github/workflows/quality.yml` into the target repo root workflow directory
- relevant `Makefile` targets

Run:

```bash
make doctor MODE=adopted PROFILE=core
make test
make validate-examples
make review-packet
```

## 2. Pick Working Paths

Decide and write down:

- Ticket path.
- Planning brief path.
- Build request path.
- Review packet command.

For frontend-heavy repos, also decide where `DESIGN.md` lives. Prefer the repo root.

## 3. Add Pevie For Frontend Work

Copy `Pevie Hischer/` when the target repo needs UI quality gates.

Run:

```bash
make -f "Pevie Hischer/Makefile" test
make -f "Pevie Hischer/Makefile" validate-examples
make -f "Pevie Hischer/Makefile" design-lint-examples
```

If adopting Pevie by itself, copy `Pevie Hischer/.github/workflows/pevie-quality.yml` into the target repo's root `.github/workflows/` directory.

## 4. Establish DESIGN.md Before UI Implementation

Create `DESIGN.md` from:

```text
Pevie Hischer/build-system/templates/DESIGN.md
```

Then run:

```bash
make doctor MODE=adopted PROFILE=pevie
make -f "Pevie Hischer/Makefile" design-lint DESIGN=DESIGN.md
```

Treat `DESIGN.md` as binding design context for non-trivial UI work.

## 5. Start With One Real Change

Use this order:

1. Fill a ticket.
2. Fill a planning brief for non-trivial work.
3. For UI work, confirm `DESIGN.md` is current.
4. Implement the smallest scoped patch.
5. Fill PR and QA notes.
6. Generate a kickoff prompt with `make kickoff`.
7. Generate a review packet.
8. Review and promote repeated friction into a durable rule, test, template, lint, or tool.

## Reference Example

Use `Pevie Hischer/examples/golden-workflow/` as the complete frontend example.
