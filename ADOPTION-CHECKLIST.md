# Adoption Checklist

Use this checklist when installing Pjario Staltman into a target repository.

## 1. Preview And Scope

- [ ] Run `python3 tools/pjario.py adopt --target <repo> --profile <core|frontend> --dry-run`.
- [ ] Review the reported files, CI choices, and removal path; the preview does not mutate the target.
- [ ] Decide whether the target needs core Pjario only or the Pevie Hischer frontend profile.
- [ ] Keep the initial adoption to one product or team path.

## 2. Install The Contract

- [ ] Copy `AGENTS.md`, `build-system/`, `tools/`, relevant tests, and Makefile targets through the target repo's normal review process.
- [ ] Copy `Pevie Hischer/` only when the frontend profile is needed.
- [ ] Ignore `.pjario/*`, then allowlist `.pjario/work/` and `.pjario/work/*.md`.
- [ ] Keep review packets, Quiet Aggregate ledgers, and other `.pjario/` runtime state private and untracked.
- [ ] Define where accepted technical-debt follow-ups live.

## 3. Exercise One Work Packet

- [ ] Create a packet with `python3 tools/pjario.py start --help`.
- [ ] Fill Scope and Non-Goals.
- [ ] For non-trivial work, fill Plan and map every active `RISK-xx` to a `PROOF-xx` requirement.
- [ ] For frontend work, set `Profile: frontend` and provide concrete Design Context.
- [ ] Run `python3 tools/pjario.py check --packet .pjario/work/WORK-ID.md`.
- [ ] Implement the change and attach real evidence to every proof ID.
- [ ] Run `python3 tools/pjario.py review --packet .pjario/work/WORK-ID.md --base <ref>`.
- [ ] Record the review decision, gaps, and next action, then run `python3 tools/pjario.py finish --packet .pjario/work/WORK-ID.md`.

## 4. Verify The Installation

- [ ] Run `make test`.
- [ ] Run `make validate-examples` if examples were copied.
- [ ] Run `make doctor MODE=adopted PROFILE=core`.
- [ ] Run the host application's own lint, typecheck, unit, integration, e2e, build, or platform checks.
- [ ] For frontend adoption, create `DESIGN.md` and run `make doctor MODE=adopted PROFILE=pevie` plus the Pevie checks.

## 5. Add CI Carefully

- [ ] Validate changed Work Packets and host-app checks in CI.
- [ ] Build a review packet as a sanity check for meaningful changes.
- [ ] Keep model invocation, credentials, privacy, and cost decisions in the host repository.
- [ ] Do not make Pjario's workflow checks a substitute for product, security, or release checks.

## 6. Learn Without Auto-Mutation

- [ ] Record only verified findings.
- [ ] Use Quiet Aggregate only when the same explicit failure class repeats across independent reviews.
- [ ] Review each proposed rule, test, lint, template, or tooling change before adoption.
- [ ] Never expose the private ledger or mutate policy automatically.

## 7. Preserve A Backout Path

- [ ] Read `docs/remove-from-target-repo.md`.
- [ ] Know which copied package files are owned by the host repo.
- [ ] Keep useful Work Packets if Pjario is removed.
- [ ] Confirm Pjario-specific CI can be removed without breaking host checks.

## Legacy Compatibility

Existing adopters may retain ticket, planning brief, QA plan, PR note, and completion report paths. Keep their current checks working, use one Work Packet for new work, and migrate active artifacts only when it reduces—not creates—ceremony.

## Done Criteria

Adoption is complete when one real Work Packet has passed check, review, finish, and the host application's own proof; the team knows where tracked work and private runtime state live; and removal is documented.
