# Caching fundamentals

Put a copy of hot data closer to the reader so most requests skip the slow path.
Caching is the highest-leverage move for read-heavy systems — and the easiest to
get subtly wrong, because a cache adds a second source of truth that can serve
stale or wrong data, and can *amplify* an outage when it misbehaves.

**Merged scope:** system design (patterns and trade-offs), Redis and HTTP/CDN
implementation, and delivery checklists (keys, TTLs, invalidation) — formerly
split across `caching`, `caching-strategies`, and `caching-strategist`.

## When to reach for this
Reads dominate (a high read:write ratio from `back-of-the-envelope`); the same
data is read repeatedly; the datastore is the read bottleneck; or recomputation
is expensive. A cache buys read latency and offloads the origin.

## When NOT to
Write-heavy or read-once data (low hit rate — pure overhead). Data that must be
exactly current with zero staleness (a cache is a stale copy by nature; when
strict freshness is required, go to the source or use `consistency-coordination`).
Don't add a cache before a number shows reads are the problem (YAGNI) — it's a new
failure mode and a second thing to operate. Not for database-internal query-plan
caching, `functools.lru_cache` / memoize helpers, or hardware cache tuning.

## Clarify first
- **Read:write ratio and hit rate** — is the working set cacheable? (→ `back-of-the-envelope`, 80/20.)
- **Staleness tolerance** — seconds? minutes? must reads see their own writes?
- **Working-set size** — does the hot set fit in RAM across cache nodes?
- **Consistency on write** — can the cache briefly disagree with the store?
- **Eviction trigger** — what's the access pattern (recency? frequency? time-bound?)?

## The options

**Where to cache** (often layered): client/browser → CDN edge (→ `content-delivery`)
→ application/in-process → distributed cache (Redis/Memcached) → database buffer
pool. Tier details: [implementation-checklist.md](implementation-checklist.md).
Domain-specific tiers: [../domains/README.md](../domains/README.md).

**Read strategy**
- **Cache-aside (lazy):** app checks cache, on miss reads the store and populates.
  Use when reads are unpredictable; the default for most systems.
- **Read-through:** the cache library fetches from the store on miss. Use to keep
  app code simple and caching policy centralized.

**Write strategy**
- **Write-through:** write cache and store synchronously. Use when reads right
  after writes must be fresh and slower writes are acceptable.
- **Write-back (write-behind):** write cache now, flush to store async. Use for
  write-heavy/bursty paths that tolerate a small loss window.
- **Write-around:** write only the store; let the cache fill on read. Use when
  written data is rarely re-read soon (avoids cache churn).

**Eviction policy** (per tier — L1 library vs Redis `maxmemory-policy` vs HTTP TTL)
- **LRU** — recency-skewed traffic; Redis `allkeys-lru` is the usual dedicated-cache default.
- **LFU** — stable hot keys (Zipf); Redis `allkeys-lfu` or in-process W-TinyLFU (e.g. Caffeine).
- **TTL** — bound staleness at the app; always add jitter; pair with server eviction, not instead of invalidation.
- **Adaptive (ARC, W-TinyLFU)** — mixed scans + hot sets; common in JVM in-process caches and DB buffer pools.
- **FIFO / random** — rarely for production hit rate. Mechanism catalog: [cache-mechanisms.md](cache-mechanisms.md).

## Trade-offs

| Option | What it solves | What it worsens | Change it when |
|---|---|---|---|
| Cache-aside | Simple, resilient (cache down ⇒ just slower) | First read per key is a miss; risk of stale after writes | Misses are too costly → read-through + warming |
| Read-through | Centralized, clean app code | Couples app to cache lib; cold-start misses | Custom per-key load logic is needed |
| Write-through | Fresh reads after write | Slower writes; writes cached data that may never be read | Writes dominate and aren't re-read → write-around/back |
| Write-back | Fast, absorbs write bursts | Data loss window on crash; complex | Durability of recent writes is required |
| Write-around | No churn from write-only data | Recently written keys miss on first read | That data IS read right after write → write-through |
| TTL eviction | Bounds staleness automatically | Mass expiry can stampede the origin | Add jitter / soft-TTL refresh |

