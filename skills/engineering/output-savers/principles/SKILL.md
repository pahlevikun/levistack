---
name: principles
description: "Engineering principles card: the smallest change that works. Do less, delete first, build only what the task needs. Full guides are in references."
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
| Handlers, services, config, API text, comments | [references/super-noslop/index.md](references/super-noslop/index.md) |
| Is this over-engineered? Repo bloat? | [references/review-over-engineering.md](references/review-over-engineering.md) |
| Overview and the deletion test | [references/engineering-principles.md](references/engineering-principles.md) |
| Pick the mode for the job | [../references/auto-detect.md](../references/auto-detect.md) |

Use the [style card](../concise/SKILL.md) when the problem is long replies and not extra code.
