# Claude Code hooks

Checked 2026-10-04 against https://code.claude.com/docs/en/hooks. The event list grows; if an event here is missing in your version, read the live page.

## Contents
- Where hooks live
- Config shape
- Events
- Matchers
- Handler types
- Exit codes and JSON output
- Placeholders and environment
- Debugging

## Where hooks live

| Location | Scope | Shared |
|---|---|---|
| `~/.claude/settings.json` | every project | no |
| `.claude/settings.json` | this project | yes, commit it |
| `.claude/settings.local.json` | this project | no, gitignored |
| plugin `hooks/hooks.json` | when the plugin is enabled | yes |
| skill or subagent frontmatter `hooks:` | while the skill or subagent runs | yes |

Hooks from all locations merge. `"disableAllHooks": true` turns them off (managed policy hooks stay).

## Config shape

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard.mjs\"", "timeout": 10 }
        ]
      }
    ]
  }
}
```

A plugin's `hooks/hooks.json` has the same shape, optionally with a top-level `description`, and uses `${CLAUDE_PLUGIN_ROOT}` in paths.

Common handler fields: `type`, `if` (a permission-rule filter such as `"Bash(rm *)"`, tool events only), `timeout` (seconds), `statusMessage`. Command handlers also take `args` (exec form, no shell), `async`, `asyncRewake`, `shell`.

## Events

| Event | Fires | Can block |
|---|---|---|
| `SessionStart` | session begins or resumes | no |
| `UserPromptSubmit` | prompt submitted | yes |
| `PreToolUse` | before a tool call | yes |
| `PermissionRequest` | a permission dialog is about to show | decides it |
| `PostToolUse`, `PostToolUseFailure` | after a tool succeeds or fails | feedback only |
| `Stop` | Claude finishes responding | yes (keeps it going) |
| `SubagentStart`, `SubagentStop` | subagent spawns or finishes | stop: yes |
| `PreCompact`, `PostCompact` | around context compaction | pre: yes |
| `Notification` | a notification is sent | no |
| `SessionEnd` | session ends | no |
| `FileChanged`, `CwdChanged`, `ConfigChange`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `InstructionsLoaded`, `UserPromptExpansion`, `PostToolBatch`, others | see the live page | varies |

## Matchers

- Letters, digits, `_`, `-`, spaces, `,` and `|` are an exact list: `"Edit|Write"`.
- Anything else is a regular expression: `"^Notebook"`, `"mcp__memory__.*"`.
- Tool events match the tool name. `SessionStart` matches `startup`, `resume`, `clear`, `compact`. `SubagentStart` matches the agent type. `Notification` matches the notification type.
- Omit the matcher, or use `"*"`, to match every occurrence.

## Handler types

| `type` | Use for |
|---|---|
| `command` | A script that reads JSON on stdin. Deterministic. The default choice |
| `http` | POST the event to a URL; 2xx with a JSON body is parsed like command output |
| `mcp_tool` | Call a tool on a configured MCP server |
| `prompt` | A one-turn model judgment (`$ARGUMENTS` is the event JSON). For policy that is easier to describe than to code |
| `agent` | A subagent that can read files (experimental) |

Default timeouts: 600 s for command, http, mcp_tool; 30 s for prompt; 60 s for agent. Set a short `timeout` on anything in the hot path.

## Exit codes and JSON output

- **Exit 0:** success. Stdout that starts with `{` and ends with `}` is parsed as JSON. Other stdout is context for `UserPromptSubmit` and `SessionStart`, and otherwise goes to the debug log.
- **Exit 2:** blocks the action on events that can block. The reason is stderr (or the JSON `reason`). JSON `allow` cannot override it.
- **Any other exit:** a non-blocking error; the action proceeds.
- Stdout must be only the JSON. A shell profile that prints on startup corrupts it.
- Each text field is capped near 10,000 characters.

Fields:

| Need | Output |
|---|---|
| Allow, ask or deny a tool call | `PreToolUse`: `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow\|deny\|ask\|defer","permissionDecisionReason":"..."}}` |
| Rewrite a tool call | `PreToolUse` with `"updatedInput": {...}` |
| Add context for the model | `hookSpecificOutput.additionalContext` on `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop` |
| Block a prompt, or keep Claude working on `Stop` | `{"decision":"block","reason":"..."}` |
| Stop everything | `{"continue":false,"stopReason":"..."}` |
| Warn the user | `{"systemMessage":"..."}` |
| Decide a permission dialog | `PermissionRequest`: `hookSpecificOutput.decision.behavior` = `allow` or `deny` |

A `Stop` hook that blocks can loop forever; check `stop_hook_active` in its input and exit 0 when it is true.

## Placeholders and environment

- `${CLAUDE_PROJECT_DIR}`: the project root. Quote it in commands; paths can contain spaces.
- `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`: a plugin's install and data folders.
- `CLAUDE_ENV_FILE` on `SessionStart`: append `export VAR=value` lines to persist environment variables.
- Input on stdin always includes `session_id`, `cwd`, `transcript_path`, `permission_mode`, `hook_event_name`. Tool events add `tool_name` and `tool_input` (for Bash `tool_input.command`; for Edit and Write `tool_input.file_path`). `UserPromptSubmit` adds `prompt`.

## Debugging

- `claude --debug-file <path>` logs each hook with input, output, timing and errors.
- If nothing fires, remove the matcher first, confirm the bare hook runs, then narrow it.
- Run the script by hand with `scripts/try-hook.mjs` before wiring it in.
