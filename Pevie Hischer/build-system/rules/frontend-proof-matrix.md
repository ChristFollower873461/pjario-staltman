# Frontend Proof Matrix

Use this matrix for Pevie Hischer work before reporting a frontend change as done.

| Work type | Required proof | Good follow-up proof |
| --- | --- | --- |
| Static visual change | Screenshot or rendered viewport proof; `DESIGN.md` token alignment | Before/after screenshot comparison |
| Responsive layout | Desktop and mobile viewport proof | Tablet or constrained-width proof for dense views |
| Interactive state | Happy path interaction proof plus disabled/loading/error state review | Keyboard-only interaction trace |
| Form or data entry | Validation, error, success, and retry proof | Screen reader labels or accessibility tree evidence |
| Navigation change | Route/back/refresh behavior proof | Deep-link and empty-state proof |
| Design-system component | Token usage, variants, accessibility labels, and docs/example update | Storybook or isolated component proof when available |
| Performance-sensitive surface | Bundle/runtime or Core Web Vitals-relevant measurement for the touched path | CI budget or production monitoring hook |
| Frontend observability | Error/event/span names and local/staging emission proof | Release-linked dashboard or alert check |
| Visual asset work | Asset loads, aspect ratios hold, and no layout shift | Slow-network or cache-miss proof |
| Frontend debt or maintainability | Debt introduced/paid-down note; component, token, state, and ownership impact stated | Story/component cleanup plan or follow-up issue for accepted debt |

For non-trivial UI work, `DESIGN.md` is proof context, not optional reference material. If a patch intentionally violates it, the planning brief or PR note must say why.
