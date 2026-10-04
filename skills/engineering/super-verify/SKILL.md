---
name: super-verify
description: "Evidence before claims and before fixes. Use before saying work is done, fixed, passing or ready (tests pass, build succeeds, bug fixed, ready to merge, handing off, before a commit, push or PR), when asked only to verify or run the gates, or when a failure has an unknown cause and must be diagnosed before editing. Requires a fresh, claim-matched proof, honest reporting of what was and was not checked, and stopping once the proof is complete."
when_to_use: "Use proactively when about to write 'done', 'fixed', 'all tests pass' or 'ready to merge'; when the user says 'verify', 'validate', 'run the gates', 'prove it', 'is it really fixed' or 'why does this fail'; when a subagent reports success; or when a request has an ambiguous scope before editing."
metadata:
  version: "1.0.0"
---

# Super Verify

A claim is only as good as the evidence behind it, and a fix is only as good as the diagnosis behind it. This skill does three jobs:

| Job | When | Where |
|---|---|---|
| **Gate a claim** (default) | You are about to say something is done, fixed, passing or ready | This file |
| **Verify only** | The task is validation, not change: run the gates, prove acceptance, stop | [verify-only.md](references/verify-only.md) |
| **Investigate first** | A failure has an unknown cause, or the problem is intermittent or a regression | [investigate-first.md](references/investigate-first.md) |

## The rule

**No completion claim without fresh evidence that matches the claim.**

- *Fresh:* produced after the last change, by a command you ran in this turn. An earlier run, a remembered pass, a subagent's report and confidence are not evidence.
- *Matches the claim:* a focused test supports the behavior it names, not "all tests pass". A linter does not prove the build. Passing tests do not prove the requirements were met.
- *Claim only what the evidence shows.* A narrower claim that is true beats a broad one that is assumed.

Rephrasing does not exempt you. "Looks good", "that should do it", "all set" and a relieved tone are claims too.

## The gate

Run this before any claim, a commit, a push, a PR, or moving to the next task.

1. **Scope.** If the request is ambiguous about how much to touch, inspect the repository and state the safe assumption; ask only when readings differ materially, and do not edit the disputed part meanwhile. Check `git status --porcelain` and leave unrelated changes alone.
2. **Identify** the command that proves this claim. For a ship-level claim run the whole applicable chain (build, types, lint, tests, security scan, diff review) in the project's own order and stop at the first failure. Use the gates the project declares in `CLAUDE.md`, `AGENTS.md` or `CONTRIBUTING.md`; do not invent gates.
3. **Run** it now, in full, against the current state.
4. **Read** all of it: the exit code, the executed and passed counts, warnings, skipped tests, missing artifacts. A suite that ran nothing exits 0. Confirm the intended binary, revision and entry point actually ran. [read-run.mjs](scripts/read-run.mjs) does the counting for common runners.
5. **Match.** Does the output cover the requirement and one failure path? Re-read the requirements line by line. A stub, a mock, an unreachable branch or a refusal-only path is partial.
6. **Claim** what the evidence establishes, plus what was not checked and the real residual risk. Use [evidence-report.md](templates/evidence-report.md) when a report helps; skip empty sections.

## What each claim needs

| Claim | Proof | Not proof |
|---|---|---|
| Tests pass | Runner output with a positive executed count and 0 failures | A previous run, "should pass", a green exit with 0 tests |
| Build succeeds | The build command, exit 0 | A clean linter, readable logs |
| Types or lint clean | That tool's own output | A different tool, a partial path |
| Bug fixed | The original reproduction now passes | "I changed the code" |
| Regression test is real | Red then green: fails without the fix, passes with it | One passing run |
| Feature complete | Each acceptance criterion checked | Tests passing |
| No regressions | The full suite, same command set as before | Only the new tests |
| Subagent finished | The diff shows the change and you ran the check | The agent's summary |

Proof by kind of change (frontend, endpoint, queue, CLI, migration, infra, package, docs) is in [proof-by-change.md](references/proof-by-change.md).

## Do not make the proof easier

Never weaken a test, assertion, validator or acceptance criterion to get green. Never delete, skip or mark a test expected-to-fail to pass. Never hard-code the exercised value or success path. Regenerate snapshots or expected output only after reviewing and justifying the change. Never bypass a failing pre-commit hook that this work caused (`--no-verify`). Fixtures, mocks and recorded responses support deterministic tests; they are not live behavior. Details: [proof-integrity.md](references/proof-integrity.md).

## When verification fails

Report the failure with its output. Do not rerun unchanged hoping it passes, and do not claim success. Fix the cause and restart the gate. Calling a failure pre-existing, environmental or flaky needs evidence: reproduce it on the base revision, or name the independent cause. Details and handoff rules: [failures-and-handoff.md](references/failures-and-handoff.md).

A clean result is a valid result. Do not invent findings to look thorough, and do not keep adding checks, polish or unrelated tests after the stated criteria are met. Stop when the proof is complete.

## Which reference

| Situation | Read |
|---|---|
| The task is only to verify or run the gates | [verify-only.md](references/verify-only.md) |
| Unknown cause, intermittent failure, regression, "why" | [investigate-first.md](references/investigate-first.md) |
| Choosing the right check for a change | [proof-by-change.md](references/proof-by-change.md) |
| Dirty tree, upgrades, strict validation, fixture vs live | [proof-integrity.md](references/proof-integrity.md) |
| Empty results, wrapper scripts, wrong binary, totals that add up | [trustworthy-output.md](references/trustworthy-output.md) |
| "Every file", repo-wide rename, audit all, ledgers | [sweeps.md](references/sweeps.md) |
| A check failed, delegated work, deliverables, staleness, the final report | [failures-and-handoff.md](references/failures-and-handoff.md) |

## Done when

- Every claim in the final message is backed by output from this turn, or is labeled as not verified.
- The report names what was run, what was skipped, and the residual risk, with no empty sections.
- Nothing was weakened, skipped or bypassed to get the result.
