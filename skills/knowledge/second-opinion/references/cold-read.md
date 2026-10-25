# Cold read of the ledger

Use this on a **large** review, or when the ledger will be pasted into a PR, MR or plan for people who were not in the chat. A fresh reader checks that the ledger stands on its own. It is the same idea as a fresh reviewer for code, applied to your own output.

## When

- The review is large (see `author-talk.md`, Size the review).
- The ledger will leave this chat.
- You made many "inferred" or "my call" resolutions.

Skip it for a small review.

## How

Start a `general-purpose` subagent with no chat history. Never use a fork, because a fork shares your blind spots. Give it the prompt below and the **output contract only** (change, findings, ledger, agreement map), not the research trail.

```
Role: a skilled engineer who owns the code that the change below touches.
Situation: you were handed this review result and must decide what to do with it. You cannot reach the author or the reviewers.
Read: <the review output, pasted or a path>
Report: only the questions you would still need answered before you could act on it.
  A question counts only if a wrong guess would matter.
  For each, give the question and why its answer would change what you do.
  Rank them by importance.
Skip: anything the ledger says plainly, anything you could decide yourself, and wording nitpicks.
If nothing important is left, say "no open questions".
```

## What to do with the answer

| Pile | Meaning | What you do |
|---|---|---|
| **Answered** | The chat or the code already answers it | Add the answer to the ledger |
| **Minor** | A sensible engineer could settle it without changing the outcome | Settle it, and mark it "my call" |
| **Yours** | Only the author can answer, and it changes the outcome | Ask the author, in one message, most important first |

Update the ledger, then hand it over with a short list of the "my call" lines so the author can check them. This is the only round of questions the cold read makes.

No subagent tool? Read the ledger yourself, as that engineer would.
