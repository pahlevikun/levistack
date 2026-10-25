# Root-cause mode (Five Whys, with evidence)

Drill from a symptom to the cause that, if fixed, stops the whole class of problem. Ask "why?" again and again. Every answer is a link in a chain, and every link needs evidence.

## Variables

| Variable | Default | Meaning |
|---|---|---|
| `ISSUE` | ask for it | The problem or symptom to analyze |
| `DEPTH` | 5 | A guide, not a target. Stop at the real root cause, which can come at 3 whys or at 8 |

## 1. State the problem

Write the problem so nobody can read it two ways:

```
Problem: <what was observed, in one line>
Where: <service, page, job, pipeline, environment>
When: <first seen, how often, still happening?>
Impact: <who or what is hurt, how much>
Evidence: <the error text, the metric, the ticket, the incident doc>
```

Keep the symptom and the cause apart. "Checkout returns 500" is a symptom. "The payment call times out" is already a cause, so it belongs in Why 1.

## 2. Pin the first cause

Why 1 must be the mechanism that directly produces the symptom, with proof.

- **The failure is live and the mechanism is not confirmed:** run `verify` in investigate-first mode (reproduce, bound, trace, falsify) before you build the chain. A chain built on a guessed Why 1 is fiction.
- **The failure is past (an incident, a postmortem):** take Why 1 from the record: error tracking, logs, the incident doc, the fixing commit. Use the investigators from rationale mode for the categories that hold this evidence (observability, error tracking, chat, tickets, source control).

## 3. Build the chain

For each answer, ask "why did that happen?" and write the next link:

```
Why 1: <cause of the symptom>
  Evidence: <citation: file:line, commit, log line, dashboard, ticket, doc>
  Tier: Direct | Supported | Inferred | Speculative
Why 2: <cause of Why 1>
  Evidence: ...
  Tier: ...
...
Root cause: <the systemic cause>
```

Tiers come from `epistemics.md`. A link with no evidence is `Speculative` and must say what evidence would confirm it.

Each link answers the link above it, and only that one. If an answer explains something else, it starts a new branch.

## 4. Branch when causes split

One why often has more than one cause. Give each its own branch (A, B, …) and finish each branch on its own:

- **Necessary causes:** the symptom needs all of them. Fixing any one prevents it. List them as separate branches that join.
- **Independent causes:** each one alone is enough. Each needs its own fix.
- **Contributing factors:** they made it worse or more likely, but did not cause it. Note them under the chain, not as roots.

## 5. Double-check every chain

Run every check in `cause-checks.md` before you accept a root cause: the backward read, the counterfactual, falsification, the timeline, the competing chain, and the human-error rule. A chain that fails a check is not done. Fix the failing link, or mark the chain `not established` and say what evidence is missing.

## 6. Know when to stop

Stop when the cause is **systemic and in the team's control**, and fixing it would stop this whole class of problem, not just this one case. Root causes usually look like one of these:

- missing validation or a missing check (in code, in CI, in review)
- missing or wrong documentation
- an unclear or missing process
- missing automation (a step a person must remember)
- a missing test or a missing alert
- a config or standard that is not the same everywhere

Do not stop at:

- **"Human error."** Keep digging: why was the error possible, and why was it not caught?
- **"A third party failed."** Ask why the system was not resilient to it.
- **"Bad luck" or "a one-off."** Ask what made the system fragile enough that luck mattered.
- **A technical detail** ("missing index") when the reason that detail could ship ("migration review does not check query plans") is still one why away.

Stop and say so when the evidence runs out. A chain that ends in `not established: <the missing log, access or person>` is honest. A chain that ends in a guess is not.

## 7. Propose fixes

For each root cause:

```
Root cause A: <one line>
  Fix: <the change that removes the root cause>
  Containment: <optional: the quick fix that stops the symptom now>
  Verify by: <how to show the symptom is gone: the test, the query, the metric>
  Watch for recurrence: <the alert, dashboard or check that would show it coming back>
```

Label containment as containment. A containment fix shipped alone is a symptom fix.

Propose only. Do not change code. The user decides, then `tdd` or `safe-refactor` makes the change and `verify` proves it.

## Output

```markdown
### Problem
<the problem block from step 1>

### Cause chain
<one chain, or Branch A, Branch B, …, each link with Evidence and Tier>

### Root cause(s)
- A: <one line> (necessary | independent)
- Contributing: <factors that made it worse, not roots>

### Checks
| Check | Result |
|---|---|
| Backward read | pass / fail: <link> |
| Counterfactual | pass / fail |
| Falsification | <what was looked for, what was found> |
| Timeline | pass / fail |
| Competing chain | <the alternative, and why it lost> |
| Human error rule | n/a / applied at Why N |

### Fixes
<one block per root cause from step 7>

### What we don't know
<gaps, with what was searched, and who might know>

### Sources consulted
<one line per evidence category, including empty and skipped ones>
```

Examples: `root-cause-examples.md`.
