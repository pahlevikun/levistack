# Commit plan: <branch or task>

Changed files: <n>. Planned commits: <n>. Base: `<git rev-parse --short HEAD>`.

| # | Commit | Files or hunks | Why it stands alone | Verify |
|---|---|---|---|---|
| 1 | `<type>(<scope>): <subject>` | `<paths>` or `<path> (hunks 1-2, git add -p)` | <one reason> | `<focused test or check>` |
| 2 | `<type>(<scope>): <subject>` | `<paths>` | <one reason> | `<check>` |

## Left out
- `<path>`: <reason: not part of this work, secret, build output>

## Order
<One sentence: which commit must come first, and why.>

## Before you start
- [ ] Unrelated changes are in the plan or in "Left out".
- [ ] No file holds two purposes without a `git add -p` note.
- [ ] Each message passes `node scripts/check-message.mjs`.
