# Domain index

Pick **one** primary domain for the task, then load the [core pack](../core/fundamentals.md) (patterns, mechanisms, Redis/HTTP depth) as needed. Layers stack — a mobile app may use on-device cache *and* CDN-backed APIs.

| Domain | File | When |
|---|---|---|
| Web app | [web-app.md](web-app.md) | Browser cache, service worker, SPA data libraries, BFF route cache |
| Mobile app | [mobile-app.md](mobile-app.md) | On-device, offline, image cache, platform HTTP stacks |
| Backend / API | [backend-api.md](backend-api.md) | Service cache-aside, BFF aggregation, GraphQL loaders, Redis |
| Edge / CDN | [edge-cdn.md](edge-cdn.md) | CDN keys, purge, edge KV/workers, origin shield |
| Database buffer pool | [database-buffer-pool.md](database-buffer-pool.md) | Engine page cache — not app object cache |
| AI / LLM | [ai-llm.md](ai-llm.md) | Prompt cache, semantic response cache (optional) |

Core references (all domains): [fundamentals.md](../core/fundamentals.md), [cache-mechanisms.md](../core/cache-mechanisms.md), [implementation-checklist.md](../core/implementation-checklist.md).
