# Pjario Work Packet

Schema: pjario.work/v1
ID: PJARIO-030
Title: Replace artifact ceremony with one executable Work Packet flow
Status: complete
Complexity: non-trivial
Profile: core
Design Context: Not applicable.

## Outcome

Pjario gives an agent one concise, executable path from scoped intent through auditable proof and review without breaking existing adopters.

## Scope

- Add the versioned Work Packet contract and unified standard-library CLI.
- Validate stable risk-to-proof mappings, terminal evidence, review state, paths, secrets, and private runtime boundaries.
- Include the Work Packet and tracked diff in review context.
- Trim and validate the exported Agent Skill while preserving the legacy artifact flow.
- Add deterministic examples, behavioral fixtures, tests, and public documentation.

## Non-Goals

- No hosted dashboard, automatic model reviewer, automatic policy mutation, or forced migration of legacy work.
- No runtime dependency or target-repository mutation during adoption preview.

## Risk Surfaces

- RISK-01 | inactive | data-writes | none
- RISK-02 | inactive | auth | none
- RISK-03 | inactive | multi-tenancy | none
- RISK-04 | inactive | external-calls | none
- RISK-05 | inactive | async-work | none
- RISK-06 | inactive | llm-ai | none
- RISK-07 | active | privacy | Work records and exported summaries must reject credentials and local host paths while private runtime state remains untracked.
- RISK-08 | inactive | billing-cost | none
- RISK-09 | active | maintainability | The new CLI must own one deterministic contract without duplicating decision logic or breaking legacy commands.
- RISK-10 | active | rollout-rollback | Existing adopters must retain a working compatibility path and be able to remove the package without losing useful work history.

## Plan

Define `pjario.work/v1`, build one parser and validator behind start/check/review/finish, route learning through the existing Quiet Aggregate helper, and keep adoption dry-run-only. Export the same executable helpers with a smaller skill prompt. Preserve old commands, add golden packets and behavioral fixtures, then run package, privacy, export, and public-release proof before protected publication. Rollback is a branch revert; legacy commands remain independently usable throughout.

## Proof Requirements

- PROOF-01 | risks=none | Run the complete public release gate across both profiles and examples.
- PROOF-02 | risks=RISK-07 | Prove credentials, local paths, traversal, symlinks, and tracked private runtime state fail closed.
- PROOF-03 | risks=RISK-09 | Prove stable IDs, lifecycle states, exported command execution, bundled helper integrity, and legacy proof compatibility.
- PROOF-04 | risks=RISK-10 | Validate legacy golden workflows, dry-run adoption, removal guidance, and reversible rollout documentation.
- PROOF-05 | risks=RISK-09 | Validate the exported Agent Skill metadata, structure, executable helpers, and context budgets.

## Evidence

- PROOF-01 | passed | `make public-ready` passed 63 core and 19 Pevie tests, both example suites, doctor, review packet generation, and three pinned design lints.
- PROOF-02 | passed | Focused path, secret, output confinement, runtime tracking, and Quiet Aggregate privacy tests passed; `make doctor` reported 13 passes, zero warnings, and zero failures.
- PROOF-03 | passed | Unit and integration tests covered risk/proof mapping, finish rejection, mandatory Work Packet review context, bundled-helper precedence, exported CLI execution, and the legacy `check-proof` flow.
- PROOF-04 | passed | Both legacy golden workflows passed, `pjario adopt --dry-run` made no target changes, and adoption/removal docs preserve tracked Work Packets and legacy compatibility.
- PROOF-05 | passed | Standard export measured 200 `SKILL.md` words and 682 Markdown words total; caveman export measured 89/89; the official Agent Skills validator returned `Skill is valid!` and generated metadata matched exactly.

## Review

Decision: PASS
Findings: none. The final review packet contained the complete Work Packet, repository rules, tracked diff, and untracked source files without truncation; no P2-or-higher issue remained after the helper-integrity, adoption-inventory, privacy, and lifecycle hardening pass.

## Known Gaps

- None recorded.

## Next Action

- Publish the reviewed change through the protected GitHub workflow and verify the default branch.

## Learning

- The durable simplification is one stateful contract with progressive depth, not more instructions around the old artifact set.
