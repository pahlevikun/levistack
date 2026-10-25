# Synthesis

How to turn several reviewers' output into one list of findings and one list of questions, before you judge anything.

## Merge findings

Two findings are the same issue when they point at the same cause, even if they name different lines or use different words. Merge them into one finding with:

- one title that names the cause, not the symptom
- every location the reviewers gave
- the highest severity any reviewer gave, with a note if they differed
- the reviewers who raised it (A, B, C)

Do not merge two findings only because they sit in the same function. Different causes stay separate.

## Weight the signal

| Signal | Weight |
|---|---|
| Two or more reviewers raised it on their own | Highest. Treat it as likely real |
| One reviewer, with a traced execution path | High. Check the path yourself |
| One reviewer, security or data loss | High. Never dismiss without tracing it |
| One reviewer, a hypothetical ("what if…") | Low until you find a real caller that triggers it |
| One reviewer, style or naming | Low. Usually Noted or Dismissed |

Agreement between reviewers on the **same model** counts less than agreement across models. Note which models agreed.

## Disagreements

When one reviewer flags something and another says the opposite:

1. Read the code yourself and see which reading it supports.
2. If the code settles it, keep the finding that matches and note the other as Dismissed with the line that disproves it.
3. If the code does not settle it, it needs a fact only the author has. Make it a Q-n node: "Reviewer A says [x], reviewer B says [y]. Which matches how this is used?"

## Calibrate severity

Reviewers often over-rate. Before you bucket, check each `critical`:

- Is there a real path to the failure, or only a possible one?
- Does the risk node change it? A crash in a one-off script is not critical. A wrong total on a checkout path is.

Lower the severity when the path is not real, and say why.

## Collect the questions

From every reviewer's Questions for the author:

1. Merge duplicates.
2. Answer any the code can answer. Mark them `inferred: <path>` in the ledger.
3. Tie each remaining question to the finding it decides.
4. Order them so the most decisive question comes first: one that could dismiss an Act on finding beats one that tweaks a Consider finding.

These become the Q-n nodes, and they get asked before lead judgment.

## Empty reviews

If a reviewer returns "no findings", record it. An empty review from a strong model on a small change is a real signal that the change is fine. Do not send it back to "try harder".
