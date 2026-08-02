# Agent Operating Rules

Humans steer. Agents execute. The goal is merged, maintainable software with clear evidence that it works.

Before changing code:

- Read the ticket or task brief and restate the outcome in your own working notes.
- Read `build-system/README.md`.
- Read the relevant rules in `build-system/rules/`.
- Keep the change scoped to the stated outcome.

While working:

- Prefer the repo's existing patterns over new abstractions.
- Make the smallest durable change that solves the real problem.
- Add tests or verification proportional to the risk of the change.
- Treat slow work, network calls, authz, tenant isolation, PII, data writes, migrations, and LLM calls as scale-readiness surfaces.
- Leave useful breadcrumbs when the next agent or human would otherwise need to rediscover context.

Before proposing completion:

- Run the relevant checks.
- Produce a short QA note with commands, results, and any gaps.
- If a check cannot be run, say exactly why.
- Do not hide uncertainty. Turn it into a follow-up, a test, a comment, or a review finding.

Review stance:

- Block on correctness, security, privacy, data loss, scale, operability, or missing proof for risky work.
- Do not block on taste when the code is coherent and local conventions support it.
- Convert repeated review feedback into durable rules, tests, lints, templates, or docs.
- Use Quiet Aggregate when review history matters: record only verified findings, require repetition across independent reviews, and review a proposal before changing policy.
