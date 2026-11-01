# Prepare a connection change

Determine the runtime and requested scope from actual project configuration and
runtime help. Runtime defaults are not interchangeable. A project-local setting,
a user-wide registry, plugin configuration and a running process are separate
owners. Inspect the smallest required surface, avoid printing complete config,
and preserve unrelated keys.

Use environment or secret-manager references supported by that host. The helper
accepts exact `${NAME}` placeholders in `env` and remote `headers`. It does not
expand them or establish that the selected host expands that syntax. Replace the
profile with a verified runtime adapter when its schema/interpolation differs.
Never place a live token in the command-line argument list or endpoint URL.

## Plan a portable JSON draft

`mcp_ops.py` supports only an explicit top-level `mcpServers` JSON profile.
A local entry accepts `command`, string-array `args`, optional `cwd`, and an `env`
map of placeholders. A remote entry accepts an HTTPS `url` without query,
credentials or fragment, and optional placeholder headers. Unsupported fields
are rejected; preserve a runtime's distinct schema through its own tooling.

```json
{
  "command": "python3",
  "args": ["server.py"],
  "env": {"SERVICE_TOKEN": "${SERVICE_TOKEN}"}
}
```

Save the entry and use a local copy of the inspected configuration as inputs.
These commands only create new files:

```sh
python3 scripts/mcp_ops.py plan --config config.json --entry entry.json --name example --out change-plan.json
python3 scripts/mcp_ops.py render --config config.json --entry entry.json --plan change-plan.json --out config-draft.json
```

The plan omits config and entry values; its hashes bind the exact files. Rendering
rejects drift and preserves every other configuration member. It creates the draft
from the same verified in-memory input snapshots, so a later input change cannot
substitute unreviewed content into the result. The resulting draft
may retain pre-existing private settings, so its mode is private and it belongs in
local scratch, not the catalog or a shared report. Review the exact diff, confirm
host compatibility and use the authorized runtime mechanism to install it. The
helper intentionally has no in-place global-configuration mutation command.

Record a rollback route before an actual runtime change: prior settings, scope,
restart/refresh behavior and a minimal smoke check. A plan being generated or a
server entry being written is not proof that the host can call the expected tools.
