> **Speciality `phoenix`**, merged from the `elixir-phoenix` skill. Original description: Use when creating a new Phoenix project, adding Phoenix to an umbrella, configuring assets with Bun, setting up devenv.nix for a Phoenix project, configuring Ecto with PostgreSQL Unix sockets, or adding end-to-end tests.

# Phoenix Project Setup

Standard patterns for Phoenix projects using Bun, Tailwind v4, devenv, and PostgreSQL.

## 1. Create the Phoenix Project

```bash
# Standard project
mix phx.new my_app --database postgres

# Umbrella app
mix phx.new my_app --umbrella --database postgres
```

After generation, replace the default esbuild config with bun.

## 2. Replace esbuild with Bun

In `mix.exs` deps, replace `{:esbuild, ...}` with:

```elixir
{:bun, "~> 1.4", runtime: Mix.env() == :dev},
{:tailwind, "~> 0.2", runtime: Mix.env() == :dev},
```

In `config/config.exs`, replace the `config :esbuild` block with:

```elixir
config :bun,
  version: "1.3.4",
  my_app: [
    args: ~w(build assets/js/app.js --outdir=priv/static/assets --external /fonts/* --external /images/*),
    cd: Path.expand("../", __DIR__)
  ]

config :tailwind,
  version: "4.1.11",
  my_app: [
    args: ~w(--input=assets/css/app.css --output=priv/static/assets/app.css),
    cd: Path.expand("../", __DIR__)
  ]
```

For umbrella apps, use `Path.expand("../apps/my_app", __DIR__)` for `cd:`.

In `config/dev.exs`, update watchers:

```elixir
watchers: [
  tailwind: {Tailwind, :install_and_run, [:my_app, ~w(--watch)]},
  bun: {Bun, :install_and_run, [:my_app, ~w(--sourcemap=inline --watch)]}
]
```

Update `mix.exs` aliases:

```elixir
"assets.deploy": [
  "phx.digest.clean",
  "tailwind my_app --minify",
  "bun my_app --minify",
  "phx.digest"
]
```

## 3. Set NODE_PATH for Phoenix Dependency Resolution

Set `NODE_PATH` to the project root's `deps/` directory so Bun resolves Node-style
packages from Phoenix's `deps/` directory. Imports like `import {Socket} from "phoenix"`
and `import "phoenix_html"` will resolve to the Elixir dependency packages without
needing `node_modules/`.

In `devenv.nix`, this is already configured using an absolute path:
```nix
env.NODE_PATH = "${config.git.root}/deps";
```

For non-devenv setups, export it in your shell or build scripts:
```bash
export NODE_PATH="$(pwd)/deps"
```

No `npm install` or symlinks needed — Phoenix ships JS alongside its Elixir source in
`deps/<package>/priv/static/`.

## 5. Configure runtime.exs for Binary Paths

In `config/runtime.exs`, read env vars so devenv-provided binaries are used instead of
downloading copies. Both packages require explicit configuration:

```elixir
if System.get_env("MIX_BUN_PATH") do
  config :bun, path: System.get_env("MIX_BUN_PATH")
end

if System.get_env("MIX_TAILWIND_PATH") do
  config :tailwind, path: System.get_env("MIX_TAILWIND_PATH")
end
```

When `path` is set, the hex packages skip downloading and use the provided binary directly.
devenv sets these env vars via `lib.getExe` to point at the Nix store paths (see step 4).

## 6. Set Up devenv

See [references/devenv-template.md](references/devenv-template.md) for the full `devenv.yaml` and `devenv.nix` templates.

Key points:
- `lib.getExe` resolves Nix store paths for `MIX_BUN_PATH` and `MIX_TAILWIND_PATH`
- PostgreSQL runs via Unix socket only (`listen_addresses = ""`) — no port conflicts
- `DATABASE_URL` uses `?socket=` parameter pointing to devenv's state directory
- `PGHOST` is set so `psql` and Ecto both find the socket automatically

## 7. Configure Ecto for URL-based Connection

In `config/dev.exs`, support both Unix socket (devenv) and TCP (manual setup):

```elixir
db_config =
  [
    username: System.get_env("POSTGRES_USER", "my_app_dev"),
    password: System.get_env("POSTGRES_PASSWORD", "my_app_dev"),
    database: System.get_env("POSTGRES_DB", "my_app_dev"),
    show_sensitive_data_on_connection_error: true,
    pool_size: 10
  ]
  |> then(fn config ->
    case System.get_env("PGHOST") do
      nil ->
        config ++ [hostname: System.get_env("POSTGRES_HOST", "localhost"),
                   port: String.to_integer(System.get_env("POSTGRES_PORT", "5432"))]
      pghost when is_binary(pghost) ->
        if String.starts_with?(pghost, "/") do
          config ++ [socket_dir: pghost]
        else
          config ++ [hostname: pghost,
                     port: String.to_integer(System.get_env("POSTGRES_PORT", "5432"))]
        end
    end
  end)

config :my_app, MyApp.Repo, db_config
```

This auto-detects whether `PGHOST` is a Unix socket path or a hostname.

## 8. Production Database via URL

In `config/runtime.exs` for prod:

```elixir
if config_env() == :prod do
  database_url =
    System.get_env("DATABASE_URL") ||
      raise "DATABASE_URL is not set"

  config :my_app, MyApp.Repo,
    url: database_url,
    pool_size: String.to_integer(System.get_env("POOL_SIZE", "10"))
end
```

## 9. End-to-End Tests

E2e tests live in `e2e_test/` alongside the standard `test/` folder. They are
expensive and must **never run automatically** — only on explicit request.

Add the `test.e2e` alias in `mix.exs`:

```elixir
defp aliases do
  [
    # ... existing aliases ...
    "test.e2e": ["run --no-halt", "cmd mix test e2e_test/"]
  ]
end
```

Configure `e2e_test/` as an extra test path in `mix.exs` project config so Mix
finds the helpers, but exclude it from the default `mix test` run:

```elixir
def project do
  [
    # ...
    test_paths: ["test"],
    elixirc_paths: elixirc_paths(Mix.env()),
  ]
end
```

Run e2e tests explicitly:

```bash
mix test.e2e
```

> **Never** add `test.e2e` to CI pipelines, pre-commit hooks, or any automated
> alias that runs as part of a normal build or test cycle.

## Quick Reference

| Tool | Hex Package | Env Var | devenv Source |
|------|------------|---------|--------------|
| Bun | `{:bun, "~> 1.4"}` | `MIX_BUN_PATH` | `lib.getExe pkgs.bun` |
| Tailwind | `{:tailwind, "~> 0.2"}` | `MIX_TAILWIND_PATH` | `lib.getExe pkgs.tailwindcss_4` |
| PostgreSQL | `{:ecto_sql, ...}` + `{:postgrex, ...}` | `DATABASE_URL` / `PGHOST` | `services.postgres` |
