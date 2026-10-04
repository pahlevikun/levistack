# Investigate first

Use when the cause is unknown: an intermittent failure, a performance regression, a change that "worked yesterday", a symptom with no obvious owner. The output is a cause with proof, or the exact blocker. A fix is a separate step the task must authorize.

## Contents
- Rules
- Procedure
- Hypothesis table
- Stopping
- Report

## Rules

1. **Separate the symptom from the cause.** The symptom is what was observed (an error, a number, a screenshot). The cause is your explanation for it. Write them as two different lines.
2. **No edits until one credible mechanism explains all the evidence.** A guess that fits some of the evidence is a hypothesis, not a cause.
3. **Cheap, falsifying tests first.** Prefer the check that would most quickly kill a hypothesis over the one that would merely support it.
4. **Make no fix unless the task authorizes implementation.** Reproduction scripts and logging that you remove afterward are not fixes; say what you added and remove it.

## Procedure

1. **State the symptom precisely.** Exact message, input, environment, frequency, first-seen revision if known. If you cannot reproduce it, say so and treat reproduction as the first job.
2. **Reproduce or bound it.** Smallest input that fails, smallest that passes. If intermittent, find what varies (timing, order, data, load) before theorizing.
3. **Trace.** Follow the inputs, the state transitions, the ownership boundaries (who writes, who reads, who retries) and the failure output from the failing line backward. Read the real code on the path, not its docs.
4. **List hypotheses and rank them** with the table below. Take the cheapest test that separates the top two.
5. **Run the test, record the result,** update the table. Repeat. Narrow by bisecting: `git bisect` for a regression, halving the input, disabling half the middleware.
6. **Confirm the mechanism.** You are done when you can predict what a change to the cause would do to the symptom, ideally by showing that removing the cause removes the symptom in a scratch copy.

## Hypothesis table

| # | Hypothesis | Evidence for | Evidence against | Cheapest test | Result |
|---|---|---|---|---|---|
| 1 | | | | | |

Rank by how much evidence supports it and how cheaply it can be falsified. Keep disproved rows; they stop you re-testing them.

## Stopping

Stop when either holds:
- the evidence names a cause and you have proof, or
- you can name the exact blocker: the access, data, log or decision that is missing, and what it would settle.

Do not keep exploring for completeness once one of those is true.

## Report

```
Symptom: <observed, with exact output>
Cause: <the mechanism, in one or two sentences> | not established
Proof: <the test or trace that shows it, with the command and result>
Ruled out: <hypotheses disproved, one line each>
Blocker: <only if the cause is not established>
Fix: <not made, as no implementation was requested> | <proposed change in one line>
```

If asked to implement the fix afterward, the gate in `SKILL.md` applies: rerun the original reproduction and show it now passes.
