# Write a descriptive message

A subject like `feat: add login page` names a thing. It does not say what the thing does or why it exists. A reader of `git log` learns that a file was added, and nothing else. This guide makes the subject say what changed for the reader, and the body say why.

## Read the diff first

Before you write a word, read the staged diff and answer three questions:

1. **Effect.** What can a user, a caller or a maintainer do, see or no longer do after this change?
2. **Reason.** What caused it: a bug, a request, a risk, a cost?
3. **Boundary.** Under which condition does it apply: always, on a timeout, for admins, above a size?

Write the subject from the answer to 1 and 3. Write the body from the answer to 2.

## The subject

```
<type>(<scope>): <verb> <what> <condition or effect>
```

- Pick the verb that names the effect, not the verb that names the act of typing. The ladder is below.
- Add the condition or the effect when the verb alone is not enough: `on timeout`, `when the avatar is missing`, `above 5 MB`.
- Keep it to 60 characters if you can. The hard limit is 72. If it will not fit, the commit may hold two purposes. Split it, or move detail to the body.
- Use the words of the product, not the words of the code, when the reader is a user. Use exact identifiers when the reader is a maintainer.

### Verb ladder

| The change does this | Use | Example |
|---|---|---|
| Stops a bad input or state | `reject`, `block`, `guard`, `limit` | `reject emails without a domain` |
| Keeps going after a failure | `retry`, `fall back to`, `resume`, `skip` | `retry upload up to 3 times on timeout` |
| Makes work cheaper | `cache`, `batch`, `defer`, `reuse` | `cache the search index per request` |
| Changes what the user sees | `show`, `hide`, `label`, `group`, `sort` | `show the unpaid total above the cart` |
| Changes a default or a limit | `default to`, `cap`, `require`, `allow` | `cap page size at 100 rows` |
| Records or reports | `log`, `report`, `expose` | `log the job id and duration on failure` |
| Changes the shape of code | `extract`, `split`, `merge`, `rename`, `move`, `replace` | `extract price calculation from CartView` |
| Corrects wrong behavior | `fix` plus the symptom | `fix the crash when the avatar is missing` |
| Takes something out | `remove`, `drop` plus the reason | `remove the v1 export. No client calls it` |

These are common words. They fit the STE rules in `ste-messages.md`.

## Rewrite the weak ones

| Weak | Descriptive |
|---|---|
| `feat: add retry` | `feat(sync): retry upload up to 3 times on timeout` |
| `feat: add validation` | `feat(signup): reject emails without a domain` |
| `feat: add logging` | `feat(worker): log the job id and duration on failure` |
| `feat: add button` | `feat(cart): let users clear the cart in one tap` |
| `feat: add endpoint` | `feat(api): return a user's orders at GET /users/:id/orders` |
| `feat: add support for dark mode` | `feat(theme): follow the system dark setting on launch` |
| `feat: add config option` | `feat(search): let teams set the result limit with SEARCH_LIMIT` |
| `fix: add null check` | `fix(profile): stop the crash when the avatar is missing` |
| `test: add tests` | `test(cart): cover a coupon that stacks with a free item` |
| `docs: add docs` | `docs(readme): explain how to run the seed script` |
| `chore: add eslint` | `chore(lint): run eslint on staged files before commit` |
| `refactor: add helper` | `refactor(cart): extract price calculation into one function` |

## When `add` is the right verb

`add` is fine when the new thing is the news. Then say what it is for:

```
feat(api): add GET /users/:id/orders to list a user's orders
feat(login): add a rate limit after 5 failed tries
```

The check script (`check-message.mjs`) warns with `bare-add` when `add` is followed by three words or fewer and no purpose or condition. A word such as `to`, `for`, `when`, `on`, `after` or `so` shows that the subject has one.

## The body

Write a body for any change that is not trivial. Always write one for:

- a change of 40 changed lines or more to `feat`, `fix`, `refactor` or `perf` (pass `--diff-lines=N` to the checker)
- a bug fix, a security fix, a migration, a revert or a breaking change
- anything that surprised you while you wrote it

Use this order. Skip a line that has nothing to say.

```
<Problem: what was wrong, or what was missing. Who saw it.>
<Cause: why it happened. One sentence.>
<Change: what this commit does about it. The idea, not the diff.>
<Effect or risk: what is different now. What could break.>
<How you checked: the test or the manual step.>

Closes #123
```

Rules for the body:

- Explain why. The diff already shows what.
- Active voice. Name the actor: `The cache kept the old name.`
- 20 words or fewer per sentence. One fact per sentence.
- Name the warning first when there is one: `Run the migration before you deploy.`
- Wrap at 72 characters. No em dash, en dash or semicolon.

### A full example

```
fix(upload): retry on timeout so large files finish

Uploads over 20 MB failed on slow networks. The client gave up after
one 30 second timeout and showed a generic error.

Retry up to 3 times with a longer timeout each time. Show the retry
count in the progress label. Small uploads behave as before.

Checked with a throttled connection. A 50 MB file finished on try 2.

Closes #412
```

## Two checks before you commit

- **The stranger test.** Read only the subject. Can someone who does not know the code decide whether to open the diff?
- **The revert test.** If this commit were reverted, would the subject tell you what you lose?

If either answer is no, rewrite the subject.

## Audit a history

```bash
node scripts/check-message.mjs --range origin/main..HEAD
```

When five or more commits are checked and more than 40 percent of the subjects start with `add`, the script prints a note. It means the subjects name objects. Rewrite them with the verb ladder before you open the MR.
