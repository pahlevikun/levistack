# Super protobuf index

Load [SKILL.md](../SKILL.md) first. Open only the files the job needs.

## Modes

| Mode | File | Use |
|------|------|-----|
| design | `modes/design.md` | New messages, RPCs, AIP-style resources |
| generate | `modes/generate.md` | buf.yaml, buf.gen.yaml, codegen |
| review-compat | `modes/review-compat.md` | Diff review, mixed-version deploys |
| lint-breaking | `modes/lint-breaking.md` | buf lint, breaking, naming |

Harden (authz, no schema leak): `core/security.md`.

## Core

| File | Holds |
|------|-------|
| `core/design.md` | File layout, AIP-style APIs, messages, enums, services |
| `core/buf-workflow.md` | buf CLI, buf.yaml, buf.gen.yaml, BSR |
| `core/compatibility.md` | Wire vs JSON vs source vs stored data |
| `core/evolution.md` | Additive change vs new `vN`, mixed-version rollout |
| `core/style.md` | Naming, lint as workflow, EasyP alternative |
| `core/security.md` | Defensive gRPC/protobuf review only |
| `core/protovalidate.md` | Field and CEL constraints |
| `core/review-checklist.md` | Review items before an API stabilizes |
| `core/quick-reference.md` | Field numbers, types, buf commands |
| `core/troubleshooting.md` | Lint, breaking, generate, import errors |
| `core/migration.md` | protoc → buf |
| `core/protoc-toolchain.md` | Legacy protoc projects |
| `core/research-synthesis.md` | Merge notes and design themes |

## Tech tracks

See `tech/README.md`. Files: `go.md`, `elixir.md`, `csharp.md`, `connect-vs-grpc.md`.

## Templates and assets

- `templates/` — copy-paste starters (`resource.proto`, `service.proto`, `buf.yaml`). Index: `templates/README.md`.
- `assets/` — existing buf configs, Makefile, and the book example: `buf.yaml`, `buf.lock`, `buf.gen.yaml`, `buf.gen.go.yaml`, `buf.gen.go-connect.yaml`, `buf.gen.ts.yaml`, `buf.gen.python.yaml`, `buf.gen.java.yaml`, `Makefile.example`, `book.proto`, `book_service.proto`.
