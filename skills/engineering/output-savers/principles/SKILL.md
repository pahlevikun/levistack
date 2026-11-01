---
name: principles
description: "Engineering principles card: the smallest change that works. Do less, delete first, build only what the task needs, plus named working principles to steer by (attack the premise, sequence verifiable units, boundary discipline, model the domain, never block on the human, and more). Use when writing or reviewing code for over-engineering, or when the user names a principle such as 'apply laziness protocol' or 'subtract before you add'. Full guides are in references."
---

Prefer the smallest change that satisfies the request. Do not add abstractions, dependencies, or files that the task does not need.

Smallest diff only. No drive-by refactors. Write a comment only when the code cannot carry the intent. Run the deletion test before you add a layer.

## Guides

| Decision | Read |
|----------|------|
| Writing or changing code, choosing a dependency | [references/engineering-principles.md](references/engineering-principles.md) |
| "Just in case", future-proofing, optional parameters | [references/yagni.md](references/yagni.md) |
| Duplication, extracting a helper | [references/dry.md](references/dry.md) |
| A new module, interface, or abstraction | [references/solid.md](references/solid.md) |
| Handlers, services, config, API text, comments | [references/noslop/index.md](references/noslop/index.md) |
| Is this over-engineered? Repo bloat? | [references/review-over-engineering.md](references/review-over-engineering.md) |
| Overview and the deletion test | [references/engineering-principles.md](references/engineering-principles.md) |
| Pick the mode for the job | [../references/auto-detect.md](../references/auto-detect.md) |

Use the [style card](../concise/SKILL.md) when the problem is long replies and not extra code.

## Named principles

The user may steer with a name ("apply attack the premise"). Apply the line, and cite the name when it changed a decision.

| Name | Rule |
|---|---|
| Laziness protocol | Do the least work that fully meets the goal. One pass of rigor is enough when the shape is settled; a second review of a settled design is waste |
| Subtract before you add | Remove the dead path, flag, or layer before adding a new one. The new design starts smaller than the old |
| Attack the premise | Check the request's assumption before solving it. A wrong premise gets named with evidence, then the user decides |
| Sequence verifiable units | Build, prove, and land one small unit before starting the next. Batched checks at the end hide which unit broke |
| Boundary discipline | Validate and convert at the edges: input, I/O, network, storage. Inside the boundary, trust the types |
| Foundational thinking | Scaffold and the check come before features. Land the skeleton and the harness first |
| Model the domain | Pick the data shape before the logic: a state machine over scattered booleans, a table over branching, a typed model over repeated shape guesses |
| Minimize reader load | Write so the next reader opens the fewest files. Names say what, the structure says how, a comment only says why |
| Migrate callers, then delete | Move every caller to the new API, then delete the old one in the same change. No shim left behind without a named removal date |
| Outcome-oriented execution | Judge a step by whether it moves the outcome. Planned, scoped breakage during a rewrite is fine when the end state is checked |
| Redesign from first principles | When fixes keep piling onto one design, redesign as if today's constraints were known on day one |
| Exhaust the design space | Sketch at least two whole-shape alternatives before picking. Throwaway builds go to `prototype-wireframe` |
| Experience first | Start from what the user sees and does, then derive the code that serves it |
| Make operations idempotent | A retry, rerun, or resume must be safe. Prefer upserts, keyed writes, and checks before side effects |
| Separate before serializing shared state | Split shared state so workers own disjoint parts. Lock or serialize only for a real invariant |
| Never block on the human | Keep moving on reversible work and record the assumption. Outward and destructive actions still stop for a yes |
| Guard the context window | Read only what the step needs. Delegate wide reads, summarize big outputs, and keep the main thread for judgment |

Enforced elsewhere: prove it works and explain the number (`verify`), fix root causes (`trace`), test behavior, not implementation (`tdd`).

## Related skills

- `output-savers`: the parent skill; use it to apply these rules to a job.
- `noslop`: filter generated code for slop.
- `safe-refactor`: apply the rules as a behavior-preserving refactor.
- `code-review`: review a diff for over-engineering.
