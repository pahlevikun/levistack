# levistack

One source tree of skills, rules, subagents, commands, and hooks for Claude Code, Cursor, Codex, and the skills CLI. `CLAUDE.md` is a symlink to this file.

Human install steps and the skill-group table live in `README.md`.

## Before you change anything

**Maintaining this repository** (anything under the catalog tree or under `.cursor/`):

1. Read and follow `.cursor/skills/manage-stack/SKILL.md`.
2. Prefer the `repo-maintainer` agent (`.cursor/agents/repo-maintainer.md`) for a bounded catalog edit.

**Using the published catalog** (explore, plan, implement, review in this or another repo):

- Load the skill whose `description` matches the task (`skills/<group>/<skill>/SKILL.md`).
- Delegate to a subagent when its `description` fits; roster and flow: `docs/agents/README.md`.
- Apply rules from `rules/` (Cursor: `generated/cursor/rules/` after sync). Project sessions in *this* repo also load `.cursor/rules/` (for example `manage-stack.mdc`).

Do not invent a parallel workflow when a skill, agent, or rule already covers the work.

## Two write surfaces

| Surface | What it is | You edit |
|---|---|---|
| **Catalog** | Shipped by the plugins and `npx skills add` | `skills/`, `agents/`, `rules/`, `commands/`, `hooks/` |
| **Project agent tree** | How agents work *in this repo* only | `.cursor/agents/`, `.cursor/rules/`, `.cursor/skills/` |

Claude Code reads `.claude/agents`, `.claude/rules`, and `.claude/skills` as **directory symlinks** to `.cursor/`. `npm run sync` recreates them. Never add stack tooling under `.claude/`; change `.cursor/` instead.

Catalog rules are authored as `rules/<topic>/*.md`. Sync writes Cursor `.mdc` files to `generated/cursor/rules/` (see `.cursor-plugin/plugin.json`). Only `alwaysApply: true` files in `rules/core/` feed the `session-start` hook (`hooks/README.md`).

## Commands

Requires Node **≥ 20**.

```bash
npm run sync          # manifests, README group table, hooks.json, .claude → .cursor symlinks
npm run check         # sync --check, validate, tests
npm run validate
npm test
npm run check:publish # strict; run before making the repo public
```

**After editing a catalog skill or agent:**

```bash
node skills/agent-authoring/create-agent/scripts/lint.mjs skills/<group>/<name>
node skills/agent-authoring/create-agent/scripts/lint.mjs agents/<name>.md
```

**Local dev (optional):** `./scripts/link-skills.sh` symlinks catalog skills into `~/.claude/skills` and `~/.agents/skills`. **Statusline:** `node scripts/install-statusline.mjs` (see `statusline/README.md`).

## Verify before reporting done

```bash
npm run sync && git diff --exit-code   # fail = generated output changed; stage it with your source edit
npm run validate
npm test
claude plugin validate . --strict      # when plugin manifests or the tree changed
```

Do not commit or push unless asked.

## Boundaries

- **Edit only** catalog paths above, plus `docs/agents/README.md` when the agent roster changes, and `.cursor/` for stack tooling.
- **Never hand-edit** `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`, `skills/<group>/.claude-plugin/`, `generated/`, `hooks/hooks.json`, or the generated tables in `README.md` and `hooks/README.md`. Run `npm run sync`.
- Skill folder name = frontmatter `name`. `description` is one quoted line, ≤ 1024 characters, and says when to use the skill.
- No employer-owned content, secrets, or personal paths. No `THIRD_PARTY.md`, `UPSTREAM.md`, or other import-provenance manifests in this catalog.

## Where to look

| I want to… | Look at… |
|---|---|
| Add or change a shipped skill | `skills/<group>/<name>/SKILL.md` plus that group's DESCRIPTION.md; follow `manage-stack` |
| Add or change a catalog subagent | `agents/<name>.md`, `docs/agents/README.md` |
| Add or change a rule | `rules/<topic>/<name>.md` |
| Add a slash command | `commands/<name>.md` |
| Add or change a hook | `hooks/<name>.mjs`, `hooks/lib/`, `hooks/README.md` |
| Change how this repo is maintained | `.cursor/skills/manage-stack/`, `.cursor/rules/manage-stack.mdc` |
| Understand sync / validate | `scripts/sync.mjs`, `scripts/validate.mjs` |
| Install or group list | `README.md` |

## Runtime entry points

| Runtime | Reads |
|---|---|
| Skills CLI | `skills/**/SKILL.md` via `npx skills add` |
| Claude Code plugin | `.claude-plugin/`, per-group `skills/<group>/.claude-plugin/` |
| Claude Code (this repo) | `.claude/{agents,rules,skills}` → `.cursor/`, this file via `CLAUDE.md` |
| Cursor plugin | `.cursor-plugin/` → `skills/`, `agents/`, `generated/cursor/rules/` |
| Cursor (this repo) | `.cursor/{agents,rules,skills}/` (source) |
| Codex | `.codex-plugin/plugin.json`, this file |
