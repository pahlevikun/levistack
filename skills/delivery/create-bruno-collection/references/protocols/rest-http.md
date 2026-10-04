# REST / HTTP requests

`meta.type: http`. Default for OpenAPI and most framework route scanners.

## Minimal JSON GET

```bru
meta {
  name: Get order
  type: http
  seq: 2
}

get {
  url: {{baseUrl}}/api/orders/{{orderId}}
  body: none
  auth: bearer
}

auth:bearer {
  token: {{accessToken}}
}

headers {
  Accept: application/json
}

docs {
  Fetch one order by ID. Bearer `accessToken` (run **auth/login** first).
}
```

## POST with JSON body

```bru
post {
  url: {{baseUrl}}/api/orders
  body: json
  auth: bearer
}

headers {
  Content-Type: application/json
  Accept: application/json
}

body:json {
  {
    "items": [{ "sku": "ABC", "quantity": 1 }],
    "idempotencyKey": "{{idempotencyKey}}"
  }
}
```

## Other body tags (same `type: http`)

| Body | Bru block | When |
|---|---|---|
| JSON | `body:json { ... }` | Default APIs |
| Form URL-encoded | `body:form-urlencoded { key: value }` | HTML forms, legacy APIs |
| Multipart | `body:multipart-form { field: value ~file: path }` | Uploads, mixed fields |
| Raw text | `body:text { ... }` | Plain text payloads |
| XML | `body:xml { <root>...</root> }` | SOAP-style HTTP, XML APIs |
| File / binary | Body type **File** in UI; path or `{{var}}` | Downloads, binary upload |

Prefix a multipart field with `~` when it is a file path. Match `Content-Type` in `headers` when the server is strict.

## Server-Sent Events (still HTTP)

Long-lived **HTTP** responses with `Accept: text/event-stream`. Bruno streams chunks in the UI; collection runner and CLI **skip** these requests so runs do not hang. Document in `docs` that operators must send manually. Bruno SSE docs are listed in `references/bruno-documentation.md`.

## Conventions

- URLs: `{{baseUrl}}/path` — no double slashes; align trailing slash with the service.
- Name requests by intent ("Create order"), not raw paths.
- Chained IDs: `script:post-response` with `bru.setEnvVar` (canonical login pattern in `environments-and-auth.md`).
