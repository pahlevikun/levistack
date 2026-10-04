# Environments and auth chaining

Bruno 2.x uses **environment files** (`.bru` under `environments/`) for values that change per deployment. **Request scripts** read responses and write back into those variables so later requests stay authenticated without manual copy-paste.

Official scripting API (Bruno collection runner): `bru.setEnvVar`, `bru.getEnvVar`, `bru.setVar`, `bru.getVar`. Prefer **`bru.setEnvVar`** for tokens and credentials so the active environment in the UI stays consistent across requests.

## Environment file

```bru
vars {
  baseUrl: http://localhost:8080
  accessToken:
  username: demo@example.com
  password: changeme
}

vars:secret [
  accessToken
  password
]
```

- **`baseUrl`** — no trailing slash unless the API requires it; all request URLs use `{{baseUrl}}/path`.
- **Empty token slot** — declare `accessToken:` with no value; the login script fills it at runtime.
- **`vars:secret`** — marks vars Bruno treats as secrets (redacted in UI). Never commit real tokens or production passwords; use placeholders and local overrides.

Add **Local**, **Staging**, etc. when operators need different `baseUrl` values. Keep variable **names** identical across env files so requests do not branch on environment name.

## Auth folder and sequence

Put login, OAuth token exchange, or API-key bootstrap under `auth/` with low `seq` (e.g. login = 1). Document in the login request docs: "Run this first" or "Required before protected endpoints."

## Capture token from login (canonical pattern)

Login with no auth; on success, persist token to the environment:

```bru
meta {
  name: Login
  type: http
  seq: 1
}

post {
  url: {{baseUrl}}/auth/login
  body: json
  auth: none
}

headers {
  Accept: application/json
  Content-Type: application/json
}

body:json {
  {
    "email": "{{username}}",
    "password": "{{password}}"
  }
}

script:post-response {
  if (res.status === 200) {
    const body = res.body;
    const token = body.access_token || body.token;
    if (token) {
      bru.setEnvVar("accessToken", token);
    }
  }
}
```

Adjust JSON paths to match the real API (`data.jwt`, `access_token`, nested `auth.token`, etc.). Use one env var name consistently (e.g. `accessToken`) in all `auth:bearer` blocks.

## Use token on protected requests

```bru
get {
  url: {{baseUrl}}/api/me
  body: none
  auth: bearer
}

auth:bearer {
  token: {{accessToken}}
}
```

Alternatives:

- **Basic** — `auth: basic` with `username` / `password` from env vars (no post-response script).
- **API key** — header or query from `{{apiKey}}`; bootstrap request may set `bru.setEnvVar("apiKey", ...)` the same way as JWT.

## Collection-level vs request-level vars

- **Environment vars** (`bru.setEnvVar`) — shared for all requests while that environment is selected; right choice for JWT and base URL.
- **Runtime vars** (`bru.setVar` / `bru.getVar`) — request or collection scope; use for one-off IDs extracted from a create response (`bru.setEnvVar("orderId", body.id)` when the ID should be reused across requests in the same session).

Example after creating a resource:

```bru
script:post-response {
  if (res.status === 201 && res.body.id) {
    bru.setEnvVar("orderId", String(res.body.id));
  }
}
```

## Pre-request scripts (optional)

```bru
script:pre-request {
  const token = bru.getEnvVar("accessToken");
  if (!token) {
    console.warn("accessToken is empty — run auth/login first");
  }
}
```

## Other protocols (same env vars)

- **GraphQL** — `graphqlUrl` plus shared `accessToken` on `auth:bearer` or `auth: inherit`.
- **gRPC** — `grpcHost`; pass `Bearer {{accessToken}}` in `metadata { }` or `script:grpc:before-call-start`.
- **WebSocket** — `wsUrl`; `Authorization` header with `{{accessToken}}`.
- **SOAP** — `soapEndpoint`; often basic auth vars instead of JWT.

Script differences per type: load `references/scripts-and-env-by-protocol.md` from SKILL.md.

## Operator notes

- Select the correct environment in Bruno before running the collection.
- Re-run login when tokens expire; document TTL or refresh in the login request `docs` block if the API supports refresh tokens (optional second request with its own post-response script).
