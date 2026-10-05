---
name: super-caching
description: "Super caching: domain router for web (browser, CDN, service worker, HTTP Cache-Control, BFF/API route cache), mobile (on-device, offline, image cache, NSURLSession/OkHttp guidance), server (in-process L1, Redis/Memcached, cache-aside and invalidation), edge/CDN, DB buffer-pool pointers, and optional LLM prompt cache. Covers LRU/LFU/W-TinyLFU, TTL, stampede and hot-key mitigation. Use when choosing or fixing caching in web apps, mobile clients, APIs, distributed cache layers, or CDN headers — not for ORM query-plan cache, pure-function memoization, or CPU cache tuning."
---

# Super caching

Put hot data closer to the reader. One router for **web**, **mobile**, **backend/API**, **edge/CDN**, and related tiers — with shared mechanics in `references/core/`.

**Merged scope:** formerly `caching`, `caching-strategies`, and `caching-strategist`.

## Step 0: pick a domain

Do this first; load only what the task needs. Index: [references/domains/README.md](references/domains/README.md).

| If the task touches… | Domain | Load |
|---|---|---|
| Browser, SPA data libs, service worker, SSR/BFF routes | **web** | [web-app.md](references/domains/web-app.md) + core pack |
| iOS/Android HTTP, offline, images, local stores | **mobile** | [mobile-app.md](references/domains/mobile-app.md) + core pack |
| Services, workers, Redis, GraphQL loaders, API keys/TTL | **backend** | [backend-api.md](references/domains/backend-api.md) + core pack |
| CDN, purge, edge KV/workers, `s-maxage` | **edge** | [edge-cdn.md](references/domains/edge-cdn.md) + [http-caching.md](references/core/http-caching.md) |
| `shared_buffers`, InnoDB pool, page eviction | **database pool** | [database-buffer-pool.md](references/domains/database-buffer-pool.md) |
| Prompt prefix cache, semantic answer cache | **AI/LLM** | [ai-llm.md](references/domains/ai-llm.md) + backend core as needed |

**Core pack** (patterns, trade-offs, stress, checklist): [fundamentals.md](references/core/fundamentals.md). Add depth by topic:

| You need… | Read |
|---|---|
| LRU, LFU, ARC, W-TinyLFU, L1 vs Redis, eviction policies | [cache-mechanisms.md](references/core/cache-mechanisms.md) |
| Invalidation, single-flight, L1+L2, Redis vs Memcached | [deep-dive.md](references/core/deep-dive.md) |
| Redis keys, locks, Lua, pub/sub, pipelines | [redis-patterns.md](references/core/redis-patterns.md) |
| Cache-Control, ETags, CDN, browser | [http-caching.md](references/core/http-caching.md) |
| Keys, TTL table, correctness checklist | [implementation-checklist.md](references/core/implementation-checklist.md) |
| AWS, Azure, GCP managed cache | [providers/generic.md](references/core/providers/generic.md), [aws](references/core/providers/aws.md), [azure](references/core/providers/azure.md), [gcp](references/core/providers/gcp.md) |

## Package layout

```
super-caching/
├── SKILL.md
└── references/
    ├── core/          # fundamentals, mechanisms, Redis, HTTP, checklist, providers
    └── domains/       # web, mobile, backend, edge, DB pool, AI — README index
```

## Quick defaults

- Read-heavy origin pain → **cache-aside** + TTL with jitter + invalidate on write.
- Multi-instance → **Redis/Memcached**; optional **L1** on hottest keys only.
- Public static assets → **HTTP/CDN** first ([http-caching.md](references/core/http-caching.md)).
- Before adding any layer → confirm reads are the bottleneck (`back-of-the-envelope`).

Full trade-off tables, failure modes, and apply steps: [fundamentals.md](references/core/fundamentals.md).

## Related skills

- `super-architecture`: decide where the cache layer sits in the system.
- `super-nodejs`: build server-side caching in a Node service.
- `super-tech-blueprint`: compare Redis, Memcached or a CDN as a stack choice.
- `super-verify`: prove hit rate and latency before you claim a win.

## Old skill names

| Old | Use |
|---|---|
| `caching` | This skill (`super-caching`) |
| `caching-strategies` | `super-caching` |
| `caching-strategist` | `super-caching` |
