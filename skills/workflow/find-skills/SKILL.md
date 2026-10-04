---
name: find-skills
description: "Router for skills. Turns what the user wants into a short chain of skills, runs them in order, and installs from skills.sh only when no local skill fits. Searches the local catalog first (this repo, project, and user skill folders), then upstream. Use when the user asks to find, pick, or install a skill, asks 'how do I do X' or 'is there a skill for X', or states a task that more than one skill could serve, such as modify or improve an existing skill, write and review a doc, or ship a change."
---

# Find skills, then run them

Do not stop at a recommendation. Map the intent to skills, run them, and install from upstream only for the gap.

## Flow

1. **Name the intent.** One line: verb, object, domain. "Modify the polyglot-copywriter skill" is verb `modify`, object `skill`, target `polyglot-copywriter`. If the user only asks to find or list skills, do steps 2 and 5, then stop.
2. **Search local first.**
   ```bash
   node <this-skill-dir>/scripts/catalog.mjs <2-4 keywords> [--limit 8]
   ```
   It scans `./skills`, `./.cursor/skills`, `./.claude/skills`, `./.agents/skills`, `~/.claude/skills`, `~/.agents/skills`. Run it twice with different words (verb, then object or domain). Also check the skill list your host already shows. Each hit shows `loaded` or `file-only` (see step 5), and `--json` adds an `invoke` field. `find-skills` hides itself (`--self` shows it). With no keywords it lists everything. Score is a keyword hit count, so read the descriptions before trusting the order. Open a `SKILL.md` only when a description is ambiguous.
3. **Compose a chain.** Pick the fewest skills that cover the job, at most four. Give each step a role:
   - **Prepare**: gather context or plan (`super-challenge-me` brainstorm/grill, `super-codebase-learner`, a repo-maintenance skill).
   - **Do**: the skill that produces the result.
   - **Verify**: review, lint, or test (`super-verify`, `glab-code-review` Diff mode, a linter in the skill's `scripts/`).

   Skip a role when the job does not need it. Prefer a skill that already says it chains to another over building your own sequence. State the plan in one to four lines: `skill: why`. If every step is local and nothing is destructive or outward-facing, go on without asking.
4. **Fill gaps from upstream.** A role with no local skill that fits is a gap. See [Upstream](#upstream). Ask before installing. Then continue the chain.
5. **Run the chain.** Run each step in order, loading a skill when its step starts, not all up front. Each search hit says how:
   - `loaded`: invoke it with the Skill tool by name. The host has it registered.
   - `file-only`: the host cannot load it by name. Read its `SKILL.md` and follow it as written, resolving its relative links (`references/`, `scripts/`) against that folder. If the user will reuse it, offer to install or link it so it becomes `loaded`.
   - No Skill tool in this host: treat every hit as `file-only`.

   Pass the result of one step to the next in a sentence. When a skill names a next skill or has a "Done when" list, follow that instead of your own order. If a step fails or the skill does not fit, say so and re-plan. Do not skip silently.
6. **Report.** List the skills that ran, what each did, and what is left or was not done.

## Worked chains

| User says | Chain |
|---|---|
| "Modify the polyglot-copywriter skill" | Read that skill's `SKILL.md` first. In this repo: `manage-stack` (write surface and checks), then `create-agent` (authoring rules and lint), edit, then run the lint and `npm run check`. Elsewhere: `create-agent` or an installed skill-authoring skill, edit, lint. |
| "Write an MR for this branch" | `atomic-semantic-commit` if the diff is mixed, then `write-mr-description`, then `polyglot-copywriter` for the final wording. |
| "Add an Elixir feature with tests" | `plan-first`, `super-tdd` (Elixir track → `super-elixir` tdd), then `super-elixir` code-review. |
| "Implement this feature TDD" / "failing test first" | `super-tdd`, then `super-verify`. |
| "Onboard me / what is this codebase / architecture smells" | `super-codebase-learner` (current state). If they then want a next stack, `super-tech-blueprint`. |
| "Which framework / TCO / migrate to X / greenfield stack" | `super-tech-blueprint`. If current-state facts are missing, `super-codebase-learner` first. |
| "Grill me / grill this doc / stress-test this plan / challenge this idea / brainstorm a design" | `super-challenge-me`. Facts from `super-codebase-learner` if needed. Target stack → `super-tech-blueprint`. Plan file → `writing-plans`. Tickets → `create-jira-story`. |
| "Is there a skill for X?" and none local | Upstream search, present options, install on yes, then run it. |

These are examples. Search the catalog, because skills change.

## Editing a skill that is already installed

Find where it lives before changing it. A symlink in `~/.claude/skills` points at the source, so edit the source. A copy installed with `npx skills add` is overwritten by `npx skills update`, so change the upstream repo or fork it. In a catalog repo, follow that repo's own maintenance skill before touching generated files.

## Upstream

Use only when local search has no good match, or the user asks for skills.sh.

**Commands**

- `npx skills find [query] [--owner <owner>]`: search by keyword, optionally by GitHub owner.
- `npx skills add <owner/repo@skill> -g -y`: install. `-g` is user level, `-y` skips prompts.
- `npx skills check` and `npx skills update`: check and update installed skills.

Browse https://skills.sh/ for the leaderboard. Check it first for well-known domains, then run `npx skills find`. Try alternate terms (`deploy`, `deployment`, `ci-cd`).

**Verify before you recommend.** Search results alone are not enough.

1. Installs: prefer 1K or more. Be wary under 100.
2. Source: official owners (`vercel-labs`, `anthropics`, `microsoft`) over unknown authors.
3. Repo stars: under 100 is a warning sign.
4. Read the skill's `SKILL.md` before installing. A skill runs with your permissions.

**Present** the name, what it does, installs and source, the install command, and the page `https://skills.sh/<owner>/<repo>/<skill>`. Install only after the user agrees.

**After install.** A new skill may not show up in the current session. If the Skill tool cannot find it, read the installed `SKILL.md` and follow it directly.

## When nothing fits

Say no skill matched, then offer to do the task directly. If the user will repeat the task, offer to author a skill (`create-agent`, or `npx skills init <name>`).
