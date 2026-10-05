# Hook recipes

Start from the closest recipe, then narrow it. Five are working Node scripts in `scripts/recipes/`, covered by tests; the rest are configuration over a command you already have. Claude Code shapes are shown; for Cursor map the event and the output field using `references/cursor.md`.

## Contents
- The scripts
- Wiring a script
- Configuration-only recipes
- Choosing the event
- Habits every recipe follows

## The scripts

| Script | Event and matcher | What it does | Output |
|---|---|---|---|
| `guard-bash.mjs` | `PreToolUse`, `Bash` | Denies `rm -r` aimed at `/`, `~` or `$HOME`, `mkfs`, writes to a raw disk. Asks before a force push or a hard reset | `permissionDecision` `deny` or `ask` |
| `protect-files.mjs` | `PreToolUse`, `Edit\|Write` | Denies edits to lock files, `.env*`, `credentials.json`, `generated/` | `permissionDecision` `deny` |
| `format-after-edit.mjs` | `PostToolUse`, `Edit\|Write` | Runs the formatter for the file's extension; ignores a missing formatter | none |
| `stop-gate.mjs` | `Stop` | Keeps the agent working while `npm test` fails; does nothing if `stop_hook_active` is true | `decision: "block"` |
| `session-context.mjs` | `SessionStart` | Adds the current branch and `.agent-notes.md` | `additionalContext` |

Edit the constants at the top of each script (the deny lists, the protected patterns, the formatter table, the test command). They fail open: unreadable input exits 0 with no output.

Try one before wiring it:

```bash
node scripts/try-hook.mjs --event PreToolUse --tool Bash --command "rm -rf ~/" --expect block -- node scripts/recipes/guard-bash.mjs
```

A guard like `guard-bash.mjs` is a seat belt, not a sandbox: a determined command can say the same thing another way. For real isolation use the tool's permission rules or a sandbox.

## Wiring a script

Copy the script into `.claude/hooks/` (or ship it in a plugin) and register it with the narrowest matcher:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.mjs\"", "timeout": 5 } ] },
      { "matcher": "Edit|Write", "hooks": [ { "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/protect-files.mjs\"", "timeout": 5 } ] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write", "hooks": [ { "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/format-after-edit.mjs\"", "timeout": 10 } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/stop-gate.mjs\"", "timeout": 100 } ] }
    ]
  }
}
```

Timeouts are in seconds. Quote the path; it can contain spaces. Do not rely on the order in which several matching hooks run.

## Configuration-only recipes

| Goal | Event, matcher | Handler | Notes |
|---|---|---|---|
| Desktop notification when input is needed | `Notification` | `command`: `osascript -e 'display notification "Needs input" with title "Claude Code"'` on macOS, `notify-send "Claude Code" "Needs input"` on Linux | No output needed. Add a sound with `afplay` if you want one |
| Audit every shell command | `PreToolUse`, `Bash` | `command`: a script that appends `{time, tool_name, tool_input.command}` as one JSON line to a log file outside the repo | Observe only; exit 0. Do not log secrets that appear in commands |
| Log every file edit | `PostToolUse`, `Edit\|Write` | Same, with `tool_input.file_path` | |
| Require a conventional commit message | `PreToolUse`, `Bash`, `if: "Bash(git commit *)"` | `command`: parse the `-m` value, deny with the expected format in the reason | Deterministic. Use a `prompt` hook only if the rule needs judgment |
| Run the project's pre-commit checks before a commit | `PreToolUse`, `Bash`, `if: "Bash(git commit *)"` | `command` that runs the checks and denies with their tail on failure | Keep it fast, or move the work to a Stop gate |
| Warn on a risky prompt | `UserPromptSubmit` | `command` that checks the text and returns `additionalContext` or `decision: "block"` | Block rarely: it interrupts the user |
| Check a finished subagent's report is complete | `SubagentStop` | `prompt`: "Does this report give a severity, location and fix for each finding? `$ARGUMENTS`" | Judgment, so a prompt hook is right |
| Archive the transcript | `SessionEnd` | `command` that copies `transcript_path` to a dated file | Cannot block. Keep the destination outside the repo |
| Load per-project context | `SessionStart` | `session-context.mjs`, or a script that prints the context | Keep it short; it is in context every session |
| Only react to one kind of command | any tool event | the `if` field with a permission rule such as `"Bash(rm *)"` | Filters before the script starts |

## Choosing the event

- **Before it happens and you may stop it:** `PreToolUse` (a tool call), `UserPromptSubmit` (a prompt), `PreCompact`.
- **After it happened:** `PostToolUse` for follow-up (format, test, log); it cannot undo the tool.
- **When the agent wants to finish:** `Stop` or `SubagentStop`, and check `stop_hook_active`.
- **Session edges:** `SessionStart` for context, `SessionEnd` for cleanup.
- **Needs the person:** `Notification`.

Use the narrowest event. A hook on every event is a hook on every action.

## Habits every recipe follows

- Read stdin once, parse inside `try`, and on any problem do nothing and exit 0.
- Print only the output JSON on stdout. Reason text for a block goes in the JSON field, or on stderr with exit 2.
- Keep the hot path quick: no network, no full test suite in `PreToolUse`.
- Quote `$CLAUDE_PROJECT_DIR`. Use absolute or project-relative paths, never `./`.
- Never put secrets or personal paths into a hook you share.
- Test with a triggering input and a passing one (`scripts/try-hook.mjs`), then in a real session with the debug log on.
