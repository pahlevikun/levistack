# Research synthesis (lightweight)

Captured during the `refactor` → `super-refactor` merge. Not a verbatim import.

## Shared themes across sources

1. **Behavior preservation is the default contract.** Feature work and refactors do not mix in one change set unless the user explicitly scopes both.
2. **Verification before and after structural edits.** Baseline tests or an agreed proof (compile, lint, manual scenario) bracket each boundary move.
3. **Plan before multi-file work.** Inventory and confirm scope before editing; user confirmation is a gate.
4. **One atomic step at a time.** One ownership boundary per step; separate structure from behavior; extract helpers then simplify orchestrators.
5. **Review pass optional but distinct.** Check standards and preservation without silently expanding scope.
6. **Complexity has measurable targets.** Use explicit thresholds where the repo defines them.
7. **Duplication is leveled.** Textual → structural → conceptual; map smells to catalog refactors.
8. **Domain-specific tracks.** Module refactor (interfaces, state), language tooling (small PRs), UI (hierarchy and scale, not logic refactors).

## Gaps levistack fills

- **Single router** for mode detection across languages (prior `refactor` was one long generic doc).
- **output-savers** as mandatory simplicity lens (minimal scope, YAGNI, noslop) on every execute path.
- **Elixir**: delegate idiomatic OTP/Ecto refactors to `super-elixir` (antipatterns / thinking), not duplicate BEAM guides here.
- **Retained catalog content**: code smell diffs, extract-method walkthrough, design-pattern refactor examples, operations table — under `references/legacy/`.

## Out of scope for this skill

- Greenfield architecture or feature implementation.
- Full repo rebuild (use dedicated rebuild / migration skills if present).
- UI visual polish when the user did not ask for UI (ui-refactor mode is opt-in via signals).

## Recommended default flow

```
detect job → (optional) plan → safe-execute in small steps → verify → (optional) review-and-align
```

Load `core/auto-detect.md` for signals; load `core/output-savers-integration.md` before editing code (linked from [SKILL.md](../../SKILL.md)).
