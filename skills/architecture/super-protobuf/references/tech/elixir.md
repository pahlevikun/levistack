# Elixir track

Do not duplicate BEAM or gRPC-Elixir guides here. Load catalog **`super-elixir`** (architect / phoenix / otp as the job needs) and keep schema work on this skill's core modes.

**Use when:** protobuf-elixir, gRPC in an umbrella `transport_*` app, or "Elixir proto" in the request.

## Boundaries

- Domain apps do not import protobuf or gRPC types (see catalog Elixir umbrella rules). Transport owns generated stubs and mapping.
- Buf (or the repo's mix wrap) still owns lint, breaking, and generate.
- Pair with design mode for the `.proto` files; this track does not replace `super-elixir`.
