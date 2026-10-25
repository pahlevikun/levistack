# Status line

One status line for Claude Code, the Cursor CLI agent and Codex, from the same install.

```
you@example.com | my-repo | main | Sonnet 5.5 Medium Thinking | 5h ▰▰▰▱▱▱▱▱ 40% | 1w ▰▱▱▱▱▱▱▱ 12% | ctx ▰▰▱▱▱▱▱▱ 25%
```

Order: account, folder, git branch, model (with effort and thinking), 5-hour limit, weekly limit, context. A segment is hidden when the tool does not provide it. Gauges are green below 60%, yellow from 60% and red from 85%.

## Install

```bash
node scripts/install-statusline.mjs --dry-run     # see what would change
node scripts/install-statusline.mjs               # install for every tool whose config folder exists
node scripts/install-statusline.mjs --runtime=cursor,codex
node scripts/install-statusline.mjs --uninstall
```

The installer merges into your existing config, writes a timestamped `.bak` next to each file it edits, and **will not replace a status line it did not write** unless you pass `--force` (the old value stays in the backup). It copies `statusline.mjs` to `~/.levistack/` so the configs keep working if you move the clone. Restart the tool afterward.

## What each tool supports

| Tool | Mechanism | Config written | What you get |
|---|---|---|---|
| Claude Code | Custom command | `statusLine` in `~/.claude/settings.json` | Everything above |
| Cursor CLI agent | Custom command | `statusLine` in `~/.cursor/cli-config.json` | Folder, branch, model with effort/thinking/Max, context. No account email and no rate limits: Cursor's payload does not include them |
| Codex | **Built-in items only.** Codex has no custom-command status line (tracked upstream in openai/codex#20244) | `[tui].status_line` in `~/.codex/config.toml` | `current-dir`, `git-branch`, `model-with-reasoning`, `context-used`, `five-hour-limit`, `weekly-limit`. No email and no custom gauges |

Codex's own footer styles those items, so it looks different from the other two. Item IDs were checked against codex-cli 0.154.0. Other versions may differ; `/statusline` inside Codex lists what yours supports.

Cursor's input format is documented by the `statusline` skill bundled with the Cursor CLI. Claude Code's is at https://code.claude.com/docs/en/statusline.

## Options (environment variables)

| Variable | Effect |
|---|---|
| `LEVISTACK_STATUSLINE_SEGMENTS` | Choose and order segments, e.g. `dir,branch,model,ctx` (ids: `email,dir,branch,model,5h,1w,ctx`) |
| `LEVISTACK_EMAIL` | Show this account label (useful in Cursor) |
| `NO_COLOR` or `LEVISTACK_STATUSLINE_COLOR=0` | Plain text |
| `CLAUDE_CONFIG_DIR`, `CURSOR_CONFIG_DIR`, `CODEX_HOME`, `LEVISTACK_HOME` | Use different config locations (also how the tests run in a sandbox) |

When the tool reports its width (Cursor does), the line drops the least important segments first: email, 1-week limit, 5-hour limit, folder, branch.

## Notes
- Runs locally with no network and no dependencies, in about 80 ms. It always exits 0 and prints nothing on bad input, so it cannot break a session.
- Cursor kills a status command after 2 seconds; this one finishes far inside that.
- The email comes from Claude Code's own login file (`.claude.json`). Nothing is sent anywhere.
