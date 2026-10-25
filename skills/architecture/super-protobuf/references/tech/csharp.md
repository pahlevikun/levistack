# C# track (stub)

Optional language track. Core schema rules stay language-agnostic.

**Use when:** grpc-dotnet, generated C# stubs, or `csharp_namespace` / protobuf-net.

## Defaults

- Prefer buf managed `csharp_namespace_prefix` over hand-written `option csharp_namespace` in every file.
- grpc-dotnet for new services. protobuf-net only if the repo already uses it — do not mix stacks in one contract.
- Pin plugin versions in `buf.gen.yaml`. See buf generate docs for the current C# plugin id.
- Same evolution and protovalidate rules as core; do not treat `[Optional]` C# attributes as a substitute for proto `optional` + protovalidate.

When this skill gains a full C# sample, put it under `templates/` and keep this file short.
