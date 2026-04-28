# How Pevie Hischer Operates

This is a frontend-focused build system for agentic delivery with real production constraints.

## Loop

1. **Ticket**: Define outcome, scope, acceptance criteria, complexity, and required proof.
2. **Design Context**: For user-facing UI work, read or create `DESIGN.md` before implementation planning.
3. **Planning Brief**: For non-trivial work, lock non-goals, design context, risk-to-proof mapping, and rollout plan.
4. **Implementation**: Agent ships the smallest durable patch.
5. **Local Proof**: Agent runs tests, lint, accessibility/perf checks, design checks, and manual smoke where needed.
6. **Review Agent**: Staff-level reviewer checks correctness, `DESIGN.md` alignment, UX quality, accessibility, performance, and operability.
7. **Human Steering**: Human accepts, redirects, or escalates.
8. **Garbage Collection**: Repeated findings become guardrails.

## Review Severity

- **P0**: Incident-level risk (security/privacy breach, destructive rollout, major outage).
- **P1**: Must block merge (broken requirement, accessibility regression, severe UX/perf regression).
- **P2**: Usually block (missing significant proof, missing/ignored `DESIGN.md`, brittle design-system use, observability gap).
- **P3**: Non-blocking polish (naming, copy tweaks, optional refactors).

Default block threshold is P2+.

## Frontend-Specific Merge Bias

Bias toward shipping meaningful improvements with:

- User-visible quality
- Stable design context before implementation
- Measurable performance/accessibility posture
- Clear rollback path for risky changes

Bias against:

- Perfection loops
- broad rewrites without concrete risk
- subjective style debates that are not grounded in `DESIGN.md`, user impact, or production impact
