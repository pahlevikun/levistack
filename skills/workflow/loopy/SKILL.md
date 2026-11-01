---
name: loopy
description: "Repeat one bounded improvement until the named conditions pass or a stop state is reached. Use when asked to loopy, loop until it passes, iterate with fixes, keep going until every check is green, or polish until the gate is met. Not for a one-pass evidence task (evidence), test-first development (tdd), a single check report (verify), or specifying a recurring personal workflow."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: workflow
  category: workflow
  department: workflow
  related_skills:
    - evidence
    - verify
    - tdd
    - second-opinion
  invokes:
    - skill: verify
      when: A round needs a fresh check of the named pass conditions
    - skill: second-opinion
      when: The same actor should not both create and approve a consequential code change
  tags:
    - loopy
    - loop
    - iterate
    - stop-state
    - pass-condition
  capabilities:
    - bounded_improvement_loop
    - stop_state_receipt
  languages:
    - en

---

# Loopy

Repeat one bounded improvement until the named conditions pass or a stop state is reached. This skill owns the cycle and the stop rules. The task skill owns the edit. `verify` owns the check.

## When to use

- "Loopy", "loop until it passes", "keep fixing until every check is green", "iterate until the conditions are met".
- Not for a one-pass task (`evidence`), red-green-refactor (`tdd`), a single check report (`verify`), a spec for a recurring personal workflow, or a published loop catalog.

If a fresh observation cannot change the next action, do the work once and stop. That request is not a loop.

## Before round 1

1. Write the pass conditions as observations. If the user did not name them, ask. Do not invent a score, a coverage target, or a round cap.
2. Name the task skill that will make the change, the check, and the files or systems in scope.
3. Use a finite boundary only when the user supplied one: a round count, a time box, or a finite work list. Otherwise the extra stop is no progress.

## Each round

1. Re-read the current artifact and the last check. Do not act on a stale failure.
2. Choose one reversible change aimed at one failed condition. Invoke the task skill for that change. Do not copy its procedure here.
3. Invoke `verify` on that condition. A missing check is **blocked**, not a pass.
4. When the same actor should not both create and approve a consequential code change, invoke `second-opinion`, or a fresh reviewer that sees the product and not the worker's reasoning. Treat that review as a finding to check, not as proof.
5. Record the action, the check, the result, and what the next round would change.

A repeated failure with no new change is **no progress**. Stop. Do not start another round.

## Stop states

| State | Meaning |
|---|---|
| **Passed** | Every named condition matched a fresh check. |
| **Clean no-op** | The artifact already met the conditions before any edit. |
| **Blocked** | A required check, tool, or source is unavailable. |
| **Approval required** | The next action is destructive, production, financial, privacy-sensitive, or outward. Stop and ask. |
| **Boundary reached** | The user-supplied round, time, or work-list limit is spent. |
| **No progress** | A round repeated the same failure without a new change. |

Never report a failed check, an error, or a reached boundary as **Passed**.

## Receipt

Return the receipt from [references/receipt.md](references/receipt.md) in the reply. Write a file only when the user asks or the repo already keeps run notes.

## Related skills

- `evidence`: one evidence-led pass, a plan, or a read-only judge. Use it when the user did not ask to repeat until the conditions pass.
- `verify`: run the fresh check for a round.
- `tdd`: test-first red-green-refactor. Do not replace it with this loop.
- `second-opinion`: independent review when self-approval is the wrong gate.

## Done when

- The reply names one stop state and the checks behind it.
- Each round names one change and one fresh check, or an explicit gap.
- [evals/evals.json](evals/evals.json) covers a passing loop, a missing pass condition, and a request that belongs to `tdd` or `verify`.
