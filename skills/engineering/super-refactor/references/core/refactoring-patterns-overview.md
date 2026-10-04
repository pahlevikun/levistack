# Refactoring patterns overview

Use with `legacy/legacy-design-patterns.md` and `legacy/legacy-steps-checklist-operations.md` (operations table; see [SKILL.md](../../SKILL.md)).

## Composing methods

Master **Extract Method** first. Comment urge → extract and name. **Inline** when the name adds no clarity.

| Situation | Pattern |
|-----------|---------|
| Block with comment | Extract Method |
| Temp used once | Inline Variable |
| Tangled locals | Replace Method with Method Object |

## Moving features

| Smell | Pattern |
|-------|---------|
| Feature Envy | Move Method / Move Field |
| God class | Extract Class |
| Train wreck `a.b().c()` | Hide Delegate (sparingly) |
| Pure forwarding class | Remove Middle Man |

## Smell families (high level)

- **Bloaters**: Long Method, Large Class, Long Parameter List
- **Change preventers**: Divergent Change, Shotgun Surgery
- **Dispensables**: Dead Code, Duplicate Code
- **Couplers**: Feature Envy, Inappropriate Intimacy

Detailed before/after examples: `legacy/legacy-code-smells.md`.
