# Advanced Atomic Commits Patterns

## Interactive Staging

When a single file contains multiple logical changes:

```bash
git add -p path/to/file.ts
```

This allows staging individual hunks (sections) of changes.

## Using Stash for Isolation

Temporarily hide unrelated changes while committing:

```bash
git stash push -m "unrelated work" -- path/to/unrelated/
git add path/to/related/
git commit -m "feat(billing): add invoice export"
git stash pop
```

## Splitting a Large Commit

If you already made a large commit and need to split it:

```bash
git reset HEAD~1          # Undo last commit, keep changes
git add src/parser/
git commit -m "refactor(parser): extract token reader"
git add src/cli/
git commit -m "feat(cli): add --json flag"
```

## Handling Dependencies Between Changes

When changes depend on each other, commit in dependency order:

1. Base/shared code first
2. Dependent features second
3. Tests that verify both last

## Verifying Atomicity

After you create the commits, check that each one stands alone. The tree must be clean first (`git status`).

```bash
git log --oneline -5
git checkout <sha>        # detached HEAD, read only
# run the focused test or build for that commit
git switch -              # return to your branch
```

Never commit while you are on a detached HEAD.

## Types

The seven base types, the extra types, and how to choose are in `semantic-types.md`. The message rules are in `ste-messages.md`. Both are in this folder.

## Scope Examples

```
feat(auth): add OAuth2 support
fix(api): handle null response from /users
docs(readme): add installation instructions
refactor(utils): extract date formatting
test(cart): add checkout flow tests
```

## Check every message with a git hook

Save this as `.git/hooks/commit-msg` and run `chmod +x .git/hooks/commit-msg`. It blocks a message that has an error. Warnings still pass.

```sh
#!/bin/sh
exec node path/to/atomic-semantic-commit/scripts/check-message.mjs --file "$1"
```

Add `--types=base` to allow only the seven base types, or `--strict` to fail on warnings too. This is a local hook: it is not shared with the team unless the repository ships it.

## Check old commits

```bash
node scripts/check-message.mjs --range origin/main..HEAD
```

Fix a message only on commits that are not pushed. Use `git commit --amend` for the last commit. For older commits, see the autosquash steps in `SKILL.md`.
