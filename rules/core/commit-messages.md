---
description: "Conventional Commits format, one purpose per commit, and never commit or push unless asked."
alwaysApply: true
---

# Commit messages

Use Conventional Commits unless the repository defines a stricter convention:

`<type>(<optional-scope>): <optional-[TICKET]> <imperative description>`

| Type | When |
|---|---|
| `feat` | New behavior or capability |
| `fix` | Bug fix |
| `refactor` | Restructure without behavior change |
| `perf` | Performance improvement |
| `test` | Add or correct tests |
| `docs` | Docs, rules, skills |
| `build` / `ci` | Dependencies, tooling, pipelines |
| `chore` / `revert` | Housekeeping, reverts |

- Subject: imperative, lowercase, 72 characters or fewer, no trailing period.
- Add a ticket reference when one exists (`fix(auth): [PROJ-123] reject expired tokens`).
- Add a body only when motivation or rollout context helps review. Explain why, not what.
- Breaking change: add `!` after the type and a `BREAKING CHANGE:` footer.
- One purpose per commit. If the diff has two purposes, make two commits.

Never commit, push, create a branch or open a review unless the user or the active workflow asks for it.

## Incorrect
```
Added new script for bulk migration
fix bug
Updated dependencies
```

## Correct
```
feat(scripts): add bulk migration script
fix(runner): correct checkpoint index off-by-one on resume
build(deps): bump tqdm to 4.70.0
```
