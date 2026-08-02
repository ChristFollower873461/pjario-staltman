# Review Standards

These are the durable expectations for agent-produced code.

## What Good Looks Like

- The change solves the ticket without unrelated churn.
- The implementation follows nearby patterns unless the ticket explicitly calls for a new one.
- Public interfaces are hard to misuse.
- Errors are explicit, actionable, and observable.
- Tests cover the main path and at least one important failure path.
- QA evidence is written down in the PR note.
- Risky behavior is reversible through rollback, feature flag, or configuration.

## Agent-Friendly Codebase Rules

- Keep files small enough to fit in context. Prefer extracting cohesive helpers over adding another long mixed-purpose file.
- Keep related code close together when it changes together.
- Prefer one canonical utility over local clones.
- Make package boundaries and dependency direction obvious.
- Write error messages that tell the next agent how to fix the failure.
- Make recurring standards mechanically checkable when reasonable.

## Review Feedback Triage

Good review feedback is:

- Specific to the diff.
- Connected to a user, production, security, data, or maintainability risk.
- Fixable without guessing.
- Promotable into a durable rule if it repeats.

Poor review feedback is:

- Style-only without local convention.
- A broad rewrite request without a concrete failure mode.
- A preference framed as a blocker.
- A future project disguised as review.

## Garbage Collection Day

Once a week, collect the friction:

- What comments did reviewers repeat?
- What did agents keep getting wrong?
- What manual checks consumed human attention?
- Which tests were flaky, slow, or missing?
- Which docs were missing when the agent needed context?

Then add exactly one durable improvement per recurring failure class.

Use Quiet Aggregate when the recurrence claim needs evidence across reviews. Only verified `actionable` records count, two findings from one review remain one source, and generated proposals must be reviewed before policy changes.
