# Scope and context

How to package what the reviewers see. Reviewers only know what you give them, so a bad package means bad findings.

## Pick the base

1. Use the base the user named.
2. Otherwise use the PR or MR target branch (`gh pr view --json baseRefName`, `glab mr view`).
3. Otherwise use the default branch (`git symbolic-ref refs/remotes/origin/HEAD`), usually `main`.
4. Diff from the merge base, not the branch tip: `git diff <base>...HEAD`. The three dots matter. Two dots would include changes that landed on the base after the branch was cut.

Uncommitted work counts too. If `git status` shows changes, ask in the scope node whether to include them (`git diff HEAD` for staged and unstaged together).

## Size

| Changed lines | Do |
|---|---|
| Under about 400 | One package. Send the whole diff to every reviewer |
| About 400 to 800 | One package, but add a short map at the top: each file and what changed in it |
| Over about 800 | Recommend a split in the scope node: one review per area (for example the API layer, then the jobs). Or keep one review and send each reviewer the whole diff with the map |

Never cut a reviewer's copy in half silently. If something is left out, say what in the prompt.

## What to leave out

Recommend excluding these in the scope node, and list what you excluded:

- Generated files: lockfiles, compiled assets, generated clients, snapshots, `*.pb.go`, migration dumps.
- Vendored code and large fixtures.
- Pure formatting changes, when the user confirms they are formatting only.

Keep a lockfile in scope when the change is a dependency bump.

## Context files to add

The diff alone hides how the code is called. Add the smallest set that lets a reviewer trace the change:

- **Types and interfaces** the changed code uses or returns.
- **One caller and one callee** of each changed public function.
- **Existing tests** for the changed code, even unchanged ones.
- **Config and flags** the change reads.
- **The contract**: an OpenAPI file, a `.proto`, an event schema, when the change touches one.

When the change lands in a subsystem you do not know, run `codebase-learner` in explain mode first and pass its How It Works and Gotchas sections as `{HOW_CONTEXT}`.

## Change types

Spot the kinds of change in the diff with `change-type-checks.md`, and fill `{CHANGE_TYPE_CHECKS}` with the matching rows.

## Brief for the prompt

Fill `{BRIEF}` with the resolved brief nodes, one line each:

```
Focus: security of the new webhook endpoint. Skip the generated client.
Risk: production hot path (every checkout calls it).
Merge pressure: can wait.
Known gaps: load test deferred to PR #88. Docs come in a follow-up.
```
