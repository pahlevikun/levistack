# Subagents: formats, fields and patterns

Verified on 2026-10-04 against https://code.claude.com/docs/en/sub-agents and https://cursor.com/docs/subagents. Fields change between versions; re-check before relying on an edge case.

## Where they live

| Tool | Locations, highest precedence first |
|---|---|
| **Claude Code** | managed settings, `--agents` CLI JSON, `.claude/agents/` (project, found by walking up from the working directory), `~/.claude/agents/`, a plugin's `agents/` |
| **Cursor** | project: `.cursor/agents/`, `.claude/agents/`, `.codex/agents/`; user: `~/.cursor/agents/`, `~/.claude/agents/`, `~/.codex/agents/`. `.cursor/` wins over `.claude/` over `.codex/`; project wins over user |

Same `name` in two places: the higher-precedence one wins. One file in `.claude/agents/` is therefore visible to both Claude Code and Cursor.

## Frontmatter

Both tools need only `name` and `description` to be useful. Everything else is optional and tool-specific.

**Claude Code**

| Field | Meaning |
|---|---|
| `name`, `description` | Required. `name` cannot start with `-` or contain `:`; the filename need not match |
| `tools` / `disallowedTools` | Allowlist or denylist. Omit `tools` to inherit all. MCP patterns: `mcp__server`, `mcp__server__*` |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, `manual` |
| `maxTurns`, `effort`, `isolation: worktree`, `background`, `color`, `initialPrompt` | Run controls |
| `skills` | Skills preloaded in full at startup |
| `mcpServers`, `hooks`, `memory` (`user`/`project`/`local`), `omitClaudeMd`, `experimental` | Advanced |

**Cursor**

| Field | Meaning |
|---|---|
| `name` | Optional; lowercase letters and hyphens; defaults to the filename |
| `description` | Drives automatic delegation |
| `model` | `inherit` (default) or a model ID with optional parameters, such as `id[fast=false,effort=high]` |
| `readonly` | `true` makes the agent read-only |
| `is_background` | `true` returns immediately and runs in parallel |

**Portable subset:** `name` and `description`. Model values and tool names differ between tools (Claude's tools are `Read`, `Grep`, `Glob`, `Bash`, `Edit`, `Write`; "Shell" is not a Claude tool name). When one file serves several tools, either omit `model`, or confirm the value resolves in each.

## The description drives delegation

The model reads descriptions to decide whether to hand work over. A good one:

- says **when**: "Use after writing or modifying code", "Use when a test fails";
- names the **output** or the specialty in the first clause;
- adds "use proactively" if it should trigger without being asked;
- stays short, because every description is loaded all the time (Claude warns when the combined total passes 15,000 tokens).

```yaml
# Too vague
description: Helps with code
# Specific
description: Expert code reviewer. Use proactively after writing or modifying code to catch bugs, missing tests and security issues.
```

## Tools, models and authority

- Give read-only agents `Read, Grep, Glob` (plus `Bash` only to run `git` or tests); in Cursor use `readonly: true`.
- Only implementers get `Write` and `Edit`.
- Pin a small model (`haiku`) only for mechanical work: bulk reading, template filling. Keep planning, review and security on the default model.
- Background subagents in Claude Code get a narrower tool set; foreground ones get the full set.
- Do not put keys, provider URLs or personal paths in an agent file.

## Limits to design around

- **Claude Code:** subagents can spawn subagents up to 3 levels (default; `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`), at most 20 concurrently.
- **Cursor:** the main agent and its direct subagents can launch subagents; a subagent launched by another cannot launch further.
- Tell every subagent whether it may dispatch others. The safe default is no.
- A subagent starts with no memory of the conversation. Everything it needs goes in the prompt or the files it can read.

## Body: a short system prompt

```markdown
You are a <role>. <One sentence on the job and the output.>

When invoked:
1. <First action, usually reading the diff or the named files.>
2. <Next step.>

Inputs you must receive: <goal>, <file ownership>, <success command>.

Report:
- <Output format, ordered by priority.>

Do not: <edit outside ownership>, <commit>, <spawn another agent>.
```

Keep it under about 80 lines. Link to project rules instead of pasting them. Read-only agents should say so and say where judgment calls go ("hand security questions to `security-reviewer`").

## Patterns that work

- **Reviewer:** read the diff, apply a checklist, report by priority with a fix for each, say "clean" when it is.
- **Locator/explorer:** read-only, returns `path:line` bullets, never file contents.
- **Implementer:** needs an ownership list and a success command; verifies before reporting.
- **Cheap mechanical:** small model, literal instructions, stops and reports on anything missing instead of guessing.

## Anti-patterns

- Dozens of generic agents. Start with two or three focused ones.
- A vague description ("helps with coding").
- Duplicating a slash command: make it a command instead (`create-command`).
- An agent that both plans and implements, or reviews its own work.
- Full tool access "just in case".
- Hand-written ownership of the same files by two parallel agents.
