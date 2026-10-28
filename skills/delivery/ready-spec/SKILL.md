---
name: ready-spec
description: "Draft a repo-grounded, execution-ready spec for a backend or API change: frozen current contract, target modes, full lifecycle, error catalog, testable backward-compatibility guarantees, ordered tasks, test matrix, traceability and an independent adversarial review, a file map, per-task interfaces, blind spots and a hand-off choice, gated READY or BLOCKED. Use when the user asks for a detailed spec or design plan for an endpoint, event, consumer or contract change before an agent implements it. Not for a general step-by-step coding plan (write-plan) or grilling an idea (challenge-me)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - write-plan
    - codebase-learner
  invokes:
    - skill: codebase-learner
      when: API or flow in the repo is unknown
  tags:
    - spec
    - api
    - backend
  capabilities:
    - implementation_spec
  languages:
    - en

---

# Ready spec

Turn a feature request into a plan another agent can execute without making product or architecture decisions.

## Who reads this

The reader is an executor (an agent or a person) who has not seen the request, this chat or the repo. They write good code in the project's language once they know the exact interface and the exact test. Where the plan leaves a small gap, they can choose sensibly. What they cannot know is **what you decided**: which files, which names and signatures, which values the request pins, and which tests prove each task.

So the plan holds **decisions only**. Two failures to avoid:

- **Too thin.** Lines that decide nothing: "TBD", "handle edge cases", "add proper validation", "write tests for the above", or a type or function that no task defines.
- **Too thick.** A plan that is much longer than the code it describes has written the code. Give signatures, test names and exact values. Leave out bodies that the signature and the tests already decide.

## Scope check

If the request covers several independent subsystems, split it into separate plans, one per subsystem. Each plan should deliver working, testable software on its own. Tell the user about the split before you go on.

## Workflow

### 1. Ground the current behavior

Read the smallest evidence set that settles the change:

1. Route or entry point.
2. Controller, handler, or consumer.
3. Service, concern, client, and configuration on the request path.
4. Existing tests.
5. Published API or event contract.
6. Shared error handlers and middleware.
7. Library version and supported method signatures.

Use current source and tests over old notes. Cite every material claim with a path and symbol or line. Label anything inferred.

Do not plan a new error handler, state store, helper, route, or dependency until checking whether the repo already has one.

Also write down the **global constraints**: limits the request or the repo states for the whole change, such as version floors, banned or required dependencies, naming rules and platform needs. Copy the exact values. Every task inherits this list.

### 2. Freeze today's contract

Document what existing callers send and receive before describing the new design:

- Method and path.
- Request fields, defaults, limits, and combinations.
- Response body and status.
- Existing errors.
- Side effects and external calls.
- Current terminal behavior.

Include one sequence diagram and one representative request/response example. Preserve exact field and error names from the code.

### 3. Define the target as explicit modes

Name each request mode and its discriminator. Use a mode table when one endpoint supports multiple flows.

For every mode, define:

- Required, optional, ignored, and forbidden fields.
- External call made.
- Response shape.
- Terminal signal.
- Cleanup behavior.

Prefer additive fields and the current endpoint when that preserves semantics. Add a route, state store, or abstraction only when a current requirement needs it.

### 4. Specify the full lifecycle

Cover more than the happy path:

1. First request.
2. Continuation request.
3. Last non-empty result.
4. Terminal empty result or completion event.
5. Early cancellation or cleanup.
6. Expiration and retry.
7. Reuse of an expired or completed token.
8. Upstream timeout or partial failure.

State the exact loop condition a caller should use. Do not make callers infer completion from an unstable upstream detail.

### 5. Build the error catalog

Check shared handlers before adding local rescue logic.

For each failure, record:

| Field | Required content |
|---|---|
| Label | Stable spec/test identifier. Do not add it to runtime responses unless required. |
| HTTP or event outcome | Exact status or failure classification. |
| Trigger | Concrete invalid state or upstream response. |
| Response | Exact current or proposed body. |
| Likelihood | Integration-time, expected production, or operational. |
| Recovery | What the caller should do. |
| Compatibility | New-only or existing behavior. |

Define validation precedence. The first failing condition must be deterministic. Validation failures must assert that no downstream call happened.

Do not parse upstream error strings when an existing typed exception or shared handler already owns the mapping.

### 6. Lock backward compatibility

Write hard guarantees that tests can prove:

