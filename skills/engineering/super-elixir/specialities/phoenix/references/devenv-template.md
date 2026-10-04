# devenv Templates for Phoenix

## devenv.yaml

```yaml
# yaml-language-server: $schema=https://devenv.sh/devenv.schema.json
inputs:
  nixpkgs:
    url: github:cachix/devenv-nixpkgs/rolling
  nixpkgs-stable:
    url: github:nixos/nixpkgs/release-25.11

allowUnfree: true
```

## devenv.nix

Replace `my_app` with your project/database name throughout.

```nix
{ pkgs, lib, config, inputs, ... }:

let
  pkgs-stable = import inputs.nixpkgs-stable { system = pkgs.stdenv.system; };
in
{
  # Asset tooling — tells Mix to use Nix-managed binaries
  env.MIX_BUN_PATH = lib.getExe pkgs-stable.bun;
  env.MIX_TAILWIND_PATH = lib.getExe pkgs-stable.tailwindcss_4;
  env.NODE_PATH = "${config.git.root}/deps";  # lets Bun resolve Phoenix packages (phoenix, phoenix_html, etc.)

  packages = with pkgs-stable; [
    git
    tailwindcss_4
    beam28Packages.elixir-ls
  ] ++ lib.optionals stdenv.isLinux [
    inotify-tools   # required for Phoenix live reload on Linux
  ];

  # Elixir
  languages.elixir.enable = true;
  languages.elixir.package = pkgs-stable.beam28Packages.elixir;

  # JavaScript / Bun
  languages.javascript.enable = true;
  languages.javascript.bun.enable = true;
  languages.javascript.bun.package = pkgs-stable.bun;

  # PostgreSQL — Unix socket only, no port conflicts
  services.postgres = {
    enable = true;
    package = pkgs-stable.postgresql_16;
    listen_addresses = "";  # empty = Unix socket only
    initialDatabases = [
      { name = "my_app_dev"; }
      { name = "my_app_test"; }
    ];
    initialScript = ''
      CREATE USER my_app_dev WITH PASSWORD 'my_app_dev' CREATEDB;
      GRANT ALL PRIVILEGES ON DATABASE my_app_dev TO my_app_dev;
      GRANT ALL PRIVILEGES ON DATABASE my_app_test TO my_app_dev;
      ALTER DATABASE my_app_dev OWNER TO my_app_dev;
      ALTER DATABASE my_app_test OWNER TO my_app_dev;
    '';
  };

  # Database env vars — Ecto and psql both use these
  env.DATABASE_URL = "postgres://my_app_dev:my_app_dev@localhost/my_app_dev?socket=${config.env.DEVENV_STATE}/postgres";
  env.PGHOST = "${config.env.DEVENV_STATE}/postgres";
  env.PGUSER = "my_app_dev";
  env.PGDATABASE = "my_app_dev";

  # Convenience scripts
  scripts.db-setup.exec = ''
    echo "Setting up database..."
    mix ecto.create
    mix ecto.migrate
    echo "Database setup complete!"
  '';

  enterShell = ''
    echo "PostgreSQL socket: $PGHOST"
  '';
}
```

## .lsp.json

Add this to your project root so Claude Code uses `elixir-ls` for LSP:

```json
{
  "elixir": {
    "command": "elixir-ls",
    "args": [],
    "extensionToLanguage": {
      ".ex": "elixir",
      ".exs": "elixir",
      ".heex": "html-eex",
      ".leex": "html-eex"
    }
  }
}
```

## Key Design Decisions

### Unix Socket (`listen_addresses = ""`)
- Avoids port 5432 conflicts with system-level PostgreSQL or other projects
- Each devenv project gets its own socket in `$DEVENV_STATE/postgres`
- Set via `PGHOST` so both `psql` CLI and Ecto find it automatically

### `lib.getExe` for Binary Paths
- Resolves to full Nix store path (e.g., `/nix/store/...-bun-1.3.2/bin/bun`)
- Survives `nix-collect-garbage` as long as devenv shell is active
- Prevents Mix from downloading its own copies of bun/tailwind

### `DATABASE_URL` with `?socket=` Parameter
- Standard Ecto URL format with socket path appended
- Works with `Ecto.Repo` `url:` config in production
- The `PGHOST` env var is a parallel mechanism for `psql` and `socket_dir:` config