## Behavior under stress
A cache that misbehaves doesn't just stop helping — it can take down the origin.

- **Thundering herd / stampede:** a hot key expires (or the cache restarts) and
  thousands of concurrent misses hit the store at once. *Mitigate:* per-key locks
  / request coalescing (single-flight), early/probabilistic refresh, TTL jitter.
  Code patterns: [redis-patterns.md](redis-patterns.md).
- **Cache penetration:** requests for keys that don't exist bypass the cache every
  time (often malicious). *Mitigate:* cache the negative result (short TTL), or a
  Bloom filter in front.
- **Hot key:** one key exceeds a single node's throughput. *Mitigate:* replicate
  across nodes, add L1, or shard the value.
- **Eviction storm / cold cache:** after a flush or deploy, hit rate craters.
  *Mitigate:* warm critical keys; ramp traffic.
- **Stale-after-write:** the store changed but the cache didn't. *Mitigate:*
  invalidate on write, write-through, or short TTL — pick per staleness budget.

**Monitor:** hit rate, p99 latency, eviction rate, key distribution (hot spots),
and origin QPS during cache restarts.

## How to apply
1. **Clarify the inputs** — confirm read:write ratio, staleness budget, hot-set size.
   If reads aren't the bottleneck yet, stop (→ `back-of-the-envelope`).
2. **Pick strategies** from the trade-off table (read, write, eviction).
3. **Set key knobs** — naming, TTL with jitter, invalidation per family; decide
   negative caching and single-flight up front ([implementation-checklist.md](implementation-checklist.md)).
4. **Implement** — application/Redis: [redis-patterns.md](redis-patterns.md); HTTP/CDN: [http-caching.md](http-caching.md).
5. **Stress-test** — walk stampede, penetration, hot key, cold cache, stale-after-write.
6. **Size with numbers** — hot set in RAM, target hit rate 90%+, node QPS (below).
7. **Provider** — generic Redis/Memcached unless user named a cloud (`providers/`).

## Dos and don'ts
**Do**
- Default to cache-aside; it stays correct (just slower) when the cache is down.
- Set a TTL on every entry and add jitter so keys don't expire in lockstep.
- Add single-flight for hot keys before launch.
- Invalidate on write (or write-through, or short TTL) to a stated staleness budget.
- Size to the hot set; alert on hit rate, evictions, and origin QPS.

**Don't**
- Don't cache before a number proves reads are the bottleneck.
- Don't cache data that must be exactly current.
- Don't let mass-expiry or cold start dump full load on the origin.
- Don't ignore missing-key floods — negatives or Bloom filter.
- Don't reuse keys across schema versions — bump `...:v2` instead.
- Don't rely on TTL alone for permissions, prices, or roles — invalidate on write.

## Numbers that matter
A cache node serves ~**100k–1M QPS**, far above an RDBMS (~1k). Memory access is
~100 ns vs ms-scale disk. Size the cache to the hot set (~20% of data ≈ 80% of reads).
Target hit rates are usually 90%+; below that, question cacheability. → `back-of-the-envelope`.

## Interface sketch
A cache entry is a contract: a **key** (stable, namespaced), a **value** (serialized;
watch size), and a **TTL**. Define the **invalidation event** per key family.
Versioned keys (`...:v2`) turn invalidation into a write instead of a delete race.

## Choosing a provider
Default to the generic recipe (Redis or Memcached). If the user names a cloud,
read `providers/<provider>.md`. If no file exists, use the generic recipe.

## Diagram
Use the in-plugin `architecture-diagram` skill for cache-aside or stampede flows —
cache nodes use the cache color, the origin its store color, miss path dashed.

## Related building blocks
- `content-delivery` — CDN/edge layer above application cache.
- `data-storage` — origin the cache protects; replicas as an alternative to caching reads.
- `consistency-coordination` — when staleness is unacceptable or sharding theory applies.
- `back-of-the-envelope` — read ratio and hot-set sizing.
- `resilience-failure` — rate limits and breakers for retry storms.
- `system-design` — orchestration and trade-off method.
