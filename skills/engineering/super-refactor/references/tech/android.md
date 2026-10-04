# Android / mobile refactor track (placeholder)

Full mobile playbooks are not duplicated here yet. Apply platform conventions plus the core safe-refactor protocol.

**Use when:** Kotlin, Swift, Android/iOS UI, Gradle modules, or mobile-specific "clean up" / extract / rename requests.

## Boundaries

1. **Behavior preserved** — same as `references/core/safe-refactor-protocol.md`; run platform tests (instrumented/unit) before and after each step.
2. **One atomic change** — resource rename, extract composable/fragment, or module move — not mixed with feature work.
3. **Platform tools first** — Android Studio refactor, Kotlin IDE rename, Swift "Refactor" menu before hand edits.

## Typical signals

| Signal | Direction |
|--------|-----------|
| God Activity/Fragment | Extract ViewModel + UI state; split layouts |
| Duplicate UI in XML/Compose | Extract component; shared theme tokens |
| Gradle module tangle | plan mode — map dependencies before `include` moves |

When `super-refactor` gains dedicated Kotlin/Swift references, this file will link them; until then, follow official style guides and keep diffs minimal via output-savers.
