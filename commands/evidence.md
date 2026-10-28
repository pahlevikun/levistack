---
description: "Frame a goal, run an evidence-led task, or judge a finished artifact or parallel agent results."
argument-hint: "<goal|run|plan|judge|report|domain> <request>"
---

Use the `evidence` skill for $ARGUMENTS. Select its mode from the request. If no mode is named, infer it from what the user wants and state the choice. Goal writes a prompt only when requested. Judge is read-only. Use `verify` for fresh checks and `second-opinion` for an adversarial code-change decision ledger when those jobs are needed.

Return the requested artifact or verdict with the evidence and limits that support it.
Do not edit the judged artifact in Judge mode or claim that Goal mode's future work has been completed.
