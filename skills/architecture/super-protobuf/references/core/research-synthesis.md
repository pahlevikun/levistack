# Research synthesis

Captured during `protobuf` → `super-protobuf`. Ideas synthesized; not a verbatim import.

## Shared themes

1. **Proto3 + directory-mirrored packages + version suffix.** `acme.library.v1` lives at `acme/library/v1/`. One service per file is the scalable default.
2. **Buf as the operator.** `buf.yaml` / `buf.gen.yaml`, remote plugins, managed mode, `buf lint`, `buf breaking`, `buf generate`, protovalidate. EasyP offers the same jobs with `easyp.yaml`; keep buf as the catalog default.
3. **Lint and breaking are a workflow, not a custom linter.** Prefer `buf lint` (`STANDARD`) in CI. Do not ship a Python style checker unless the repo already has one.
4. **Compatibility is an envelope, not a boolean.** Binary wire, ProtoJSON/names, generated source, and stored/replayed bytes can disagree. Mixed-version deploys need reader-before-writer sequencing.
5. **Resource APIs stay generic.** Get/List/Create/Update/Delete, unique request/response types, pagination, field masks — without requiring `google.api` HTTP annotations.
6. **Protovalidate (CEL) at the boundary.** Production fields get constraints; skip deprecated PGV.
7. **gRPC is an API.** Authz, TLS, no production reflection, no leaked descriptors. grpc-web is still HTTP. This skill covers **review and hardening only**.

## What this catalog already had

The prior `protobuf` skill: proto design, buf CLI, Connect/gRPC gen templates, protovalidate, migration from protoc, troubleshooting, book service samples. Those assets stay under `assets/` and `references/core/`.

## Gaps this merge fills

- Router modes (design / generate / review-compat / lint-breaking) so agents load one path.
- Compatibility review with mixed-version and storage/JSON dimensions.
- Defensive security review (no attack playbooks).
- AIP-style resource shape without Google package names.
- Optional language tracks (Go, Elixir pointer, C# stub) plus Connect vs gRPC.
- Contribution notes so others add a track or template without bloating the router.

## Out of scope

- REST-only OpenAPI or GraphQL schema design.
- Offensive testing, exploit payloads, fuzz-the-unknown-schema recipes.
- A second lint source of truth (EasyP docs, custom Python linters).
- Per-language server frameworks (Spring, Phoenix) — point at language skills instead.
