# Command patterns

Copy the closest one and cut. Each is written so the agent runs the read-only commands itself, which keeps it safe in a shared command. A personal command may use shell injection instead (see `references/formats.md`).

## Contents
- Git
- Review and analysis
- Issue and PR work
- Files
- Thinking and planning
- Gated and multi-step work
- Wrapper for a skill
- Anti-patterns

## Git

**Commit with context**

```markdown
---
description: "Create one commit for the current changes, in this repo's style."
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git add *) Bash(git commit *)
---

Create a single commit for the current changes.

1. Run `git status`, `git diff HEAD`, `git branch --show-current` and `git log --oneline -10`.
2. Stage only the files that belong to this change.
3. Write a message in the style of the recent log.
4. Commit. Do not push.

Reply with the hash and the subject line.
```

Why it holds: it names the exact git subcommands, reads state before acting, and ends with "do not push".

## Review and analysis

**Performance, from the conversation**

```markdown
---
description: "Find the three most worthwhile performance improvements in the code under discussion."
---

Analyze the code we are discussing for performance problems. Suggest three specific optimizations, each with the reason and an estimated effect. Do not edit anything.
```

**Security review with severity**

```markdown
---
description: "Review code for security vulnerabilities, with severity and a fix for each."
argument-hint: "[path]"
allowed-tools: Read Grep Glob
---

Review `$ARGUMENTS` (the current changes if empty) for injection, authentication and authorization flaws, and data exposure.

For each issue: severity (Critical, High, Medium, Low), `file:line`, the risk, and the specific fix. If there are none, say what you checked.
```

**Compare two files**

```markdown
---
description: "Explain the behavioral differences between two files."
arguments: [old, new]
argument-hint: "<old> <new>"
---

Compare `$0` with `$1`. List the differences in behavior, not formatting, and say which matter for callers.
```

## Issue and PR work

**Fix an issue**

```markdown
---
description: "Fix an issue at its root cause, with a test and a PR description."
argument-hint: "<issue-number>"
---

Fix issue #$ARGUMENTS.

1. Read the issue and restate the failure.
2. Find the code responsible and fix the root cause.
3. Add a test that fails without the fix.
4. Run the test suite.
5. Draft a short PR description. Do not open the PR.
```

**Review a PR with priority**

```markdown
---
description: "Review a pull request at a chosen depth."
arguments: [pr, priority]
argument-hint: "<pr> <high|normal|low>"
allowed-tools: Bash(gh pr diff *) Bash(gh pr view *)
---

Review PR #$0. Priority $1: high means line by line; normal means each changed file; low means the shape of the change.

Run `gh pr diff $0` and `gh pr view $0`. Report findings by severity with `file:line`. Do not comment on the PR.
```

## Files

**Review one file**

```markdown
---
description: "Review a file for quality and suggest specific changes."
argument-hint: "<path>"
---

Read `$ARGUMENTS`. If it is empty, ask which file. Assess structure, clarity and risk, and suggest specific changes with the reason for each.
```

## Thinking and planning

**First principles**

```markdown
---
description: "Re-derive a problem from first principles and compare with the current approach."
allowed-tools: Read Grep Glob
---

Take the problem we are working on. List the assumptions, say which are facts and which are habit, rebuild a solution from the facts, and compare it with the current approach. Do not edit files.
```

**Plan a task**

```markdown
---
description: "Break a task into phases with dependencies and risks."
argument-hint: "<task>"
---

Plan: $ARGUMENTS. Split it into phases, name the dependencies between them, rate each phase's difficulty, recommend an order, and list the main risks and how to reduce them. Do not start work.
```

## Gated and multi-step work

**Deploy only if the tests pass**

```markdown
---
description: "Deploy to staging if the tests pass."
allowed-tools: Bash(npm test *) Bash(npm run deploy:staging)
---

1. Run `npm test`.
2. If any test fails, stop. List the failures and do not deploy.
3. If all pass, run `npm run deploy:staging` and report the result.

Never deploy to production from this command.
```

**Feature workflow with a check**

```markdown
---
description: "Plan, build and verify a feature, then draft the commit."
argument-hint: "<feature>"
---

Feature: $ARGUMENTS.

1. Plan: restate the requirement, list the files to change.
2. Build: implement and add tests.
3. Check: run the tests and the linter. Fix what fails.
4. Draft a commit message. Do not commit.

Done when the tests and linter pass.
```

**Analyze, then act**

```markdown
---
description: "Find and fix the top performance problems in a file, with measurements."
argument-hint: "<path>"
---

Profile or inspect `$ARGUMENTS`. Pick the three highest-impact problems, fix them, and measure before and after. Report the numbers. Stop if a change does not help.
```

## Wrapper for a skill

Give a skill a typed entry point in a tree that uses commands, or a shorter name. Keep the wrapper to the invocation. Use `templates/command-wrapper.md`.

```markdown
---
description: "Create or edit an agent skill, with guidance on structure."
argument-hint: "[what the skill should do]"
allowed-tools: Skill(create-skill)
---

Use the create-skill skill for: $ARGUMENTS
```

In Claude Code a skill already creates `/name`, so a wrapper is only needed where the repo or tool is command-based. Do not copy the skill's procedure into the wrapper.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| No description | One line saying what it does; it appears in the `/` menu |
| Vague body ("do the thing for $ARGUMENTS") | The steps, the output and the guard |
| Git or deploy command with no scope on tools | Pre-approve the exact subcommands |
| A state-dependent command that never looks at state | Tell it to run `git status` or read the file first |
| Arguments declared but never used, or used with no meaning | Remove the hint, or say what the value is |
| A 100-line command | Move the method into a skill and point to it |
| Several outcomes in one command | One command, one outcome |
