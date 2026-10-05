# Designing a command's arguments

## Contents
- Does it take arguments?
- One string or several values
- Writing the argument into the prompt
- Empty and awkward input
- Combining arguments with other features

## Does it take arguments?

| The command works on... | Arguments | Example |
|---|---|---|
| Something the user names (an issue, a PR, a path, a topic) | Yes: add `argument-hint` and use the value in the body | `/fix-issue 123` |
| The conversation or the repo's current state | No: omit the hint and do not mention `$ARGUMENTS` | `/handoff`, `/whats-next` |
| Usually the current state, sometimes a named target | Optional: use the value if present, otherwise infer | `/review [path]` |

State the answer to "what does it do when I type nothing" in the body. Do not leave it to chance.

## One string or several values

**Pass-through.** `$ARGUMENTS` is everything typed after the name. Use it when the whole text is one input: an issue number, a topic, a path, a free-text description.

```markdown
Fix issue #$ARGUMENTS. Understand it, find the code, fix the root cause, add a test, and draft a short PR description.
```

`/fix-issue 456` reaches the agent as "Fix issue #456. ...".

**Structured.** Declare names in `arguments` and refer to the positions when each value means something different:

```markdown
---
description: "Review a pull request, set its depth by priority, and name who to assign."
arguments: [pr, priority, assignee]
argument-hint: "<pr> <priority> <assignee>"
---

Review PR #$0 at priority $1 (high means line-by-line; low means a skim) and assign it to $2.
```

`/review-pr 456 high alice`. Positions are zero-based in the current Claude Code documentation (`$0`, `$1`, or `$ARGUMENTS[N]`). Older examples count from `$1`. Run one example and read what the agent received before relying on it.

Arguments split on whitespace. A value with spaces must be quoted: `/command "a value with spaces"`. Values arrive as typed, with no parsing, so tell the agent how to validate them ("the PR must be a number").

## Writing the argument into the prompt

Put the value where the agent will use it, and give the type of value:

- In the objective: "Fix issue #$ARGUMENTS."
- In a step: "Read the ticket for #$ARGUMENTS."
- As a file to read: write the path reference in backticks, for example `@src/utils/helpers.js`, or ask the agent to read the file named by `$ARGUMENTS`.

Say what the value is ("a path", "an issue number"). "Do the thing for $ARGUMENTS" gives the agent nothing to check.

## Empty and awkward input

```markdown
Analyze $ARGUMENTS for performance problems. If nothing was typed, analyze the code discussed so far in this conversation. If that is not clear, ask once which file.
```

- Empty: infer from context, or ask once, or stop with the usage line. Choose one.
- Wrong type: "If `$0` is not a number, reply with the usage and stop."
- Too many values: say whether extras are ignored or an error.

## Combining arguments with other features

| With | How |
|---|---|
| Current repo state | Tell the agent to run `git status` and `git diff` itself. A backticked command prefixed with `!` runs before the model sees the prompt; it fails the whole command if the shell command fails, and plugin-supplied commands do not run it, so keep it out of shared commands |
| File reads | "Compare `$0` with `$1` and list the behavioral differences" |
| Tool pre-approval | `allowed-tools: Bash(git status *) Bash(git diff *)` so the commands run without prompting (see `references/safety.md`) |
| A skill | "Use the `<skill>` skill. Topic: `$ARGUMENTS`" |
