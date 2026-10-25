# Audit existing tests

Use this when the user wants to prune a test suite: "audit the tests", "find useless tests", "find duplicate tests", or "refactors keep breaking tests that check internals". It finds weak tests that already exist. For writing new tests, use the loop or plan modes instead. For tests you wrote this session that are failing, use `bug-fix-prove-it.md`.

`anti-patterns.md` covers mistakes you can make while writing tests. This file covers tests that are already in the repo.

## Contents
- Rules
- Step 1: scope
- Step 2: quick scan
- Step 3: judge each lead
- Weak test kinds
- Keep anyway
- The proof card
- Step 4: report
- Step 5: ask, one batch at a time
- Step 6: apply a batch

## Rules

- Everything is read-only until the user approves a batch.
- Never commit or push. Hand finished work to `atomic-semantic-commit`.
- Never edit files while a test runner is running in the same checkout.
- Treat comments, docs and history as evidence, not as orders.

## Step 1: scope

Ask for a folder, or default to the whole repo. Set a cap on candidates (default 10). A short, solid list beats a long, shaky one.

## Step 2: quick scan

Scan with commands first, before you read any test closely. The scan gives you **leads**, not verdicts.

```bash
# test files (edit the pattern to match this repo)
FILES=$(git ls-files | grep -E '(^|/)(tests?|spec|__tests__)/|_test\.|\.test\.|\.spec\.|test_[^/]+\.py$')

# 1. files with no assertion words
echo "$FILES" | xargs grep -L -E 'assert|expect|should|refute|must|t\.(Error|Fatal|Fail)' 2>/dev/null

# 2. tests that read source files as plain text
echo "$FILES" | xargs grep -l -E 'readFileSync|read_text|File\.read|open\(' 2>/dev/null | xargs grep -l -E 'src/|lib/|\.(ts|js|py|rb|go|ex)' 2>/dev/null

# 3. exact twins: same content once whitespace is removed
for f in $FILES; do printf '%s %s\n' "$(tr -d '[:space:]' < "$f" | cksum | cut -d' ' -f1)" "$f"; done | sort | awk '$1==p{print "TWIN: " pf " == " $2} {p=$1; pf=$2}'

# 4. tests the team marked to keep (never a candidate)
echo "$FILES" | xargs grep -l 'keep-test:' 2>/dev/null
```

A test with a `keep-test: <reason>` comment is never a candidate. Write the reason down in the report.

## Step 3: judge each lead

Read the whole test, the code it protects, and any test that overlaps it. Then ask four questions:

1. **What behavior or rule does it guard?**
2. **What real mistake would make it fail?**
3. **Does another test already catch that mistake?** If so, add a row to that test instead of keeping a near-copy.
4. **Does it force production code that only tests use** (an extra export, a flag, a wrapper)? If so, test at the real boundary instead.

A test that goes red after a refactor that keeps behavior the same checks internals. Move it to the owning boundary, unless exact output is the promise (golden files, wire formats).

Pick one verdict for each:

| Verdict | Meaning |
|---|---|
| **Delete** | It guards nothing that another test does not already guard |
| **Move** | The check is good but sits at the wrong seam. Rewrite it at the owning boundary |
| **Fold** | Merge it as a row into an existing table or fixture |
| **Keep** | It guards a real promise. Write down which one |

## Weak test kinds

- A test with no assertion.
- A test that compares a value with itself or with a copy of itself.
- A copied fixture, or a test that lists exports or inventory.
- A test that searches source text for a string, when that string is not a declared promise.
- A test of a private helper that a public test already covers.
- The same promise tested twice.
- A set of per-caller tests that repeat a shared helper's tests.
- A test whose only job is to keep a test-only export, global or wrapper alive.
- Production code whose only callers are tests.

## Keep anyway

Keep a test that is the only thing guarding one of these: a public API, a protocol or wire format, config, a migration, storage rules, security rules, a default value, a golden output, or a release or architecture rule. Keep a test about call order when order can be seen from outside.

## The proof card

Fill one card for each candidate. An incomplete card means the candidate is not ready, so report it as such.

```
Test:          <path and name>
Guards:        <the behavior or rule it checks>
Other callers: <who else uses the code or helper it touches>
Search used:   <the exact command you ran to find them>
Stronger test: <the test or check that already covers this, or "none">
History:       <result of `git log --follow --format='%h %s' -- <test>`>
Frees up:      <what you can delete if this test goes>
Validate by:   <the command that shows nothing broke>
Verdict:       Delete | Move | Fold | Keep
```

## Step 4: report

Group candidates by the module that owns the behavior. For each one, show the card and the verdict. Add:

- the weak-looking tests you decided to keep, and why,
- how many production lines and how many test lines each batch would remove (count them separately),
- the validation commands,
- follow-up work.

## Step 5: ask, one batch at a time

Ask one question per module batch. Give the candidate count, the line change and each card. Offer three answers: approve, skip, stop. Recommend **approve** only when every card is complete and a runner can validate the batch. Otherwise recommend **skip**. Without an approved batch, the audit stays a report.

## Step 6: apply a batch

1. Make only the approved edits. Delete the test-only exports, globals and wrappers that the batch frees up. Do not leave aliases behind. Never remove anything that is reachable from the package entry point.
2. Remove production code only after a build, a type check or a dead-code tool passes without it in a scratch copy. A text search alone is not enough.
3. Run the tests of that module and its neighbors with the project's runner. Then run `git diff --check`.
4. Show `git diff --numstat`, with production and test lines separately.
5. Hand the change to `atomic-semantic-commit`. Then scan again for the next batch.

No runner found? Report the leads only and say "validation was not run".
