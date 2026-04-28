# How We Build

This is the operating system for agentic engineering in this repo. It is based on a few constraints:

- Human time and attention are scarce.
- Code is cheap to produce, refactor, and delete.
- Context is scarce, so rules must appear when they matter.
- Review feedback should become durable guardrails.

## The Loop

1. **Ticket**: Define outcome, user impact, risk surfaces, acceptance criteria, expected proof, and implementation complexity (`trivial` or `non-trivial`).
2. **Planning Brief**: For non-trivial work, fill `build-system/templates/planning-brief.md` before coding. Lock approach, non-goals, risk-to-proof mapping, and rollout/rollback plan.
3. **Implementation**: An agent owns the patch end to end. It may plan privately, but it must optimize for a working, reviewed change.
4. **Local Proof**: The agent runs tests, linters, smoke checks, or manual QA and records what happened. For non-trivial work, evidence should map back to the active ticket risks.
5. **Review Agent**: A staff-engineer review agent checks the diff against repo rules, scale readiness, and the stated ticket.
6. **Human Steering**: A human accepts, redirects, or escalates. The human should spend attention on product judgment, architecture, and risk.
7. **Garbage Collection**: Repeated review feedback becomes a rule, test, lint, template, or tool.

## Review Severity

- **P0**: Must stop immediately. Security incident, data loss, production outage, cross-tenant leak, irreversible destructive action.
- **P1**: Must block merge. Correctness regression, auth/privacy failure, scale failure on a critical path, migration hazard, missing rollback for risky work.
- **P2**: Usually blocks merge. Missing important test, brittle design, operational blind spot, non-idempotent side effect, missing timeout, unclear ownership.
- **P3**: Should not block. Naming, taste, small refactors, polish, optional cleanup.

The default review bar is P2 and above. Do not bury the author in trivia.

## Rule Promotion

When a review comment appears twice, promote it:

- Documentation if humans and agents need to know a standard.
- Template change if the missing context should be collected before work begins.
- Test or lint if the failure can be detected mechanically.
- Runtime guardrail if the failure can hurt users in production.

## Agent Handoff Contract

Every implementation handoff should include:

- The ticket or task brief.
- For coordinated build work, `build-system/templates/build-request.md`.
- Relevant files, APIs, or user flows.
- Risk surfaces: data, authz, tenancy, async, external calls, LLMs, privacy, rollout.
- Required evidence: tests, screenshots, logs, migration proof, load test, runbook, or manual QA.
- Any explicit non-goals.
- The planning brief when the task is non-trivial.
- The completion report after implementation.

## Coordinator And Implementation Agent Build Contract

A coordinator should frame build intent, release constraints, and follow-up actions. The implementation agent should inspect the repo, make the patch, run the relevant checks, and return concrete evidence.

For build work, the handoff is incomplete unless it names the target surface, current failure or desired artifact, constraints such as signing or release track, and required proof. The handoff back is incomplete unless it names the commands run, result, artifact identity or path when produced, and any exact gap that remains.

## Merge Bias

Bias toward accepting useful code that meets the ticket and has credible proof. Bias against perfection loops, sprawling refactors, and review comments that cannot be tied to user risk, system risk, or maintainability.

## Optional Enforcement

Use `make check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md` to enforce that non-trivial tickets include a filled planning brief.

Use `make check-proof TICKET=path/to/ticket.md QA=path/to/qa-plan.md PR=path/to/pr-note.md COMPLETION=path/to/completion-report.md` to check that proof evidence covers the ticket's active risk surfaces.

Use `make kickoff-build REQUEST=path/to/build-request.md` when a coordinator starts from a build request instead of a ticket.
