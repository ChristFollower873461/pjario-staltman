# Trust Contract

Use this page to decide whether Pjario Staltman is safe to inspect, clone, run, or adapt.

## Short Answer

- Safe to inspect: yes.
- Safe to run locally: yes, after cloning into a normal development sandbox and reviewing the commands below.
- Ready for public reuse: not until a license is chosen; see `docs/license-posture.md`.
- Network access: only Pevie's optional `design-lint` path and the full `make public-ready` gate use npm through `npx`.
- Destructive behavior: no tracked-source destructive behavior is part of the normal workflow.

Runtime prerequisites are listed in `docs/prerequisites.md`.

## What This Package Does

Pjario Staltman gives agents and humans a repeatable build loop:

1. Define work with a ticket.
2. Require a planning brief for non-trivial work.
3. Generate compact kickoff prompts for implementation or build coordination.
4. Capture proof in QA notes, PR notes, completion reports, commands, logs, screenshots, or artifacts.
5. Generate review packets that preserve the diff under review.
6. Review against correctness, user risk, production risk, security, privacy, scale, and maintainability.
7. Promote repeated friction into a rule, template, test, lint, or tool.

Pevie Hischer adds frontend-specific discipline: `DESIGN.md`, accessibility, viewport proof, frontend performance, frontend observability, and production UI review.

Oh Shucksenburg adds a debt-control check: accepted debt needs an owner, trigger, and removal path.

## What It Does Not Do

- It does not deploy applications.
- It does not push commits or change remote repository settings.
- It does not collect telemetry.
- It does not read credentials for package behavior.
- It does not send repository contents to a third-party service through its Python tools.
- It does not replace host-repo tests, linters, security scanners, or release runbooks.

## Commands That Write Files

These commands write generated local artifacts:

```bash
make review-packet
make pevie-review-packet
make export-skill
make export-skill SKILL_MODE=caveman
make triage-review-finding FINDING=path/to/finding.md DECISION=test
```

`make local-ready` and `make public-ready` also generate review packets and temporary skill exports, then remove the generated review packets from the package root.

Generated review packets and `.dist/` exports are ignored so they are not committed by accident.

## Commands That Read Git State

These commands inspect local git state:

```bash
make review-packet
make pevie-review-packet
make doctor
make local-ready
make public-ready
```

They read tracked files, changed files, and eligible untracked files for validation or review context. Review-packet tooling excludes likely sensitive untracked files by default.

## Commands That Use Network

Core Pjario commands are local Python and Makefile commands.

Pevie design linting uses npm:

```bash
make pevie-design-lint
make -f "Pevie Hischer/Makefile" design-lint DESIGN=DESIGN.md
make public-ready
```

Those Pevie lint paths execute:

```bash
npx -y @google/design.md@0.1.1 lint DESIGN.md
```

Run the local design-context checks instead when offline:

```bash
make pevie-validate-examples
make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md
```

## Local-Only Preflight

To validate without npm/network access, run:

```bash
make local-ready
```

Expected result:

- unit tests pass
- core examples validate
- Pevie examples validate through local checks
- package doctor reports no failures
- skill exports build
- skill context budgets pass
- review packets build without dropping the diff
- generated review packets are removed

## Cold-Start Proof

For the full clean package proof, run:

```bash
make doctor
make test-all
make public-ready
```

Expected result:

- unit tests pass
- core examples validate
- Pevie examples validate
- Pevie `DESIGN.md` examples lint
- package doctor reports no failures
- skill exports build
- skill context budgets pass
- review packets build without dropping the diff
- generated review packets are removed by `make public-ready`

## Public-Release Gate

Before making the repository public:

1. Complete `PUBLICATION-CHECKLIST.md`.
2. Resolve `docs/license-posture.md`: choose a license, publish only for inspection, split a generic package, or keep the repository private.
3. Confirm `SECURITY.md` points to the intended disclosure channel.
4. Confirm `docs/prerequisites.md` matches the tested toolchain.
5. Run `make local-ready`.
6. Run `make public-ready`.
7. Confirm the adoption and removal paths are understandable from `docs/adopt-in-15-minutes.md` and `docs/remove-from-target-repo.md`.
8. Confirm GitHub Actions passes on the default branch.

The root GitHub Actions quality workflow runs `make public-ready`, so the badge and the local public-release gate represent the same contract.

If any of those fail, the repository is not public-ready yet.
