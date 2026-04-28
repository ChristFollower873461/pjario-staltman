# Research Notes: Taste + Scalable Frontend Production

This package is grounded in these external references and operating principles.

## Core References

- [web.dev metrics overview](https://web.dev/explore/metrics)
  - Prioritize user-centric metrics and track LCP, INP, CLS, TTFB, FCP, TBT.
- [MDN web performance best practices](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/Best_practices)
  - Keep JS payload lean, use CDN/compression, apply lazy loading thoughtfully, define performance budgets.
- [W3C WCAG 2 overview](https://www.w3.org/WAI/standards-guidelines/wcag/)
  - Align accessibility expectations with WCAG 2.2 AA-level success criteria posture.
- [Playwright best practices](https://playwright.dev/docs/best-practices)
  - Test user-visible behavior, isolate tests, prefer resilient locators, run in CI.
- [GitHub Primer foundations](https://primer.style/design/foundations)
  - Treat accessibility and design primitives/tokens as shared system foundations.
- [Shopify Polaris overview](https://polaris.shopify.com/)
  - Keep design-system consistency central to scaled product quality.
- [Sentry frontend monitoring](https://sentry.io/for/frontend/)
  - Capture frontend errors/traces with release context to reduce production blind spots.
- [Google Stitch: DESIGN.md](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/)
  - Treat agent-readable design rules as portable context across design and coding tools.
- [google-labs-code/design.md](https://github.com/google-labs-code/design.md)
  - Use `DESIGN.md` as a structured visual identity contract with machine-readable tokens and human-readable rationale.

## Synthesis For Pevie Hischer

High-taste frontend teams at scale typically do all of the following:

1. Standardize visual and interaction patterns with a design system and tokens.
2. Put `DESIGN.md` at the start of UI work so agents inherit product taste before implementation.
3. Treat accessibility as a product quality gate, not post-hoc cleanup.
4. Manage performance with explicit budgets and regression checks.
5. Require failure-state UX (loading/empty/error/retry) for core flows.
6. Wire observability to frontend releases so regressions are diagnosable.
7. Keep review quality focused on risk and user impact, not cosmetic preference.

This package encodes those ideas into rules, templates, and agent prompts.
