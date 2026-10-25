# AI / LLM caching (optional)

Caching for inference workloads: reduce cost and latency when inputs or outputs repeat. Keep privacy and tenancy in mind — never cache another user's prompts or PII-bearing completions in a shared store without strict key isolation.

## Provider prompt / context cache
- Many APIs offer **prefix caching** (system prompt, tool definitions, long documents): identical leading tokens skip recompute on subsequent requests within a TTL window.
- Design prompts with **stable prefixes** (static system block first, variable user content last) to maximize cache hits.
- Track provider docs for cache TTL, minimum token thresholds, and billing — behavior changes by vendor.

## Application-level semantic cache
- **Exact match**: hash normalized prompt + model + temperature → Redis key; short TTL for non-deterministic models unless temperature is 0.
- **Semantic / embedding match**: store embedding of prompt; on near-duplicate, return prior answer — tune similarity threshold and TTL; risk stale or wrong answers if domain drifts.
- **RAG**: cache retrieved chunks separately from generation; invalidate chunk cache when corpus version bumps (`corpus:v3`).

## What not to cache
- Responses that must reflect **live** data (prices, inventory, auth) without invalidation hooks.
- **Tool-call** results that side-effect external systems unless idempotent and keyed by tool args hash.

## Checklist
- [ ] Cache keys include tenant/user when responses must not leak across customers
- [ ] TTL aligned with product staleness; security-sensitive flows use `no-store`
- [ ] Metrics: cache hit rate vs token spend

For general TTL, stampede, and Redis patterns, use [backend-api.md](backend-api.md) and [redis-patterns.md](../core/redis-patterns.md).
