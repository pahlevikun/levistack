# Tool access and safety in commands

## Contents
- Pre-approve, do not assume restrict
- When to narrow
- Patterns
- Side effects stay explicit
- Test the boundary
- Document the why

## Pre-approve, do not assume restrict

In Claude Code, `allowed-tools` in a command's frontmatter **pre-approves** tools for that command's turn: the agent can use them without a permission prompt. It is not a sandbox, and omitting it does not add one. To remove tools for the turn use `disallowed-tools`; to forbid a pattern everywhere use permission rules in settings. Verify behavior in your version: the field names and pattern syntax have changed over time. Older material writes `Bash(git add:*)`; current documentation writes `Bash(git add *)`.

Cursor commands are plain Markdown and carry no tool settings. Put the restriction in the wording ("Do not run anything but `git status` and `git diff`") and rely on the tool's own permission prompts.

## When to narrow

| Narrow it when | Leave it open when |
|---|---|
| It touches git history, deploys, publishes or deletes | The work is exploratory and the tools needed are not known in advance |
| It should only read or analyze | The command runs in a sandbox or a throwaway environment |
| It processes content you do not control | The user supervises every step anyway |
| It will be shared across a team | It is a personal convenience command |

The default is the minimum that does the job: the exact subcommands, not the whole program.

```yaml
# Broad
allowed-tools: Bash(git *)
# Better
allowed-tools: Bash(git add *) Bash(git status *) Bash(git commit *)
# Best for an analysis command
allowed-tools: Bash(git status *) Bash(git diff *)
```

## Patterns

**Commit.** Pre-approve only `git add`, `git status`, `git diff` and `git commit`. Not `git push`, not `git reset`.

**Read-only analysis.** Pre-approve read tools only (`Read`, `Grep`, `Glob`). It cannot write or execute, so it cannot damage anything.

**No exfiltration.** For a command that reads local code, leave out network tools (`WebFetch`, `WebSearch`) and arbitrary `Bash`, so the code cannot be sent anywhere.

**No destruction.** For a review command, allow reads and `git diff` and `git log`, and nothing that writes, resets or force-pushes.

**Controlled deploy.** Pre-approve one target explicitly: `Bash(npm run deploy:staging)`, not `Bash(npm run deploy *)`. A typo cannot reach production. For production, pre-approve nothing and let the permission prompt confirm.

**Gate on tests.** A deploy command's first step runs the tests; if any fail, stop and report the failures. The gate is in the prompt, so say it plainly: "If any test fails, do not deploy; list the failures."

## Side effects stay explicit

A command is the right place for an action with side effects, because the user chose to run it. Inside the command:

- Name each side effect ("create a commit", "post a comment") rather than implying it.
- Add the guard: "Do not push", "Do not edit files outside `docs/`", "Do not include secrets".
- Ask for confirmation before an irreversible step if the command could run unattended.
- Keep secrets, tokens and personal paths out of any shared command.

## Test the boundary

1. Run the command and confirm the allowed operations work.
2. Ask it, inside the command's turn, to do something outside the allowed set and confirm it is prompted or refused.
3. Read the error text; it should tell the user what happened.

## Document the why

Say in the description or in a comment why access is narrow ("commit only: no push"), so the next editor does not widen it by accident.
