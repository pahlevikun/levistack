# Commit messages in STE

Write a commit message that is short and exact. Use Conventional Commits. Explain why, not what.

If the project has its own commit rule (types, ticket reference, subject length, capitalization), follow that rule first. Use this file for the discipline of the body.

## Subject line

- Use this format: `<type>(<scope>): <imperative summary>`. The scope is optional.
- Use one of these types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`.
- Use the imperative mood: "add", "fix", "remove". Do not use "added", "adds", or "adding".
- Keep the subject to 50 characters when possible. The hard limit is 72.
- Do not end the subject with a period.
- Follow the project rule for capitalization after the colon.

## Body

- Omit the body when the subject explains the change.
- Add a body only for a non-obvious reason, a breaking change, a migration note, or a linked issue.
- Wrap lines at 72 characters.
- Use `-` for bullets, not `*`.
- Put issue references at the end: `Closes #42`, `Refs #17`.

## Never include

- "This commit does X", "I", "we", "now", or "currently". The diff shows what changed.
- "As requested by ...". Use a `Co-authored-by` trailer.
- AI attribution text such as "Generated with ...". If a user rule requires an `Assisted-by` or similar trailer, add it as a trailer.
- Emoji, unless the project requires them.
- The file name, when the scope already names it.

## Examples

The diff adds an endpoint, and the reason is not obvious.

- Wrong: `feat: add a new endpoint to get user profile information from the database`
- Right:

  ```
  feat(api): add GET /users/:id/profile

  The mobile client needs profile data without the full user payload.
  This reduces bandwidth on cold-launch screens.

  Closes #128
  ```

The diff is a breaking change.

- Right:

  ```
  feat(api)!: rename /v1/orders to /v1/checkout

  BREAKING CHANGE: clients on /v1/orders must move to /v1/checkout
  before 2026-06-01. The old route returns 410 after that date.
  ```

## Always write a body for

A breaking change, a security fix, a data migration, and a revert. Future readers need the reason. Do not shorten these to a subject only.

## Boundaries

Output the message only, in one code block, ready to paste. Do not run `git commit`. Do not stage files. Do not amend. Say "normal mode" to return to a verbose commit style.
