---
description: "Umbrella and multi-app Mix projects: inward dependencies, mix.exs as the source of truth, pinned contract dependencies."
globs: "**/mix.exs,apps/**/*.{ex,exs}"
alwaysApply: false
---

# Umbrella and multi-app projects

Applies the `layering-and-dependency-direction` rule to Mix.

- **`mix.exs` is the dependency truth.** Declare every internal dependency there. A cross-app reference that was never declared compiles in an umbrella and later breaks the release.
- **Inner apps never reference outer types.** The domain app imports no Ecto, gRPC, Phoenix or protobuf types and has no internal dependencies. Persistence depends inward on the domain. Transport apps compose capabilities and own listeners, handlers, transformers and endpoint policy.
- **No horizontal coupling** between client and persistence apps.
- **Composition-root injection.** Runtime config may inject an implementation from another app without a compile dependency, provided the receiver uses a behaviour-shaped interface and never names the implementation module.
- **One storage boundary module** selects adapters. Public and cache facades must not call each other to discover the selected adapter.
- **Ports only for a real need.** Add a behaviour when an inner layer needs inversion and a real outer implementation exists. Not speculatively.
- **Only the web app uses Phoenix/Plug; only the data app uses Ecto/Postgrex.**
- **Name apps by runtime role** before bounded context: `transport_*` (listeners), `worker_*` (one-shot or scheduled jobs), `service_*` (deployable runtimes), `shared_*` (cross-cutting libraries), `core_*` (domain, persistence, outbound integrations). A rename is complete only when directory, Mix project, OTP app atom, release, config, module namespace, Docker target, compose service, CI job and docs all agree. Do not rename persisted vocabulary, protobuf names, API paths or env vars to mirror it.

## Verify
```bash
mix xref graph --format cycles
mix xref graph --format cycles --label compile-connected
```
Check both runtime and compile-connected cycles. Use the code graph first if one exists, then confirm against each `mix.exs`.

## External contract dependencies
See `external-contracts`. Every app that consumes the contract package declares identical git dependency options, pinned to a tag or a full commit SHA, never a branch. Commit `mix.lock` after changing the revision.
