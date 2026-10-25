# Investigate first

Use when the cause is unknown: an intermittent failure, a performance regression, a change that "worked yesterday", a symptom with no obvious owner. The output is a cause with proof, or the exact blocker. A fix is a separate step the task must authorize.

## Contents
- Rules
- Get a loop that can fail
- Procedure
- Hypothesis table
- Same fix keeps failing
- Stopping
- Report

## Rules

1. **Separate the symptom from the cause.** The symptom is what was observed (an error, a number, a screenshot). The cause is your explanation for it. Write them as two different lines.
2. **No edits until one credible mechanism explains all the evidence.** A guess that fits some of the evidence is a hypothesis, not a cause.
3. **Cheap, falsifying tests first.** Prefer the check that would most quickly kill a hypothesis over the one that would merely support it.
4. **Make no fix unless the task authorizes implementation.** Reproduction scripts and logging that you remove afterward are not fixes; say what you added and remove it.
5. **Redact secrets before you show anything.** Commands, outputs and captured files go into the report. Write `<REDACTED>` for every token, key and password, and build loops against environment variables so the secret stays in the environment.

## Get a loop that can fail

Before you theorize, get one command that fails when this bug is present. That command is your loop. With it you can test every idea fast. Without it you are guessing.

Pick the cheapest loop that fits. These are the usual families:

| Family | Loops |
|---|---|
| Test shaped | A failing test at the nearest seam. A CLI run on a fixed input, diffed against known good output. |
| Request shaped | A `curl` script against a dev server. A headless browser script that checks the page, the console or the network. |
| Data shaped | Replay a captured request, payload or event log through the code path alone. Run old and new versions on the same input and diff. A bisection harness for a bug that appeared between two states (`git bisect run`). |
| Stress shaped | A fuzz or property loop for "sometimes wrong output". Run the trigger 100 times in parallel. |
| Fallback | A small throwaway harness that starts one part of the system with fakes. A script that walks a person through each step and records what they report. |

Then make the loop **quick, sharp and steady**:
- **Quick:** cache the setup. Narrow the test.
- **Sharp:** assert the exact symptom, not just "did not crash".
- **Steady:** pin the clock, seed the random numbers, isolate the files, freeze the network.

A flaky loop that takes 30 seconds helps little. A steady one that takes 2 seconds is a big advantage.

**Flaky bug?** You do not need a clean repro. You need a higher hit rate. Repeat the trigger, add parallel load, shrink the timing window, add sleeps. A bug that shows up half the time is easy to chase. One that shows up 1% of the time is not, so keep raising the rate.

**The loop is ready when it has all four:**
1. **Red on purpose.** It runs the real bug path and checks the user's exact symptom. It can go red on this bug and green once fixed. "Runs without errors" is not enough.
2. **Same result each time.** Or, for a flaky bug, a stated high hit rate.
3. **Quick.** Seconds, not minutes.
4. **Solo.** You can run it without a person, unless it is the walk-through fallback.

If you catch yourself reading code to build a theory before this command exists, stop and build the loop first.

**Cannot build one?** Say so and list what you tried. Then ask for one of these: access to an environment that reproduces it, a captured artifact with secrets removed (a HAR file, a log dump, a core dump, a screen recording with times), or permission to add temporary instrumentation in production. Do not guess without a loop.

## Procedure

1. **State the symptom precisely.** Exact message, input, environment, frequency, first-seen revision if known. If you cannot reproduce it, say so and treat reproduction as the first job.
2. **Reproduce or bound it.** Get the loop first (see above). Then shrink the repro. Remove one input, caller, setting or step at a time and rerun. Keep only what the failure needs. You are done when removing anything left makes the loop pass. If it is intermittent, find what varies (timing, order, data, load) before you theorize.
3. **Trace.** Follow the inputs, the state transitions, the ownership boundaries (who writes, who reads, who retries) and the failure output from the failing line backward. Read the real code on the path, not its docs.
4. **List three to five hypotheses and rank them** with the table below. Each one must predict something you can check: "if X is the cause, then changing Y makes the bug go away." A hypothesis that predicts nothing is a guess. Sharpen it or drop it. If the user is around, show them the ranked list first. They often know something that changes the order. Then take the cheapest test that separates the top two.
5. **Run the test, record the result,** and update the table. Repeat. Change one thing at a time. A debugger, or one log at the point that separates two hypotheses, beats many logs. Start every debug log with the same unique tag, such as `[DEBUG-a4f2]`, so cleanup is one search. For a slow path, logs are the wrong tool. Measure a baseline first with a timer, a profiler or a query plan, then bisect. Narrow it down by bisecting: `git bisect` for a regression, half the input, half the middleware off.
6. **Confirm the mechanism.** You are done when you can predict what a change to the cause would do to the symptom, ideally by showing that removing the cause removes the symptom in a scratch copy.

## Hypothesis table

| # | Hypothesis | Evidence for | Evidence against | Cheapest test | Result |
|---|---|---|---|---|---|
| 1 | | | | | |

Rank by how much evidence supports it and how cheaply it can be falsified. Keep disproved rows; they stop you re-testing them.

## Same fix keeps failing

If two or more fixes have failed the same check, the fixes may not be the problem. They may share a wrong assumption. A third fix on that assumption wastes time.

1. List the fixes you tried. Write down what each one assumed. Find the assumption they share.
2. Design one observation that would look different if that assumption were false. Look at how the failures are spread, not only how large they are.
3. Run it. If the result contradicts the assumption, the cause is somewhere else. Look for what the failures have in common that the assumption did not predict. If the result agrees, ask the next "why".

Do not write the next fix until you have written the assumption down and tested it.

## Stopping

Stop when either holds:
- the evidence names a cause and you have proof, or
- you can name the exact blocker: the access, data, log or decision that is missing, and what it would settle.

Do not keep exploring for completeness once one of those is true.

## Report

```
Symptom: <observed, with exact output>
Cause: <the mechanism, in one or two sentences> | not established
Proof: <the test or trace that shows it, with the command and result>
Ruled out: <hypotheses disproved, one line each>
Blocker: <only if the cause is not established>
Fix: <not made, as no implementation was requested> | <proposed change in one line>
```

If asked to implement the fix afterward, the gate in `SKILL.md` applies: rerun the original reproduction and show it now passes.
