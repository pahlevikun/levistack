# Stack-specific refactor tracks

Load **one** track plus the core protocols from [SKILL.md](../../SKILL.md). Always pair execute modes with `references/core/output-savers-integration.md` and the safe-refactor boundary rules.

| Stack | Use when | Reference |
|-------|----------|-----------|
| Go | `.go` files, gopls, import cycles, package splits | `tech/golang/refactoring.md` |
| Elixir / OTP | `.ex`/`.exs`, GenServer, Ecto idioms | `tech/elixir.md` → `super-elixir` |
| Terraform | `.tf`, module extraction, state migration | `tech/terraform/module-refactor.md` |
| React | `.tsx`, huge components, split hooks | `tech/react/component-refactor.md` |
| Web UI | Tailwind, hierarchy, spacing (not logic) | `tech/web-ui/refactoring.md` |
| Android / mobile | Kotlin, Swift, Android/iOS layout or platform APIs | `tech/android.md` |

Language-agnostic modes (plan, safe-execute, smells, duplication) live under `references/core/`. Legacy catalog depth is under `references/legacy/`.
