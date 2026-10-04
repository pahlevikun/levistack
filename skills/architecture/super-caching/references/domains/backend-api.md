# Backend and API caching

Application servers, workers, and BFFs: in-process L1, distributed L2, and origin protection. This is the default path for Redis/Memcached design.

## Stack (usual)
1. **L1 in-process** — hot keys, parsed objects ([cache-mechanisms.md](../core/cache-mechanisms.md) § in-process).
2. **L2 Redis/Memcached** — shared across instances ([redis-patterns.md](../core/redis-patterns.md)).
3. **Origin** — database or upstream HTTP.

Default read pattern: **cache-aside** with TTL + **invalidate on write** for mutable entities.

## Key design
- Follow [implementation-checklist.md](../core/implementation-checklist.md) for naming, TTL table, correctness.
- **BFF keys** include tenant, locale, or feature flags when responses differ.
- **Pagination**: cache page keys or cursors separately; invalidating a list often means deleting `list:*` patterns or tag buckets.

## Patterns by API style
| Style | Cache surface | Caveat |
|---|---|---|
| REST resource | Per-entity key `service:entity:id` | Invalidate related collections |
| GraphQL | Per-resolver or DataLoader batch keys | Avoid caching mutations; watch N+1 on miss |
| gRPC | Metadata + protobuf blobs in Redis | Version protos in key (`:v2`) |
| Event-driven | Invalidate on domain events (pub/sub) | Ordering vs eventual consistency |

## Failure modes (server-focused)
- Implement **single-flight** before launch on catalog/home keys ([deep-dive.md](../core/deep-dive.md)).
- **Graceful degradation**: cache down → origin only; do not fail requests.
- **Hot keys**: local L1 replica, read replicas, or key splitting — see fundamentals stress section.

## Managed cloud
If the user names AWS/Azure/GCP, read [../core/providers/](../core/providers/) for ElastiCache, Azure Cache, Memorystore, etc.

## Checklist
- [ ] Every write path lists cache keys to delete or update
- [ ] L1 TTL ≤ L2 TTL
- [ ] Metrics: hit rate, origin QPS, eviction rate
- [ ] Load test cold start and mass TTL expiry
