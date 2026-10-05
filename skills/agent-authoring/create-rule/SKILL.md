---
name: create-rule
description: "Create, audit or tighten persistent rules for coding agents: .claude/rules/*.md, .cursor/rules/*.mdc, a catalog rules/ tree, CLAUDE.md or AGENTS.md. Use when asked to add a rule or coding standard, scope a rule to file globs or paths, fix a rule the agent ignores, or decide whether something is a rule, a skill or a hook."
---

# Create a rule

A rule is a short, standing instruction that is loaded into context, always or when matching files are touched. It guides; it does not enforce. If an action must be blocked every time, use a hook.

## Principles

1. **A rule earns its tokens every session.** If it only matters for one task, make it a skill. If it must be enforced, make it a hook.
2. **One concern per rule, under 50 lines.** Split a long rule by topic.
3. **Say what to do, concretely.** "Use `snake_case` for Python functions" beats "follow naming conventions". Give a good and a bad example when the fix is not obvious.
4. **Give the reason in one clause** when it is not obvious, so the agent can judge edge cases.
5. **Do not restate a linter or formatter.** Point to the tool's command instead.
6. **No contradictions.** Read the existing rules first. Edit an overlapping rule rather than adding a competing one.
7. **Scope as narrowly as is true.** Always-on only for what holds in every task; otherwise scope by globs or by description.
8. **Write it so it binds.** "Always", "never", "only", or "if X, then Y", with the exception named. "Try to", "generally", "consider" and "where appropriate" make the rule optional, and an optional rule is the first one the agent drops. Say what to do for the case a reader would ask about.

## Rule, skill, hook, or AGENTS.md?

| It is... | Use |
|---|---|
| A standing preference or constraint for every task | Always-on rule, or `AGENTS.md` / `CLAUDE.md` for repo facts and commands |
| A convention for certain files (`**/*.ts`, `migrations/**`) | File-scoped rule |
| A procedure with steps, run on demand | Skill (`create-skill`) |
| Must be enforced, blocked or automated | Hook (`create-hook`) |

## Steps

1. **Gather requirements.** Infer from the conversation; ask only for what is missing:
   - what the rule enforces or teaches;
   - scope: always, certain files (concrete globs, not "the backend"), or by description only;
   - target: which tool and which folder (step 3).
   You may write several rules when the conversation covers distinct topics.
2. **Check overlap.** List the rule files in the target tree and read the nearest ones.
3. **Pick the format** by target. Details and frontmatter are in [formats.md](references/formats.md).

   | Target | File |
   |---|---|
   | Claude Code | `.claude/rules/<name>.md`, optional `paths:` |
   | Cursor | `.cursor/rules/<name>.mdc` with `description`, `globs`, `alwaysApply` |
   | A shared catalog | `rules/<topic>/<name>.md`; a sync step may generate the `.mdc` copies |
   | Both tools, one repo | Follow what the repo already does (often one tree symlinked into the other) |

4. **Write it** from [templates/rule.md](templates/rule.md). Lead with the instruction, not a title paragraph. Quote YAML values that contain `:`, `#` or start with `*`.
5. **Check it.** `node scripts/check-rule.mjs <file-or-dir>` catches YAML traps, a rule that can never apply, contradictory scope fields and oversize. In a repo with its own validation (for example `npm run validate`), run that too.
6. **Test it.** Start a fresh session, do a task the rule covers, and confirm it was followed. For a file-scoped rule, open a matching file and a non-matching one. If it is ignored, shorten it, make it more specific, or move enforcement to a hook.

## Audit

1. Run `node scripts/check-rule.mjs <dir>` on the rules tree. It reports YAML traps, rules that can never apply, conflicting scope, oversize, secrets, and hedged wording.
2. Read each rule and the ones beside it. For each, ask: is it one concern? Is the instruction concrete enough to check? Does it contradict another rule? Is it scoped as narrowly as it is true? Should it be a hook (must be enforced), a skill (a procedure), or nothing (the agent already does it)?
3. Report findings by priority with the rule path and a concrete fix: **Broken** (never loads, YAML error, secret), **Weak** (vague, contradictory, too broad, too long), **Polish**. Edit only what the user asks.

## Do not

- Put secrets, personal paths or employer names in a shared rule.
- Write `globs: *.ts` unquoted (YAML reads `*` as an alias). Write `globs: "**/*.ts"`.
- Mark everything `alwaysApply: true`. Always-on rules compete for attention.
- Hedge. A rule that says "try to" or "generally" is a suggestion.
- Duplicate a rule in two folders by hand. Generate or symlink instead.

## Related skills

- `create-hook`: enforce a rule.
- `create-skill`: write a procedure, not a rule.
- `create-agents-md`: put the rule in AGENTS.md.

## Done when

- The file is in the right folder for its tool, with frontmatter that tool reads.
- `check-rule.mjs` reports no errors and the repo's own validation passes.
- The rule is one concern, concrete, and does not contradict another rule.
- The wording is firm and the exception, if any, is named.
- A fresh session followed it on a real task.
