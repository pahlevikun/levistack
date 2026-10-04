# Duplication levels

Optional tooling (`indexion plan refactor` or similar) can help; the levels apply without it.

| Level | What | Detection | Fix |
|-------|------|-----------|-----|
| Textual | Copy-paste blocks, identical functions | diff, jscpd, `plan refactor` | Extract shared function/module |
| Structural | Same shape, different names | similarity tools, solid/unwrap plans | Unify API, remove wrappers |
| Conceptual | Same domain rule in many places | explore + domain review | Single source of truth type or service |

## Workflow

1. Fix high-confidence textual dupes first (often same-file).
2. Trace references before consolidating.
3. Re-run detection after each extraction.
4. Lower similarity threshold only after wins at higher threshold.

## When to run

- After new abstraction or I/O boundary
- When one fix touched 3+ files for the same reason
- After refactor cleanup (remove trivial wrappers)
