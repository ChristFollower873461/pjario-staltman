# Garbage Collection

Use this weekly or after a painful review.

## Repeated Friction

- Core implementation handoffs sometimes name tests but do not prove active risks like LLM/AI prompt context, privacy scan coverage, or rollback path.

## Failure Class

What kind of problem is this?

- Missing context: Yes.
- Missing test: Yes.
- Missing lint/source check: No.
- Missing template field: Yes.
- Missing runtime guardrail: No.
- Slow/flaky workflow: No.

## Root Cause

The base package had templates and a proof matrix, but no complete golden flow or command that checked whether evidence mentioned active ticket risks.

## Durable Fix

Choose one:

- Rule: Use `build-system/rules/proof-matrix.md`.
- Template: Fill `build-system/templates/completion-report.md`.
- Test: Cover `tools/check-proof.py`.
- Lint/source check: Run `make check-proof` on non-trivial handoffs.
- Runtime guardrail: Not applicable.
- Tooling: Use `make kickoff-build` and `make public-ready`.

## Acceptance Criteria

- `make validate-examples` validates this golden workflow.
- Missing proof for an active ticket risk fails in tests.

## Owner

- Coordinator
