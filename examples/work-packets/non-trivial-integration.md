# Pjario Work Packet

Schema: pjario.work/v1
ID: API-014
Title: Add a bounded inventory provider integration
Status: complete
Complexity: non-trivial
Profile: core
Design Context: Not applicable.

## Outcome

The inventory screen can read provider availability without hanging the request path when the provider is slow.

## Scope

- Add the provider adapter, timeout handling, response validation, and fallback state.

## Non-Goals

- No provider-side writes or retry queue.

## Risk Surfaces

- RISK-01 | inactive | data-writes | none
- RISK-02 | inactive | auth | none
- RISK-03 | inactive | multi-tenancy | none
- RISK-04 | active | external-calls | Provider reads need a bounded timeout and explicit degraded state.
- RISK-05 | inactive | async-work | none
- RISK-06 | inactive | llm-ai | none
- RISK-07 | inactive | privacy | none
- RISK-08 | inactive | billing-cost | none
- RISK-09 | inactive | maintainability | none
- RISK-10 | active | rollout-rollback | The adapter must be reversible without changing callers.

## Plan

Introduce one adapter behind the existing interface, validate provider responses, use a two-second timeout, and retain the local fallback. Roll out behind the existing provider flag; rollback disables the flag.

## Proof Requirements

- PROOF-01 | risks=RISK-04 | Contract tests cover a valid provider response.
- PROOF-02 | risks=RISK-04 | A timeout test proves the degraded state returns promptly.
- PROOF-03 | risks=RISK-10 | Flag-off verification proves rollback restores the local fallback.

## Evidence

- PROOF-01 | passed | Provider contract fixture and adapter unit tests passed.
- PROOF-02 | passed | Timeout fixture returned the degraded state within the configured boundary.
- PROOF-03 | passed | Flag-off smoke test used the unchanged local catalog.

## Review

Decision: PASS
Findings: none.

## Known Gaps

- None recorded.

## Next Action

- Merge and begin the internal-only rollout stage.

## Learning

- None recorded.
