# Red-green-refactor loop

Use in **loop** mode. Discover this repo's test command first; do not assume `npm test`.

## Discover the stack

Before the first test, find how *this* repository tests:

- Manifests: `package.json`, `go.mod`, `mix.exs`, `pyproject.toml`, `Cargo.toml`, Gradle/Maven wrappers
- Focused vs full-suite commands in README, CONTRIBUTING, or CI
- Neighboring test file names and seams

Run the focused command during the loop. Run the project's full gate before claiming done (peer `super-verify`).

## Vertical slice (required)

One behavior per cycle:

```
RED → watch fail → GREEN (minimal) → watch pass → REFACTOR (stay green) → next behavior
```

Do **not** write all tests then all code. That is a horizontal slice (`core/anti-patterns.md`, linked from [SKILL.md](../../SKILL.md)).

## RED

Write one test that states desired behavior through a public seam (`core/seams.md`).

Requirements:

- One behavior. "And" in the name → split.
- Name reads like a spec ("rejects empty email"), not "test1".
- Real code at the seam. Mocks only when the collaborator is slow, non-deterministic, or side-effecting in a way you cannot control.

## Watch RED (mandatory)

Run the focused test. Confirm:

- It **fails**, not errors (or compile-time RED is the intended missing symbol)
- The message matches the missing behavior, not a typo or broken import
- You can say in one sentence why it failed

If it **passes**, you tested existing behavior. Change the test until it would catch the missing change.

If it **errors**, fix the test harness, re-run, until the failure is the intended one. Do not start production code until RED is real.

Exploration spikes are allowed. Throw the spike away. Implement from the tests.

## GREEN

Write the smallest production change that makes this test pass. No extra parameters, no extra features, no drive-by refactors.

If you already wrote production code: delete it. Do not keep it as "reference" and adapt it — that is tests-after.

## Watch GREEN (mandatory)

Re-run the same focused target. Confirm this test passes. Then run nearby tests that share the seam.

If the new test fails, fix production code, not the assertion (unless the spec was wrong and the user agreed).

If other tests fail, fix or report them by name. A green file is not a green suite.

## REFACTOR

Only after green. Remove duplication, improve names, extract helpers. **Do not add behavior.**

Load peer `super-refactor` for multi-file or smell-driven cleanup. Stay green after each step. Pair with `core/output-savers-integration.md`.

## Repeat

Next failing test for the next agreed behavior. Stop when the planned behaviors at the seam are covered, not when every imaginable edge exists.
