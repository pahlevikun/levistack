# Scripts and environment variables by protocol

Bruno 2.x: environment files under `environments/*.bru` with `vars { }` and `vars:secret [ ... ]`. Cross-request chaining uses **`bru.setEnvVar`** / **`bru.getEnvVar`** so the active environment in the UI stays consistent.

| Protocol | Typical env vars | Auth chaining | Post-call chaining |
|---|---|---|---|
| HTTP / REST | `baseUrl`, `accessToken`, resource IDs | `auth/login.bru` → `script:post-response` sets token | `res.status`, `res.body` in `script:post-response` |
| GraphQL | `graphqlUrl`, shared `accessToken` | Same HTTP login | Read `res.body.data` / `errors` |
| gRPC | `grpcHost`, `accessToken`, trace IDs | HTTP login or metadata from env | `script:grpc:after-call-end` (beta); prefer metadata from env |
| WebSocket | `wsUrl`, `accessToken`, `channelId` | Headers from env | Manual; optional pre-request guard |
| SOAP (HTTP) | `soapEndpoint`, basic creds | Basic or bearer on HTTP block | XML parsing in post-response if required |

## HTTP / GraphQL (canonical JWT chain)

Unchanged from the login pattern in `environments-and-auth.md`:

```bru
script:post-response {
  if (res.status === 200) {
    const token = res.body.access_token || res.body.token;
    if (token) bru.setEnvVar("accessToken", token);
  }
}
```

GraphQL login mutations use the same hook; extract from `res.body.data.login.token` when the API nests tokens.

## gRPC

- Pass tokens in **`metadata { authorization: Bearer {{accessToken}} }`** or `script:grpc:before-call-start` with `bru.grpc.request.metadata.upsert`.
- Assert success with status code **0** in `script:grpc:after-call-end`, not HTTP `res.status`.
- gRPC scripting is **beta** and geared to interactive runs; do not rely on it alone in CI until Bruno CLI documents support.

## WebSocket

- No response object like HTTP; use **pre-request** to validate `bru.getEnvVar("accessToken")`.
- Put dynamic values in `body:ws` content with `{{var}}` interpolation.

## Collection runner caveats

- **SSE** (`Accept: text/event-stream`) — skipped in runner/CLI.
- **WebSocket / long-lived gRPC streams** — treat as manual or narrowly scoped tests.
- Keep **auth** requests at low `seq` in `auth/` so folder runs hit login first.

## Runtime vs environment vars

- **`bru.setEnvVar`** — persists for the selected environment (JWT, `baseUrl`, IDs reused across requests).
- **`bru.setVar`** — narrower scope; use only when the value must not leak across environments.
