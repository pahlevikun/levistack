# AGENTS.md templates

Delete any section that has nothing true to say. An empty heading is noise.

## Root

```markdown
# <Project name>

<One or two sentences: what this is and who uses it.>

## Commands
- Install: `<cmd>`
- Build: `<cmd>`
- Run one test: `<cmd path/to/test>`
- Run all tests: `<cmd>`
- Lint and format: `<cmd>`
- Type check: `<cmd>`

## Conventions
- <Rule that differs from the language default, with the reason in a clause.>
- <Naming, error handling, logging, or API shape the code follows.>

## Boundaries
- Generated, do not edit: `<path>` (regenerate with `<cmd>`).
- `<layer>` must not import `<layer>`.
- Never <dangerous action> without asking.

## Traps
- <Thing that looks fine and fails later, and what to do instead.>

## Verify
Before reporting done: `<command>`. <What "green" means here.>

## Git
- Commit format: `<format>`.
- <Branch or PR rule, if any.>
- Do not commit or push unless asked.
```

## Nested (package, service or directory)

Only what differs from the root. Do not repeat it.

```markdown
# <package name>

Applies to `<path>` and below. Root rules still apply; these add or override.

## Commands
- Test this package: `<cmd>`
- Run locally: `<cmd>`

## Differences
- <Language, framework or style that differs from the root.>
- <Stricter rule, with the reason.>

## Traps
- <Package-specific trap.>
```

## Global (user level)

Personal and true in every repo. No project facts.

```markdown
# Personal preferences

- <Communication style: concise, lead with the result, say what was verified.>
- <Tool habits: prefer `rg` over `grep`, use `uv` for Python.>
- <Safety habits: ask before destructive commands; never commit unless asked.>
```

## CLAUDE.md shim (when the repo also needs a CLAUDE.md)

Preferred: a symlink, `ln -s AGENTS.md CLAUDE.md`. Or a file that imports it:

```markdown
@AGENTS.md

## Claude Code only
- <Anything that applies only to Claude, such as a slash command or a plugin.>
```

Do not add a `CLAUDE.local.md` to a repo that relies on `AGENTS.md` alone: it counts as a `CLAUDE.md` and stops Claude Code from reading `AGENTS.md`.
