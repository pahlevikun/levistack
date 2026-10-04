---
name: convert-as-skill
description: "Convert existing material into a skill: agent-requested rules, slash commands, subagents, or the current conversation (a workflow that just worked). Use when asked to migrate rules, commands or agents to skills, turn a command into a SKILL.md, save this session as a skill, or capture what we just did as a reusable skill."
---

# Convert as skill

Skills are the more capable format: supporting files, a trigger description, optional `paths` scoping, and Claude Code has merged commands into them. This skill moves existing material over, or captures a session as a skill, through four mechanisms.

For writing a skill from scratch use `create-skill`. For new rules, commands or agents use `create-rule`, `create-command` or `create-agent`.

## Principles

1. **Copy file-based sources verbatim.** A rule, command or agent body is not rewritten during conversion. Improvements are a separate, reviewed change. The only allowed edits are the description and, for a subagent, lines that speak as a separate agent; list them.
2. **Convert only what fits a skill.** An always-on rule must stay a rule. An agent that exists for isolation or a tool limit should stay an agent.
3. **The description is the part to write well.** Rules have one; commands usually do not (the script drafts one and flags it); a conversation has none.
4. **Preview before writing, and never delete on your own.** Dry-run first. Remove originals only after the user has reviewed the skill and asked.
5. **A conversation is evidence, not a spec.** Keep what worked and what the user confirmed; leave out dead ends, secrets and one-offs.

## What do you want to convert?

| Source | Mechanism | Go to |
|---|---|---|
| A rule (`.mdc` or `.md`, agent-requested) | Script, body verbatim | [Rules and commands](#rules-and-commands), [mapping.md](references/mapping.md) |
| A slash command | Script, body verbatim | [Rules and commands](#rules-and-commands), [mapping.md](references/mapping.md) |
| A subagent | Decide keep, wrap or convert; script with `--fork` | [subagent.md](references/subagent.md) |
| This conversation, or one the user pastes | Extraction and review, then `create-skill` | [conversation.md](references/conversation.md), worksheet [harvest.md](templates/harvest.md) |
| A long section of `CLAUDE.md` or `AGENTS.md` | Extract by hand with `create-skill` | not scripted |

If the request names one, go straight to it. A request like "convert these" with several kinds means run each mechanism on its own files. Ask only if it is unclear whether "this" means a file or the conversation.

## What converts

| Source | Converts? | Result |
|---|---|---|
| Rule with `description`, no globs, not always-on | Yes | `name` + `description`, body verbatim |
| Rule with `globs` or `paths` | Only with `--paths` | Scope kept as `paths`; behavior changes |
| Rule with `alwaysApply: true`, or no frontmatter | No | Stays a rule |
| Command, with or without frontmatter | Yes | `name`, `description`, `disable-model-invocation: true`, other keys kept |
| Subagent | Yes, with loss | `name`, `description`, `model`, body; `tools` and other agent-only keys dropped; `--fork` keeps isolation |
| Conversation | Yes, by extraction | A new skill written with `create-skill` |

## Rules and commands

1. **Find the sources** using the locations in [mapping.md](references/mapping.md). Skip anything in a tool's built-in folder (for example Cursor's `skills-cursor`).
2. **Choose the destination:** the project's skills folder (`.claude/skills/`, `.cursor/skills/` or `.agents/skills/`), the user's, or a catalog's `skills/<group>/`. Match what the project already uses. In a catalog repo follow its maintenance instructions and add the group's `DESCRIPTION.md` if the group is new.
3. **Preview:**

   ```bash
   node scripts/convert.mjs <source...> --out <skills-dir> --dry-run
   ```

   It prints what it would convert, what it skipped and why, and warnings. `--kind rule|command|agent` is inferred from the path (`rules/`, `commands/`, `agents/`); pass it for a file elsewhere. `--name` and `--description` apply to one source.
4. **Write the descriptions.** For each warning about an inferred description, rewrite it as what the skill does plus `Use when ...` with the words a user would say, then re-run with `--description "..."` for that file.
5. **Convert:** run again without `--dry-run`. It refuses to overwrite an existing skill unless you pass `--force`.
6. **Verify:** diff each body against its source (the text after the frontmatter must be identical). Lint with the `create-skill` linter (`<create-agent>/scripts/lint.mjs <skill-dir>`). In a catalog repo run its sync and validate commands.
7. **Try it:** run `/name` for a command, or ask for something the description should match. Confirm it loads.
8. **Originals:** report the source paths and what replaced them. Delete them only when the user asks; offer to restore from version control if the conversion is rejected.

## Do not

- Delete or edit a source file during conversion.
- Convert an always-on or file-scoped rule unless the user wants on-demand loading.
- Turn an isolation-first subagent into an inline skill without telling the user what is lost.
- Write into a tool's built-in skills folder.
- Put secrets, personal paths or session-specific values into a skill made from a conversation.

## Done when

- Every converted skill has `name` equal to its folder, a one-line quoted `description`, and (for file sources) a body identical to the source apart from listed edits.
- The linter reports no errors, and each skipped file has a stated reason.
- A skill made from a conversation was shown to the user as an outline first and replayed once on its original request.
- The user knows which originals remain and how to remove or restore them.
