# Job detection

Do this first. Do not announce it.

One-hop links for every mode live in [SKILL.md](../../SKILL.md). This file is the expanded signal list; load targets are paths under `references/core/`, `references/legacy/`, and `references/tech/`.

## Precedence

1. Safety: missing tests on critical paths → stop and propose test harness first.
2. User explicit mode ("plan only", "reduce complexity", "Terraform module", "UI looks off").
3. Signals below.

## Mode signals

| Signals | Mode | Load |
|---------|------|------|
| "plan", "sequence", "multi-file", "before you change", scope across packages | plan | `core/refactor-plan-protocol.md` |
| "refactor", "extract", "rename", "clean up", "safe", executing edits | safe-execute | `core/safe-refactor-protocol.md`, `legacy/legacy-steps-checklist-operations.md` |
| "review and refactor", "align with standards", `.github/instructions` | review-and-align | `core/review-and-align-protocol.md` |
| named method + "complexity", "cognitive complexity", "too nested" | reduce-complexity | `core/reduce-complexity-protocol.md` |
| "smell", "duplication", "DRY", "pattern", Fowler | patterns/smells | `core/refactoring-patterns-overview.md`, `legacy/legacy-code-smells.md` |
| `.go`, `gopls`, "Go refactor", import cycle | language: Go | `tech/golang/refactoring.md` |
| `.ex`, `.exs`, GenServer, "Elixir refactor" | language: Elixir | `tech/elixir.md` → `super-elixir` |
| `.tf`, "Terraform module", "extract module" | language: Terraform | `tech/terraform/module-refactor.md` |
| `.tsx`, "split component", analyze-component, line count | language: React | `tech/react/component-refactor.md` |
| "UI looks off", Tailwind, hierarchy, spacing, grayscale | ui-refactor | `tech/web-ui/refactoring.md` |
| Kotlin, Swift, Android, iOS, Gradle module | language: mobile | `tech/android.md` |
| indexion, "three levels duplication", SoT | duplication-levels | `core/duplication-levels.md` |

## Combined flows

| User intent | Order |
|-------------|-------|
| Large refactor | plan → user confirms → safe-execute (repeat verify each step) |
| "Review and clean up" | review-and-align → safe-execute only for approved items |
| Complexity on one method | reduce-complexity (may skip full plan if single file) |
| Go package split | plan → `tech/golang/refactoring.md` execute conventions |

Always load `core/output-savers-integration.md` before code edits in execute modes.
