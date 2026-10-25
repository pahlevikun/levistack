# Prime from the prompt

**Step 2**, right after you accept the user message and before [invoke.md](invoke.md).

## What this is

Load [output-savers](../../../engineering/output-savers/SKILL.md) **Step 0** and its [auto-detect.md](../../../engineering/output-savers/references/auto-detect.md) against the **user's prompt**.

You do not compress or rewrite the user's words. You choose:

- the **safety override**: security, secrets, irreversible actions or ordered steps get full sentences
- the **job** (auto-detect 1 to 14): commit, review, code change, procedure, question, prose for people, …
- the **principles** to keep in scope during the work: minimal scope, YAGNI, context hygiene
- the **reply level** for step 7

Record the pick. Do not announce it unless it changes what you ask the user.

## Quick read of the workspace

Before step 3, note what the workspace already answers so you never ask it: the cwd, `git status` and branch, any file, link, MR or ticket the user named, and the newest handoff note if the user is resuming.

## What this is not

- Not the skill pick. That is [invoke.md](invoke.md).
- Not the final pass on your reply. That is [deliver.md](deliver.md).
