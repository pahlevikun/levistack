# Mobile app caching

On-device memory and disk, platform HTTP stacks, and offline stores. Align TTL and invalidation with server caches so the app does not show stale data longer than the API tier allows.

## Layers

| Layer | iOS (guidance) | Android (guidance) |
|---|---|---|
| Memory | `NSCache` (evicted under pressure) | `LruCache` / in-memory repo |
| HTTP disk | `URLCache` + `NSURLSession` policy | OkHttp `Cache` (per-client, size-bound) |
| Images | `NSCache` + disk via SDWebImage/Kingfisher | Coil/Glide disk + memory tiers |
| Offline DB | Core Data / SQLite / Realm | Room / SQLite |
| Push invalidation | Silent push → purge keys | FCM data message → purge |

## HTTP client cache (NSURLSession / OkHttp)
- Set **disk cache size** explicitly (e.g. 10–50 MB); unbounded disk caches fill storage and get cleared by OS.
- Respect **`Cache-Control`** from APIs — mobile clients are HTTP caches too.
- For authenticated APIs, default to **no cache** or very short TTL unless responses are explicitly `private` with a defined staleness budget.
- **ETag** support: enable transparent revalidation on OkHttp; on iOS use `URLSession` with appropriate `requestCachePolicy`.

## On-device application cache
- Cache **stable reference data** (categories, config flags) with version keys; bump app config version on breaking schema change.
- **User-specific** data: prefer short TTL + pull-to-refresh; invalidate on logout (wipe namespaced keys).
- **Offline-first**: write to local DB first, sync with background task; define conflict resolution — caching docs do not replace sync design.

## Images
- Use a library with **memory + disk** tiers; size memory cache to device class.
- Cache key = URL + transform parameters (width, crop).
- Purge on memory warning (iOS) and low-memory callbacks (Android).

## Relation to server tiers
- Mobile often hits **CDN + API** — coordinate `Cache-Control` on list endpoints with client `staleTime`.
- Do not duplicate large payloads in SW (web) and native disk without a size budget.

## Checklist
- [ ] Logout clears user-scoped caches (HTTP + app + images)
- [ ] Disk cache capped; sensitive responses not written to disk
- [ ] Offline mode documents max staleness per screen
- [ ] Server hot keys still protected (client cache does not replace API single-flight)

See: [web-app.md](web-app.md) for shared HTTP rules, [backend-api.md](backend-api.md) for API cache keys.
