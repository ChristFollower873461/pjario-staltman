# Planning Brief

Use for non-trivial work before implementation.

## Ticket Restatement

Ship an account health status panel that is visually consistent with `DESIGN.md`, handles all important UI states, and has enough proof for frontend review.

## Scope And Non-Goals

In:

- One reusable status-panel pattern.
- Loading, empty, error, and healthy states.
- Design, accessibility, and state-proof notes.

Out:

- Dashboard-wide redesign.
- New backend scoring logic.
- New telemetry vendor integration.

## Approach

- Read `DESIGN.md` before coding.
- Use existing dashboard/card/button primitives if present.
- Add the smallest component or view change needed for the panel.
- Keep state handling explicit and visible.

## Design Context

- DESIGN.md path: `Pevie Hischer/examples/golden-workflow/DESIGN.md`.
- Relevant brand/tone constraints: Quiet operational UI, dense but readable, no marketing-style dashboard cards.
- Existing components/tokens to use: page, card, button-primary, status-muted, status-success, status-warning, status-danger.
- Explicit forbidden patterns: Purple-blue gradients, oversized hero treatment, hidden recovery actions.
- Reference screenshots/links, if any: Use before/after screenshots from the target dashboard.

## Dependencies And Unknowns

Dependencies:

- Existing dashboard shell.
- Account-health API or mock state data.

Unknowns:

- Whether the host app already has a canonical status panel component.

## Risk-To-Proof Mapping

- Design coherence -> Run DESIGN.md validation and compare implementation screenshots to the design contract.
- Accessibility -> Keyboard through panel actions and verify state labels are announced or readable.
- Performance -> Confirm no dashboard shell layout shift or blocking load.
- Data/API correctness -> Verify each API state maps to the correct UI state.
- External dependency reliability -> Force timeout/error response and confirm visible recovery.
- Privacy/PII -> Confirm logs do not include customer account values.
- Rollout/rollback -> Use existing dashboard flag or revert the component patch.

## QA Strategy

Automated:

- Relevant app test command.
- `make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md`

Manual:

- Capture or inspect loading, empty, error, and healthy states.
- Compare spacing, tone, colors, and component states against `DESIGN.md`.

Failure-path:

- Force API error and timeout.
- Confirm retry or recovery action remains usable by keyboard.

## Rollout And Rollback

- Feature flag: Use existing dashboard flag if available.
- Rollout stages: Internal review, limited operator cohort, full dashboard release.
- Rollback trigger: Incorrect health status, accessibility regression, or visible layout instability.
- Rollback steps: Disable flag or revert the panel component commit.

## Ready-To-Implement Gate

- [ ] Scope and non-goals are explicit.
- [ ] Design context is identified or explicitly not applicable.
- [ ] Key risks are mapped to proof.
- [ ] QA plan is concrete.
- [ ] Rollout/rollback is realistic.
- [ ] Unknowns are resolved or intentionally tracked.
