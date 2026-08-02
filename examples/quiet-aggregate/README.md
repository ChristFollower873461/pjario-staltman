# Quiet Aggregate Example

The bundled `autoreview-report.json` matches the structured finding contract tested against the maintained OpenClaw autoreview helper.

Record it twice with distinct source references to exercise the repetition gate:

```bash
python3 tools/quiet-aggregate.py record \
  --from-autoreview examples/quiet-aggregate/autoreview-report.json \
  --source-ref example-pr-1/cycle-1 \
  --observed-at 2026-07-01T12:00:00Z \
  --failure-class missing-rollback-proof \
  --owner-boundary release-proof \
  --durable-fix template

python3 tools/quiet-aggregate.py record \
  --from-autoreview examples/quiet-aggregate/autoreview-report.json \
  --source-ref example-pr-2/cycle-1 \
  --observed-at 2026-07-02T12:00:00Z \
  --failure-class missing-rollback-proof \
  --owner-boundary release-proof \
  --durable-fix template

python3 tools/quiet-aggregate.py report
```

The example writes to the ignored `.pjario/quiet-aggregate.jsonl` ledger. It never edits a rule or template automatically.
