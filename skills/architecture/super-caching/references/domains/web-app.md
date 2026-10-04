# Web app caching

Browser, CDN, service worker, and server-rendered/BFF layers. HTTP semantics are authoritative — start with [http-caching.md](../core/http-caching.md).

## Layers (typical SPA or SSR)

| Layer | What it caches | Invalidation lever |
|---|---|---|
| Browser HTTP cache | GET responses per URL + `Cache-Control` | Headers, URL/version bump |
| Memory cache (tab) | Same-origin fetches within navigation | Short-lived; follow HTTP |
| Service worker | Assets and API shells you register | SW version + cache name purge |
| CDN / edge | Shared cache for `public` responses | Purge API, surrogate keys, short `s-maxage` |
| BFF / route handler | Aggregated JSON per user/session | App TTL + Redis; often `private` at CDN |
| Client data library | Normalized server state in memory | Stale time, invalidation on mutation |

## Browser and HTTP
- Treat **HTML** as revalidate often (`no-cache` or short `max-age`) unless fully static.
- **Content-hashed assets** (`app.[hash].js`): `Cache-Control: public, max-age=31536000, immutable`.
- **Personalized JSON**: `private` or `no-store`; do not let a shared CDN cache user-specific bodies.
- **ETags / `If-None-Match`**: save bandwidth on revalidation; pair with sensible `max-age`.
- **Vary**: only on headers that truly change the representation (`Accept-Encoding`, `Accept-Language`); avoid `Vary: Cookie` on widely cached paths.

## Service workers
- **Cache-first**: offline shells, fonts, icons — version caches on deploy (`cacheName` bump).
- **Network-first**: auth, cart, anything that must be fresh when online.
- **Stale-while-revalidate**: list UIs where slightly stale is OK; align with product staleness budget.
- Never cache authenticated API responses in a shared SW cache without scoping by credential mode and explicit TTL.

## Client-side data caches (React Query, SWR, TanStack Query, Apollo)
- These are **in-memory app caches**, not HTTP caches — configure `staleTime`, `gcTime`/`cacheTime`, and mutation-driven invalidation.
- **Deduping** in-flight requests is single-flight at the client — still add server-side single-flight for hot keys.
- SSR/hydration: align server fetch cache (e.g. Next.js `fetch` cache, `unstable_cache`) with client `staleTime` to avoid flash of stale UI.

## BFF and API routes
- Cache **aggregated** responses (dashboard, home feed) with keys that include tenant + user segment when needed.
- Prefer **cache-aside in Redis** behind the BFF over caching at the CDN for mixed public/private fields.
- GraphQL: field-level caching is rare; cache resolver results or persisted queries at the BFF with explicit TTL.

## Checklist
- [ ] Every cacheable GET has explicit `Cache-Control` (or deliberate `no-store`)
- [ ] CDN only sees responses meant to be shared (`public` / anonymous)
- [ ] SW cache names versioned on release
- [ ] Client library stale times documented per resource family
- [ ] Stampede path tested on hot list endpoints

See also: [edge-cdn.md](edge-cdn.md), [backend-api.md](backend-api.md), `content-delivery`.
