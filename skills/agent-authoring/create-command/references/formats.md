# Command formats

Claude Code details checked 2026-10-04 against https://code.claude.com/docs/en/skills. Cursor commands are plain Markdown files in `.cursor/commands/`; the Cursor commands page was not available when this was written, so confirm frontmatter behavior in your version.

## Contents
- Locations and names
- Frontmatter (Claude Code)
- Arguments
- Dynamic context
- Precedence and migration
- Example

## Locations and names

| Tool | Location | Name |
|---|---|---|
| Claude Code | `.claude/commands/<name>.md`, `~/.claude/commands/<name>.md`, a plugin's `commands/` | filename without `.md`; `a/b.md` is `/a:b` |
| Cursor | `.cursor/commands/<name>.md`, `~/.cursor/commands/<name>.md` | filename without `.md` |
| Catalog or plugin | `commands/<name>.md` | the tool that installs it decides |

## Frontmatter (Claude Code)

Commands accept the skill frontmatter except `name` (the filename names it), `paths`, `context`, `agent` and `background`.

| Field | Use |
|---|---|
| `description` | One line: what it does. Quote it. Shown in the `/` menu |
| `argument-hint` | Autocomplete hint, for example `[topic]` or `<file> [--dry-run]` |
| `arguments` | Named positional arguments, for example `[component, from, to]` |
| `allowed-tools` | Tools pre-approved for this command's turn only, for example `Bash(git add *) Bash(git commit *)` |
| `disallowed-tools` | Tools removed for the turn |
| `disable-model-invocation` | `true` stops the model from running it on its own |
| `user-invocable` | `false` hides it from the `/` menu |
| `model`, `effort` | Override the session's model or effort |

Keep frontmatter values quoted when they contain `:` or `#`.

## Arguments

- `$ARGUMENTS` is everything typed after the command name.
- With `arguments: [a, b]`, positional values are available as `$0`, `$1`, ... (zero-based in Claude's docs example), or `$ARGUMENTS[N]`.
- Always say what to do when the arguments are empty.

```markdown
---
description: "Migrate a component between languages."
arguments: [component, from, to]
---

Migrate the $0 component from $1 to $2. Keep behavior identical and update its tests.
```

## Dynamic context

A backticked command prefixed with `!` (or a fenced block that starts with `!`) is run before the model sees the prompt and its output replaces the text. It runs on the user's machine, so it can fail the whole command, and Claude Code does not run it for plugin-supplied commands or synced skills (v2.1.228 and later). Keep it out of shared commands, or tell the agent to run the command itself.

## Precedence and migration

- A skill and a command with the same name: the skill wins.
- Existing `.claude/commands/` files keep working. To migrate, move the file to `.claude/skills/<name>/SKILL.md`, add a `name` and a `description` that says when to use it, and add `disable-model-invocation: true` to keep it manual. The `convert-as-skill` skill does this.

## Example

```markdown
---
description: "Write a dated handoff note so a fresh session can continue this work."
argument-hint: "[topic]"
---

Use the handoff skill to write a dated handoff note. Topic: $ARGUMENTS (infer it from the work when empty).

Name the file `YYYY-MM-DD-handoff-<topic-slug>.md` in `handoffs/`. Take the branch and uncommitted files from git. Do not include secrets. Do not commit the file. Reply with the path and a three-line summary.
```
