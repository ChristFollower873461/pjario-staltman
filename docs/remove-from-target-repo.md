# Remove From A Target Repo

Use this when a target repository tried Pjario Staltman and needs to back it out cleanly.

## Before Removing

Record why the workflow is being removed:

- too much ceremony for the repo size
- wrong fit for the team
- replaced by a lighter local convention
- split into a different package
- temporary evaluation complete

If the package created useful tickets, QA notes, PR notes, completion reports, or review records, keep those project artifacts unless they are only sample files.

## Remove Core Files

Remove copied package files only if they are not used by other local workflows:

- `build-system/`
- `tools/check-planning-brief.py`
- `tools/check-proof.py`
- `tools/kickoff.py`
- `tools/review-packet.py`
- `tools/triage-review-finding.py`
- `tools/quiet-aggregate.py`
- copied package `tests/`
- copied package `examples/`
- package-specific `Makefile` targets

Remove or edit `AGENTS.md` only after preserving any repo-specific agent rules that should stay.

The default `.pjario/quiet-aggregate.jsonl` ledger is local and ignored. Preserve it only if its verified review history is still useful; otherwise remove the repo-local `.pjario/` directory through the host repo's normal recoverable cleanup process.

## Remove CI Hooks

Remove Pjario-specific CI jobs from root `.github/workflows/`.

If the workflow file was copied directly from this package, remove it. If checks were folded into an existing workflow, remove only the Pjario-specific steps.

## Remove Pevie

For frontend-only removal:

- remove `Pevie Hischer/`
- remove Pevie-specific Makefile targets
- remove Pevie-specific CI steps
- keep `DESIGN.md` if the product team still uses it as the design source of truth

## Validate The Backout

Run the host repo's normal checks:

```bash
git diff --check
```

Then run the host repo's standard lint, typecheck, tests, build, or smoke checks.

## Keep The Learning

If Pjario caught repeated problems before removal, keep the useful guardrail in the host repo as a smaller local rule, test, template, lint, or checklist item.
