# Cache mechanisms catalog

From **in-process LRU** through **distributed Redis**, eviction policy often matters
more than “which product.” Use this file when the user asks *how* a cache decides
what stays in memory, or when to pick LRU vs LFU vs adaptive policies.

Sources (2024–2026 docs where noted): Redis eviction reference, Caffeine W-TinyLFU
wiki, Megiddo & Modha ARC paper, PostgreSQL buffer-pool notes.

## Taxonomy: where the cache lives

| Layer | Examples | Scope | Typical eviction | Best for |
|---|---|---|---|---|
| **CPU / hardware** | L1/L2/L3, page cache | Per core / OS | Hardware-specific | Not covered by this skill |
| **In-process (L1)** | Caffeine, Guava `Cache`, .NET `MemoryCache`, `lru_cache` | One app instance | Size + time + W-TinyLFU / LRU | Hot keys, config, parsed objects; accept per-instance staleness |
| **Distributed (L2)** | Redis, Memcached, Valkey | All instances | `maxmemory-policy` + app TTL | Shared session, catalog, rate limits |
| **CDN / browser** | Cloudflare, `Cache-Control` | Edge / client | HTTP freshness rules | Static assets, cacheable GETs → [http-caching.md](http-caching.md); [web-app.md](../domains/web-app.md) |
| **Database buffer pool** | PostgreSQL shared buffers, InnoDB buffer pool | DB process | Clock / LRU / ARC (engine-specific) | Pages, not your app objects — different tuning surface |

**Stacking:** L1 → L2 → origin is standard. Each tier can use a *different* eviction
logic; align **TTL** and **invalidation** across tiers so L1 does not hide stale L2.

## Eviction and admission (concepts)

**Eviction** — which entry to remove when full. **Admission** — whether a new entry
may enter at all (TinyLFU rejects one-hit wonders before they evict hot data).

| Policy | Idea | Strength | Weakness | Typical use |
|---|---|---|---|---|
| **FIFO** | Oldest inserted leaves first | Simple | Ignores reuse; poor hit rate | Rare; queues with strict ordering |
| **LRU** | Evict least *recently used* | Good for recency bursts | Scan streams pollute the pool | Default mental model; Redis `allkeys-lru` |
| **LFU** | Evict least *frequently used* | Stable hot set | Slow to forget old popularity | Redis `allkeys-lfu`; skewed Zipf workloads |
| **TTL / expire** | Drop after wall-clock age | Bounds staleness | Mass expiry → stampede | Always combine with jitter; app-level `EXPIRE` |
| **Random** | Evict arbitrary key | Cheap, uniform | Unpredictable hit rate | Redis `allkeys-random`; testing only |
| **ARC** | Adaptive balance recency (T1) vs frequency (T2) via ghost lists | Scan-resistant; self-tuning | More metadata; patent history (expired 2024) | DB buffer pools; some `contrib` engines |
| **W-TinyLFU** | Small LRU *window* + main SLRU; Count–Min Sketch admission | Strong general-purpose hit rate; O(1) | In-process libraries, not Redis native | Caffeine default for `maximumSize` |

**LRU vs scan workloads:** a one-time sequential scan touches many “recent” pages
and can evict the real working set (classic buffer-pool problem). Prefer **scan-resistant**
policies (ARC, LIRS, or separate **recycle** pools for scans) for DB caching; for
app caches, **do not cache full scan results** or use very short TTL.

