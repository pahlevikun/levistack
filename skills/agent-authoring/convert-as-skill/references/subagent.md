# Subagent to skill

A subagent and a skill are different tools. Converting one loses something, so decide first whether to convert at all.

## Contents
- Keep, wrap or convert?
- What maps and what is lost
- Steps
- Example

## Keep, wrap or convert?

| Goal | Do |
|---|---|
| Give a subagent a `/name` entry point, or let the model load it | **Wrap**: keep the subagent, add a thin skill with `context: fork` that tells it what to do |
| Its knowledge should load into the current context, no isolation needed | **Convert** (below) |
| It exists to isolate noisy work, restrict tools or use a cheaper model | **Keep it a subagent** |

Default to keeping or wrapping. Convert only when isolation and the tool list do not matter.

## What maps and what is lost

| Subagent field | In the skill |
|---|---|
| `name` | `name` (must equal the folder) |
| `description` | `description`. Rewrite if it says only when to call an agent; a skill description should say what it does and `Use when ...` |
| `model` | `model` is kept |
| Body (system prompt) | The body, verbatim. Check it reads as instructions to the current agent, not "You are a separate agent" |
| `tools`, `disallowedTools` | **Lost.** A skill's `allowed-tools` only pre-approves tools; it does not restrict them. Remove tool-limit statements from the body or accept they are advisory |
| `permissionMode`, `maxTurns`, `mcpServers`, `hooks`, `memory`, `skills`, `isolation` | **Lost** |
| Isolated context and a summarized return | **Lost** unless `context: fork` is set |

With `--fork` the converted skill carries `context: fork`, so it runs in a subagent. That subagent is a general-purpose one, not the original definition, so the tool restrictions still do not apply.

## Steps

1. Read the subagent. List the fields from the table that would be lost and say so to the user before converting.
2. Preview: `node scripts/convert.mjs agents/<name>.md --out <skills-dir> --dry-run` (add `--fork` to keep it isolated).
3. Rewrite the description and fix any body lines that speak as a separate agent ("Return a summary to the caller"). Those edits are the one allowed deviation from verbatim; list them.
4. Convert, lint with the `create-skill` linter, and try it on the task the agent was built for.
5. Keep the subagent file until the skill has been tried. Roster docs (for example `docs/agents/README.md`) must change only if the agent is removed, and removal is the user's call.

## Example

```markdown
# before: agents/summarizer.md
---
name: summarizer
description: "Summarizes a long file. Use after a large read."
tools: Read
model: haiku
---
Read the file and return a ten-line summary.
```

```markdown
# after: skills/summarizer/SKILL.md  (--fork)
---
name: summarizer
description: "Summarizes a long file. Use after a large read."
model: haiku
context: fork
---
Read the file and return a ten-line summary.
```

Warnings: `tools` dropped; runs in a general-purpose subagent.
