---
name: create-agent
description: "Create, audit, test or improve subagents (agents/*.md for Claude Code and Cursor), including prompts, tool and model choice, multi-agent orchestration and failure handling. Use when asked to add or review a subagent, fix an agent description that never delegates, choose its tools and model, coordinate several agents, make an agent more reliable, or debug one that misbehaves. Not for skills (use create-skill)."
---

# Create subagents

A **subagent** is a Markdown file whose body is a system prompt. It runs in its own context, optionally with fewer tools or another model, and returns one report.

Related skills in this group: `create-skill` (SKILL.md folders), `create-rule`, `create-hook`, `create-command`, `convert-as-skill`, and `create-agents-md` (AGENTS.md).

## Principles

1. **The description is the router.** The model decides to delegate from `description` alone. Write what it does, when to use it, what it does not cover, and the words a user would say.
2. **Assume the model is smart.** Add only what it lacks: your conventions, your commands, the traps. Cut explanations of common knowledge.
3. **One job per agent.** If it needs "and", split it. If two overlap, merge them.
4. **Smallest authority.** Grant the fewest tools and the smallest model that works. Read-only unless it must write. An agent that reads untrusted content gets no execution.
5. **A subagent cannot ask the user.** It returns one report. Keep questions and confirmations in the main session; make the agent stop and list what is missing, and return open questions and assumptions in its report ([prompts.md](references/prompts.md)).
6. **Keep the prompt short.** About 80 lines. Link to rules and references instead of pasting them.
7. **Fail visibly.** The report says what was covered and what was not. A silent partial result is worse than an error ([reliability.md](references/reliability.md)).
8. **Test by using it.** An untested description is a guess ([testing.md](references/testing.md)).

## Choose the right mechanism

| Need | Use |
|---|---|
| Isolate noisy or parallel work, restrict tools, use a cheaper model | **Subagent** |
| A reusable procedure or knowledge, loaded when relevant | **Skill** (`create-skill`) |
| Facts true for the whole repo, always in context | `AGENTS.md` (`create-agents-md`) or a rule (`create-rule`) |
| Must happen every time, not model-decided | **Hook** (`create-hook`) |
| A saved prompt you type as `/name` | A command (`create-command`) |
| A single small task on 10 lines of code | Do it in the main session; do not delegate |

A skill can run as a subagent: in Claude Code set `context: fork` and `agent: <type>` (see `create-skill`).

## What do you want to do?

| Request | Go to |
|---|---|
| New subagent | [New subagent](#new-subagent) |
| Audit existing agents | [Audit](#audit) |
| Write or tighten the prompt | [prompts.md](references/prompts.md) |
| Several agents working together, or a plan run by agents | [orchestration.md](references/orchestration.md) |
| Make an agent more reliable, or stop it losing context | [reliability.md](references/reliability.md) |
| Test an agent, or find out why it misbehaves | [testing.md](references/testing.md) |
| Fields, locations, limits | [subagents.md](references/subagents.md) |
| New or oversized skill | `create-skill` |

Infer the intent from the request; ask only if it is unclear. If the conversation already described a recurring task, derive the agent from it instead of asking again.

## New subagent

1. **Check for overlap.** List the existing agents (project, user, plugin). Extend or merge before creating. A large roster of vague agents makes delegation worse.
2. **Pick the location.** Shared with the team: the project's `agents/` (plugin) or `.claude/agents/` / `.cursor/agents/`. Personal: `~/.claude/agents/` or `~/.cursor/agents/`. Cursor also reads `.claude/agents` and `.codex/agents`, so one file can serve several tools. See [subagents.md](references/subagents.md).
3. **Write the frontmatter** from [templates/subagent.md](templates/subagent.md): `name`, a `description` that says *when to call it*, `tools` (or `readonly`), and `model` only if the work is mechanical.
4. **Write the body** as a short system prompt: a specific role, the inputs the caller must pass and what to do when one is missing, numbered steps, how to verify, the output format with a covered / not-covered line, an explicit "Do not" list. About 80 lines at most. Wording rules are in [prompts.md](references/prompts.md).
5. **Lint** with `node scripts/lint.mjs <file>`.
6. **Test:** ask for it by name ("use the X subagent to ..."), then give a task that should delegate on its own, then a near-miss that should not. Adjust the description until it triggers on the second and not on the third. Run the case matrix in [testing.md](references/testing.md) for anything that matters.

## Audit

1. Run `node scripts/lint.mjs <path>` on an agent file or a directory of agents. The same linter also checks skill folders (`create-skill` uses it).
2. Read each agent in full and walk the checklist in [audit.md](references/audit.md) for what a linter cannot judge (is the description specific, are the steps actionable, is the tool list minimal). Look for equivalent content under another name before calling anything missing.
3. Report a score and findings by priority with `file:line` and a concrete fix each: **Broken** (will not load or trigger), **Weak** (loads but misroutes or wastes context), **Polish**. Add what to keep.
4. Edit nothing until the user asks; then apply only the fixes they chose, keeping the author's structure and voice.

## Related skills

- `create-skill`: write a skill.
- `create-command`: write a /name prompt.
- `create-hook`: run code on an event.
- `create-rule`: set a rule for every task.

## Done when

- `name` matches the filename; `description` states when to call it; the linter reports no errors.
- Tools and model are the minimum that works.
- It never depends on asking the user, and its report states what it covered.
- It was exercised at least once on a real task, and the description triggered correctly.
- No overlap with an existing agent, or the overlap was merged.
