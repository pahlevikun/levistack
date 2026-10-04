# Database buffer pool (pointer)

The database engine caches **disk pages** (blocks), not your API DTOs or assembled views. Tuning `shared_buffers` (PostgreSQL), InnoDB buffer pool, or similar is **storage-layer** work — see `data-storage` and the buffer-pool section in [cache-mechanisms.md](../core/cache-mechanisms.md).

## When this skill still applies
- You need **lower read latency for composed data** (joins, aggregations, cross-service reads) → application or Redis cache.
- You see **scan workloads** evicting hot pages → fix queries and indexes; do not mirror full scans in an LRU object cache.

## When to stop at the DB layer
- Single-table hot row repeatedly read → index + buffer pool may be enough.
- Working set fits in RAM and queries are simple — measure before adding Redis.

**Do not** confuse ORM second-level cache or query-plan cache with distributed application caching; those are engine/ORM-specific and out of scope for this skill's primary path.
