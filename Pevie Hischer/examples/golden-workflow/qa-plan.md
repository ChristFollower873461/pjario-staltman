# QA Plan

## Critical User Journeys

- Operator opens dashboard and scans account health.
- Operator sees loading state without layout jump.
- Operator sees empty state when no accounts need attention.
- Operator sees error state and uses recovery action.

## Automated Checks

- Relevant app unit or component tests.
- Relevant accessibility check if available.
- `make -f "Pevie Hischer/Makefile" check-design-context DESIGN=DESIGN.md`

## Manual Checks

- Loading state.
- Empty state.
- Error/retry state.
- Healthy state.
- Responsive check at narrow and desktop widths.

## Design Checks

- `DESIGN.md` reviewed: yes.
- Brand/tone alignment: quiet operational UI, no marketing treatment.
- Token/component alignment: status colors and card/button rules follow `DESIGN.md`.
- Forbidden-pattern check: no gradients, no oversized hero cards, no hidden recovery.
- Screenshot/reference comparison: attach before/after panel screenshots.

## Accessibility Checks

- Keyboard navigation: tab reaches recovery action.
- Focus visibility: visible on all interactive controls.
- Screen reader labels/announcements: state text is readable and action labels are explicit.
- Contrast verification: status text and actions meet AA contrast.

## Performance Checks

- Core Web Vitals notes: no expected LCP/INP/CLS regression.
- Bundle/runtime regression notes: no new heavy dependency.

## Failure Cases

- API error.
- API timeout.
- No accounts returned.

## Not Tested

- Production telemetry routing, unless host app already exposes local verification.
