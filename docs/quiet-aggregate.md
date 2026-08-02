# Quiet Aggregate

Quiet Aggregate is Pjario Staltman's recovered review-learning loop. It quietly records **verified** review findings, groups the same failure class across independent reviews, and produces an auditable guardrail proposal after the finding repeats.

It does not silently edit `AGENTS.md`, rules, templates, tests, or runtime policy. Promotion remains a deliberate human or implementation-agent action.

## What Was Recovered

Two related artifacts survived:

1. An early structured `codex-review` skill, later renamed `autoreview`, that reviews a local diff and emits validated JSON findings.
2. The Quiet Aggregate v2 operating rules: keep the original goal fixed, work one target per loop, checkpoint state and next action, measure launch readiness, stop stalled work, and provide before/after evidence.

The maintained descendant now lives in OpenClaw's `autoreview` skill. Pjario does not vendor that large engine. Quiet Aggregate consumes its stable JSON finding shape and keeps Pjario's aggregation and policy-promotion logic local, deterministic, and standard-library-only.

Tested upstream reference:

- Repository: `openclaw/openclaw`
- Commit: `55816c47d133d00bf0b6306881589975505338a9`
- Finding fields: `title`, `body`, `priority`, `confidence`, `category`, and `code_location`
- Local audit: 271 upstream autoreview hardening tests passed, with 3 environment-specific skips

That commit is a tested compatibility reference, not a runtime dependency. Core Pjario never downloads or invokes it automatically.

## Safety Contract

- Review findings are advisory until a human or main agent verifies them.
- Only records marked `actionable` participate in aggregation.
- Promotion requires the same failure class across at least two independent source references by default.
- Repeated findings from one review do not count as independent confirmation.
- Finding class and owner boundary are explicit inputs; Quiet Aggregate does not use fuzzy or model-based grouping.
- The ledger rejects local absolute paths, common credential shapes, malformed records, duplicate IDs, traversal outside the repository, and symlinked ledgers.
- Autoreview input is capped at 2 MB; ledgers are capped at 10 MB and 10,000 records; output paths cannot replace the ledger or write inside `.git`.
- The default ledger is `.pjario/quiet-aggregate.jsonl`, which is ignored because review metadata may be sensitive.
- A proposal is evidence, not an applied policy change.

## End-To-End Use

First, run a maintained autoreview helper and request structured output. The exact install path is intentionally external to Pjario:

```bash
"$AUTOREVIEW" --mode branch --base origin/main --max-priority P2 \
  --json-output .pjario/autoreview.json
```

Pjario's normal review bar is P2 and above, so the example widens the maintained helper's stricter P0-only default explicitly. Autoreview returns a non-zero status when it finds an actionable issue. Inspect the real code path and decide whether each finding is valid before recording it.

## Revival Scope

In scope: a local verified-finding ledger, deterministic recurrence detection, explicit rejected/follow-up audit records, a tested structured-autoreview adapter, exported-skill support, and guardrail proposals.

Out of scope: bundling a 20,000-line external review engine, choosing or invoking a model, GitHub review automation, fuzzy clustering, background telemetry, and automatic policy mutation.

Rollout is opt-in per repository. Roll back by removing the Quiet Aggregate tool/docs/export references and preserving or discarding the ignored `.pjario/` ledger according to the host repository's review-retention needs. No migration or production service is involved.

Record one verified finding:

```bash
python3 tools/quiet-aggregate.py record \
  --from-autoreview .pjario/autoreview.json \
  --finding-index 0 \
  --source-ref pr-42/cycle-1 \
  --reviewer codex \
  --disposition actionable \
  --failure-class missing-rollback-proof \
  --owner-boundary release-proof \
  --durable-fix template
```

Use the same stable `failure-class` and `owner-boundary` labels when the same underlying gap appears again. A deterministic fingerprint is derived from those two labels.

Inspect the aggregate:

```bash
python3 tools/quiet-aggregate.py report
python3 tools/quiet-aggregate.py report --format json --output .pjario/quiet-report.json
```

Once a class is ready, generate a proposal:

```bash
python3 tools/quiet-aggregate.py propose \
  --fingerprint qac-0123456789abcdef \
  --decision template \
  --owner release-coordinator \
  --output docs/guardrail-proposal.md
```

Review the proposal, implement the smallest durable fix, run the relevant proof, and reference the fingerprint in the resulting rule, test, template, lint, tooling, or runtime guardrail change.

## Manual Findings

Quiet Aggregate can also record findings from human review, CI, or another source:

```bash
python3 tools/quiet-aggregate.py record \
  --title "Missing timeout on external call" \
  --summary "The new client relies on the library default timeout." \
  --priority P2 \
  --confidence 1 \
  --category bug \
  --file-path src/client.py \
  --line 44 \
  --source-kind human-review \
  --source-ref pr-51/staff-review \
  --failure-class missing-external-timeout \
  --owner-boundary external-clients \
  --durable-fix lint
```

Use `--disposition rejected` to retain an audited rejection or `--disposition follow-up` for a real issue outside the current change. Neither contributes to promotion counts.

## Repairing A Classification

The source reference, finding title, and code location form the stable observation identity. Recording the same observation twice is an idempotent no-op. If its verification decision changes, rerun `record` with the corrected classification and `--replace`.

## Limits

Quiet Aggregate does not prove that a reviewer finding is correct, infer semantic equivalence between differently classified findings, call an LLM, submit code to a model provider, or apply generated policy. Those boundaries are intentional.
