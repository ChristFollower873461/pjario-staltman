# Oh Shucksenburg: Frontend Debt Control

Use this Pevie profile when UI work risks visual drift, duplicate components, one-off styling, brittle state, unowned tokens, inaccessible shortcuts, or deferred cleanup.

## Blockers

- New one-off component when a canonical component exists.
- Token bypass without a documented reason.
- UI state added without loading, empty, error, disabled, and retry behavior where relevant.
- Accessibility debt introduced without owner and removal trigger.
- Performance debt accepted without budget or measurement plan.

## Acceptable Debt

Debt can be accepted only when the PR note names:

- the reason it is necessary now
- the component or surface that owns it
- the trigger for removal
- the proof that users are not exposed to broken behavior

## Proof

- `DESIGN.md` alignment is stated.
- Component/token reuse is stated.
- A11y/performance impact is tested or explicitly not applicable.
- Accepted debt has an owner and removal trigger.
