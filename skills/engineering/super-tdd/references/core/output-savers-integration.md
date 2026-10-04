# output-savers during TDD

Every **green** and **refactor** step applies peer [output-savers](../../output-savers/SKILL.md). Do not paste the noslop corpus here.

## Call pattern

- **GREEN:** minimal scope and YAGNI — only what this test requires.
- **REFACTOR:** DRY after the third duplication; still no new behavior. For structural moves, load `super-refactor`.

## TDD-specific rules

1. Minimal pass, not a framework. Extra options and callbacks wait for a failing test that needs them.
2. Delete the spike. Do not ship exploration.
3. Tests may repeat setup when repetition makes the spec readable (DAMP). Do not "DRY" tests into opacity.
4. No narrating comments in production or tests; names carry the spec.

If output-savers and a failing test conflict, **the test wins**: write the smallest code that makes RED turn GREEN, then slim the diff.
