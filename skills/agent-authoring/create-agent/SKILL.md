---
name: create-agent
description: "Create, audit or improve subagents (agents/*.md for Claude Code and Cursor). Use when asked to add or review a subagent, fix an agent description that never delegates, or choose its tools and model. Not for skills (use create-skill)."
---

# Create subagents

A **subagent** is a Markdown file whose body is a system prompt. It runs in its own context, optionally with fewer tools or another model, and returns a summary.

Related skills in this group: `create-skill` (SKILL.md folders), `create-rule`, `create-hook`, `create-command`, `convert-as-skill`, and `create-agents-md` (AGENTS.md).

## Principles

1. **The description is the router.** The model decides to delegate from `description` alone. Write what it does, when to use it, and the words a user would say.
2. **Assume the model is smart.** Add only what it lacks: your conventions, your commands, the traps. Cut explanations of common knowledge.
3. **One job per agent.** If it needs "and", split it. If two overlap, merge them.
4. **Smallest authority.** Grant the fewest tools and the smallest model that works. Read-only unless it must write.
5. **Keep the prompt short.** About 80 lines. Link to rules and references instead of pasting them.
6. **Test by using it.** An untested description is a guess.

## Choose the right mechanism

| Need | Use |
|---|---|
| Isolate noisy or parallel work, restrict tools, use a cheaper model | **Subagent** |
| A reusable procedure or knowledge, loaded when relevant | **Skill** (`create-skill`) |
| Facts true for the whole repo, always in context | `AGENTS.md` (`create-agents-md`) or a rule (`create-rule`) |
| Must happen every time, not model-decided | **Hook** (`create-hook`) |
| A saved prompt you type as `/name` | A command (`create-command`) |

A skill can run as a subagent: in Claude Code set `context: fork` and `agent: <type>` (see `create-skill`).

## What do you want to do?

1. **New subagent** → [New subagent](#new-subagent)
2. **Audit existing agents** → [Audit](#audit)
3. **New or oversized skill** → use `create-skill`

Infer the intent from the request; ask only if it is unclear. If the conversation already described a recurring task, derive the agent from it instead of asking again.

## New subagent

1. **Check for overlap.** List the existing agents (project, user, plugin). Extend or merge before creating. A large roster of vague agents makes delegation worse.
2. **Pick the location.** Shared with the team: the project's `agents/` (plugin) or `.claude/agents/` / `.cursor/agents/`. Personal: `~/.claude/agents/` or `~/.cursor/agents/`. Cursor also reads `.claude/agents` and `.codex/agents`, so one file can serve several tools. See [subagents.md](references/subagents.md).
3. **Write the frontmatter** from [templates/subagent.md](templates/subagent.md): `name`, a `description` that says *when to call it*, `tools` (or `readonly`), and `model` only if the work is mechanical.
4. **Write the body** as a short system prompt: mission, the inputs the caller must pass, numbered steps, how to verify, the output format, an explicit "Do not" list. About 80 lines at most.
5. **Lint** with `node scripts/lint.mjs <file>`.
6. **Test:** ask for it by name ("use the X subagent to ..."), then give a task that should delegate on its own. Adjust the description until it triggers on the second and not on unrelated tasks.

## Audit

1. Run `node scripts/lint.mjs <path>` on an agent file or a directory of agents. The same linter also checks skill folders (`create-skill` uses it).
2. Walk the checklist in [audit.md](references/audit.md) for what a linter cannot judge (is the description specific, are the steps actionable, is the tool list minimal).
3. Report a score and findings by priority, each with a concrete fix: **Broken** (will not load or trigger), **Weak** (loads but misroutes or wastes context), **Polish**.
4. Apply only the fixes the user asked for. Preserve the author's structure and voice.

## Done when

- `name` matches the filename; `description` states when to call it; the linter reports no errors.
- Tools and model are the minimum that works.
- It was exercised at least once on a real task, and the description triggered correctly.
- No overlap with an existing agent, or the overlap was merged.
