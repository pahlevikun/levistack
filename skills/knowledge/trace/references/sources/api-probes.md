# API probes (read-only HTTP)

Ask a running service what it thinks: the current state of a record, a config endpoint, a health or version endpoint.

**Ask the user before you call a production API.** `GET` and `HEAD` only.

## How to search it

1. **Find the endpoint** in the OpenAPI file, the `.proto`, or a Bruno or Postman collection (`create-bruno-collection` keeps them as files).
2. **Use the user's own token or session**, from an environment variable. Never paste a token into the chat or the output.
3. **Start with health and version**: `/health`, `/ready`, `/version`, `/info`. They tell you which build is running.
4. **Then the record**: `GET` the entity the problem is about, and compare it with what the database or the logs say.

```bash
curl -sS -H "Authorization: Bearer $TOKEN" "https://<host>/v1/<resource>/<id>" | jq '.'
curl -sS -o /dev/null -w '%{http_code} %{time_total}s\n' "https://<host>/health"
```

Never send `POST`, `PUT`, `PATCH` or `DELETE`, even to an endpoint that "only reads". If a search endpoint needs `POST`, ask the user first and say why it is safe.

## What good evidence looks like

- A version endpoint that shows an older build than expected
- A record whose state differs between the API and the database (a cache)
- A health endpoint that reports a dependency as down

## Pitfalls

- **Prod access.** Some hosts need a VPN or a bastion. If it fails, report the gap. Do not route around it.
- **Personal data** in responses. Use `jq` to select only the fields you need, and mask ids.
- **Rate limits.** Probe once, not in a loop.

## What to return

Method, URL with ids masked, status code, latency, the response fields that matter, and the time of the call in UTC.
