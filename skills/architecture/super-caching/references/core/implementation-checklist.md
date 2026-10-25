# Implementation checklist

Use when shipping or reviewing a cache layer: keys, TTLs, invalidation, and ops.

## Cache layers

| Layer | Typical tech | Latency | Shared? |
|---|---|---|---|
| L3 Edge/CDN | Cloudflare, Fastly, CloudFront | 10–100ms+ saved | Global |
| L2 Distributed | Redis, Memcached | ~1–5ms | All app instances |
| L1 In-process | Map, LRU in app | ~0ms | Per instance only |
| Origin | Database, API | 10–100ms+ | Source of truth |

Invalidation flows **outward**: origin → L2 → CDN. Do not skip tiers.
Eviction policies per tier: `cache-mechanisms.md`.

## Key naming

- Pattern: `{service}:{entity}:{id}` with optional `:field` or `:page`.
- Version bumps: `...:v2` instead of racing deletes across schema changes.
- Namespace prefixes so SCAN/pattern delete and cluster routing stay predictable.

## TTL starting points

| Data | TTL | Notes |
|---|---|---|
| Session / auth | Match session expiry | Security-bound |
| User profile | 5–15 min | Rare writes |
| Permissions / roles | Short + **invalidate on change** | Never TTL-only |
| Product catalog | 1–4 hours | Acceptable lag |
| Inventory / counts | ~30s | Volatile |
| Static config / flags | ~60s + pub/sub on change | Push invalidation |
| Content-hashed assets | Long + `immutable` | See `http-caching.md` |

Add **jitter** to TTLs so keys do not expire in lockstep.

## Correctness checklist

- [ ] Keys are unique, namespaced, and documented per family
- [ ] Every entry has a TTL (or explicit “immutable until version bump”)
- [ ] Invalidation on every write path (delete or write-through), not TTL alone for security-sensitive data
- [ ] Related keys invalidated together (or tag-based invalidation)
- [ ] Stampede mitigation: single-flight, early refresh, or lock on hot keys
- [ ] Negative caching or Bloom filter for missing keys (penetration)
- [ ] Graceful degradation when cache is down (cache-aside default)
- [ ] Hit rate, evictions, origin QPS monitored; hot keys visible
- [ ] No unbounded growth; sensitive data not cached plain-text

## Deliverables (strategist output)

When asked for a “cache strategy” document, include: key scheme, TTL per family, invalidation triggers, read/write pattern choice, stampede plan, warming if cold-start matters, and monitoring signals.
