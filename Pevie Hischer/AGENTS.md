# Agent Operating Rules

Humans steer. Agents execute. The goal is maintainable frontend software with quality that is visible to users and verifiable in production.

Before changing code:

- Read the ticket and restate the outcome in working notes.
- Read `build-system/README.md`.
- Read relevant rules in `build-system/rules/`.
- Keep the patch scoped to the requested outcome.

While working:

- Prefer existing UI patterns and design-system components before creating new ones.
- Treat accessibility, performance, and error handling as product requirements.
- Add checks and tests proportional to risk.
- Leave useful breadcrumbs in PR notes for the next agent or reviewer.

Before completion:

- Run relevant checks and record exact commands.
- Provide a short QA note with result and any gaps.
- If you could not run a check, state why and what unblocks it.

Review stance:

- Block on correctness, accessibility regressions, user-facing performance regressions, security/privacy, and missing proof on risky changes.
- Do not block on taste-only comments when local conventions are coherent.
- Convert repeated review comments into durable rules, tests, or tooling.
