---
description: "Write a dated handoff note so a fresh session can continue this work."
argument-hint: "[topic]"
---

Use the handoff skill to write a dated handoff note for the current work. Topic: $ARGUMENTS (infer it from the work when empty).

Name the file `YYYY-MM-DD-handoff-<topic-slug>.md` with today's date from `date +%F`, in `handoffs/` or the project's own notes folder. Fill the template with goals, context, state, checklist, decisions, open questions, and exact resume commands. Take the branch, commit, and uncommitted files from git. Mark anything unverified. Do not include secrets. Do not commit the file. Reply with the path, a three-line summary, and a prompt I can paste into the next session.
