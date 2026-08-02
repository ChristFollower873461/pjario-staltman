# Oh Shucksenburg: Technical Debt Control

Use this profile when a change risks adding shortcuts, duplicated logic, unstable abstractions, hidden coupling, stale TODOs, weak ownership, or future maintenance cost.

## When To Invoke

- A patch adds a workaround, adapter, migration bridge, or temporary compatibility layer.
- A patch touches shared code, architecture boundaries, build tooling, or long-lived templates.
- Review feedback repeats because the same class of mess keeps coming back.
- A fix is correct but leaves known cleanup behind.

## Rules

- Name debt explicitly in the Work Packet. Existing adopters may use the equivalent legacy artifact.
- Separate acceptable debt from accidental debt.
- If debt is accepted, state owner, trigger, and removal path.
- If debt is paid down, state the simplification and proof that behavior still holds.
- Do not add a new abstraction unless it removes real duplication, risk, or cognitive load.
- Do not hide debt in vague follow-ups like "clean up later."

## Proof

- Existing behavior still passes.
- The changed boundary is named.
- New coupling, duplication, or temporary code is documented.
- A follow-up exists only when the debt is intentionally accepted.
