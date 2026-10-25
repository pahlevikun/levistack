---
description: "Prove the branch works, then draft the merge request description. Does not push or open anything without a yes."
argument-hint: "[target branch]"
---

Get this branch ready for review. Target branch: $ARGUMENTS (use the repository default when empty).

Use the verify skill first: run the gates (tests, lint, build) and report what you saw. Stop if a gate fails and show the output. When all gates pass, use the write-mr-description skill to draft the description from the commits since the branch diverged.

Reply with the gate results and the draft text. Ask before you push or open the MR. Do not claim a gate passed that you did not run.
