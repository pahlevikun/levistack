---
name: create-agents-md
description: "Create, audit or refresh AGENTS.md files: the repo root, nested package files, and the user-level global file, for Claude Code, Cursor and Codex. Use when asked to write, improve, split, shrink or migrate AGENTS.md or CLAUDE.md."
---

# Create AGENTS.md

An `AGENTS.md` is a README for coding agents: the commands, conventions and traps an agent cannot infer quickly from the code. One canonical file at the repo root, optional nested files where a package genuinely differs, and an optional personal file for rules that apply to every repo.

## Pick the mode

| The request | Mode |
|---|---|
| "Write / set up AGENTS.md" | **Root** |
| "This package works differently", monorepo | **Nested** |
| "My preferences for every repo" | **Global** |
| "Improve / shrink / it's ignored / out of date" | **Audit and refresh** |
| "We have CLAUDE.md / .cursor/rules / copilot instructions" | **Migrate** |

Infer the mode from the request. Ask only if it is genuinely ambiguous.

## How each tool reads the files

Checked against the tools' docs on 2026-10-04 (sources and re-check steps in [tool-behavior.md](references/tool-behavior.md)). Behavior changes between versions, so treat this as a map and verify with the commands below.

| | Global | Project root | Nested | Notes |
|---|---|---|---|---|
| **Codex** | `~/.codex/AGENTS.md` (`AGENTS.override.md` wins; first non-empty only) | Yes | Walks git root down to the working directory, one file per directory, concatenated root to leaf, closer text last | Stops adding files at 32 KiB combined |
| **Cursor** | None. Personal rules live in Settings → Rules | Yes | Combined hierarchically, more specific wins | Plain Markdown: no frontmatter, no globs |
| **Claude Code** | `~/.claude/CLAUDE.md` | Reads `AGENTS.md` **only if no `CLAUDE.md` exists** in the working directory or above (v2.1.277+) | Subdirectory files load on demand when Claude reads files there | Otherwise import it with `@AGENTS.md` |

Across all of them the agents.md convention holds: the nearest file wins, and an explicit user prompt overrides every file.

## Decide placement

- **Root** holds everything true for the whole repo.
- **Nested** only when a directory has different build or test commands, a different language or framework, stricter rules, or risky areas. A nested file adds or overrides specifics. It never restates the root, and never contradicts it: Codex and Claude put both in context.
- **Global** only for personal preferences that are true in every repo (communication style, tool habits). Never project facts.
- One source of truth. If the repo also needs a `CLAUDE.md`, make it a symlink to `AGENTS.md`, or a two-line file: `@AGENTS.md` plus Claude-only notes.

## Create or refresh (root and nested)

1. **Inspect before writing.** Read build files, scripts, CI config, test and lint config, `README`, `CONTRIBUTING`, recent commit subjects, and every existing instruction file (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`). Run `node scripts/audit.mjs <repo>` to see what already exists and how big it is.
2. **Keep only what an agent cannot get quickly from the code:**
   - exact commands to install, build, run one test, run all tests, lint, format
   - conventions that differ from the language default, with the reason
   - boundaries: what not to touch, generated files, layers that must not import each other
   - traps that look fine and fail later
   - how to verify work, and what "done" means
   - commit, branch and PR rules
3. **Draft from the templates** in [templates.md](references/templates.md). Write instructions a reviewer could check: "Run `npm test -- path` before committing", not "test your changes".
4. **Prove it.** Run each command you wrote, or mark it `(unverified)`. Confirm every path exists.
5. **Keep it short.** Root: aim for 150 lines or fewer. Nested: 60 or fewer. Claude's guidance is under 200 lines per file; Codex's whole chain must fit in 32 KiB.
6. **Run `node scripts/audit.mjs <repo>`** and fix the findings.

## Global mode

Write `~/.codex/AGENTS.md` and/or `~/.claude/CLAUDE.md` with the same short personal preferences. Keep them in one file and import it from the other (`@~/.codex/AGENTS.md` works in a Claude user file). Tell the user that Cursor has no global file and the same text must be pasted into Settings → Rules. Do not write to the user's home directory without saying which file and why.

## Audit and refresh

Run the audit script, then read each file against the content rules below. Report findings by priority:

- **Broken:** commands that fail, paths that do not exist, a `CLAUDE.md` that hides `AGENTS.md` from Claude.
- **Costly:** files over the line or byte budget, text that duplicates the README or the code, stale directory listings.
- **Risky:** secrets, personal paths, contradictions between root and nested files.

Propose the smallest edits. Preserve auto-managed marker blocks and the maintainers' sections.

## Migrate

Merge `CLAUDE.md`, `.cursor/rules`, and copilot instructions into one `AGENTS.md`, deduplicating. Keep file-scoped rules that need globs as Cursor or Claude rules, since `AGENTS.md` has no metadata. Replace the old `CLAUDE.md` with the shim. Do not delete the originals until the user confirms.

## Content rules

**Belongs:** commands, non-default conventions, boundaries, traps with rationale, verification steps, git rules.
**Does not belong:** directory trees and dependency lists (they go stale and the agent can read them), architecture overviews derivable from code, generic advice ("write clean code"), persona text, anything already in the README, long prose, secrets, tokens, personal paths, or `@`-imports of files that may not exist.
Use headings and bullets. Use backticks around any path you do not want imported (`@path` outside backticks is an import in Claude).

## Verify what loaded

- **Codex:** `codex --ask-for-approval never "Summarize the current instructions."`
- **Claude Code:** run `/memory` and look for the file's path.
- **Cursor:** ask the agent to summarize the instructions it has for a file in the target directory.

## Related skills

- `create-rule`: a standard should apply by file glob or path.
- `create-skill`: a long procedure belongs outside AGENTS.md.
- `create-hook`: something must be enforced, not just asked.
- `super-codebase-learner`: the file must describe a codebase you have not read yet.
- `concise`: keep the file short and plain.

## Done when

- The right files exist at the right levels, and nothing is duplicated between them.
- Every command was run or is marked unverified, and every path exists.
- The audit script reports no warnings, or the user accepted the remainder.
- Claude can see the content (symlink or import), and the user knows Cursor has no global file.
