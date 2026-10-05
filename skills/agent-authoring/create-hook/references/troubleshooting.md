# Hook troubleshooting

Work from the symptom. Change one thing at a time, and run the script by hand before blaming the harness.

## Contents
- First: see what the harness saw
- The hook never fires
- It fires and fails
- A prompt hook misbehaves
- It blocks too much
- The agent loops on Stop
- Output is missing or garbled
- It is slow
- Environment and paths
- A debugging routine

## First: see what the harness saw

Claude Code: `claude --debug-file <path>` logs each hook with the matcher query, how many hooks matched, the command, its input and output, the exit status and the timing. Cursor: the Hooks tab and the Hooks output channel. Read the log before guessing.

## The hook never fires

| Check | How |
|---|---|
| Is the config file read? | Claude Code reads `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, a plugin's `hooks/hooks.json`, and skill or agent frontmatter. Cursor reads `.cursor/hooks.json` or `~/.cursor/hooks.json`. A file with the wrong name or in the wrong folder is ignored |
| Is the JSON valid? | `node -e "JSON.parse(require('fs').readFileSync('.claude/settings.json','utf8'))"`. A trailing comma or an unquoted key breaks the whole file, and every other setting with it |
| Is `disableAllHooks` set? | Look in every settings layer |
| Does the matcher match? | Tool names are case-sensitive (`Bash`, not `bash`). Letters, digits, `_`, `-`, spaces, `,` and `\|` make an exact list; anything else is a regular expression. In a regular expression `*` repeats the previous character, so `mcp__memory__*` is not a glob: write `mcp__memory__.*`. In Cursor, matchers are JavaScript regular expressions |
| Is the event right? | `PostToolUse` cannot stop a tool; `Stop` fires when the agent finishes, not on every message |
| Is it behind a flag file? | A hook gated on an opt-in file does nothing until that file exists |
| Is the `if` filter too tight? | Remove it and see whether the hook fires |

Bisect: remove the matcher and the `if`, confirm the bare hook fires, then narrow again.

Test a matcher on its own: `node -e "console.log(/mcp__memory__.*/.test('mcp__memory__store'))"`.

## It fires and fails

Run the exact command by hand with a sample payload:

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"ls"}}' | node .claude/hooks/guard-bash.mjs; echo "exit=$?"
```

or use `scripts/try-hook.mjs`, which also reports how the harness would read the result.

| Symptom | Cause and fix |
|---|---|
| `command not found` | The binary is not on the hook's `PATH`. Check with `command -v <tool>`; use Node to avoid `jq`; use an absolute path |
| `permission denied` | The script is not executable (`chmod +x`), or you ran it directly instead of `node script.mjs` |
| Works by hand, fails in the harness | Different working directory or environment. Use `$CLAUDE_PROJECT_DIR` for the script path and `cwd` from the payload for the project |
| Non-zero exit but nothing blocked | Only exit 2 blocks. Any other non-zero exit is a non-blocking error and the action proceeds |
| Timeout in the log | Raise `timeout` (seconds, not milliseconds), or make the script quicker, or run slow work in the background and return at once |
| Path with a space breaks | Quote it: `node "$CLAUDE_PROJECT_DIR/.claude/hooks/x.mjs"` |

## A prompt hook misbehaves

| Symptom | Cause and fix |
|---|---|
| Blocks everything, or nothing | The criteria are vague. Name what is blocked and what is allowed, and what to do when unsure |
| Sees nothing to judge | `$ARGUMENTS` is missing from the prompt |
| Hook error about the reply | The model answered in prose. Say "reply with only the JSON the protocol requires" and give the exact shape from the hooks documentation for your version |
| Different answer each time | Expected. If you need repeatability, write it as a command hook |

## It blocks too much

1. Feed it inputs that should pass and see which one is stopped. The cause is usually a pattern that is too broad (`*rm*` matches `format`, `farm`).
2. Default to allow. Compute `decision = allow`, then change it only on a specific, explainable match.
3. Anchor patterns and parse the command rather than substring-matching it.
4. On any parse problem, allow. A hook that blocks on its own bug stops the whole session.

## The agent loops on Stop

A `Stop` hook that returns `decision: "block"` makes the agent continue; if the condition is still true it blocks again, forever. Read `stop_hook_active` from the input and exit 0 without a decision when it is true. `scripts/recipes/stop-gate.mjs` does this. In a prompt hook, state the same rule in the prompt.

## Output is missing or garbled

- Stdout must be only the JSON. A shell profile that prints a banner, a stray `console.log`, or a progress line corrupts it. Send diagnostics to stderr.
- Plain stdout is added to the context only for `UserPromptSubmit` and `SessionStart`; elsewhere it goes to the debug log.
- A message for the user goes in `systemMessage`. A reason for the model goes in the decision's reason field or `additionalContext`.
- Each text field is capped at roughly 10,000 characters.
- Validate with `echo '<json>' | node -e "JSON.parse(require('fs').readFileSync(0,'utf8'))"`.

## It is slow

A hook on the hot path runs on every call. Narrow the matcher and the `if` filter, drop network calls, avoid starting heavy tools (a formatter launched through a package runner can take a second), set a short `timeout`, and move slow work to `Stop` or into the background. Prefer one fast check to three slow ones.

## Environment and paths

- `$CLAUDE_PROJECT_DIR` is the project root; `${CLAUDE_PLUGIN_ROOT}` is a plugin's folder. Check the spelling: a wrong name expands to nothing.
- Read the project directory from `cwd` in the payload inside scripts.
- To set a variable for the session, `SessionStart` can append `export` lines to the file named by `CLAUDE_ENV_FILE`.

## A debugging routine

1. Turn on the debug log and trigger the event once.
2. Does the log show the hook matched? If not, fix config, matcher or event.
3. Run the command by hand with the logged input. Does it reproduce?
4. Add `console.error` lines to the script (stderr is safe) and re-run.
5. Check the output with a JSON parser, not by eye.
6. Fix one thing, re-run the real trigger, and read the log again.
7. Test one input that should trigger and one that should pass. Remove the debug lines.
