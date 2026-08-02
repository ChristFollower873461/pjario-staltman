# Trust Contract

Use this page to decide whether Pjario Staltman is safe to inspect, clone, run, or adapt.

## Short Answer

- Safe to inspect: yes.
- Safe to run locally: yes, after cloning into a normal development sandbox and reviewing the commands below.
- Ready for public reuse: yes, under the repository's MIT License; see `docs/license-posture.md`.
- Network access: only Pevie's optional `design-lint` path and the full `make public-ready` gate use npm through `npx`.
- Destructive behavior: no tracked-source destructive behavior is part of the normal workflow.

Runtime prerequisites are listed in `docs/prerequisites.md`.

External tool pinning and network touchpoints are listed in `docs/supply-chain.md`.

## What This Package Does

Pjario Staltman gives agents and humans a repeatable build loop:

1. Keep intent, scope, risk, plan, proof IDs, evidence, review, gaps, and next action in one versioned Work Packet.
2. Require a concrete Plan only for non-trivial work.
3. Require every active risk to map to proof before implementation.
4. Generate review packets that preserve both the Work Packet and tracked diff.
5. Validate terminal evidence structurally by proof ID.
6. Review against correctness, user risk, production risk, security, privacy, scale, and maintainability.
7. Optionally route independently repeated verified findings through Quiet Aggregate without automatic policy mutation.

Pevie Hischer adds frontend-specific discipline: `DESIGN.md`, accessibility, viewport proof, frontend performance, frontend observability, and production UI review.

Oh Shucksenburg adds a debt-control check: accepted debt needs an owner, trigger, and removal path.

## What It Does Not Do

- It does not deploy applications.
- It does not push commits or change remote repository settings.
- It does not collect telemetry.
- It does not read credentials for package behavior.
- It does not send repository contents to a third-party service through its Python tools.
- It does not invoke the optional external autoreview engine; operators run and authorize that separately.
- It does not replace host-repo tests, linters, security scanners, or release runbooks.

## Commands That Write Files

These commands write generated local artifacts:

```bash
python3 tools/pjario.py start ...
python3 tools/pjario.py review --packet .pjario/work/WORK-ID.md
python3 tools/pjario.py finish --packet .pjario/work/WORK-ID.md --output .pjario/completion.md
make review-packet
make pevie-review-packet
make export-skill
make export-skill SKILL_MODE=caveman
make triage-review-finding FINDING=path/to/finding.md DECISION=test
python3 tools/quiet-aggregate.py record ...
python3 tools/quiet-aggregate.py report --output .pjario/quiet-report.json
python3 tools/quiet-aggregate.py propose ... --output path/to/proposal.md
```

`make local-ready` and `make public-ready` also generate review packets and temporary skill exports, then remove the generated review packets from the package root.

Every exported skill includes the repository's MIT `LICENSE` file. The license file is not Markdown and therefore does not consume the agent instruction budget measured by `make skill-budget`.

Generated review packets and `.dist/` exports are ignored so they are not committed by accident.

Work Packets under `.pjario/work/` are intended to be tracked. Private runtime state elsewhere under `.pjario/`, including the Quiet Aggregate ledger and generated review/completion packets, remains ignored. Repo-confined outputs fail closed on traversal and symlink boundaries.

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

Quiet Aggregate is also local and standard-library-only. It can consume a JSON report previously produced by an external autoreview helper, but it does not launch that helper or contact a model provider.

The `pjario` Work Packet CLI is local and standard-library-only. `adopt` is dry-run-only; it reports proposed file operations and makes no changes.

Pevie design linting uses npm:

```bash
make pevie-design-lint
make -f "Pevie Hischer/Makefile" design-lint DESIGN=DESIGN.md
make public-ready
```

Those Pevie lint paths execute:

```bash
npx -y @google/design.md@0.4.0 lint DESIGN.md
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

Before a public release or material change to the public package contract:

1. Complete `PUBLICATION-CHECKLIST.md`.
2. Confirm `LICENSE` and `docs/license-posture.md` still match the intended reuse and packaging terms.
3. Confirm `SECURITY.md` points to the intended disclosure channel.
4. Confirm `docs/prerequisites.md` matches the tested toolchain.
5. Confirm `docs/supply-chain.md` matches the external tools in use.
6. Run `make local-ready`.
7. Run `make public-ready`.
8. Confirm the adoption and removal paths are understandable from `docs/adopt-in-15-minutes.md` and `docs/remove-from-target-repo.md`.
9. Confirm GitHub Actions passes on the default branch.

The root GitHub Actions quality workflow runs `make public-ready`, so the badge and the local public-release gate represent the same contract.

If any of those fail, the repository is not public-ready yet.
