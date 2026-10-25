# Hooks

One flat tree, one language (Node ESM). Every hook is `hooks/<name>.mjs`, exports its own `meta`, and runs through `lib/launcher.mjs`. `hooks/hooks.json` and the table below are generated from `meta` by `npm run sync`.

<!-- hooks:start -->
| Hook | Claude Code event | What it does |
|---|---|---|
| `careful-guard` | `PreToolUse` (Bash) | Asks before `rm -rf /`, force-push, `reset --hard`, `git clean -f` and `DROP TABLE` |
| `generated-file-guard` | `PreToolUse` (Write\|Edit\|MultiEdit) | Asks before editing files marked generated ("do not edit", `@generated`) or writing coverage artifacts |
| `large-read-guard` | `PreToolUse` (Read\|Bash) | Blocks full reads of files over 350 lines (Read, or bare cat/head/tail/less/more) and points to `bulk-reader` |
| `notify-done` | `Stop` | Desktop notification when the agent finishes (terminal bell off macOS) |
| `session-start` | `SessionStart` (startup\|resume\|clear\|compact) | Injects a short digest of the always-on rules in `rules/core/` as context |
<!-- hooks:end -->

## Opt in
```
mkdir -p ~/.levistack
touch ~/.levistack/session-start.on ~/.levistack/careful-guard.on ~/.levistack/large-read-guard.on
```
Delete the `.on` file to turn a hook off. Set `LEVISTACK_HOME` to use a different folder. A hook with `meta.optIn = false` runs without a flag; it is not wired into `hooks.json`, so a project has to call it explicitly.

Settings: `LEVISTACK_MAX_READ_LINES` (default 350) for `large-read-guard`; `LEVISTACK_METRICS_DIR` for its block log (default `~/.levistack/metrics/`).

## How it fits together
```
hooks/
  <name>.mjs        meta + handler, one per hook
  hooks.json        generated
  lib/
    launcher.mjs    entry: parse args, opt-in check, run the handler, render, always exit 0
    input.mjs       normalizes Claude Code and Cursor stdin into { tool, command, filePath, cwd, ... }
    result.mjs      allow() / note(msg) / ask(msg) / deny(msg), and one renderer per runtime
    registry.mjs    discovers hooks and lints their meta
    generate.mjs    builds hooks.json and the table above
    files.mjs, metrics.mjs   small shared helpers
```
A handler never prints JSON itself. It returns a result and the renderer picks the output format for the runtime, so the same hook runs in either agent.

## Agent support
- **Claude Code:** `hooks.json` is loaded automatically when the plugin is installed.
- **Cursor:** not wired by the plugin. To use a hook, point your own `.cursor/hooks.json` at `node <levistack>/hooks/lib/launcher.mjs --runtime=cursor <name>`; `deny` then exits 2 with the `permission: "deny"` JSON Cursor expects.
- **Codex:** not wired.

## Adding a hook
1. Create `hooks/<name>.mjs`:
   ```js
   import { allow, ask } from './lib/result.mjs';
   export const meta = { event: 'PreToolUse', matcher: 'Bash', description: 'One line: what it does' };
   export default function myHook({ input, root, args, runtime, event }) {
     return input.command.includes('x') ? ask('Why this needs a look') : allow();
   }
   ```
   `meta.event` is the Claude Code event. Optional: `matcher`, `timeout` (seconds), `optIn` (default `true`).
2. Run `npm run sync` to regenerate `hooks.json` and the table.
3. Add a test in `tests/hooks.test.mjs`, then run `npm run check`.

Rules: Node only (no shell scripts, `npm run validate` rejects `.sh` here), nothing project-specific, fail open on anything ambiguous, and use `deny` only for a deliberate blocker.
