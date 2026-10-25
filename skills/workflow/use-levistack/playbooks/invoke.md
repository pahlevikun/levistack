# Invoke the first skill

**Step 3**, after [prime.md](prime.md). Pick **one** first skill before any catalog hunt, unless the user clearly asked for two things (see Chaining).

## Intent map

| The user wants to… (signals) | First skill |
|---|---|
| Know how X works, walk through a flow, find where something lives or should live | `codebase-learner` (explain mode) |
| Know why X is this way, the tradeoff, the history, whether a guard is still needed | `trace` (rationale mode) |
| Find the root cause of a bug, an incident, a flaky test or a slow pipeline; a postmortem; five whys | `trace` (root-cause mode). If the failure is live and its mechanism unknown, `verify` (investigate first) runs inside it |
| Understand a whole repo, onboard, write ARCHITECTURE.md or CLAUDE.md of what exists | `codebase-learner` (onboard or summarize mode) |
| Grill a plan, doc, idea or design; poke holes; brainstorm before code | `challenge-me` |
| Get a detailed spec for a backend or API change before an agent builds it | `execution-ready-spec-plan` |
| Get a step-by-step coding plan from a spec | `write-plan` |
| Build a feature or fix a bug | `tdd` |
| Refactor without changing behavior | `safe-refactor` |
| Tear apart a diff or branch, find blind spots before merge | `second-opinion` |
| Review an MR, or act on review comments | `glab-code-review` |
| Commit, split commits, open or describe an MR or PR | `atomic-semantic-commit`, then `write-mr-description` |
| Prove something is done, run the gates, find why it fails | `verify` |
| Audit or polish an existing product's code, UI, journeys or branding | `product-polish-workflow` |
| Write or rewrite text for people | `polyglot-copywriter` |
| Build a skill, agent, rule, hook, command or AGENTS.md | the matching `create-*` skill |
| Stuck, overwhelmed, or a tangent showed up | `get-moving` or `later-list` |
| Stop or resume a session; write a standup | `handoff`; `standup` |
| A domain is named: architecture, caching, Node, protobuf, Elixir, slop, design system, stack choice | that `super-*` domain router |
| Anything else, or two rows fit equally | step 4: [find-skills](../../find-skills/SKILL.md) |

## Named one-shots

The user named a skill: invoke it and skip step 4. Steps 5, 6 and 7 still run. Read-only skills (`codebase-learner`, `trace`, `second-opinion`, `challenge-me`) skip step 6 unless they made a claim that needs a command to prove it.

**Not invoke picks:** `output-savers` and `polyglot-copywriter` are gates in steps 2 and 7, not routes, unless the user's whole job is writing or shrinking text.

## Agents

Spawn one only for a bounded job, and keep routing in this session.

| Spawn | When |
|---|---|
| `context-harvester` | The task needs facts gathered from several places first |
| `explorer` | `codebase-learner` on a wide subsystem: one angle per agent |
| `reviewer`, `security-reviewer` | `second-opinion` reviewers |
| `planner` | A large plan before `write-plan` |
| `tdd-runner`, `implementer` | A planned task with clear acceptance |
| `bulk-reader` | A huge file or log; judgment stays here |

## Chaining

Allowed when one output feeds the next:

- `codebase-learner` or `trace` → `execution-ready-spec-plan` → `write-plan` → `tdd`
- `challenge-me` → `write-plan`
- `codebase-learner` → `super-architecture` or `super-tech-blueprint`
- `tdd` or `safe-refactor` → `second-opinion` → `atomic-semantic-commit` → `write-mr-description`

Do not run `second-opinion` and `challenge-me` on the same artifact unless the user asked for both.
