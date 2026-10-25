# Commit plan: <branch or task>

Changed files: <n>. Planned commits: <n>. Base: `<git rev-parse --short HEAD>`.

| # | Commit | Files or hunks | Why it stands alone | Verify |
|---|---|---|---|---|
| 1 | `<type>(<scope>): <verb> <what> <condition or effect>` | `<paths>` or `<path> (hunks 1-2, git add -p)` | <one reason> | `<focused test or check>` |
| 2 | `<type>(<scope>): <verb> <what> <condition or effect>` | `<paths>` | <one reason> | `<check>` |

## Left out
- `<path>`: <reason: not part of this work, secret, build output>

## Bodies
- Commit <n>: <why, in one line. Required for 40 lines or more, a fix, a migration, a revert.>

## Order
<One sentence: which commit must come first, and why.>

## Before you start
- [ ] Unrelated changes are in the plan or in "Left out".
- [ ] No file holds two purposes without a `git add -p` note.
- [ ] Each message passes `node scripts/check-message.mjs`.
