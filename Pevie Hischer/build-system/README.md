# How Pevie Hischer Operates

This is a frontend-focused build system for agentic delivery with real production constraints.

## Loop

1. **Ticket**: Define outcome, scope, acceptance criteria, complexity, and required proof.
2. **Planning Brief**: For non-trivial work, lock non-goals, risk-to-proof mapping, and rollout plan.
3. **Implementation**: Agent ships the smallest durable patch.
4. **Local Proof**: Agent runs tests, lint, accessibility/perf checks, and manual smoke where needed.
5. **Review Agent**: Staff-level reviewer checks correctness, UX quality, accessibility, performance, and operability.
6. **Human Steering**: Human accepts, redirects, or escalates.
7. **Garbage Collection**: Repeated findings become guardrails.

## Review Severity

- **P0**: Incident-level risk (security/privacy breach, destructive rollout, major outage).
- **P1**: Must block merge (broken requirement, accessibility regression, severe UX/perf regression).
- **P2**: Usually block (missing significant proof, brittle design-system use, observability gap).
- **P3**: Non-blocking polish (naming, copy tweaks, optional refactors).

Default block threshold is P2+.

## Frontend-Specific Merge Bias

Bias toward shipping meaningful improvements with:

- User-visible quality
- Measurable performance/accessibility posture
- Clear rollback path for risky changes

Bias against:

- Perfection loops
- broad rewrites without concrete risk
- subjective style debates without user or production impact
