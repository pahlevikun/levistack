---
name: super-protobuf
description: "Protocol Buffers (proto3) design, buf.yaml/buf.gen.yaml, Connect and gRPC services, protovalidate, lint and breaking checks, schema evolution, mixed-version compatibility review, and defensive gRPC hardening. Use when writing or reviewing .proto files, setting up buf, generating Connect or gRPC code, adding protovalidate, catching breaking changes, or hardening an exposed gRPC surface — not for REST-only OpenAPI, GraphQL schemas, or offensive testing."
paths:
  - "**/*.proto"
  - "**/buf.yaml"
  - "**/buf.*.yaml"
  - "**/buf.gen.yaml"
  - "**/buf.gen.*.yaml"
  - "**/buf.lock"
---

# Super protobuf

One router for proto3 schemas, the **buf** toolchain, Connect/gRPC services, and compatibility review. Language-agnostic core; language tracks are optional and short.

**Merged scope:** formerly `protobuf`. Index: [references/README.md](references/README.md). Research: [research-synthesis.md](references/core/research-synthesis.md).

## Principles

1. **Match the repo first.** Copy existing package layout, field order, validation, and comments. If none exist, use this skill's defaults.
2. **Buf is the default toolchain.** `buf format -w && buf lint`, then `buf breaking --against '.git#branch=main'` when the schema already shipped. EasyP is a buf-compatible alternative, not a second source of truth.
3. **Protovalidate on production fields.** The `.proto` file is the contract for structure and constraints.
4. **Evolve additively.** New fields, enum values, and RPCs stay in `v1`. Breaking changes get a new package version. Never reuse field or enum numbers.
5. **Treat gRPC as an API.** Authz on every method, including "internal" services that just became reachable. Do not leak `.proto` files or descriptors. Do not run or document attacks.

## Step 0: detect the job

Do this first; do not announce it. If the request already names a mode, go there.

| If the user is doing this | Mode | Load |
|---|---|---|
| New messages, RPCs, package layout, AIP-style resources | **design** | [modes/design.md](references/modes/design.md), [design.md](references/core/design.md) |
| `buf.yaml` / `buf.gen.yaml`, generate stubs, Connect vs gRPC | **generate** | [modes/generate.md](references/modes/generate.md), [buf-workflow.md](references/core/buf-workflow.md) |
| Review a proto diff, mixed-version deploys, wire vs JSON vs storage | **review-compat** | [modes/review-compat.md](references/modes/review-compat.md), [compatibility.md](references/core/compatibility.md) |
| `buf lint` / `buf breaking`, naming, EasyP as alternative | **lint-breaking** | [modes/lint-breaking.md](references/modes/lint-breaking.md), [style.md](references/core/style.md) |
| Auth on gRPC, reflection, grpc-web, leaked schemas | **harden** | [security.md](references/core/security.md) |
| Go plugins, opaque API | **language: Go** | [go.md](references/tech/go.md) |
| Elixir / protobuf-elixir | **language: Elixir** | [elixir.md](references/tech/elixir.md) |
| C# / grpc-dotnet | **language: C#** | [csharp.md](references/tech/csharp.md) |
| Connect vs gRPC choice | **rpc stack** | [connect-vs-grpc.md](references/tech/connect-vs-grpc.md) |

Stack index: [references/tech/README.md](references/tech/README.md). Depth: [evolution.md](references/core/evolution.md), [protovalidate.md](references/core/protovalidate.md), [review-checklist.md](references/core/review-checklist.md), [quick-reference.md](references/core/quick-reference.md), [troubleshooting.md](references/core/troubleshooting.md), [migration.md](references/core/migration.md), [protoc-toolchain.md](references/core/protoc-toolchain.md).

## Default pipeline

1. Detect the job (table above).
2. **Design** the messages and RPCs. Copy [templates/](templates/README.md) or [assets/proto/example/v1/](assets/proto/example/v1/).
3. **Generate** with the project's `buf.gen.yaml` (templates in [assets/](assets/)).
4. **Verify:** `buf format -w && buf lint`. If the schema shipped, `buf breaking --against '.git#branch=main'`.
5. **Review-compat** when consumers, storage, or mixed versions exist.

Check the Makefile or `package.json` first—many repos wrap these as `make lint` / `make generate`.

## Contribute

Keep this router lean. Do not paste language samples or extra checklists here.

- **Language track:** add `references/tech/<lang>.md` (one screen), one row in `references/tech/README.md`, and one row in the Step 0 table.
- **Template:** add a file under `templates/` or `assets/` and mention its basename in [templates/README.md](templates/README.md).
- **Core topic:** add `references/core/<topic>.md` and one table row here. Prefer extending an existing file.

## Old skill name

| Old | Use |
|---|---|
| `protobuf` | This skill (`super-protobuf`) |

## Done when

- The matching mode ran; only needed references were opened.
- `buf format -w && buf lint` (or the project's wrap) succeeded; breaking check ran when the schema already shipped.
- Production fields have protovalidate constraints; reserved numbers cover removals.
- gRPC exposure was treated as an API (authz, no schema leak) when that was in scope.
