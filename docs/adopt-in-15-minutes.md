# Adopt In 15 Minutes

Use this path when installing Pjario Staltman into a target repository for the first time.

Start with a non-mutating inventory:

```bash
python3 tools/pjario.py adopt --target /path/to/repo --profile core --dry-run
```

## 1. Copy The Core

Copy:

- `AGENTS.md`
- `build-system/`
- `tools/`
- `tests/`
- `.github/workflows/quality.yml` into the target repo root workflow directory
- relevant `Makefile` targets
- `evals/skill-behavior.json` when the target will maintain or extend the skill

Run:

```bash
make doctor MODE=adopted PROFILE=core
make test
make validate-examples
make review-packet
```

## 2. Pick The Work Packet Path

Track Work Packets under `.pjario/work/`. Keep other `.pjario/` runtime state ignored:

```gitignore
.pjario/*
!.pjario/work/
!.pjario/work/*.md
```

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

1. Create one packet with `python3 tools/pjario.py start --help`.
2. Fill Scope; fill Plan only for non-trivial work.
3. Activate relevant risks and map them to stable proof IDs.
4. For UI work, set Profile to `frontend` and name the current `DESIGN.md` path.
5. Run `pjario check`, implement, and attach terminal evidence to every proof ID.
6. Run `pjario review`, record the decision, and run `pjario finish`.
7. Promote independently repeated verified friction through `pjario learn` and Quiet Aggregate.

Existing adopters may keep the older ticket, planning brief, QA plan, PR note, and completion report flow while migrating active work incrementally.

When the recurrence claim needs history across reviews, use [`docs/quiet-aggregate.md`](quiet-aggregate.md). Quiet Aggregate records only verified findings, requires independent repetition, and generates a proposal without changing policy automatically.

## Reference Example

Use `examples/work-packets/` as the preferred core examples. `examples/golden-workflow/` demonstrates the supported legacy flow.

Use `Pevie Hischer/examples/golden-workflow/` as the complete frontend example.

## Backout

If the workflow is not a fit for the target repo, use `docs/remove-from-target-repo.md` to remove copied package files and keep any project artifacts that still matter.
