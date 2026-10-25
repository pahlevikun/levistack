# Git history (commit forensics)

Use with `code-archaeology.md`. That file covers in-repo artifacts. This one goes deep on commits: who changed what, when, together with what, and in which release.

## What this source holds

- Every commit: message, author, date, diff, trailers (`Refs:`, `Fixes:`, `Co-authored-by:`)
- Merge and squash commits that carry PR or MR numbers
- Tags and releases, which give the ship date
- Files that change together (co-change)
- The exact commit that introduced a line, a string or a behavior

## How to search it

```bash
# When a line was born, following moves and copies across files
git blame -w -C -C -L <start>,<end> -- <file>

# The history of one function, even as it moves inside the file
git log -L :<function_name>:<file>

# Commits that added or removed an exact string, or matched a regex
git log -S '<string>' --format='%h %ad %an %s' --date=iso
git log -G '<regex>' -- <path>

# Commit messages that mention a ticket, an incident or a word
git log --all --grep='<ticket-id or word>' -i --format='%h %ad %s' --date=iso

# Which release first contained a commit
git tag --contains <sha> | sort -V | head -1
git describe --contains <sha>

# The merge (PR or MR) that brought a commit into the main branch
git log --merges --ancestry-path <sha>..origin/main --format='%h %s' | tail -1

# Files that usually change together with this one
git log --format='' --name-only -- <file> | sort | uniq -c | sort -rn | head

# The first bad commit for a regression (read-only: bisect only checks out commits)
git bisect start <bad> <good>   # then mark each step good or bad, and run: git bisect reset
```

## What good evidence looks like

- A commit message that says why: "clamp to 100 because the upstream rejects more"
- A trailer that links a ticket or an incident
- A revert, then a re-apply "with fix", which marks a known failure
- The tag date, for the timeline check

## Pitfalls

- **Squash merges** hide the inner commits. Read the PR or MR for the real story.
- **Formatting commits** steal blame. Use `-w` and `--ignore-rev` (or `.git-blame-ignore-revs`).
- **Rebased history** can change dates. Prefer the merge or tag date for "when did it ship".
- **Shallow clones** cut the history. Check `git rev-parse --is-shallow-repository` and say so if true.
- **`git bisect`** changes the checkout. Tell the user before you run it, and always end with `git bisect reset`.

## What to return

Each commit with its short hash, date, author, subject, the lines that matter quoted, and the PR, MR, ticket or tag it links to.