- Existing requests retain their meaning.
- Existing response keys, values, and statuses stay unchanged.
- New validation applies only to the new mode.
- Existing errors keep their body and status.
- No hidden session affinity or new server-side state appears.
- No unrelated endpoint, model, or public search path changes.

Name the regression test that proves each guarantee. “Should remain compatible” is not acceptance criteria.

### 7. Define the maintenance contract

Identify where future changes could fork behavior. Typical hazards are copied mapping loops, duplicated validation, separate PII handling, and per-mode response builders.

For each hazard, name:

- The single source of truth.
- The shared helper or boundary.
- The parity test.
- The rule for adding a future mode or field.

Extraction is justified only when it prevents two real paths from diverging. Keep one-caller helpers inline unless the lifecycle becomes clearer by naming them.

### 8. Group files into ordered tasks

**Map the files first.** Before you draw task boundaries, list every file to create or change, and give each one a single responsibility. Files that change together live together, so split by responsibility, not by layer. Follow the patterns the repo already uses. Propose splitting a file only if a file you must touch is already too big to hold in your head.

Group file-level changes into a task only when they share one behavior boundary, one rollback unit, and one
verification boundary. Split into separate tasks when any of those differ — a task is a unit someone could revert
or re-verify alone.

Assign each task a stable ID (`T1`, `T2`, ...) ordered by dependency, then by the mode or goal it serves. A task
depends on another only for data flow, contract sequencing, or an explicit mode precedence — name the reason, not
just the order.

For each file inside a task:

1. Name the symbol to change.
2. State the smallest behavior change.
3. Show short pseudocode only where branch ownership is unclear.
4. State what remains untouched.
5. Name the focused verification command.

Do not use drifting line numbers as the primary anchor. Use symbols, with lines only as supporting evidence.

#### Interfaces between tasks

An executor may see only their own task. So each task states what it **consumes** (names and signatures from earlier tasks) and what it **produces** (names, parameters and return types that later tasks rely on). When one task refers to another, it points at that task's interface. It does not repeat that task's code.

#### What each step must say

A step is done when the executor can write exactly one reasonable thing from it. That is the test: clear, not complete. Each kind of step carries what makes it clear and nothing more.

| Step | Must contain |
|---|---|
| **Test** | The test's name, and its assertions as code, with the exact values the request pins |
| **Code** | The file, the exact signature (name, parameters, return type), and the values the request pins. A body only for an algorithm that the signature and tests do not decide, or for text the request fixes exactly. One line on the approach when a real choice is left (which library call, which data structure) |
| **Verify** | The command to run, and the output that means it passed |
| **Cross-task** | A pointer to the other task's interface |

### 9. Write the test matrix

Split coverage into:

1. New happy paths.
2. Boundaries and terminal states.
3. Validation failures.
4. Upstream failures.
5. Cleanup and idempotency.
6. Existing behavior regression.

Each row states Given, When, and exact assertions. Include outbound method, path, body, response shape, transformed fields, status, and whether the downstream was called.

Keep existing cases unedited when they are the compatibility proof. Add focused parity tests when shared logic is extracted.

Before you write rows, choose the **seams** the tests will cross. Prefer an existing seam to a new one, and use the highest seam that still exercises the behavior. Fewer seams is better, and one is the ideal. Confirm the seams with the user. The rules are in `tdd` (`references/core/seams.md`).

**Blind spots.** The request describes what the software must do. It does not list everything the software will meet, and silence about an input is not permission for that input to break. After the matrix, name up to five inputs or conditions that the request implies, that no row exercises, and that are most likely to hurt a real user. Put the most likely first. For each, say the behavior a reasonable person would expect. Then add a test row for each to the task that owns the code. An empty list means you checked and found none. It does not mean you skipped the check.

### 10. Trace goals to tasks and tests

Build one table: each goal or mode maps to the task ID(s) that implement it and the test ID(s) that prove it.

Close every gap before presenting the plan:

- A goal with no task is missing implementation.
- A task with no test is unproven.
- A test with no goal or task behind it is scope creep — cut it or name the goal it actually serves.

### 11. Run a completeness pass

Before presenting the plan, challenge it:

- Can an existing caller observe any difference?
- Is there an undefined terminal state?
- Can two request modes be selected at once?
- Can validation reach the upstream unnecessarily?
- Is cleanup defined for completion, cancellation, and expiration?
- Did the plan duplicate an existing handler or helper?
- Does every error have caller recovery?
- Does every hard guarantee have a test?
- Can an executor implement it without choosing between alternatives?

Resolve open technical facts from the repo or documentation. Ask the user only for genuine product choices.

