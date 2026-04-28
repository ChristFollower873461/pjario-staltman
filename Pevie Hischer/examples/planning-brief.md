# Planning Brief

Use for non-trivial work before implementation.

## Ticket Restatement

Frontend planning briefs must contain real implementation, risk, QA, and rollout content before a non-trivial UI change begins.

## Scope And Non-Goals

In:

- Reject empty required sections.
- Require the ready-to-implement gate from the template.
- Add regression tests for both failure modes.

Out:

- No stack-specific lint rules.
- No change to the frontend review severity model.

## Approach

- Parse each required section body.
- Treat placeholder-only sections as empty.
- Fail when the ready gate has drifted from the template.

## Design Context

- DESIGN.md path: `Pevie Hischer/examples/DESIGN.md`.
- Relevant brand/tone constraints: Quiet operational UI, precise hierarchy, no generic decoration.
- Existing components/tokens to use: Declared colors, typography, spacing, radii, button, and card tokens.
- Explicit forbidden patterns: Purple-blue gradients, novelty accents, one-off card styles.
- Reference screenshots/links, if any: Not applicable for this package example.

## Dependencies And Unknowns

Dependencies:

- Existing Pevie checker and unit test layout.

Unknowns:

- None.

## Risk-To-Proof Mapping

- Design coherence -> Validate `DESIGN.md` and require planning briefs to identify design context.
- Accessibility -> Require planning briefs to name accessibility proof for changed user flows.
- Performance -> Require planning briefs to name performance evidence for user-facing changes.
- Data/API correctness -> Require API-state proof where UI state depends on server behavior.
- External dependency reliability -> Require fallback or degraded-state proof where relevant.
- Privacy/PII -> Require safe logging and redaction notes where user data is touched.
- Rollout/rollback -> Require concrete flag, staged rollout, or revert path for risky UI changes.

## QA Strategy

Automated:

- `make -f "Pevie Hischer/Makefile" test`
- `make -f "Pevie Hischer/Makefile" validate-examples`

Manual:

- Read the generated validation error for an empty section and confirm it names the bad section.

Failure-path:

- Empty required section fails.
- Missing ready-gate item fails.

## Rollout And Rollback

- Feature flag: Not needed.
- Rollout stages: Package tooling change only.
- Rollback trigger: Valid planning briefs are incorrectly rejected.
- Rollback steps: Revert the checker commit.

## Ready-To-Implement Gate

- [ ] Scope and non-goals are explicit.
- [ ] Design context is identified or explicitly not applicable.
- [ ] Key risks are mapped to proof.
- [ ] QA plan is concrete.
- [ ] Rollout/rollback is realistic.
- [ ] Unknowns are resolved or intentionally tracked.
