---
name: create-hook
description: "Create, wire up and test agent hooks: Claude Code settings.json or plugin hooks, Cursor hooks.json, or a shared hooks/ tree. Use when asked to run something automatically on an agent event, block or rewrite a tool call, format after edits, inject session context, or debug a hook that never fires."
---

# Create a hook

A hook is a script or check the harness runs on an agent event. The harness runs it, not the model, so it happens every time. Use a hook to observe, block, rewrite or add context. If the guidance only needs to be remembered, write a rule instead.

## Principles

1. **Hooks are for what must happen every time.** "Always format after an edit", "never run `rm -rf /`". Preferences belong in rules.
2. **Narrowest event, narrowest matcher.** `PreToolUse` on `Bash` is better than a hook on every event. Filter in the script when a matcher gets tricky.
3. **Fail open unless it is a deliberate blocker.** A crash, a timeout or unexpected input should let the action proceed. Reserve blocking (`deny`, exit 2, `failClosed`) for a rule you would defend.
4. **Fast and quiet.** A hook on the hot path runs on every call. Set a short `timeout`, do no network work, and keep stdout to the JSON the harness expects.
5. **Deterministic over clever.** A script beats a `prompt` hook when the result must be auditable. Use a `prompt` hook only for policy that is easier to describe than to code.
6. **Portable.** Prefer Node over shell, and verify every binary the script calls exists on the hook's `PATH`.
7. **Opt-in for personal tooling.** A hook shared through a plugin or repo affects everyone who installs it. Keep it conservative, or gate it behind a flag file.

## Steps

1. **Gather requirements.** Infer from the conversation; ask only for what is missing:
   - **Trigger:** which event, and which tool, command or file it should react to.
   - **Behavior:** audit, block, ask, rewrite input, inject context, or continue a workflow.
   - **Scope:** this user, this project, or a shared plugin or catalog.
   - **Failure:** fail open or closed.
2. **Pick the target.**

   | Target | Config | Reference |
   |---|---|---|
   | Claude Code, project or user | `.claude/settings.json`, `~/.claude/settings.json` | [claude-code.md](references/claude-code.md) |
   | Claude Code plugin | `hooks/hooks.json` | [claude-code.md](references/claude-code.md) |
   | Cursor | `.cursor/hooks.json`, `~/.cursor/hooks.json` | [cursor.md](references/cursor.md) |
   | A shared hooks tree (`hooks/<name>.mjs` with a launcher) | the tree's own convention | its `hooks/README.md` |

   If a repo already has hooks, extend its setup and keep unrelated entries.
3. **Choose the event** from the table in the reference for your target. Check what that event can return; not every event can block.
4. **Write the script** (Node by default). Read the JSON from stdin, decide, print only the output JSON, and exit 0. Block with the event's documented decision or with exit 2, never with prose on stdout. Ambiguous input returns allow.
5. **Wire it up** with the smallest matcher that works. Start with no matcher or a simple one and tighten after it fires. Quote path placeholders (`"$CLAUDE_PROJECT_DIR"`), because paths contain spaces.
6. **Try it by hand** before the harness does:

   ```bash
   node scripts/try-hook.mjs --event PreToolUse --tool Bash --command "git push --force" --expect ask -- node .claude/hooks/guard.mjs
   ```

   It builds a Claude Code payload, runs the command, and reports the exit code, the decision and any invalid JSON. `--json '<payload>'` sends a raw payload for other events or for Cursor. Run it for one input that should trigger and one that should pass. A hook behind an opt-in flag file reports allow until the flag exists.
7. **Trigger it for real** in a session and read the harness's hook log (`claude --debug-file <path>`, or Cursor's Hooks tab). Confirm the matcher matched.
8. **Check the repo's gates.** In a catalog with its own hook tests or sync step, add a test and run them.

## Output at a glance

| Goal | Claude Code | Cursor |
|---|---|---|
| Allow | exit 0, no output | `{"permission":"allow"}` |
| Ask the user | `PreToolUse` `permissionDecision: "ask"` | `{"permission":"ask"}` |
| Block | `permissionDecision: "deny"` or exit 2 with a stderr reason | `{"permission":"deny"}` or exit 2 |
| Add context | `hookSpecificOutput.additionalContext` | `additional_context` (post events) |

## Do not

- Print anything but JSON on stdout (a shell profile banner also breaks it).
- Block on an ambiguous or unparseable input.
- Add a `Stop` hook that blocks without checking `stop_hook_active`; it can loop.
- Put secrets or personal paths in a shared hook, or call the network in a hot-path hook.
- Overwrite a user's existing `settings.json` hooks; merge.

## Related skills

- `create-rule`: a request is enough and nothing must be enforced.
- `create-command`: the action should run on /name, not on an event.
- `create-skill`: the automation needs a procedure the model follows.
- `create-agent`: the event should start a delegated job.

## Done when

- The event, matcher and handler are the narrowest that work.
- `try-hook.mjs` shows the expected decision for one triggering input and one passing input.
- It fired in a real session, and the log shows the expected result.
- It fails open on bad input, unless blocking is its stated purpose.
