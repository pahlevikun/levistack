# Principles and user-facing copy

Noslop is the **backend and message filter**. The engineering principles (`engineering-principles` rule) shape the **smallest correct change**. Pair them; do not duplicate them.

| Artifact | Role |
|----------|------|
| `engineering-principles` rule | KISS, YAGNI, DRY, SOLID, deletion test, minimal scope |
| Root `AGENTS.md` | The project's own standards for language, tone and output format |

## User-facing copy (R-02)

- CLI strings, API error messages and shipped skill examples use one language, the project's, and tests assert on it.
- No em dash in user-facing API or CLI text.
- Generic errors carry a stable code or field wherever the repo uses coded errors.

Carve-out: this skill's own docs and examples may show forbidden patterns as **Tell** rows in [slop-patterns.md](slop-patterns.md).
