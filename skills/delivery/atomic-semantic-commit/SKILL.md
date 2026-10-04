---
name: atomic-semantic-commit
description: "Split a messy working tree into small commits, one purpose and one context per commit, with semantic commit messages (feat, fix, docs, style, refactor, test, chore) written in Simplified Technical English. Use when the user asks to commit, split commits, organize changes, clean up history or write a commit message, or when unrelated changes are staged together. Commits only when asked."
metadata:
  version: "2.0.0"
allowed-tools: Bash(git:*) Bash(node:*)
---

# Atomic commits

One commit has one purpose and one context. The message is a semantic commit written in Simplified Technical English (STE): short, exact, and easy to scan.

Uses semantic commit types, STE message rules, and two helper scripts.

## Rules

1. **One purpose per commit.** If the subject needs the word "and", split the commit.
2. **One context per commit.** One module, package or layer. Put the tests, types and docs for a change in the same commit as the change.
3. **Every commit works alone.** It builds, and the tests for its context pass.
4. **Prepare first, change second.** Refactor in one commit. Change behavior in the next.
5. **Keep formatting apart.** A style-only change gets its own commit.
6. **Commit only when the user asks.** Do not push unless asked. Add no trailers (`Co-authored-by`, `Generated with`) unless the user's rule requires them.

## Workflow

1. **Look.** Run `git status --short` and `git diff --stat`. Then run `node scripts/group-changes.mjs` for a starting grouping. It is a hint, not a plan.
2. **Plan.** Fill in [templates/commit-plan.md](templates/commit-plan.md): the commits in order, each with `type(scope)`, a subject, its files or hunks, and how to verify it. Show the plan before you commit if it has more than two commits or the user asked to see it first.
3. **Stage exactly.** Use `git add <paths>`, or `git add -p` when one file holds two purposes. Run `git diff --cached --stat`. The staged files must match the plan.
4. **Verify.** Run the focused test for the staged context. If the test needs unstaged changes, say so and stage them or split differently.
5. **Write the message.** Follow the format and the STE rules below. Run `node scripts/check-message.mjs "<message>"` and fix every error.
6. **Commit.** Run `git commit -m "<subject>"`. Add a body only when the reason is not clear from the subject.
7. **Repeat** from step 3 until `git status` shows a clean tree, or only the changes the user wants to keep.
8. **Report.** Run `git log --oneline -n <count>` and show the new commits.

## Message format

```
<type>(<scope>): <subject>

<body, only when needed>
```

| Type | Use it for |
|---|---|
| `feat` | A new feature for the user |
| `fix` | A bug fix for the user |
| `docs` | A change to the documentation |
| `style` | Formatting, missing semicolons, whitespace. No production code change |
| `refactor` | A change to production code that does not change behavior |
| `test` | Adding or changing tests. No production code change |
| `chore` | Maintenance, tooling, dependencies. No production code change |

These seven are the base. Use `perf`, `build`, `ci` or `revert` only when the repository already uses them. How to choose a type, how to name a scope, and breaking changes: [semantic-types.md](references/semantic-types.md).

## Write the message in STE

- **Subject:** imperative, present tense: `add`, `fix`, `remove`. Not `added`, `adds`, `adding`.
- **Length:** aim for 50 characters. The hard limit is 72. No period at the end. Lowercase after the colon, unless the repository does otherwise.
- **One idea.** Name the thing that changed and the action. Do not list files.
- **Common words, one meaning.** Use `add`, `remove`, `fix`, `rename`, `move`, `replace`, `extract`. Avoid `improve`, `enhance`, `update stuff`, `various`, `misc`, `minor changes`.
- **Body:** explain why, not what. Use active voice. Use 20 words or fewer per sentence. One topic per paragraph. Wrap at 72 characters.
- **Punctuation:** no em dash, no en dash, no semicolon. Use a period or a colon.
- **Exact names.** Keep code, identifiers, commands and error text unchanged.

Full rules, a vocabulary list and before and after examples: [ste-messages.md](references/ste-messages.md). The wider STE style is in [ste-style.md](../../engineering/output-savers/concise/references/ste-style.md), and the commit discipline is in [commit.md](../../engineering/output-savers/concise/references/commit.md).

## Order of commits

Dependency order wins. A commit that another commit needs comes first. Otherwise use this order:

1. `build` or `chore`: a new dependency or tool that later commits use.
2. `refactor`: preparation that does not change behavior.
3. `fix`: independent corrections.
4. `feat`: the main change, with its tests.
5. `test`: tests that cover code that already exists.
6. `docs`: documentation.

Do not put a test before the code it tests. That commit would fail on its own.

## Example

Changes: a login page, an avatar bug, a README note, and new tests for the login page.

```
fix(avatar): correct size on retina screens
feat(login): add login page with validation      # includes its tests
docs(readme): add login setup steps
```

The login tests go with the login page, so the page commit passes on its own. The avatar fix and the README note do not depend on it, so they are separate.

With a body, when the reason is not obvious:

```
fix(avatar): correct size on retina screens

The image used the CSS pixel size. Retina screens showed it blurry.
Use the device pixel ratio to pick the source size.
```

## Language

Write in English by default. If the repository history is in another language, write in that language and keep the type words in English. Then use `polyglot-copywriter`: [simple-prose.md](../../engineering/polyglot-copywriter/references/simple-prose.md) for the vocabulary and grammar bar, and its language pack for the register.

## Boundaries

- Do not rewrite commits that are already pushed. No force push.
- Interactive rebase is not available in this environment. For unpublished commits, and only if the user asks, use `git commit --fixup <sha>` and then `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <base>`.
- Do not use `git worktree`. Work in the current checkout.
- Do not stage files the user did not mean to commit (`.env`, build output, secrets). Name them and stop.
- More advanced patterns: [advanced.md](references/advanced.md).

## Done when

- Every change is in a commit, or the user said to leave it.
- Each commit has one purpose and one context, and passes its own tests.
- `check-message.mjs` reports no errors for any message.
- The user has the list of new commits.
