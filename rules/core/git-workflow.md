---
description: "Work in one checkout on one branch; no git worktrees; commit only when asked; run local gates before pushing."
alwaysApply: true
---

# Git workflow

- Use **one working tree** on the current branch, or a short-lived feature branch checked out in the repo root. Do not use `git worktree` or an agent "isolated worktree" option for routine work: it creates detached state that needs manual cleanup.
- For parallel work, run background agents in the same tree on disjoint file sets.
- For a risky change, use a feature branch in the same checkout, not an extra worktree.
- Commit and merge or rebase before starting unrelated work. Stash or commit WIP when switching tasks.
- Commit only when the user asks. Do not push unless explicitly requested.
- Update the changelog under an `Unreleased` heading for user-facing changes, when the repo keeps one.
- **Preserve unrelated changes.** Other work may be in the tree. Do not initialize, stage, amend, rewrite, discard, branch, release or deploy without explicit authorization, and keep a requested commit focused.
- Never commit generated artifacts such as coverage output, build products or local caches.

## Before pushing
Run the repository's normal gate (format, lint, type check, tests) and `git status` to confirm no stray artifacts are staged. Report any gate you could not run.
