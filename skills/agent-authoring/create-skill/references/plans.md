# Plans as prompts

How to write a skill that produces plans, or a plan an agent can execute without asking questions. A plan is not a document that later becomes a prompt. The plan is the prompt.

## Contents
- When this applies
- Anatomy of an executable plan
- Anatomy of a task
- Size plans to stay in the good zone
- Checkpoints
- Deviations during execution
- Execution and fresh context
- Summary, handoff and resume
- Research before planning
- Gates and commits
- Keep planning light

## When this applies

- A skill whose output is a plan (roadmap, phase plan, migration plan).
- A skill that executes a plan someone else wrote.
- Any task big enough that one session will not hold it.

For a task that fits in one session, skip the plan and act.

## Anatomy of an executable plan

A plan is executable when the agent can start without a clarifying question. If it must guess, the plan is vague. Use `templates/plan.md`. Every plan has:

| Part | Holds |
|---|---|
| **Objective** | What it delivers and why; the artifact it produces |
| **Context** | The files and prior outputs to read first, by exact path |
| **Tasks** | Ordered, each with files, action, verify and done |
| **Verification** | Overall checks that run after the last task |
| **Success criteria** | Measurable conditions for "complete" |
| **Output** | What to write when finished (a summary file), with its structure |

Lower levels read the higher ones for context (a phase plan reads the roadmap; the roadmap reads the brief). Scope narrows going down; progress aggregates going up. If a prerequisite is missing, offer to create it rather than skip it.

## Anatomy of a task

| Field | Rule | Good | Bad |
|---|---|---|---|
| **Files** | Exact paths created or changed | `src/app/api/auth/login/route.ts` | "the auth files" |
| **Action** | What to do, what to avoid and why | "POST endpoint taking {email, password}; compare with bcrypt; return a JWT in an httpOnly cookie, 15-minute expiry. Use `jose`, not `jsonwebtoken` (CommonJS breaks on the Edge runtime)" | "Add authentication" |
| **Verify** | A command, test or observable behavior | `curl -X POST /api/auth/login` returns 200 with `Set-Cookie` | "It works" |
| **Done** | A testable acceptance state | "Valid credentials give 200 and a cookie; invalid give 401" | "Authentication is complete" |

If you cannot fill all four, the task is too vague. Do not write the code into the plan: say what and why, and trust the agent with how. Avoid "handle edge cases", "follow best practices" and "like the other endpoints"; the agent does not know your standards.

Size a task at roughly 15 to 60 minutes of agent work. Merge trivial ones; split any that would take several sessions.

## Size plans to stay in the good zone

Quality falls as context fills, and it falls earlier than the limit: when the agent senses the window closing it starts to compress ("I'll do the rest more concisely"). Plan for the good zone, not the maximum.

| Context used | Behavior |
|---|---|
| 0 to 30% | Thorough, full detail |
| 30 to 50% | Still good |
| 50 to 70% | Efficiency mode, shortcuts appear |
| 70%+ | Rushed, minimal |

**Rules:** a plan fits in about half the context, with **two or three tasks**. Treat these as heuristics to tune from experience, not measurements.

Split when any of these hold:
- more than three tasks;
- more than one subsystem (schema, API and UI are three plans);
- a task touches more than about five files;
- a checkpoint sits in the middle (work after a decision is a separate plan);
- research and implementation share a plan (research writes a findings file; implementation reads it);
- the domain is hard (auth, payments, data modeling) or the approach is uncertain ("figure out X" is its own plan).

Split by subsystem, by dependency, by complexity (simple, moderate, hard), or by verification point. Rough cost per task: simple CRUD about 15% of context, business logic 25%, a data model 35%, a complex algorithm 40%. Two moderate tasks are already at target; three hard ones will not fit.

Smaller plans also give smaller commits: each is reviewable and revertable on its own. More small plans beat fewer degraded ones.

## Checkpoints

A checkpoint stops execution for a person. Use few.

| Type | Use for | Share |
|---|---|---|
| `human-verify` | A person confirms what the agent built: visual layout, an interactive flow, playback quality | Most |
| `decision` | A person picks a direction: provider, architecture, design | Some |
| `human-action` | A step with no API or CLI: an emailed verification link, an SMS code, a 3-D Secure flow | Rare |

**The rule:** if the agent can do it through a CLI, an API or a tool, it must. Never ask a person to deploy, create a webhook, run a build, write a `.env` file or create a database. Automate everything, then checkpoint to verify.

**Authentication is a gate, not a failure.** When a command reports "not authenticated", stop, give the exact login step, wait, verify (`<tool> whoami`), retry the original step, and record it as normal flow. Do not retry in a loop.

**Protocol:** stop at once, show the checkpoint (what was built, numbered steps to verify, how to resume), wait for the answer, never invent the result, verify what can be verified, then continue.

**Placement:** after automation, before dependent work, at integration points. One verification at the end beats one after every task: more than that is checkpoint fatigue. For a `decision`, give balanced pros and cons for each option and no recommendation unless asked.

## Deviations during execution

The plan will be wrong somewhere. Decide in advance what the agent may do alone.

