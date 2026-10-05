# pr-description — use case pack

**Status:** `validated`

Use cases are orthogonal to language. This file teaches **structure**, not vocabulary.

## When to load

The body of a pull request or merge request, a commit message body, or a one-line changelog entry. For comments on a diff use [glab-code-review](../glab-code-review/pack.md). For ticket text use [create-jira-story](../create-jira-story/pack.md).

## Sentence 1 job

Say what the change does and why it was needed, in one sentence a reviewer can accept or challenge. Lead with the reason, not the file list.

## Section order

1. Summary: the problem and what this change does about it
2. Breaking changes and migration: first after the summary when there are any, with the exact old and new names
3. What changed: grouped by area, user-visible effects before internals
4. How to verify: a checklist, see below
5. Changelog line: one line a user would understand

Skip a section that has nothing to say. Do not pad it with "N/A" unless the repo template requires the heading.

## Use the repo's template

If the repo has a PR or MR template, fill that template. Keep its headings and order. Answer every question it asks. Do not add sections it does not have, and do not delete required ones. If there is no template, use the order above.

## Verification checklist

A box is a claim about something that happened.

- Tick `[x]` only for a step you ran in this session, with the command and a passing result.
- Leave `[ ]` for a step that failed, and write what failed on the same line.
- Leave a manual step (a screen, a device, an outside service) unticked and name it, so the author knows to do it.
- Never tick on belief. If you could not run it, say so.

Apply the `super-verify` rules when the description makes a test claim.

## Write for the reviewer

- Why before what. The diff already shows what.
- Short bullets. Use a table only when comparing things. No bold labels on every line (§19).
- Name the risk where the reviewer will look: migrations, config changes, new dependencies, behavior change for existing users.
- Do not narrate the diff file by file or describe the description itself (§25).
- Updating an existing description: read it, then change only what the new commits changed.

## Commit messages

- Subject: imperative mood, one purpose, short enough to read in a log. Say what the commit does now, not what you did.
- Body: the reason, and anything a future reader of `git blame` needs. Skip a body when the subject says it all.
- One purpose per commit. Splitting a mixed tree and choosing the type prefix belong to `atomic-semantic-commit`.
- Do not add or remove attribution lines. Follow the repo and the user's tools.

## Default register

`santai` + [simple-prose.md](../../simple-prose.md). Use `profesional` for an external or open-source project.

## When invoked by write-mr-description

- Scope: the description text. Do not change issue keys, branch names, `file:line` references or the template's fixed headings.
- Mode: rewrite on the structured draft the caller built. Do not add a test result the caller did not run. Use `[TK: …]` for a missing fact.
- The description is posted in the user's name. Follow the send gate in [substance.md](../../substance.md) unless the caller already holds a draft MR the user will review.

## Do not steal from other formats

- Not a release announcement. A changelog line is one plain sentence.
- Not a design doc. Link it instead of copying it in.
- Not a review. Do not grade your own change.

## Aliases (registry)

`PR description`, `MR description`, `pull request description`, `describe the PR`, `commit body`, `changelog entry`
