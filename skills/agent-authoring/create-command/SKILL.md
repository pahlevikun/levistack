---
name: create-command
description: "Create, audit or improve slash commands (commands/<name>.md, .claude/commands, .cursor/commands): saved prompts you run as /name, with arguments. Use when asked to add a slash command or custom command, pass arguments to one, make a repeatable prompt, or choose between a command and a skill."
---

# Create a slash command

A command is a saved prompt the user runs as `/name`. The body is an instruction to the agent, with optional arguments. It runs when the user asks for it, not when the model decides.

## Principles

1. **One command, one outcome.** `/handoff` writes a handoff note. If the name needs "and", split it.
2. **A command is for explicit, repeatable actions.** Anything with side effects (commit, deploy, post, delete) belongs behind a command, so the user stays in control.
3. **Short and imperative.** Say the outcome, the inputs, the output, and what not to do, in under about 30 lines. Point to a skill for the method instead of repeating it.
4. **Handle empty arguments.** State what to do when nothing is typed after the name (infer from context, or ask once).
5. **Do not rely on shell injection in a shared command.** Backticked commands prefixed with `!` run before the model sees the prompt, and plugin-supplied commands do not run them.

## Command or skill?

Claude Code has merged commands into skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`, and the skill wins if both exist.

| You need | Use |
|---|---|
| A short prompt, one file, typed as `/name` | **Command** (this skill) |
| Supporting files, scripts, or the model loading it on its own | **Skill** with `disable-model-invocation: true` if it must stay manual (`create-skill`) |
| A command that already exists and has grown | Convert it (`convert-as-skill`) |

Default to a command when the repo or target tool uses one; Cursor and catalog `commands/` trees are command-based. Otherwise a skill is the more capable format.

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
5. **Write it** from [templates/command.md](templates/command.md): a one-line quoted `description`, an `argument-hint` when it takes arguments, then the body. Use `$ARGUMENTS` for everything typed after the name.
6. **Check it.** The description is one line, says what it does, and the body names the output. If the repo has its own validation (for example `npm run validate`), run it. Cursor commands are plain Markdown; frontmatter there is optional.
7. **Run it** with `/name` and with no arguments, then with a typical argument. Fix the wording until both behave.

## Writing the body

- Lead with the outcome: "Write a dated handoff note ...".
- Name the arguments and the empty case: "Topic: `$ARGUMENTS` (infer it from the work when empty)".
- State the output: a file path, a short summary, a prompt to paste.
- Add the guardrails: "Do not commit the file", "Do not include secrets".
- Reference a skill by name when one exists for the method.

## Do not

- Copy a skill's whole procedure into the command.
- Put secrets, personal paths or employer names in a shared command.
- Add `allowed-tools` broader than the command needs.
- Leave a side effect (commit, push, post) implicit.

## Related skills

- `create-skill`: the prompt needs scripts, references or model-triggered loading.
- `create-hook`: the action must run on an event, not on /name.
- `convert-as-skill`: turn a command into a skill.
- `create-agent`: the job needs its own context and tools.

## Done when

- The file is at the right path for its tool and the filename is the intended `/name`.
- The description is one quoted line; arguments are named and the empty case is handled.
- It ran with and without arguments and produced the stated output.
- No existing command or skill already does this.
