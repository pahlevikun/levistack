# Verify only

The task is validation, not change: "run the gates", "check this is ready", "does it meet the acceptance criteria", a last-mile proof before merge. The output is a verdict backed by commands, not a better codebase.

## Contents
- Rules
- Steps
- Reusing a result
- Status words
- Report

## Rules

1. **Do not edit product code** unless the request includes fixing what fails. Report failures; do not repair them.
2. **Smallest sufficient proof.** Translate each acceptance condition into the cheapest check that settles it. Do not run everything because everything exists.
3. **Focused before wide.** Run the check closest to the claim first, then widen only to the gate the claim names (full suite for "no regressions", the build for "ships").
4. **Stop when the criteria are proven.** No cleanup, no polish, no extra tests, no "while I'm here" findings after the last criterion passes.

## Steps

1. **List the acceptance conditions.** From the request, the ticket, the plan or the PR description. Number them. If none were given, state the ones you will assume and why.
2. **Map each to a proof.** One command, URL, click path or diff check per condition. See `proof-by-change.md` for the right check by kind of change. A condition with no possible proof is marked `unavailable`, not skipped silently.
3. **Check what is still valid.** See "Reusing a result".
4. **Run in order, narrow to wide.** Stop at the first failure of a blocking gate and report it; continue past a failure only when the conditions are independent and the user wants the full picture.
5. **Read each output** the way the gate in `SKILL.md` requires: exit code, executed counts, skips.
6. **Report** with the status words below and stop.

## Reusing a result

A result from earlier in the session may be reused only when all of these hold:
- the repository state is the same: same commit and no changes since (`git rev-parse HEAD` and `git status --porcelain` match what they were when it ran);
- it was the same command with the same configuration and environment;
- its output is in front of you, not remembered.

Otherwise run it again. Say which results were reused and which were fresh.

## Status words

Use exactly these, per condition:

| Status | Meaning |
|---|---|
| `pass` | The proof ran and confirms the condition |
| `fail` | The proof ran and contradicts it |
| `unavailable` | No way to run the proof here (missing tool, no access, external system) |
| `blocked` | The proof could not run because something else failed first or needs a decision |

Never fold `unavailable` or `blocked` into `pass`.

## Report

```
Verdict: <ready | not ready | partially verified>
1. <condition>: <status> - <command> -> <result>
2. ...
Not verified: <conditions that were unavailable or blocked, and what would settle them>
Residual risk: <only what is material>
```

Commands, results and unresolved risk only. No narrative, no recommendations beyond what unblocks a `blocked` item.
