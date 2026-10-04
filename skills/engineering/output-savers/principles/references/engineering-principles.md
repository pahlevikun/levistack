# Engineering principles

These principles push the work toward the **smallest correct change**. They shape what you edit. The STE style shapes what you say. [Context hygiene](../../references/context-hygiene.md) shapes what you read.

If the project has its own engineering rules, follow them first. Where two rules differ, the stricter one wins.

## Core rules

| Principle | In practice |
|-----------|-------------|
| **KISS** | Use one obvious path. Do not add a parallel abstraction for the same job. |
| **YAGNI** | Do not add types, files, flags, or hooks that the task does not need. |
| **DRY (bounded)** | Extract only after the third real duplicate. Do not extract early. |
| **Deletion test** | If removing code spreads the complexity, keep it. If removing it makes things simpler, the extra layer was slop. |
| **Code speaks** | Write a comment only for a non-obvious invariant, a trust boundary, or an external contract. Do not narrate what the line already says. |
| **Occam** | Extend an existing command or flag before you add a new one. |

## Comment slop (reject)

- A header comment that repeats the function name.
- "Initialize variable" or "Return result" on an obvious line.
- Commented-out dead code left "for later".
- A TODO with no owner and no issue link, when the task is to ship now.

Prefer a better name, a well-named helper, or deleting the comment.

## Guides

Load the guide that matches the decision. [../../references/auto-detect.md](../../references/auto-detect.md) picks for you.

| Decision | Guide |
|----------|-------|
| Writing or changing code, choosing a dependency | This card (core rules above); [yagni.md](yagni.md) for dependencies |
| "Just in case", future-proofing, optional parameters | [yagni.md](yagni.md) |
| Duplication, extracting a helper, jscpd clones | [dry.md](dry.md): rule of three, iron laws, refactoring workflow |
| A new module, interface, or abstraction | [solid.md](solid.md) |
| Handlers, services, config, API text, comments | [super-noslop/index.md](super-noslop/index.md): rules R-01 to R-38, delivery gate, comment hygiene |
| Is this over-engineered? Repo bloat? | [review-over-engineering.md](review-over-engineering.md) |

## Principles and STE together

| Risk | Use |
|------|-----|
| Extra files, layers, and abstractions | These principles |
| Long, padded replies | The STE style ([../../concise/SKILL.md](../../concise/SKILL.md)) |
| Huge inputs and long histories | [Context hygiene](../../references/context-hygiene.md) |

Use them together. They fix different problems: too much code, too many words, and too much reading.

## What never bends

"Do less" never excuses weak validation, missing authorization, unsafe queries, non-idempotent financial writes, secrets in logs, skipped tests, or an undocumented contract change. Cut the extra layer. Keep the safety.
