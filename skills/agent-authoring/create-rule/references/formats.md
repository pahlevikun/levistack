# Rule formats by tool

Claude Code details checked 2026-10-04 against https://code.claude.com/docs/en/memory. Cursor details follow the Cursor rules documentation and existing rule files; confirm an edge case in a session before depending on it.

## Contents
- Claude Code
- Cursor
- Shared catalog (rules/ tree)
- AGENTS.md and CLAUDE.md
- Writing the globs
- Examples

## Claude Code

- **Location:** `.claude/rules/*.md` (project, discovered recursively, subfolders allowed) and `~/.claude/rules/` (every project on the machine). Symlinks work; a symlink that points outside the project needs the user's approval for imports.
- **Frontmatter:** `paths` is the only field Claude Code reads. Every other field (`description`, `alwaysApply`, `globs`) is ignored without an error. It accepts a YAML list or a comma-separated string.
- **Loading:** a rule without `paths` loads at launch with the same priority as `.claude/CLAUDE.md`. A rule with `paths` loads when Claude reads, writes or edits a matching file, not on every tool call.
- **Compaction:** project-root `CLAUDE.md` is re-read after `/compact`. Path-scoped rules reload when a matching file is read again.
- **Bad frontmatter:** if the YAML does not parse, the rule loads as if it had no `paths`. Run `claude --debug` to see the error.

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API rules
- Validate every request body at the handler boundary.
```

## Cursor

- **Location:** `.cursor/rules/<name>.mdc`. A rule may also be a folder with a `RULE.md`. Nested `.cursor/rules/` folders apply to their subtree.
- **Frontmatter:**

| Field | Meaning |
|---|---|
| `description` | What the rule is for. The agent decides from this when `alwaysApply` is false and no `globs` are set |
| `globs` | File patterns. When a matching file is in play, the rule attaches |
| `alwaysApply` | `true` puts the rule in every session |

- **Four modes:** Always (`alwaysApply: true`), Auto-attached (`globs`), Agent-requested (`description` only), Manual (the user mentions the rule by name). A rule with no description, no globs and `alwaysApply: false` is manual only.
- Cursor can also read `AGENTS.md` at the repo root.

```markdown
---
description: "TypeScript error handling conventions"
globs: "**/*.ts"
alwaysApply: false
---

# Error handling
- Throw typed errors with a `cause`; never swallow an exception.
```

## Shared catalog (rules/ tree)

In a catalog repo like this one, rules are authored once as `rules/<topic>/<name>.md` with `description` (quoted, one line), `alwaysApply`, and `globs` only when file-scoped. A sync step writes the Cursor `.mdc` copies into a generated folder; never edit those. Only some always-on rules may be injected by a session-start hook, so check the repo's README before assuming a rule is loaded. Follow the repo's `CLAUDE.md` or maintenance skill for sync and validation commands.

## AGENTS.md and CLAUDE.md

Use them for repo facts every task needs: build and test commands, layout, hard boundaries. Keep each under about 200 lines and link out for depth. See the `create-agents-md` skill. Claude Code can read `AGENTS.md`; a common pattern is a `CLAUDE.md` that imports it.

## Writing the globs

- Quote the value. `**/*.ts` and `{a,b}` need quotes in YAML.
- Be specific: `src/api/**/*.ts` rather than `**/*`.
- Braces expand: `src/**/*.{ts,tsx}`. Claude Code caps the total expansion, so keep brace groups few.
- Match what Claude reads: a path-scoped rule fires on Read, Write and Edit of a matching file.
- One list for `paths`, one string for `globs`. A rule shared by both tools may carry both fields; each tool ignores the other's.

## Examples

Always-on, catalog format:

```markdown
---
description: "Commit only when asked; never push without explicit approval."
alwaysApply: true
---

# Git workflow
- Commit only when the user asks. Do not push unless told to.
```

Good versus bad instruction:

| Weak | Concrete |
|---|---|
| "Write clean error handling" | "Return `Result` from service functions; map errors to HTTP codes only in `handlers/`" |
| "Keep functions small" | "Split a function that needs more than one level of nesting" |
