# Rule and command conversion mapping

Subagents are in `subagent.md`; conversations are in `conversation.md`.

## Contents
- Source and destination locations
- Rule to skill
- Command to skill
- Behavior that changes
- Undo

## Source and destination locations

| Kind | Sources | Destinations |
|---|---|---|
| Rules | `.cursor/rules/**/*.mdc`, `.claude/rules/**/*.md`, `rules/<topic>/*.md` in a catalog | `.cursor/skills/<name>/`, `.claude/skills/<name>/`, `.agents/skills/<name>/`, or `skills/<group>/<name>/` |
| Commands | `.cursor/commands/*.md`, `.claude/commands/**/*.md`, `~/.cursor/commands/`, `~/.claude/commands/`, `commands/*.md` in a catalog or plugin | the same destinations, user level at `~/.claude/skills/` or `~/.cursor/skills/` |

Rules can sit in nested folders; search recursively. Ignore `~/.cursor/worktrees` and any built-in `skills-cursor` folder.

## Rule to skill

```markdown
# before: .cursor/rules/api-style.mdc
---
description: "REST API conventions for handlers and responses"
globs:
alwaysApply: false
---
# API style
Body...
```

```markdown
# after: .cursor/skills/api-style/SKILL.md
---
name: api-style
description: "REST API conventions for handlers and responses"
---
# API style
Body...
```

- `name` is the filename without its extension. Under a catalog `rules/<topic>/`, the name is `<topic>-<file>`, matching the generated Cursor name.
- `globs`, `alwaysApply` and any other keys are removed. The script reports dropped keys.
- If the description reads like a label ("API style") rather than a trigger, rewrite it as what it does plus `Use when ...`.

## Command to skill

```markdown
# before: .cursor/commands/commit.md
# Commit current work
Instructions...
```

```markdown
# after: .cursor/skills/commit/SKILL.md
---
name: commit
description: "Commit current work"
disable-model-invocation: true
---

# Commit current work
Instructions...
```

- `name` is the path under `commands/` joined with `-` (`frontend/component.md` becomes `frontend-component`; Claude Code called it `/frontend:component`).
- An existing `description` is kept. With none, the first line is used as a draft and flagged.
- `disable-model-invocation: true` keeps it manual, as a command is.
- Keys such as `argument-hint`, `arguments`, `allowed-tools` and `model` are kept as written.
- `$ARGUMENTS` and `$0`, `$1` work the same in a skill.

## Behavior that changes

| Change | Effect |
|---|---|
| Rule becomes a skill | Loaded when the description matches the task, not by file or on every session. Test that the trigger fires |
| Rule with `globs` becomes `paths` | A skill's `paths` limits when it is offered; it does not inject the rule on every file read the way a rule does |
| Command becomes a skill | Same `/name`. If a command and a skill share a name, the skill runs, so the old command file is dead weight |
| Dynamic injection (`!` before a backticked command) | Still runs for user-owned skills; plugin-supplied and synced ones do not run it |
| Catalog `commands/` entry becomes a skill | The plugin that shipped `/name` now ships it as a skill; update any README or manifest text that lists commands |

## Undo

The script never touches the sources, so undoing a conversion means deleting the new skill folder. If the originals were deleted at the user's request, restore them from version control (`git checkout -- <path>`) or recreate the rule from the skill: add back the `globs` and `alwaysApply` lines that were dropped.
