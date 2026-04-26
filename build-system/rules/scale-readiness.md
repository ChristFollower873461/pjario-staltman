# Scale Readiness Rules

Production-bound code follows these rules. A deviation needs an explicit code comment or PR note explaining why.

## Principles

- Stateless app servers. State goes external.
- Async anything slow. Never block on email, HTTP, or IO in request handlers.
- Externalize state, secrets, storage, and logs. Nothing important lives on app server disk.
- Fail loud, recover gracefully, and ship observability with the feature.

## Data

- Index every foreign-key column.
- Explain all joins. No sequential scans on foreign-key joins.
- Use `DATABASE_URL` for writes and `DATABASE_REPLICA_URL` for reads when replicas exist.
- Wrap multi-step writes in transactions.
- Parameterize all SQL. No string concatenation.
- Run migrations as a gated CI step. Never auto-run migrations on app boot.
- Restore-test backups. Untested backups do not count.
- Keep schema changes backward-compatible across rolling deploys: add, use, then drop.
- Store UTC. Convert at the API or UI boundary.

## App Server

- Do not store session data in process memory. Use Redis, a database, or signed cookies.
- Stream uploads to object storage. Never rely on local disk.
- Soak test for memory leaks. RSS should stay flat under sustained load.
- Handle `SIGTERM`: stop accepting work, drain in-flight requests, and exit cleanly.
- `/health` must check the database and critical dependencies, and return non-200 when they are down.

## Async And Background Work

- Have a queue system from day one: BullMQ, SQS, Celery, Sidekiq, or equivalent.
- Do not call email, SMS, notification, or slow external services synchronously in request handlers. Enqueue.
- Queue image processing, PDFs, exports, and outbound webhooks.
- Make jobs idempotent. Assume at-least-once delivery.

## External Calls

- Set connect and read timeouts on every outbound HTTP call. Do not rely on defaults.
- Add a circuit breaker or fallback for critical third parties.
- Keep secrets in a secret manager. Never inline them or print them in CI logs.

## Network

- Use a CDN for static assets. App servers should not serve images, CSS, or JS in production.
- Enable gzip or Brotli on JSON responses over 1 KB.
- Rate limit every public endpoint per IP and per user or tenant.
- Put WebSockets on a stateful service or a pub/sub backplane.

## Observability

- Send logs to a centralized service. Application code writes structured logs to stdout; the platform ships them.
- Wire error alerting and test it with a fake error before launch.
- Use structured JSON logs with correlation or request IDs propagated through async work.
- Load test before launch. Know the QPS where p95 latency degrades.

## Ops

- Include a `RUNBOOK.md` per project with deploy, rollback, log access, and incident steps.
- Rollback should take less than 2 minutes and require no rebuild.

## Auth

- Authorize at the query layer, not only at the route.
- Protected queries must constrain by the authorized subject, such as `WHERE user_id = ?`.
- Access tokens should expire in 15 to 60 minutes.
- Refresh tokens must be server-side and revocable.
- Default-deny. Public routes are an explicit allowlist.

## Multi-Tenancy

- Add `tenant_id NOT NULL` and an index to every tenant-scoped table.
- Enforce tenant filters at the query layer.
- Add a cross-tenant fetch test that returns 404.
- Key rate limits per tenant, not only per IP.

## Idempotency

- Honor `Idempotency-Key` on payment, booking, and side-effect endpoints.
- Dedupe inbound webhooks by event ID.
- Make webhook handlers tolerate replay.

## Cost And Resource Limits

- Add spending caps and budget alerts for every cloud and AI provider account.
- Add per-user or per-tenant quotas on expensive operations such as LLM calls, image generation, and exports.
- Add hard limits on upload size, request body size, pagination, and search result count.

## LLM And AI

- Delimit user input in prompts. Assume prompt injection.
- Validate LLM output against a schema such as Zod or Pydantic.
- Retry invalid LLM output when safe. Do not crash on invalid output.
- Log `input_tokens`, `output_tokens`, `cost_estimate`, `user_id`, `tenant_id`, and `model` per call.
- Provide a fallback model or degraded mode for provider outages.
- For tool calling, use an explicit server-side allowlist and confirmation for destructive actions.

## Privacy

- Redact PII at the logger layer.
- Implement account deletion and test it end to end across all systems.
- Provide a data export endpoint that produces machine-readable output.

## Supply Chain

- Commit the lockfile.
- Run CI with `--frozen-lockfile` or equivalent.
- Enable Dependabot, Snyk, Renovate, or equivalent and route alerts to a real inbox.
- Pin production base images. Do not use `:latest`.

## Feature Flags

- Ship risky or reversible changes behind a flag that can flip without deploy.
- Roll out core-flow changes gradually: internal, 1%, 10%, 50%, 100%.

## Definition Of Done

- Inputs validated with structured error responses.
- Query-layer authz for protected data.
- `tenant_id` on new tenant-scoped tables.
- Multi-step writes in transactions.
- Slow operations queued instead of awaited inline.
- External calls have timeouts.
- Idempotency keys honored on side-effect writes.
- PII flows through the redaction layer.
- LLM output schema-validated, with tokens and cost logged per user.
- At least one error case tested.
- New public endpoints have rate limits.
- No new in-memory state that breaks horizontal scale.
- Risky changes are behind a flag.
- Schema changes are backward-compatible across a rolling deploy.

## Pre-Launch

- Load tested, with breaking QPS known.
- Honest `/health` endpoint.
- Graceful shutdown verified.
- Backup restored at least once.
- Error alerting fired by a test error.
- Logs centralized.
- PII redaction verified with fake email or SSN.
- CDN serving static assets.
- Rate limits per IP and per tenant.
- Secrets in a manager, with zero secrets in CI logs.
- Spending caps and budget alerts configured.
- Per-user or per-tenant quotas active.
- Account deletion and data export tested.
- Cross-tenant access returns 404.
- Idempotency keys on side-effect endpoints.
- LLM features have fallback paths and output validation.
- Lockfile, dependency scanning, and pinned images in place.
- Runbook written.
- Rollback exercised.
- Migrations gated to a single runner.
- Foreign-key columns indexed.
- No session data in process memory.
- Uploads go to object storage.
- Outbound HTTP has timeouts and, where critical, circuit breakers.