Then check the plan against the request, one pass each:

1. **Coverage.** Take each requirement in the request. Can you point at a task that does it? List the gaps and add the missing tasks.
2. **Step scan.** Can the executor write exactly one reasonable thing from every step? Fix steps that decide nothing, and steps that carry a body the signature and tests already decide.
3. **Name check.** Do names, signatures and field names in later tasks match the ones you defined earlier? A function called `clearLayers()` in Task 3 and `clearFullLayers()` in Task 7 is a bug.
4. **Blind spots.** Is each blind-spot line backed by a test in the owning task?
5. **Proportion.** Compare the length of the plan with the length of the request. If the plan is several times longer than it needs to be, or code blocks are most of the page, replace bodies with signatures, test names and assertions, and check each step is still clear.

Fix what you find, then go on. No second round is needed.

### 12. Get an independent adversarial review

A self-check inherits the same blind spots that produced the draft. Before presenting the plan, hand the
finished draft — not the research trail that produced it — to one fresh reviewer with no prior exposure to this
conversation: use the Agent tool with a `general-purpose` or `Plan` subagent (not `fork` — a fork inherits your
context and your blind spots along with it). Give it the draft plan, the completeness questions from step 11,
and the "Done when" checklist below, and ask it to name concrete failure scenarios, not style opinions.

Sort every finding the reviewer returns into one bucket:

| Bucket | Meaning |
|---|---|
| Act on | A real gap in lifecycle, errors, compatibility, or test coverage. Fold it into the plan before presenting. |
| Consider | Legitimate but genuinely optional for this change's scope. Surface it to the user; do not fold it in silently. |
| Noted | Correct but low-impact or premature at this stage. |
| Dismissed | Wrong, or missing context the draft already covers. State why in one line. |

Skip this step only for a change small enough that step 11's self-check already exhausts the failure surface
(for example, an additive field with no new lifecycle or error path) — say so explicitly instead of silently
omitting it.

### 13. Hand off the plan

After the gate and the review, give the plan to the user and ask them to read it. Save it where the repo keeps specs (`docs/specs/` if it has none), unless the user names a path. Wait for their answer before any implementation starts.

If the user has not chosen how it will be built, offer the two ways, and recommend one:

- **One executor per task.** A fresh agent builds each task (`implementer` or `tdd-runner`), and a fresh reviewer checks it before the next task starts, coordinated by the `coordinator` agent. Most thorough. Costs a fresh context for every task and every review.
- **One session.** You build every task in this session with `tdd`, then run one independent review of the whole branch with `second-opinion`. Faster and cheaper. There is no independent review until the end.

Give your pick and one reason from the plan itself: how much the tasks depend on each other's interfaces, how many tasks there are, and what a shipped mistake would cost. If the user already chose a method, keep it and only ask whether the plan captures what they want.

## Output

Use [SPEC_TEMPLATE.md](SPEC_TEMPLATE.md). Keep the plan proportional to the change, but do not omit lifecycle,
errors, compatibility, or tests for stateful API work.

Mark the plan `Gate: READY` only once every "Act on" finding from step 12 is folded in and no genuine product
decision is open. Otherwise mark `Gate: BLOCKED` and list the open product decision or unresolved "Act on" item
in place of a plan that looks finished but isn't.

## Done when

- Current and target flows are both visible.
- Every mode has a terminal state and cleanup rule.
- The error catalog names exact outcomes and recovery.
- Backward compatibility is expressed as testable guarantees.
- Shared logic has one named owner.
- Tasks have stable IDs, dependency order, and a named rollback/verification boundary.
- The traceability table has no goal without a task, no task without a test, and no test without a goal.
- The test matrix covers behavior, boundaries, errors, and regression.
- An independent adversarial review ran (or its skip was stated and justified) and every "Act on" finding is
  resolved.
- No unresolved technical decision is left to the executor.
- Every file in the plan has one responsibility, and every task lists what it consumes and produces.
- No step says "TBD", "handle edge cases" or anything else that decides nothing, and no step carries a body the signature and tests already decide.
- Names and signatures match across tasks.
- Blind spots are listed, and each has a test in the owning task.
- The user was offered the choice of how to execute, with a recommendation.

## Related skills

- `codebase-learner` or `trace`: ground the current behavior or its constraints first.
- `challenge-me`: a product decision is still open.
- `write-plan`: turn a READY spec into bite-sized coding tasks.
- `second-opinion`: one independent review of the whole branch after the tasks are built.
- `tdd`: execute the tasks test-first.
