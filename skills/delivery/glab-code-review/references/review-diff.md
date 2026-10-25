# Diff review (pre-PR)

Review your own change the way a careful teammate would, before anyone else sees it. Use this mode for **local working tree** review (`git diff`, `git diff --staged`), not GitLab MR drafts.

## Procedure

1. Read the full diff (`git diff` plus `git diff --staged`). Do not skim.
2. For each changed function, ask: what input breaks this? Check empty, null, huge, concurrent and error cases.
3. Check that every behavior change has a test, and that the tests would fail without the change.
4. Flag scope creep: edits unrelated to the stated goal belong in a separate change.
5. Report findings grouped as **Must fix**, **Should fix**, **Nit**. For each give the file and line, the failure scenario, and a suggested fix.

## Pitfalls

- Say "no findings" when there are none. Do not invent nits to look thorough.
- Separate what you verified (ran it) from what you only read.

## When to use

Before opening a PR or MR; after a large local edit when you want a structured self-review without dispatching a subagent. For **git-range** review with a dispatched reviewer, use **Request** mode in the skill router instead.
