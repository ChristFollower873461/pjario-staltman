# Proof Matrix

Use this matrix to choose the minimum proof expected before an implementation agent reports done.

| Work type | Required proof | Good follow-up proof |
| --- | --- | --- |
| Trivial docs or copy | Targeted diff review; affected markdown renders or links are sane | Spellcheck or link check when available |
| Core logic | Unit tests for happy path and one meaningful failure path | Property, fixture, or regression test for the bug class |
| Refactor | Existing tests still pass; before/after behavior is named | Small characterization test before risky rewrites |
| API or data contract | Contract/schema test; compatibility note | Consumer fixture or generated client check |
| Migration or persistence | Forward path, rollback path, and data-loss risk statement | Dry run, backup proof, or idempotency check |
| Auth, permissions, or privacy | Negative access test; least-privilege proof | Audit/event evidence for denied and allowed paths |
| External integration | Timeout/error handling test; mock or sandbox proof | Retries/backoff and rate-limit behavior evidence |
| Release/build/package | Build artifact identity, version, and command transcript | Install/run smoke test in a clean environment |
| UI-visible frontend | Screenshot or viewport proof; accessibility check; `DESIGN.md` alignment | Cross-browser/mobile evidence and interaction trace |
| Performance-sensitive change | Baseline and after measurement for the affected path | Budget threshold in CI or monitoring |
| Observability change | Event/log/span names and a local or staging proof sample | Dashboard or alert link once deployed |
| Agent workflow/tooling | Unit tests plus a real command invocation | Golden fixture covering a failure case |

If the work does not fit a row, state the risk explicitly and choose the closest proof shape. Missing proof is acceptable only when the completion report names the gap and the coordinator accepts it.
