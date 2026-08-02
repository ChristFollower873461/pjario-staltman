# How We Build

This is the operating system for agentic engineering in this repo. It is based on a few constraints:

- Human time and attention are scarce.
- Code is cheap to produce, refactor, and delete.
- Context is scarce, so rules must appear when they matter.
- Review feedback should become durable guardrails.

## The Loop

1. **Work Packet**: Keep outcome, scope, complexity, risks, plan, stable proof IDs, evidence, review, gaps, and next action in one tracked `pjario.work/v1` file. Trivial work leaves Plan unused; non-trivial work completes it before coding.
2. **Readiness Check**: Every active `RISK-xx` maps to at least one `PROOF-xx` requirement before implementation.
3. **Implementation**: An agent owns the scoped patch end to end.
4. **Local Proof**: Replace each pending evidence row with a real command, artifact, measurement, or observation. Do not satisfy proof by copying requirement prose.
5. **Review Agent**: A staff-engineer review agent checks the Work Packet and diff against repo rules and scale readiness.
6. **Human Steering**: A human accepts, redirects, or escalates. The human should spend attention on product judgment, architecture, and risk.
7. **Quiet Aggregate**: Record verified findings without interrupting the active task. When the same failure class appears across independent reviews, generate an auditable guardrail proposal.
8. **Garbage Collection**: A human or implementation agent reviews the proposal and turns it into a rule, test, lint, template, runtime guardrail, or tool.

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

Use `python3 tools/quiet-aggregate.py` when the repeated-review history needs to be durable. Quiet Aggregate never applies the promotion automatically; it records the evidence and proposes the smallest guardrail category for review.

## Agent Handoff Contract

Every implementation handoff should include:

- The active Work Packet, or the legacy ticket and planning artifacts for an existing adopter.
- For coordinated build work, `build-system/templates/build-request.md`.
- Relevant files, APIs, or user flows.
- Risk surfaces: data, authz, tenancy, async, external calls, LLMs, privacy, rollout.
- Required evidence: tests, screenshots, logs, migration proof, load test, runbook, or manual QA.
- Debt posture: debt introduced, paid down, or explicitly not applicable.
- Any explicit non-goals.
- A completed Plan section when the Work Packet is non-trivial.
- Terminal evidence for every proof ID and a concrete next action.

## Coordinator And Implementation Agent Build Contract

A coordinator should frame build intent, release constraints, and follow-up actions. The implementation agent should inspect the repo, make the patch, run the relevant checks, and return concrete evidence.

For build work, the handoff is incomplete unless it names the target surface, current failure or desired artifact, constraints such as signing or release track, and required proof. The handoff back is incomplete unless it names the commands run, result, artifact identity or path when produced, and any exact gap that remains.

## Merge Bias

Bias toward accepting useful code that meets the Work Packet outcome and has credible proof. Bias against perfection loops, sprawling refactors, and review comments that cannot be tied to user risk, system risk, or maintainability.

## Optional Enforcement

Preferred flow:

```bash
python3 tools/pjario.py start --help
python3 tools/pjario.py check --packet .pjario/work/WORK-ID.md
python3 tools/pjario.py review --packet .pjario/work/WORK-ID.md --base origin/main
python3 tools/pjario.py finish --packet .pjario/work/WORK-ID.md
```

The older ticket, planning brief, QA plan, PR note, and completion report commands remain supported for compatibility.

Use `make check-planning-brief TICKET=path/to/ticket.md PLAN=path/to/planning-brief.md` to enforce that non-trivial tickets include a filled planning brief.

Use `make check-proof TICKET=path/to/ticket.md QA=path/to/qa-plan.md PR=path/to/pr-note.md COMPLETION=path/to/completion-report.md` to check that proof evidence covers the ticket's active risk surfaces.

Use `make kickoff-build REQUEST=path/to/build-request.md` when a coordinator starts from a build request instead of a ticket.

Use `build-system/rules/oh-shucksenburg-technical-debt.md` when a change risks accepted debt, coupling, duplication, unclear ownership, or future maintenance cost.
