---
name: create-skill
description: "Create, audit or improve agent skills (a folder with SKILL.md) for Claude Code, Cursor, Codex and the skills CLI. Use when asked to write or add a skill, fix a skill that never triggers, split an oversized SKILL.md, or review skill quality."
---

# Create a skill

A skill is a folder with a `SKILL.md`. Its name and description are always in context; its body loads when the task matches; `references/`, `scripts/` and `templates/` load only when the body points to them.

This skill covers skills only. For subagents use `create-agent`; for rules, hooks and slash commands use `create-rule`, `create-hook` and `create-command`; to convert a rule, command, agent, conversation, PDF or docs folder, or to merge existing skills, use `convert-as-skill`.

## Principles

1. **The description is the router.** The model loads a skill from its description alone. Say what it does, then `Use when ...` with the words a user would say.
2. **Assume the model is smart.** Add only what it lacks: your conventions, your commands, the traps. Cut explanations of common knowledge.
3. **One job per skill.** If the name needs "and", split it. If two skills overlap, merge them (`convert-as-skill` merge-skills).
4. **Match freedom to risk.** Judgment calls get principles and criteria. Fragile steps (migrations, deploys) get exact commands or a script.
5. **Progressive disclosure.** Aim for `SKILL.md` under 200 lines, never over 500. Depth goes in `references/`, one level deep.
6. **Test by using it.** An untested description is a guess.

## Is a skill the right tool?

| Need | Use |
|---|---|
| A procedure or knowledge loaded only when relevant | **Skill** |
| A fact or constraint true for every task in the repo | Rule or `AGENTS.md` (`create-rule`, `create-agents-md`) |
| Must happen every time, not model-decided | Hook (`create-hook`) |
| Isolated context, restricted tools, another model | Subagent (`create-agent`) |
| A saved prompt you type as `/name` | Command, or a skill with `disable-model-invocation: true` (`create-command`) |

## What do you want to do?

| Request | Go to |
|---|---|
| New skill | [New skill](#new-skill) |
| Skill exists but never triggers, misfires, or is too big | [Audit](#audit), then fix by symptom in [format.md](references/format.md#test-and-iterate) |
| Review a skill or a folder of skills | [Audit](#audit) |
| Turn a rule, command, agent, conversation, PDF or docs folder into a skill, or merge two skills | `convert-as-skill` |

## New skill

1. **Gather requirements.** Infer from the conversation first; ask only for what is missing:
   - the task and 2 or 3 real requests it must handle (these become the trigger words and the first tests);
   - where it lives (see [Where it goes](#where-it-goes));
   - the knowledge the model would not already have;
   - an output format, if quality depends on one.
   If the user supplied exact wording for the skill, use it verbatim. Do not paraphrase or add headings around it.
2. **Check for overlap.** List the skills in the target tree. Extend or merge before creating.
3. **Name it.** Lowercase letters, digits and single hyphens, at most 64 characters, equal to the folder name. Prefer a verb phrase or a noun that says the job (`review-diff`, `pdf-processing`). Avoid `helper`, `utils`, `tools`.
4. **Pick the shape.** One task under about 150 lines: [templates/skill.md](templates/skill.md). Three or more distinct tasks: the router in [templates/skill-router.md](templates/skill-router.md), with `SKILL.md` holding principles and routing.
5. **Write the description.** Third person, at most 1024 characters, one quoted line. What it does, then `Use when ...`. Front-load the keywords. Add "Not for ..." when a neighbor could be confused with it.
6. **Write the body** in the order the agent acts: imperative steps, each with an observable result; one term per concept; one default approach plus at most one escape hatch; a template or an input/output pair when format matters; a verification step. Patterns are in [patterns.md](references/patterns.md).
7. **Set invocation.** `disable-model-invocation: true` for side effects or anything you only want on `/name`. `user-invocable: false` (Claude Code) for background knowledge. Leave the default otherwise.
8. **Lint.** `node <create-agent>/scripts/lint.mjs <skill-dir>`, where `<create-agent>` is the sibling `create-agent` skill folder. If it is not installed, walk [audit.md](references/audit.md) by hand.
9. **Test.** Run the real requests from step 1 plus one that should not trigger it. Fix by symptom and re-run. See [format.md](references/format.md#test-and-iterate).

## Where it goes

| Target | Path |
|---|---|
| Claude Code, personal | `~/.claude/skills/<name>/SKILL.md` |
| Claude Code, project | `.claude/skills/<name>/SKILL.md` |
| Cursor, project | `.cursor/skills/<name>/SKILL.md` (also reads `.agents/skills/` and `.claude/skills/`) |
| Any agent | `.agents/skills/<name>/` or publish the repo and `npx skills add <owner>/<repo>` |
| A skill catalog like this one | `skills/<group>/<name>/SKILL.md`, plus the group's `DESCRIPTION.md` |

Never write into a tool's built-in folder (for example Cursor's `skills-cursor`). Check which of the paths above the current project already uses and follow it. In a catalog repo, follow that repo's maintenance instructions (`CLAUDE.md` or `AGENTS.md`) for sync and validation.

## Audit

1. Run the lint step above on the skill folder or the whole tree.
2. Walk [audit.md](references/audit.md) for what a linter cannot judge: specific description, principles over platitudes, actionable steps, tested triggers.
3. Report a score and findings by priority, each with a concrete fix: **Broken** (will not load or trigger), **Weak** (misroutes or wastes context), **Polish**.
4. Apply only the fixes the user asked for. Keep the author's structure and voice.

## Do not

- Write a first-person description ("I can help you ...") or one with no trigger.
- Put the core rule only in a reference file the agent may skip.
- Chain references (`SKILL.md` to a file to another file), or use Windows-style paths.
- Add time-sensitive facts without a date, or restate what the model already knows.
- Leave dynamic shell injection (a backticked command prefixed with `!`) in a published skill without guarding it.

## Done when

- `name` equals the folder; the description says what and when; the linter reports no errors.
- `SKILL.md` is under 500 lines (ideally 200) and every linked file exists, one level deep.
- It ran on at least one real request and triggered correctly, and did not trigger on the unrelated one.
- No overlap with an existing skill, or the overlap was merged.
