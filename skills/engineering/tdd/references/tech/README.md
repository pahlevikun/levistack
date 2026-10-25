# Stack-specific TDD tracks

Load **one** track plus the core loop from [SKILL.md](../../SKILL.md). Always pair green/refactor with `references/core/output-savers-integration.md`.

| Stack | Use when | Reference |
|-------|----------|-----------|
| Go | `.go` files, `go test`, table-driven tests, package API | `tech/golang.md` |
| Elixir / ExUnit | `.ex`/`.exs`, `mix test`, Phoenix | `tech/elixir.md` → `super-elixir` tdd |
| JS / TS / React | Jest, Vitest, React Testing Library, `*.test.ts(x)` | `tech/javascript.md` |
| Python | pytest, `test_*.py`, `pyproject.toml` | `tech/python.md` |
| Android / mobile | Kotlin, Swift, Espresso, XCTest | `tech/android.md` |

Language-agnostic modes (loop, plan, bug-fix, seams) live under `references/core/`. Legacy catalog mock gates are under `references/legacy/`.
