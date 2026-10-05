---
name: create-command
description: "Create, audit or improve slash commands (commands/*.md, .claude/commands, .cursor/commands): saved prompts you run as /name, with arguments and tool pre-approval. Use when asked to add a slash command or custom command, pass arguments to one, scope its tools, make a repeatable prompt, give a skill a /name entry point, review a command, or choose between a command and a skill."
---

# Create a slash command

A command is a saved prompt the user runs as `/name`. The body is an instruction to the agent, with optional arguments. It runs when the user asks for it, not when the model decides.

## Principles

1. **One command, one outcome.** `/handoff` writes a handoff note. If the name needs "and", split it.
2. **A command is for explicit, repeatable actions.** Anything with side effects (commit, deploy, post, delete) belongs behind a command, so the user stays in control.
3. **Short and imperative.** Say the outcome, the inputs, the output, and what not to do, in under about 30 lines. Point to a skill for the method instead of repeating it.
4. **Design the arguments.** Take one only when the command works on something the user names. Say what each value is, and what to do when nothing is typed ([arguments.md](references/arguments.md)).
5. **Pre-approve the least.** `allowed-tools` pre-approves tools; it does not sandbox. List exact subcommands for anything risky ([safety.md](references/safety.md)).
6. **Read state before acting.** A command that depends on the repo's state starts by looking at it.
7. **Do not rely on shell injection in a shared command.** Backticked commands prefixed with `!` run before the model sees the prompt, and plugin-supplied commands do not run them.

## Command or skill?

Claude Code has merged commands into skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`, and the skill wins if both exist.

| You need | Use |
|---|---|
| A short prompt, one file, typed as `/name` | **Command** (this skill) |
| Supporting files, scripts, or the model loading it on its own | **Skill** with `disable-model-invocation: true` if it must stay manual (`create-skill`) |
| A skill that should also be typed as `/name` in a command-based tree | A thin wrapper command ([patterns.md](references/patterns.md#wrapper-for-a-skill)) |
| A command that already exists and has grown | Convert it (`convert-as-skill`) |

Default to a command when the repo or target tool uses one; Cursor and catalog `commands/` trees are command-based. Otherwise a skill is the more capable format.

## What do you want to do?

| Request | Go to |
|---|---|
| New command | [Steps](#steps) |
| Arguments, positions, empty input | [arguments.md](references/arguments.md) |
| Which tools to pre-approve, how to keep it safe | [safety.md](references/safety.md) |
| An example to copy (commit, review, issue, deploy gate, wrapper) | [patterns.md](references/patterns.md) |
| Fields, locations, precedence | [formats.md](references/formats.md) |
| Review a command | [audit.md](references/audit.md) |

## Steps

1. **Gather requirements.** Infer from the conversation; ask only for what is missing: the outcome, the arguments it takes, any side effects, and where it lives.
2. **Check overlap.** List existing commands and skills with the same intent. Extend one instead of adding another.
3. **Pick the location** (formats in [formats.md](references/formats.md)):

   | Target | File |
   |---|---|
   | Claude Code, project or user | `.claude/commands/<name>.md`, `~/.claude/commands/<name>.md` |
   | Cursor, project or user | `.cursor/commands/<name>.md`, `~/.cursor/commands/<name>.md` |
   | A shared catalog or plugin | `commands/<name>.md` |

4. **Name it.** Lowercase, hyphens, a verb or a clear noun (`handoff`, `review-diff`). The filename without `.md` is the command name. Subfolders namespace it in Claude Code (`frontend/component.md` is `/frontend:component`).
5. **Write it** from [templates/command.md](templates/command.md), or [templates/command-wrapper.md](templates/command-wrapper.md) for a skill entry point: a one-line quoted `description` with no `<tag>` placeholders, an `argument-hint` when it takes arguments, then the body. Use `$ARGUMENTS` for everything typed after the name. Start from the closest pattern in [patterns.md](references/patterns.md).
6. **Scope the tools.** If it runs commands, set `allowed-tools` to the exact subcommands, and say in the body what it must not do.
7. **Check it.** The description is one line, says what it does, and the body names the output. If the repo has its own validation (for example `npm run validate`), run it. Cursor commands are plain Markdown; frontmatter there is optional.
8. **Run it** with `/name` and with no arguments, then with a typical argument, then with a bad one. Fix the wording until all three behave.

## Writing the body

- Lead with the outcome: "Write a dated handoff note ...".
- Name the arguments and the empty case: "Topic: `$ARGUMENTS` (infer it from the work when empty)".
- State the output: a file path, a short summary, a prompt to paste.
- Add the guardrails: "Do not commit the file", "Do not include secrets".
- Reference a skill by name when one exists for the method.
- Match size to the job: a one-action command is two or three sentences; a multi-step one gets numbered steps and a done condition. Do not pad the first or starve the second.

## Do not

- Copy a skill's whole procedure into the command.
- Put secrets, personal paths or employer names in a shared command.
- Pre-approve `Bash(...)` broader than the command needs, or treat `allowed-tools` as a restriction.
- Leave a side effect (commit, push, post) implicit.
- Put an XML-like placeholder (`<name>`) in the description.

## Related skills

- `create-skill`: add scripts or references to the prompt.
- `create-hook`: run on an event, not on /name.
- `create-agent`: give the job its own context.

## Done when

- The file is at the right path for its tool and the filename is the intended `/name`.
- The description is one quoted line; arguments are named and the empty case is handled.
- Tool pre-approval, if any, lists only what the command needs.
- It ran with and without arguments and produced the stated output.
- No existing command or skill already does this.
