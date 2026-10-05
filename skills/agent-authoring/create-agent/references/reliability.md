# Making an agent fail well

An agent that fails loudly and usefully is better than one that looks successful. Most failures trace to one of five causes.

## Contents
- Where agent failures come from
- Recovery strategies
- Failing in a way the caller can use
- Context discipline
- Checklist

## Where agent failures come from

| Cause | Looks like | Prevent with |
|---|---|---|
| **Unclear spec** | Guesses, partial output, wrong assumptions | A specific role, numbered steps, a defined output and done condition |
| **Misaligned handoffs** | Duplicate work, contradictory reports, gaps | A structured handoff and one owner per concern |
| **No verification** | Wrong results pass silently | A check step in the prompt; an independent validator for high stakes |
| **Cascading errors** | One bad output breaks every later step | Each agent validates its inputs; fall back instead of failing whole |
| **Non-determinism** | Passes sometimes, fails sometimes | Run several times before trusting a fix; tighten the output format |
| **Context** | Missing facts, buried facts, an overflowing window | See Context discipline |

Most failures are context failures rather than model failures. Before blaming the model, ask whether the fact was in the prompt, whether it was findable, and whether the window was full.

## Recovery strategies

**Degrade, do not collapse.** Define a fallback order and flag what each fallback costs:

```markdown
1. Fetch the current docs. 2. If that fails, use the cached copy and flag its date.
3. If there is no cache, use the local stub and flag it as incomplete.
Always add a TODO where the output should be verified.
```

**Retry only what is transient, a bounded number of times.** Network errors, locks and rate limits get up to three attempts with a growing pause, then the fallback. A logic error is not transient: fix it, do not repeat it. Never retry without a limit.

**Stop calling what keeps failing.** If an endpoint has failed several times in a row, stop for a while and use the fallback source instead of spending tokens on a dead call.

**Bound the time.** If an operation runs long, abort it, return the partial results, mark them incomplete, and suggest the manual step.

**Layer the checks.** Each check catches a different class of error: parse, type check, lint, security scan, run the tests. If one fails, fix and re-run all of them.

**Know when to escalate.** If an automated fix fails twice, stop. Write down what was tried and why it failed, give the diagnosis, and list the questions for a person. Continuing to patch a failing approach wastes the budget and hides the cause.

## Failing in a way the caller can use

- **Never go silent.** "No issues found" after reviewing 3 of 10 files is a false pass. Report what was covered and what was not.
- **Never give up with nothing.** If the ideal source is missing, produce the best output the constraints allow and label its limits.
- **Explain errors.** "Failed" is useless. "Cannot read `src/auth.ts`: file not found. The review of the authentication code did not run. Check the path or whether the file moved" is actionable.
- **Use typed messages** between agents when they exchange work: a request (to do something), an inform (here is what I found), a commit (I will do this), a reject (I cannot, because ...). Say which kind each message is.
- **Validate before returning.** For structured output: parseable, all required fields present, values from the allowed list, locations in the stated format.
- **Use an independent validator** for high-stakes output: a read-only agent that checks format, completeness, internal consistency and that claims match their sources. Give it only the tools to read.

## Context discipline

The context window is working memory. Keep what the next few steps need; keep everything else outside it.

- **Core memory is small.** If a fact is not needed for the next three steps, it does not belong in the prompt. It can be retrieved later.
- **Put bulk in files.** Full logs, traces, exploration and intermediate results go to disk; the context holds state, decisions and the next step.
- **Use a scratchpad** for exploration: record each hypothesis and its result in a file, keep the current hypothesis and key findings in context, and summarize the path that worked.
- **Summarize in structure and in order.** Categories beat paragraphs. Keep the sequence: "first the direct fix failed on a type mismatch, then a conversion introduced a runtime error, then a type-safe wrapper worked" teaches more than "fixed it".
- **Do not summarize away the facts.** "Tried several things, fixed the bug" loses what failed, why and what worked. Keep the decisions and the rationale; move the detail to a file.
- **Do not dump.** Everything included "just in case" buries what matters.
- **Stateful agents** (called many times on one project) read a small state file at the start, update it at the end, and cap its size by summarizing old entries. **Stateless agents** (validators, formatters) read nothing and keep nothing. Make most agents stateless.
- **Compact at a boundary.** When the window is filling, finish the current atomic step, write task, status, key findings, decisions and next steps to a file, and continue from that.

A subagent starts with none of the main conversation. Anything it must know goes in its prompt or in a file it can read.

## Checklist

Put these into the prompt of an agent that matters:

- [ ] Validate inputs before working; stop and list what is missing.
- [ ] Check each tool result for errors.
- [ ] A fallback for the primary path failing.
- [ ] A bounded retry for transient failures.
- [ ] A limit on automated fix attempts, then a report.
- [ ] A verification step before returning.
- [ ] A report that says what was covered, what was not, and why.
