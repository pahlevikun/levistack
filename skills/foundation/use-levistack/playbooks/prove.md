# Prove

**Step 6**, after the work in step 5 and before [deliver.md](deliver.md).

## Evidence for every claim

Run [verify](../../../engineering/verify/SKILL.md) before the reply says done, fixed, passing, ready or works.

- The proof is fresh (run in this session, after the last edit) and matches the claim. A unit test does not prove a UI works.
- What could not be checked is listed as **not verified**, with the reason.
- A subagent's "success" is a claim, not proof. Check its output.

Skip only when nothing was changed and the reply makes no claim about behavior (for example a `codebase-learner` or `trace` answer).

## The human gate

Local, reversible work runs without asking. These stop for a yes:

| Action | Show before asking |
|---|---|
| `git push`, force push, branch delete | Branch, remote, commits that will go out |
| Open or update an MR or PR, post a review comment | The exact title, body or comment text |
| Publish, deploy, send a message or email | The target and the exact content |
| Install a skill or package from outside the catalog | Source, install count, the command |
| Delete files, `reset --hard`, drop data | What is lost and whether it can come back |

Show it once, wait for the answer, then run it. A yes covers that one action, not the next one.

After the action runs, re-check its result (the MR exists, the push landed, the test is still green) and put that line in the reply.
