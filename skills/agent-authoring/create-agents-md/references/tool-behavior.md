# How each tool reads instruction files

Verified on 2026-10-04 against the vendors' documentation. Tool versions change this behavior; re-check before relying on an edge case.

## agents.md convention
Source: https://agents.md/
- A plain Markdown "README for agents". No required fields; any headings.
- Monorepos: nested files are fine. "The closest one takes precedence."
- Explicit user chat prompts override everything.
- Migration: `mv AGENT.md AGENTS.md && ln -s AGENTS.md AGENT.md`.

## Codex
Source: https://learn.chatgpt.com/docs/agent-configuration/agents-md (redirected from developers.openai.com/codex/guides/agents-md)
1. **Global:** `CODEX_HOME` (default `~/.codex`). Checks `AGENTS.override.md`, then `AGENTS.md`. Uses only the first non-empty file.
2. **Project:** from the Git root down to the current directory. In each directory it checks `AGENTS.override.md`, then `AGENTS.md`, then any names in `project_doc_fallback_filenames`. At most one file per directory.
3. **Merge:** concatenated from the root down, joined with blank lines. Files closer to the working directory appear later, so they take precedence.
4. **Limit:** empty files are skipped; adding stops once the combined size reaches `project_doc_max_bytes` (32 KiB by default, set in `~/.codex/config.toml`).
5. **Check:** `codex --ask-for-approval never "Summarize the current instructions."`

## Cursor
Source: https://cursor.com/docs/context/rules
- Supports `AGENTS.md` in the project root and in any subdirectory.
- Nested instructions are combined with parent directories; the more specific wins.
- Plain Markdown: no frontmatter, no globs, no `alwaysApply`. Use `.cursor/rules/*.mdc` when you need scoping.
- There is **no global AGENTS.md**. User Rules live in Settings → Rules.
- The rules page does not mention `CLAUDE.md`.

## Claude Code
Source: https://code.claude.com/docs/en/memory
- Memory files: managed policy, user `~/.claude/CLAUDE.md`, project `./CLAUDE.md` or `./.claude/CLAUDE.md`, local `./CLAUDE.local.md`.
- Files in the working directory and every directory above it load at launch, concatenated from the root down. Subdirectory files load on demand when Claude reads files there.
- **AGENTS.md:** read directly (v2.1.277 or later) only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or above. `~/.claude/CLAUDE.md`, managed files and `.claude/rules/` do not count. Not read: `AGENTS.local.md`, `AGENTS.override.md`, anything under `.agents/`.
- **Share one file:** put `@AGENTS.md` in a `CLAUDE.md` next to it, or symlink. Imports expand at launch, up to four hops deep. Relative paths resolve from the importing file. `@path` inside backticks or a code block is literal.
- Settings: `/config` → Project instructions (`claude-md-or-agents-md` default, `claude-md-and-agents-md`, `claude-md`, `managed-only`).
- Guidance: keep each file under about 200 lines; files over 4 MiB are skipped; block-level HTML comments are stripped before injection.
- Check: `/memory`.

## What this means in practice
| Goal | Do this |
|---|---|
| Every tool sees the same rules | Canonical `AGENTS.md`; `CLAUDE.md` symlink or `@AGENTS.md` import |
| Claude-only extra | Below the `@AGENTS.md` line in `CLAUDE.md` |
| Personal rules, all repos | `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md`; paste into Cursor Settings → Rules |
| Rules scoped to file types | Cursor `.mdc` rules or Claude `.claude/rules/`; `AGENTS.md` cannot scope |
| Stay inside Codex's budget | Keep root plus nested chain well under 32 KiB |

## Re-checking
Fetch the three pages above, or ask each tool to summarize its loaded instructions, and update this file and the table in `SKILL.md` together.
