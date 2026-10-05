---
name: create-bruno-collection
description: >-
  Create or extend a Bruno API collection across protocols: HTTP/REST (JSON,
  multipart, XML, SSE), GraphQL, gRPC (proto imports, streaming), WebSocket,
  and SOAP-as-HTTP. Includes bruno.json, Bruno 2.x environment files, JWT
  chaining via bru.setEnvVar, and per-request docs for success and errors.
  Scans routes, OpenAPI, GraphQL schema, or proto. Use when asked for Bruno
  collections, .bru files, gRPC/GraphQL/WebSocket examples, API environments,
  auth flow in Bruno, or runnable documented API examples for a service.
disable-model-invocation: true
---

# Create Bruno collection

[Bruno](https://www.usebruno.com/) stores collections as plain-text `.bru` files. Deliver a **runnable, documented** collection: environments, chained auth, and inline API docs — for every protocol the service exposes.

Shared references: [collection-layout.md](references/collection-layout.md), [environments-and-auth.md](references/environments-and-auth.md), [request-documentation.md](references/request-documentation.md), [scripts-and-env-by-protocol.md](references/scripts-and-env-by-protocol.md), [bruno-documentation.md](references/bruno-documentation.md).

## Step 0: pick protocol first

| If the surface is… | `meta.type` | Load |
|---|---|---|
| REST, OpenAPI, webhooks, file upload, SSE | `http` | [protocols/rest-http.md](references/protocols/rest-http.md) |
| GraphQL gateway or schema | `graphql` | [protocols/graphql.md](references/protocols/graphql.md) |
| gRPC / protobuf services | `grpc` | [protocols/grpc.md](references/protocols/grpc.md) |
| WebSocket APIs | `ws` | [protocols/websocket.md](references/protocols/websocket.md) |
| SOAP or WSDL | `http` + XML | [protocols/soap-and-sse.md](references/protocols/soap-and-sse.md) |

Mixed services: one collection, shared `environments/`, HTTP `auth/login` when tokens are JWT, then protocol-specific folders (see [collection-layout.md](references/collection-layout.md)). Index: [protocols/README.md](references/protocols/README.md).

## Prerequisites

- **HTTP** — route definitions or OpenAPI.
- **GraphQL** — schema, exported operations, or gateway config.
- **gRPC** — `.proto` files and/or reflection; optional buf layout.
- **WebSocket** — URL, message contract, auth headers.
- Optional: Bruno desktop client to run interactive streams and WebSockets.

## Workflow

1. **Discover** — list operations per protocol (paths, RPCs, queries/mutations, WS actions). Note auth scheme and error shapes.
2. **Scaffold** — `bruno.json`, `environments/`, protocol folders, one `.bru` per operation. [collection-layout.md](references/collection-layout.md).
3. **Environments** — `baseUrl`, `graphqlUrl`, `grpcHost`, `wsUrl`, credentials, empty token slots, `vars:secret`. [environments-and-auth.md](references/environments-and-auth.md).
4. **Auth chain** — HTTP login or token request in `auth/` (`seq` 1); `script:post-response` with `bru.setEnvVar`; downstream requests use `{{accessToken}}` (HTTP bearer, GraphQL, gRPC metadata, WS headers). [environments-and-auth.md](references/environments-and-auth.md), [scripts-and-env-by-protocol.md](references/scripts-and-env-by-protocol.md).
5. **Implement requests** — follow the protocol reference for `meta.type`, body blocks, and streaming rules.
6. **Document each request** — `docs { }` with success and errors (HTTP status, GraphQL `errors`, gRPC status codes). [request-documentation.md](references/request-documentation.md).
7. **Keep in sync** — API changes update the matching `.bru` in the same commit.

## Output checklist

- [ ] `bruno.json` with collection name and `type: collection`
- [ ] Environment file(s) with URLs/hosts and auth-related vars for each protocol in use
- [ ] `auth/` login or token request with post-response `bru.setEnvVar` when JWT or API keys are chained
- [ ] Each protocol: correct `meta.type` and driver block (`get`/`post`, `grpc`, `ws`, `body:graphql`)
- [ ] gRPC: proto path or collection proto settings documented for operators
- [ ] Every non-trivial request has a `docs` block (success + errors)
- [ ] No real secrets, production hostnames, or employer-only URLs in committed files

## Bruno version caveats

- **Bru tag reference** documents `http` and `graphql` tags; `grpc` and `ws` types are supported in the app (see Bruno `tests/grpc` and `tests/websockets` fixtures and [bruno-documentation.md](references/bruno-documentation.md)).
- **gRPC scripting** is beta (interactive app; limited runner/CLI).
- **SSE** and long-lived **WebSocket/gRPC streams** may be skipped or manual in collection runner — document operator steps in `docs`.
- **OpenCollection YAML** is Bruno’s recommended format for some new work; this skill targets `.bru` unless the user asks for YAML migration.

## Out of scope

Bruno desktop feature parity, cloud sync, and generating a collection from live traffic capture.

## Related skills

- `super-nodejs`: the routes come from a Node service.
- `super-protobuf`: the surface is gRPC or Connect described by .proto files.
- `super-verify`: run the collection and show the result as proof.
- `write-mr-description`: attach the collection to an MR.
