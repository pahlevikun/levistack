# Talking with the author

How to open, pace and close the conversation in a second-opinion review. The decision tree says *what* to ask. This file says *how to behave* between the questions. Read it before Step 1.

## Contents
- Triage first
- Look before you ask
- The first message
- Ask by territory, not by script
- Play it back
- Offer a look further
- When there are several fixes
- Settle a finding with a throwaway check
- Show it, do not tell it
- Size the review
- The gate
- Red flags

## Triage first

Before anything else, ask: what do I already know about this change, and what is still missing?

| What you find | What you do |
|---|---|
| **The change is tiny and the intent is plain** (a typo, a rename, a one-line fix) | Review it yourself in one pass. Say what you checked. No reviewers, no tree. |
| **Something that matters is missing**, or the change is non-trivial | Run the full review. |
| **The author says "just run it"** | Run the reviewers with sensible defaults. Say the defaults in one plain line. The tree shrinks, but the ledger and the gate still apply. |

## Look before you ask

Read the diff, the commit messages, the PR or MR body, the files the author pointed at, and the code the change touches. Keep reading until you can say how the touched area works today and what this change moves. Never ask a question that this reading already answers.

## The first message

Your first message moves the work forward. It is the restatement for node N1, and it has this shape. Keep it near 150 words.

1. **Say it back** in your own words: what the change does, who it serves, and the goal.
2. **Add what you found** that bears on it: how the touched area works today, and what the change reaches.
3. **Flag the surprise,** if there is one. A conflict, a hidden caller, a cheaper way to reach the same goal. Say it plainly.
4. **One line** that invites corrections.
5. **One question:** the open point whose answer would change the review the most.

If the author did not ask for an interview (they said "review this"), add one light line: "Or if you would rather I just run the reviewers, say so."

## Ask by territory, not by script

The brief nodes (scope, focus, risk, merge pressure, known gaps) are *ground to cover*. Do not read them out like a form. Cover them in this spirit:

- **What kind of change is this,** and what is special about it.
- **Why now,** and what the author calls success.
- **What would make it a failure,** even if the tests pass (the anti-goal).
- **What they already tried** or rejected.
- **What they care about most** in this review.
- **Who calls this code,** and what they depend on.

Build each question on the last answer or on something you found, the way a sharp colleague would. Point at a consequence the author may have missed. Say why you ask when the reason is not plain. A proposal the author can correct often beats a question: "I assume the cron job never passes a null user. Right?"

## Play it back

After a few answers, say back what you now understand, in 100 to 200 words. Do this once after the brief, and again after the findings are bucketed.

- Only what the author said goes in as theirs. Anything you filled in goes in as "my assumption", with the reason.
- End by asking what is wrong or missing.
- If the author corrects you, change the next play-back. Do not defend the first one.

```
Here is what I have so far:

<the brief, in plain words>

My assumptions (not yours): <each fill-in, and why>

What is wrong or missing?
```

## Offer a look further

When you have some grounding and looking further would help, offer it: callers across the repo, the CI history, the incident tracker, the production config. Say what you would look for. The author decides. Do not go on your own.

## When there are several fixes

If an Act on finding has two or more real fixes, put them in a message of their own before you ask which one. Drop the weak ones first. Keep two or three.

| Fix | What it does | What it gives up | Best when |
|---|---|---|---|
| A. <name> | <one line> | <cost> | <when it wins> |
| B. <name> | <one line> | <cost> | <when it wins> |

**My pick:** <A or B>, because <one sentence>. Which one?

If only one fix makes sense, say so and say why the others do not fit.

## Settle a finding with a throwaway check

When two reviewers disagree, or the author says "that cannot happen", a quick experiment can settle it faster than talking. Offer one: a failing test in a scratch copy, a one-off script, a query on a safe copy of the data.

- Label it throwaway. Do not keep it, and do not touch the branch.
- Report what it showed. Then go back to the node.
- Keeping what the experiment made is a new request. It goes to `tdd`.

## Show it, do not tell it

Per question, ask: would the author understand this better by seeing it? Use a short Mermaid diagram for a flow, a call chain, a state change or a data move, put next to the restatement or the finding. Keep trade-offs and scope questions in text. A question about a diagram topic is not always a diagram question. If the author declines, stay in text.

## Size the review

After intent is confirmed, say how big the review is, in plain words. The author can override you.

| Size | What runs |
|---|---|
| **Small** (a few files, one purpose) | One reviewer, only the nodes that apply, a short ledger |
| **Standard** | Two reviewers on different models, the full tree |
| **Large** (many areas, or a trust boundary) | Standard plus the security reviewer, and the cold-read check |

If the work is really several independent changes, say so and review them one at a time.

## The gate

**Nothing in the reviewed change gets edited until the author approves the ledger.** The review reads, asks and reports. The "fix now" items go to `tdd` or `safe-refactor` after the author says yes. The only exception: the author asked for a quick pass and no review, and then this skill is not running.

## Red flags

| If you think | Remember |
|---|---|
| "I will list every question so we move faster." | One question per turn. A list loses the author. |
| "I will fill the gaps with sensible defaults." | Fine, but say them out loud and mark them as yours. |
| "The author said it looks fine." | That covers what you showed. Findings they have not seen are not accepted. |
| "The reviewers agree, so I will skip the question." | Agreement is not an answer from the author. |
| "The experiment worked, so I will keep it." | Keeping it is a new request. |
| "I should explain how this review works first." | Ask your first question. The process shows itself. |
