# Command hook or prompt hook?

## Contents
- Decision tree
- Compared
- Writing a prompt hook that behaves
- Combining hooks
- Frequency matters

## Decision tree

```
What does the hook need to decide?
  A yes/no a program can compute (a pattern, a path, a file's existence)  -> command
  Run a tool (formatter, linter, tests, git)                              -> command
  Log, notify, archive                                                    -> command (no decision needed)
  A judgment that is easier to describe than to code                      -> prompt
  A decision that needs to read files first                               -> agent (experimental) or a command that reads them
  Hand the event to another service                                       -> http
  Call a tool on an MCP server                                            -> mcp_tool
```

If you can write the rule as code, write it as code.

## Compared

| | Command | Prompt |
|---|---|---|
| Decides by | Your script | A model reading the event |
| Speed | Milliseconds | Seconds |
| Cost | None | A model call per firing |
| Repeatable and auditable | Yes | No: the same input can differ |
| Understands meaning and context | No | Yes |
| Good for | Operations, formatting, logging, pattern rules, protected paths | Policy such as "is this command read-only?", "is this report complete?" |
| Poor for | Anything that needs interpretation | Simple pattern matching, file operations, notifications, anything on a high-frequency event |

Handler defaults and timeouts are in `references/claude-code.md`.

## Writing a prompt hook that behaves

A model reads your prompt and the event JSON, so the same rules apply as for any instruction.

- **Criteria, not vibes.** "Block if the command deletes files outside the project, forces a push, or writes credentials to a file. Otherwise allow." beats "Is this ok?"
- **Include `$ARGUMENTS`.** It is replaced by the event JSON; without it the model sees nothing to judge.
- **Say the exact reply shape** the hooks documentation specifies for your event and version, and add "reply with only that JSON, no other text". A reply that is not valid JSON fails the hook.
- **Say what to do when unsure.** For a safety check, say whether doubt means allow or ask.
- **On `Stop` hooks, say what to do when `stop_hook_active` is true** (allow), or the hook can loop.
- **Keep it short.** It runs on every matching event.

```json
{ "type": "prompt", "timeout": 20, "prompt": "Event: $ARGUMENTS\n\nIs this shell command read-only? It is read-only if it only reads files or prints output. If it writes, deletes, installs, pushes or contacts the network, it is not. If unsure, treat it as not read-only. Reply with only the JSON the hook protocol requires." }
```

## Combining hooks

Several hooks on one event are normal: a fast command for the deterministic part and a prompt for the judgment part. Do not rely on the order in which they run, and make each safe on its own. If any one blocks, the action is blocked.

## Frequency matters

| Event rate | Handler |
|---|---|
| Every tool call (`PreToolUse`, `PostToolUse`) | Command, with a narrow matcher and a short timeout. A prompt hook here slows every step and costs on every call |
| Once per turn (`UserPromptSubmit`, `Stop`) | A prompt hook is acceptable |
| Once per session (`SessionStart`, `SessionEnd`) | Either |

If a prompt hook is needed on a hot event, filter first with a matcher or the `if` field so it only runs when it can matter.
