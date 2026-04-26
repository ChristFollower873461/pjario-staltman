# Frontend Production Readiness

Production-bound frontend changes should satisfy these defaults unless explicitly exempted in PR notes.

## Accessibility

- Follow WCAG 2.2 AA expectations for touched flows.
- Preserve keyboard navigation and visible focus.
- Ensure semantic labels for inputs, controls, and landmarks.
- Validate contrast for changed components/states.

## Performance

- Track and guard Core Web Vitals impact (LCP, INP, CLS).
- Keep JS payload growth intentional; justify significant bundle increases.
- Lazy-load non-critical routes/components where appropriate.
- Avoid layout shift from late-loading content when possible.

## Resilience

- Show explicit UI for loading, empty, and error states.
- Time out critical external calls and provide user-safe fallback behavior.
- Avoid hard failures from optional third-party integrations.

## Observability

- Report frontend errors with enough context to reproduce.
- Include release/version context in telemetry where possible.
- Capture key user journey failures for changed paths.

## Release Safety

- Risky UX changes should have a feature flag or rollback plan.
- For major interaction changes, roll out gradually when feasible.
- Document known limitations and follow-ups explicitly.
