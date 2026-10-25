# Cursor hooks

Based on the Cursor hooks documentation as summarized in Cursor's built-in `create-hook` skill. Re-check field names against the Hooks tab in your Cursor version before relying on an edge case.

## Contents
- Where hooks live
- File format
- Events
- Matchers
- Input and output
- Prompt hooks
- Testing

## Where hooks live

| Scope | Config | Scripts | Path base |
|---|---|---|---|
| Project | `.cursor/hooks.json` | `.cursor/hooks/*` | the project root: `.cursor/hooks/guard.mjs` |
| User | `~/.cursor/hooks.json` | `~/.cursor/hooks/*` | `~/.cursor/`: `./hooks/guard.mjs` |

Prefer project hooks when the behavior should be shared and committed. Cursor watches `hooks.json` and reloads on save; restart Cursor if a hook still does not load.

## File format

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      { "command": "node .cursor/hooks/guard.mjs", "matcher": "curl|wget", "failClosed": true, "timeout": 10 }
    ]
  }
}
```

Hook fields: `command`, `type` (`command` default, or `prompt`), `timeout` (seconds), `matcher`, `failClosed` (block when the hook crashes, times out or prints invalid JSON), `loop_limit` (for follow-up loops on `stop` and `subagentStop`).

## Events

| Goal | Event |
|---|---|
| Gate or audit shell commands | `beforeShellExecution`, `afterShellExecution` |
| Gate or audit MCP calls | `beforeMCPExecution`, `afterMCPExecution` |
| Block or rewrite any tool call | `preToolUse`; follow-up context on `postToolUse`, `postToolUseFailure` |
| Format files after an edit | `afterFileEdit` |
| Control file reads | `beforeReadFile` |
| Check a prompt before it is sent | `beforeSubmitPrompt` |
| Control or chain subagents | `subagentStart`, `subagentStop` |
| Session setup or audit | `sessionStart`, `sessionEnd` |
| React when the agent finishes | `stop` |
| Observe output or compaction | `afterAgentResponse`, `afterAgentThought`, `preCompact` |
| Inline completion (Tab) | `beforeTabFileRead`, `afterTabFileEdit` |

Use the narrowest event that fits.

## Matchers

JavaScript regular expressions, not POSIX. Use `\s`, not `[[:space:]]`.

- `preToolUse`, `postToolUse`, `postToolUseFailure`: tool type (`Shell`, `Read`, `Write`, `Task`, or `MCP: ...`).
- `subagentStart`, `subagentStop`: subagent type.
- `beforeShellExecution`, `afterShellExecution`: the full command string.
- `beforeReadFile`: `Read` or `TabRead`. `afterFileEdit`: `Write` or `TabWrite`.
- `beforeSubmitPrompt`: the value `UserPromptSubmit`.

If a matcher is tricky, filter inside the script for the first version and add the matcher once it clearly works.

## Input and output

A command hook reads JSON on stdin and may print JSON on stdout.
- Exit 0: success. Exit 2: block, the same as returning a deny. Any other exit: fail open unless `failClosed` is true.
- `preToolUse`: `permission` (`allow`, `deny`, `ask`), `user_message`, `agent_message`, `updated_input`.
- `beforeShellExecution`, `beforeMCPExecution`: `permission`, `user_message`, `agent_message`.
- `postToolUse`: `additional_context`; for MCP also `updated_mcp_tool_output`.
- `subagentStart`: `permission`, `user_message`. `subagentStop`: `followup_message`.

Make the script executable and confirm every helper binary it calls (`jq`, `node`, `python3`) is on `PATH` in the hook environment; use `command -v`. Node scripts avoid the `jq` dependency.

## Prompt hooks

```json
{ "type": "prompt", "prompt": "Is this command read-only? Input: $ARGUMENTS", "timeout": 10 }
```

Use for lightweight policy. Prefer a command hook when the result must be deterministic and auditable.

## Testing

1. Pipe a sample payload into the script: `echo '{"command":"curl x"}' | node .cursor/hooks/guard.mjs; echo "exit=$?"`.
2. Trigger the real action and read the Hooks tab or the Hooks output channel.
3. Edit an existing `hooks.json` minimally; keep unrelated hooks.
