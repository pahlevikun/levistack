---
name: manage-stack
description: "Add or change a skill, rule, agent, command, or hook in the levistack catalog, then sync and check. Use when editing this repo's skills/, agents/, rules/, commands/, or hooks/, or when npm run sync or npm run check fails."
---

# Manage this stack

A catalog change that stays in the source tree and passes sync, validate, and tests.

This skill maintains levistack. It is not part of the published catalog. Do not copy it into `skills/`.

## When to use
- Adding or editing a skill, rule, agent, command, or hook in this repository
- Fixing a `npm run sync` or `npm run check` failure caused by that tree
- Not for: applying one of the published skills to some other project

## Project agent surface (this repo only)
- **Source:** `.cursor/agents/`, `.cursor/rules/`, `.cursor/skills/` (for example `manage-stack`, `repo-maintainer`).
- **Claude:** `.claude/agents`, `.claude/rules`, and `.claude/skills` are directory symlinks to `.cursor/`. `npm run sync` recreates them. Never edit through `.claude/`; change `.cursor/` instead.

## Steps
1. Classify the change and follow one section below. Edit only `skills/`, `agents/`, `rules/`, `commands/`, and `hooks/` for the published catalog, or `.cursor/{agents,rules,skills}/` for stack tooling.
2. Lint any skill or agent you touched.
3. Run the verify commands. If sync rewrites a file, keep that rewrite; do not hand-edit it.

## Add or edit a skill
1. Put it at `skills/<group>/<name>/SKILL.md`. `name` in the frontmatter equals `<name>`.
2. The group needs `skills/<group>/DESCRIPTION.md` with a one-line `description`.
3. `description` says what it does, then "Use when ...", is quoted, and is at most 1024 characters.
4. Lint: `node skills/agent-authoring/create-agent/scripts/lint.mjs skills/<group>/<name>`

## Add or edit a rule
1. Write `rules/<topic>/<name>.md` with `description`, `alwaysApply`, and `globs` only when the rule is file-scoped.
2. `npm run sync` writes `generated/cursor/rules/<topic>-<name>.mdc`. Do not edit that file.
3. Only `alwaysApply: true` rules in `rules/core/` are injected by the `session-start` hook.

## Add or edit an agent
1. Write `agents/<name>.md`. `name` equals the filename without `.md`. `description` says when to call it.
2. Add a row to the roster in `docs/agents/README.md`.
3. Lint: `node skills/agent-authoring/create-agent/scripts/lint.mjs agents/<name>.md`

## Add or edit a command
1. Write `commands/<name>.md` with a one-line `description`.
2. Sync. The command is picked up from that file; there is no second copy to edit.

## Add or edit a hook
1. Add `hooks/<name>.mjs` exporting `meta` and a default handler. Shared code goes in `hooks/lib/`.
2. `npm run sync` regenerates `hooks/hooks.json` and the table in `hooks/README.md`.
3. Hooks are opt-in: `touch ~/.levistack/<name>.on`. A handler returns a result from `hooks/lib/result.mjs` and exits 0 unless it is a deliberate blocker.

## Verify
```
npm run sync && git diff --exit-code
npm run validate
npm test
```
`git diff --exit-code` fails when sync changed a generated file. Stage that generated change with the source edit; do not revert it and do not hand-edit it.

## Do not
- Hand-edit `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`, `skills/<group>/.claude-plugin/`, `generated/`, `hooks/hooks.json`, or the generated tables in `README.md` and `hooks/README.md`.
- Commit, push, or add employer names, secrets, or personal paths.
- Invent a second procedure. The source-of-truth list above is the whole write surface.

## Done when
- The only hand-written edits are under `skills/`, `agents/`, `rules/`, `commands/`, `hooks/`, or `docs/agents/README.md`.
- Lint reports no errors on every skill or agent you changed.
- Sync is idempotent, validate prints no errors, and `npm test` passes.
