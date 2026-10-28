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
metadata:
  version: 1.2.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - verify
    - ready-spec
    - create-documentation
  invokes:
    - skill: verify
      when: Collection should be run to prove requests
    - skill: create-documentation
      when: A shareable client API document is requested alongside the runnable collection
  tags:
    - bruno
    - api
    - collection
  capabilities:
    - bruno_collection
    - handover_prerequisite_cases
  languages:
    - en

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

Mixed services: one collection, shared `environments/`, and protocol-specific folders. Add an auth bootstrap only when the service exposes a real acquisition operation. A JWT format does not imply a login endpoint. See [collection-layout.md](references/collection-layout.md). Index: [protocols/README.md](references/protocols/README.md).

## Prerequisites

- **HTTP** — route definitions or OpenAPI.
- **GraphQL** — schema, exported operations, or gateway config.
- **gRPC** — `.proto` files and/or reflection; optional buf layout.
- **WebSocket** — URL, message contract, auth headers.
- Optional: Bruno desktop client to run interactive streams and WebSockets.

## Workflow

1. **Discover** — list operations per protocol (paths, RPCs, queries/mutations, WS actions). Note auth scheme and error shapes.
   When called as a handover prerequisite, inspect the available code, tests, Swagger/OpenAPI, and other definitions needed to create requests. Inventory supported success and error branches, conditional payloads, business states, and transition prerequisites. Keep one operation identity with multiple meaningful scenario cases. Never invent a parameter or endpoint to force a state.
2. **Scaffold** — `bruno.json`, `environments/`, protocol folders, a primary `.bru` plus named supported scenario cases per operation. [collection-layout.md](references/collection-layout.md).
3. **Environments** — `baseUrl`, `graphqlUrl`, `grpcHost`, `wsUrl`, credentials, empty token slots, `vars:secret`. [environments-and-auth.md](references/environments-and-auth.md).
4. **Auth** — follow the actual acquisition contract. If a login or token endpoint exists, put it in `auth/` with an early sequence and capture its real token field using `bru.setEnvVar`. For externally supplied credentials, keep a secret placeholder and provisioning instructions; create no login or refresh route. Downstream requests use the supported header, metadata, or auth block. [environments-and-auth.md](references/environments-and-auth.md), [scripts-and-env-by-protocol.md](references/scripts-and-env-by-protocol.md).
5. **Implement requests** — follow the protocol reference for `meta.type`, body blocks, and streaming rules.
6. **Document each request** — `docs { }` with success and errors (HTTP status, GraphQL `errors`, gRPC status codes). [request-documentation.md](references/request-documentation.md).
   For handover evidence, include complete error examples with status, relevant headers, and actual-shaped bodies, plus trigger, prerequisites, and caller action. Capture known state variants and distinguish constructed fixtures from observed responses. Missing fixtures and unrun cases are different gaps.
7. **Keep in sync** — API changes update the matching `.bru` in the same commit.
8. **Client handover when requested** — use `create-documentation` in **handover** mode for an HTTP API packet, or **contract** mode for GraphQL, gRPC, WebSocket, and other message contracts. Supply the operation inventory, authoritative contract, `.bru` cases, sanitized examples, and verification gaps. Use protocol-specific operation identifiers and status meanings. Apply the handover export checks when a PDF, HTML or DOCX is requested. The document supplements the runnable collection.
   If `create-documentation` called this skill to create or complete its prerequisite collection, return the collection and scenario inventory to that caller. Do not launch a second handover. A request for a handover includes this collection prerequisite unless the user explicitly forbids collection edits.

## Output checklist

- [ ] `bruno.json` with collection name and `type: collection`
- [ ] Environment file(s) with URLs/hosts and auth-related vars for each protocol in use
- [ ] Real auth acquisition and chaining when supported, or secret placeholders and provisioning instructions for externally supplied credentials
- [ ] Each protocol: correct `meta.type` and driver block (`get`/`post`, `grpc`, `ws`, `body:graphql`)
- [ ] gRPC: proto path or collection proto settings documented for operators
- [ ] Every non-trivial request has a `docs` block (success + errors)
- [ ] No real secrets, production hostnames, or employer-only URLs in committed files
- [ ] When a client handover was requested, `create-documentation` received the contract and case inventory, and the shareable artifact was checked

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
- `verify`: run the collection and show the result as proof.
- `create-documentation`: turn verified contract and collection evidence into client documentation when requested.
- `write-mr-description`: attach the collection to an MR.

Behavior scenarios are in [evals/evals.json](evals/evals.json).
