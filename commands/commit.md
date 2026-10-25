---
description: "Split the working tree into small atomic commits with descriptive semantic messages. Commits only, never pushes."
argument-hint: "[scope or hint]"
---

Use the atomic-semantic-commit skill to split the current changes into commits. Hint: $ARGUMENTS (look at `git status` and group everything when empty).

Read each staged diff before you write its message. The subject says what changed for the reader and when, not just `add` plus a name. Write a body for any change of 40 lines or more, a fix, a migration or a revert. Run `scripts/check-message.mjs` with `--diff-lines` and fix what it flags.

Show the plan first when it has more than two commits. Reply with `git log --oneline` for the new commits. Do not push. Do not add trailers or attribution. Do not stage secrets or build output.