| # | Situation | Action |
|---|---|---|
| 1 | Broken behavior (wrong query, inverted condition, crash, injection) | Fix now, add a regression test, record it |
| 2 | Missing something required for correctness or security (validation, auth check, error handling) | Add now, with tests, record it |
| 3 | Blocked (missing dependency, broken import, bad config) | Fix to unblock, record it |
| 4 | Architectural change (new table, new service layer, swapping a library, changing the auth model, a breaking API change) | **Stop and ask** with the discovery, the proposed change, why, the impact, and alternatives |
| 5 | A nice-to-have (refactor, naming, extra coverage, docs polish) | Append to an issues log with a number, continue |

When more than one applies: 4 first, then 1 to 3, then 5; if unsure which, ask. Quick test: does it affect correctness, security, or the ability to finish? Yes means fix it (1 to 3). No means log it (5). Maybe means ask (4).

Record every deviation in the summary with: rule, task it was found in, the issue, the fix, files, how it was verified, and the commit.

If a task's verification fails, stop. Show expected and actual, and offer retry, skip (record it), or stop.

## Execution and fresh context

A plan with no checkpoints can run in a subagent with a fresh context, so it cannot degrade. A plan with checkpoints needs the person, so it runs in the main session. Group autonomous work into separate plans where you can.

To run a plan that has checkpoints, split it into segments at each checkpoint and route them:

| Segment | Runs in |
|---|---|
| No checkpoint before it | Subagent |
| After a `human-verify` checkpoint | Subagent (the check does not change what follows) |
| After a `decision` or `human-action` checkpoint | Main session (the next tasks need the answer) |

Brief each segment's subagent: read the plan; do only tasks X to Y; follow the deviation rules; do not write the summary and do not commit; report tasks done, files changed, deviations, blockers. Then aggregate the reports into one summary and one commit. Skip segmentation when most of the work depends on a decision. See `create-agent` for subagent prompts and orchestration.

Do not invoke a heavy planning skill just to execute: run the plan from its own file, which keeps the context small.

## Summary, handoff and resume

**Summary.** One per plan, written last. Its existence means the plan is done. Start with a one-line result that says what shipped ("JWT auth with refresh rotation using jose", not "authentication implemented"), then accomplishments, files, decisions, deviations, issues, and what the next plan can rely on. Keep "deviations" (unplanned work handled by the rules) apart from "issues" (problems in planned work).

**Handoff.** A parking lot, not a journal: written when leaving, deleted when returning. Use `templates/handoff.md`. It names the current position, what is done, what remains, the decisions with their reasons (so the next session does not re-argue them), blockers, the state of mind, and the very first action to take.

When to hand off: the user says "wrap up" or "save my place"; remaining context is about 15% (offer) or about 10% (do it without asking, at the next atomic boundary, then stop). Finish the current atomic step first (a file write, a validation run, one task); do not leave broken state.

**Resume.** Read the handoff, say how old it is (warn past about two weeks that the code may have moved), summarize position and remaining work, wait for confirmation, load the files it names, then delete it. With several handoffs, the newest is usually right; ask.

**Save context while working:** read a file once; summarize instead of quoting; read functions, not whole files; do not restate finished work.

## Research before planning

Plan only when the approach is known. If a technology choice or an API is unclear, write a research plan first, with:

- the question, what is in scope and what is not;
- exact source URLs for official documentation, and search queries that include the current year (check today's date first);
- the output file with a confidence level and open questions.

Write findings as you go, not at the end, so a token limit loses nothing: create the file with a skeleton, append each finding, finish the summary last.

After research, gate on confidence: low, ask whether to dig deeper, proceed or pause; medium, confirm briefly; high, continue. Show open questions before planning.

Avoid these research failures:

| Failure | Prevention |
|---|---|
| Assuming one configuration scope exists | List every scope (user, project, local, workspace, environment) and check each |
| "Search for docs" with no source | Name the exact official URLs |
| Concluding a feature is missing from old docs | Check the changelog and the date |
| Treating tools as interchangeable | Check each environment separately (desktop app, CLI, IDE extension, API) |
| A confident "not possible" with no citation | Require an official source; "I did not find it" is not evidence |
| Open-ended scope | Enumerate the options first, then record existence, source URL and status for each |
| One source for a critical claim | Two sources, one primary, and a contradiction check |

Distrust a report with no "not found" results, no confidence levels, no URLs, or definitive claims with no evidence.

## Gates and commits

**Ask when a decision is real, once, before writing.** Use a structured choice for two to four options, an inline question for yes or no. After gathering context, offer: proceed, ask more, or let me add context, and loop until proceed. Gate before writing artifacts, after low-confidence research, on verification failure, and before starting work that sits on top of unresolved issues. Do not ask obvious things ("save the file?"), duplicate a gate, or gate after the fact.

**Commit outcomes, not process.** Commit at initialization, when a plan completes (code plus its summary), and at handoff (as work in progress). Do not commit intermediate plan or research files on their own. A message like `feat(02-03): <one-line result>` makes the log read as a changelog.

## Keep planning light

For one person and one agent, leave out roles, stakeholders, ceremonies, hour estimates, story points and approval chains. If a section would exist only for show, delete it. The brief stays under about 50 lines with measurable success criteria and an explicit out-of-scope list; a roadmap has three to six phases and no more.

A sensible layout, if the repo has none:

```
plans/
  BRIEF.md              the vision, the only file written for people
  ROADMAP.md            phases and progress
  phases/01-name/
    01-01-PLAN.md       the executable prompt
    01-01-SUMMARY.md    exists means done
    01-02-PLAN.md
```
