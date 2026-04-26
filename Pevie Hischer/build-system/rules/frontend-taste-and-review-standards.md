# Frontend Taste And Review Standards

## What Good Looks Like

- Solves the ticket with minimal unrelated churn.
- Uses canonical components/tokens before introducing custom variants.
- Preserves visual hierarchy, spacing rhythm, and interaction consistency.
- Handles loading, empty, error, and success states coherently.
- Is understandable by the next engineer without archaeology.

## Taste Heuristics

- Prefer clarity over ornament.
- Prefer fewer strong choices over many weak options.
- Keep visual noise low; emphasize user intent and primary actions.
- Use copy that is direct, specific, and actionable.
- Keep default states calm; reserve high-emphasis styles for high-importance actions.

## Engineering Standards

- No one-off color/spacing/typography literals where tokens exist.
- No ad-hoc component forks when a shared component can be extended safely.
- Avoid deeply nested conditional rendering blocks; extract presentational units.
- Keep state ownership clear and local where possible.
- Make event/error telemetry actionable (include user/task context when safe).

## Review Feedback Triage

High-signal feedback is:

- tied to user or production risk
- specific to the changed diff
- fixable without guessing

Low-signal feedback is:

- personal style preference with no risk linkage
- broad rewrite suggestions without clear failure mode
