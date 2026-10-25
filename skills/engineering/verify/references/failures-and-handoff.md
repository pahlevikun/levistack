# Failures and handoff

What to do when a check fails, how to treat work someone else did, and how to write the final report.

## Contents
- When verification fails
- Pre-existing, environmental, flaky
- Pre-commit hook failures
- Delegated work
- Classifying deliverables
- Per-branch claims
- Stale reviews and stale state
- Final report

## When verification fails

1. **Do not claim completion.** Report the real output.
2. **Do not rerun unchanged** hoping for a different result.
3. **Return to the implementation,** fix the cause, and restart the gate from the top.
4. If the failure is not yours, say so with evidence (next section).

When the harness has a known noise floor (a stubbed dependency, an unsupported lane that fails the same block every run), the signal is the failing-set diff, not the pass count. Capture the failing test names on the unmodified base, rerun with your change, and diff the sets. An empty diff is the pass criterion.

## Pre-existing, environmental, flaky

Each label needs evidence before it is allowed.

- **Pre-existing:** reproduce the failure on the base the work was cut from, not on an intermediate state of your own branch. Show it.
- **Environmental or flaky:** name the independent cause, or show it passes alone and fails the same way on the base. Distrust a control that was expected to fail narrowly and came back wide: a whole class may not exist at that revision.
- Before either label, rule out the task's own formatters, hooks and generators. An aggregate check that broke because this change triggered a regeneration is a regression of this change.
- Flakiness is never a reason to skip the check.

## Pre-commit hook failures

A failing pre-commit hook is a checkpoint, not an obstacle. Do not use `--no-verify` when this session's changes caused the failure; fix the cause. It is allowed only when the failure reproduces on the base branch (and you showed that) and the user saw the failure first. A bypass the user never saw is a defeated check, the same failure as a completion claim with no evidence.

## Delegated work

Never relay a subagent's or another tool's "success".

1. Confirm with the version-control diff that the changes exist.
2. Run the verification command yourself.
3. Check compliance with the specification and quality separately; a change can pass review for style and miss a requirement.
4. Report what you verified, not what you were told.

## Classifying deliverables

Before calling a deliverable done, say how it can be verified, then verify that way:

| Class | Example | Route |
|---|---|---|
| Diff-verifiable | new service, validation logic, migration file | It appears in `git diff <base>...HEAD` and its check runs |
| Cross-repo | a file or contract in a sibling repository | If the sibling is on disk, check the path and content; otherwise it is unverifiable, so say what to check |
| External state | DNS record, console setting, OAuth allowlist, secret entry | Not checkable from the tree. Name the system and the exact check the user must run |
| Content shape | a file must follow a convention | Run the project's validator |

Outcome per deliverable: **done**, **partial**, **not done**, **changed** (same goal, different means; say how) or **unverifiable**. A concrete filesystem path is never unverifiable: check it exists. Code that *handles* a deliverable is not the deliverable; shipping the extractor is not shipping the extracted file. When torn between done and unverifiable, say unverifiable. A confirmation prompt costs seconds; a silently missed deliverable does not.

## Per-branch claims

"Only on main" and "the stable branch still has the guard" are claims a reviewer will test. Reading broken code on the branch you are patching proves nothing about the others. For each branch named, check that the introducing commit is or is not contained in it, and read the function at that branch's tip. A branch can contain the commit and have been fixed since, or lack it and be broken for another reason.

## Stale reviews and stale state

- **Reviews:** before shipping, check commits landed after the last review (`git log --oneline <review-commit>..HEAD`). Confirm the new commits do not undo what the review checked or approved.
- **Absence:** a snapshot fetched minutes ago supports "I did not see X", not "X does not exist". Refetch right before a conclusion that depends on nothing having happened (unpushed commits, a queued job, an unsynced remote). Line numbers and citations from the old state need recomputing too.
- **Target state:** before posting or approving, confirm the change is still open and not a draft, as well as that the head commit matches. A merged change at an unchanged head prints a clean match while the action is now impossible.
- Conclusions about a person's actions need a fresh fetch and a second corroborating signal before they go anywhere external.

## Final report

Include only what affects the handoff:

- the outcome, and the command, URL or click path that exercises it;
- the checks run, with results, where the reader cannot see them;
- anything failed, skipped, unavailable or only partly covered;
- the material residual risk, named plainly.

Name stubs, mocks, unreachable paths and refusal-only behavior as such. When blocked, name the concrete blocker and what is needed to continue. Do not add empty sections, "no concerns" lines or ledgers to look diligent, and do not state certainty you do not have.