**Approximation:** Redis LRU/LFU are **sampled** (default 5 keys per eviction), not
exact — tune `maxmemory-samples` for accuracy vs CPU ([Redis eviction docs](https://redis.io/docs/latest/develop/reference/eviction/)).

## In-process (L1) caches

Use when latency must stay sub-millisecond and slight cross-instance inconsistency
is OK (short `expireAfterWrite` / `expireAfterAccess`).

**Caffeine (Java/Kotlin)** — bounded caches use **Window TinyLFU**: new entries enter
a small admission window (LRU), then compete on estimated frequency for space in a
segmented LRU main region; window size adapts to workload ([Caffeine Efficiency wiki](https://github.com/ben-manes/caffeine/wiki/Efficiency)).
Prefer over hand-rolled `ConcurrentHashMap` + TTL for production.

Knobs: `maximumSize` / `maximumWeight`, `expireAfterWrite`, `expireAfterAccess`,
`refreshAfterWrite` (async reload), `recordStats()` for hit rate.

**Guava `Cache`** — older; still LRU-ish segments; greenfield Java often uses Caffeine.

**Go** — `groupcache`, `ristretto` (TinyLFU-style admission), or a small LRU from
`container/list` only for prototypes.

**Python** — `functools.lru_cache` for **pure function memoization** (out of scope
for distributed design); for request-scoped or shared in-process data use `cachetools.TTLCache`
or an external L2.

**Node** — `lru-cache` package (size + TTL); for multi-instance consistency use Redis.

**Design rules for L1**
- Cap entries (`maximumSize`); unbounded maps are outages waiting to happen.
- Weight large values (`maximumWeight`) when entry sizes vary wildly.
- L1 TTL ≤ L2 TTL so L2 remains source of shared truth.
- Expose hit/miss metrics before relying on L1 in production.

## Redis and Memcached (L2)

### Redis `maxmemory-policy` ([reference](https://redis.io/docs/latest/develop/reference/eviction/))

| Policy | Evicts | When to use |
|---|---|---|
| `noeviction` | Nothing; writes fail at limit | Primary store semantics; not a pure cache |
| `allkeys-lru` | LRU among **all** keys | **Default recommendation** for dedicated cache (Pareto hot subset) |
| `allkeys-lfu` | LFU among all keys | Stable popularity; less recency bias |
| `allkeys-lrm` | Least recently **modified** | Keep read-heavy keys; evict stale writes |
| `volatile-lru` / `volatile-lfu` | Only keys **with TTL** | Mixed cache + mandatory persistent keys — prefer two instances |
| `volatile-ttl` | Shortest remaining TTL | Trim soonest-expiring when memory tight |
| `volatile-random` / `allkeys-random` | Random | Avoid unless testing |

Set `maxmemory` explicitly. Pair server eviction with **application TTL** on every
cache key; do not rely on eviction alone for correctness.

**Redis is not only a key-value LRU:** hashes, sorted sets, streams, Lua, pub/sub —
see `redis-patterns.md`. Single-threaded per shard; scale with cluster/replicas.

### Memcached

Multithreaded, simple GET/SET, **slab allocator** + LRU per slab class. No rich types,
no persistence. Choose when you need maximum throughput for opaque blobs and will
handle invalidation in the app ([deep-dive.md](deep-dive.md) Redis vs Memcached).

## Database buffer pool (related, not interchangeable)

The DB caches **pages** (blocks), not your DTOs. Replacement policies (clock-sweep,
LRU, ARC, LIRS in PostgreSQL extensions) optimize **disk I/O**, not HTTP latency.
Tuning `shared_buffers` / InnoDB pool size is `data-storage` territory; **application
caching** still helps for assembled views and cross-service reads.

ARC adapts between recency and frequency and resists one-pass scans ([Megiddo & Modha, IEEE Computer 2004](https://theory.stanford.edu/~megiddo/pdf/IEEE_COMPUTER_0404.pdf)).

## Picking a mechanism (quick)

```
Read-heavy API object, multi-instance?
  → L2 Redis/Memcached (cache-aside) + optional L1 Caffeine/lru-cache on hot keys

Single JVM hot read path?
  → Caffeine with maximumSize + expireAfterWrite; metrics on stats

Ephemeral session / rate limit counters?
  → Redis strings or hashes with TTL; consider LFU if keys are long-lived popular

Static assets / public GET JSON with CDN?
  → http-caching.md + edge-cdn domain first; app cache second

Full table scan or export?
  → Do not route through LRU object cache; stream from DB or use RECYCLE-style pool at DB layer
```

## Further reading (URLs)

- https://redis.io/docs/latest/develop/reference/eviction/
- https://github.com/ben-manes/caffeine/wiki/Efficiency
- https://github.com/ben-manes/caffeine/wiki/Eviction
- https://theory.stanford.edu/~megiddo/pdf/IEEE_COMPUTER_0404.pdf
- https://wiki.postgresql.org/wiki/Multiple_Buffer_Pools
