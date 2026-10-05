# ticket-comment — use case pack

**Status:** `validated`

Use cases are orthogonal to language. This file teaches **structure**, not vocabulary.

## When to load

A comment on an existing ticket, issue or thread that reports progress, a decision, a blocker or a hand-over. To create a ticket use [create-jira-story](../create-jira-story/pack.md). For line comments on a diff use [glab-code-review](../glab-code-review/pack.md).

## Sentence 1 job

The one thing a person reading this thread next month most needs: the decision, the state change, or the blocker. The reader has the ticket open, so do not restate it (§26 in [humanizer-patterns.md](../../humanizer-patterns.md)).

## What earns a place

Keep what a future reader cannot get from the diff or the ticket body:

- the key finding, the "so that is why" moment
- a decision and its trade-off: what it allows and what it rules out
- a blocker and how it was cleared
- a state change and what it means for the next step
- a surprise that affects the work

Leave out mechanical lists of changes, anything the diff already shows, and generic summaries ("made good progress on the auth work").

## Section order

1. Headline: the decision, state or blocker, in one or two sentences
2. Why, and the trade-off, if it is not obvious
3. State for the next person: what is done, what is not, who holds the next step
4. One open question, only if it blocks someone

Most comments are two to six lines. Stop when the reader can act.

## Details

- Keep links to the source: the PR, the doc, the thread. Do not paste their contents.
- Code references as `path/to/file.ext:line`.
- Mention a person only in the tool's own format. Never invent a user id or handle.
- Dates are absolute: "2026-10-05", not "yesterday".
- Say what is unverified. "Not tested on mobile" helps. A guess written as a fact does not.

## Example

Facts the writer had: batch size 500 (it was one transaction), the old transaction held a lock on `orders` for about 40 seconds on staging, checkout writes were blocked, imports are about 2x slower on the 1M-row sample, no production-size run yet, the 5M-row sample is the next test.

Weak:

> Updated the importer. Changed the batch size, fixed a few bugs, and refactored some functions. Let me know what you think!

Better:

> Importer now commits in batches of 500, so a failure rolls back at most 500 rows. The old all-in-one transaction held a lock on `orders` for about 40 seconds on staging, which blocked checkout writes. The cost is slower imports (roughly 2x on the 1M-row sample). Not tried on production-size data yet. Next: run the 5M-row sample before we pick the batch size.

## Send gate

A comment on a shared ticket goes out in the user's name. Show the draft and post it only after the user says so, per [substance.md](../../substance.md). Do not invent a status change (moved to Done, reassigned) that the user did not ask for.

## Default register

`santai` + [simple-prose.md](../../simple-prose.md). Use `profesional` for a customer-visible thread.

## Do not steal from other formats

- Not a standup. One thread, one point.
- Not a changelog. It explains why, not every edit.
- Not a ticket body. Do not rewrite the problem statement here.

## Aliases (registry)

`ticket comment`, `issue comment`, `status comment`, `progress comment`, `Jira comment`, `update the ticket`
