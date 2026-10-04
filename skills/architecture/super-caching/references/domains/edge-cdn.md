# Edge and CDN caching

Shared caches between your origin and clients. Full header and directive reference: [http-caching.md](../core/http-caching.md). Broader delivery context: `content-delivery`.

## What belongs at the edge
- Static and content-hashed assets (long TTL, `immutable`).
- Anonymous, cacheable GET JSON where the body is identical for all users in a region.
- HTML only when truly static or with short `s-maxage` + surrogate control.

## What does not
- Responses that vary per cookie/session without careful `Vary` design.
- `Set-Cookie` on cacheable paths (often prevents caching).
- Write methods and non-idempotent GETs with side effects.

## Cache keys and variants
- Normalize **query string** order in origin or at edge rules.
- **Geo / device** variants: separate cache keys or use regional caches — document staleness per variant.
- **Surrogate-Key** / **Cache-Tag** headers for bulk purge (Fastly, Cloudflare, Akamai patterns).

## Purge and propagation
- Invalidate **outward**: origin commit → L2 app cache → CDN purge → clients revalidate.
- Prefer **short TTL + stale-while-revalidate** over manual purge for low-risk data.
- After deploy, expect **cold edge** — warm critical URLs or accept origin spike.

## Edge compute (Workers, Lambda@Edge, etc.)
- **KV / edge cache** for config and feature flags — sub-ms reads; cap entry size and TTL.
- Do not treat edge KV as durable storage — always have origin fallback.

## Checklist
- [ ] `s-maxage` defined where CDN should differ from browser `max-age`
- [ ] Purge runbook for security incidents (bad asset, leaked JSON)
- [ ] Origin shield or tiered CDN if origin is fragile

See: [web-app.md](web-app.md) for browser + SW interaction.
