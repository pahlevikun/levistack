# Per-request documentation

Use Bruno's **`docs { ... }`** block on each `.bru` file. Content is Markdown-friendly plain text: headings, lists, and fenced code examples render in the Bruno UI.

Document what operators and agents need without opening the server codebase: purpose, auth, success, and **errors**.

## Minimum bar

Every request should include:

1. **Purpose** — one sentence on what the endpoint does.
2. **Auth** — none, bearer (`accessToken`), basic, etc.; note if login must run first.
3. **Success** — typical HTTP status (200, 201, 204) and brief response shape or link to a shared schema name.

Non-trivial endpoints (creates, updates, searches, admin) also need:

4. **Request** — required headers, path/query/body fields (names and constraints from OpenAPI or handlers).
5. **Errors** — status codes, machine-readable error codes, example JSON bodies.

Skip duplicating full OpenAPI in every file; repeat only what differs per endpoint.

## Protocol-specific error documentation

| Protocol | Document in `docs` |
|---|---|
| HTTP / REST | HTTP status + JSON error body (`code`, `message`, fields) |
| GraphQL | HTTP status **and** `errors[]` with `message`, `path`, `extensions.code` (200 responses can still fail) |
| gRPC | gRPC status names/codes (e.g. `INVALID_ARGUMENT`, `UNAUTHENTICATED`) and example `grpc-message`; unary vs stream behavior |
| WebSocket | Handshake failures vs application JSON error frames after connect |
| SOAP | SOAP Fault (`faultcode`, `faultstring`, detail) on HTTP 500/200 |

Examples: GraphQL and gRPC `docs` fragments are in `references/protocols/graphql.md` and `references/protocols/grpc.md` (load from SKILL.md).

## Template (inside `docs { }`)

```bru
docs {
  Create an order for the authenticated user.

  ## Auth
  Bearer `accessToken` (run **auth/login** first).

  ## Request body
  - `items` (required): array of `{ sku, quantity }`
  - `idempotencyKey` (optional): string, max 64 chars

  ## Success
  - **201** — order created; body includes `id`, `status`, `total`

  ## Errors
  - **400** `VALIDATION_ERROR` — invalid item or quantity
    ```json
    {
      "code": "VALIDATION_ERROR",
      "message": "quantity must be positive",
      "field": "items[0].quantity"
    }
    ```
  - **401** — missing or expired token
  - **409** `DUPLICATE_IDEMPOTENCY_KEY` — replay with same key and different body
  - **422** — business rule failure (document `code` values from the service)
}
```

Use real `code` values and field names from the API's error module or OpenAPI `responses` — do not invent codes the server does not emit.

## Where to find error shapes

- OpenAPI `responses` for 4xx/5xx with `content.application/json.examples`
- Central error handler or `errors/*.go`, `ProblemDetail`, RFC 7807 types, etc.
- Handler tests that assert status and JSON body

If the API returns a stable envelope (`{ "error": { "code", "message" } }`), show one example per distinct **code**, not every possible message string.

## Success-only endpoints

For simple GETs with only 200/404:

```bru
docs {
  Fetch a single order by ID.

  ## Success
  - **200** — order object (`id`, `status`, `items`, ...)

  ## Errors
  - **404** — order not found or not visible to the caller
}
```

## Folder-level docs

Optional `folder.bru` `meta` name is for grouping only. Keep detailed docs on individual requests unless an entire folder shares one auth and error convention (then a short note in each file: "Errors: standard API envelope; see auth/login docs").

## Checklist per request

- [ ] Purpose and auth requirement stated
- [ ] Success status and response summary
- [ ] Documented error statuses relevant to this operation
- [ ] At least one example error JSON when the body is structured
- [ ] Path/query/body parameters mentioned when not obvious from the `.bru` file alone
