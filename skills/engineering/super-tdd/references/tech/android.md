# Android / mobile TDD track (placeholder)

Full mobile playbooks are not duplicated here yet. Apply platform conventions plus the core loop in [SKILL.md](../../SKILL.md).

**Use when:** Kotlin, Swift, Android/iOS tests, Espresso, XCTest, or mobile "failing test first".

## Boundaries

1. **Public seam** — ViewModel/use-case API, or UI via the project's testing library; not private Activity methods as the spec.
2. **Runner** — Gradle `test` / `connectedAndroidTest`, or Xcode/`xcodebuild` as the repo documents. Do not invent a second mobile TDD workflow.
3. **Impractical instrumented tests** — if the only repro is a slow device farm for a tiny logic bug, say why and use a local unit/ViewModel test (`core/bug-fix-prove-it.md`).

When `super-tdd` gains dedicated Kotlin/Swift references, this file will link them.
