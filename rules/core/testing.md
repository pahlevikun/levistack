---
description: "TDD and test conventions: tests are the spec, red-green-refactor, table-driven cases, mock only boundaries."
globs: "**/*test*,**/*spec*,**/tests/**"
alwaysApply: false
---

# Testing discipline

Tests are the primary spec. Write or lead with the failing test, make it pass with the smallest change, then refactor with tests green.

## Rules
- **Never weaken a test to get green.** No deleted or loosened assertions, no added skips, no fixtures bent to fit broken code. If a test looks wrong, show the evidence to the user.
- **Table-driven by default** for pure logic and validators: one row per case, named, with the expected result or error code.
- **Assert on error codes or types**, not message substrings.
- **Run the narrowest scope first** (a file or a single test), then the package, then the full suite in proportion to risk.
- **A race or flaky failure is real.** Fix the shared state or synchronization. Do not rerun and hope.
- **Do not mock the database or ORM.** Use a real database (a sandbox, a transaction per test, a container) and test real behavior.
- **Mock at the boundary**, not inside your own code: HTTP clients, queues, clocks. Prefer real collaborators for pure logic. Generated mocks are regenerated, never hand-edited.
- **Patch the layer you own.** Patch the HTTP wrapper you call, not the transport underneath it.
- **No PII or secrets** in test logs or committed fixtures.

## Per function, at minimum
Happy path; invalid input returning the documented error; edge values (blank, boundary); not-found where persistence is involved; and the specific error `type` or code each new error value introduces.

## Cases most suites forget
- Empty, null and zero-length input; very large input.
- The error path of every upstream call, including non-2xx and timeouts.
- Registration and wiring (a nil router, a missing dependency).
- A default or "unknown value" branch of every switch.
- Rows or fields that are absent from an upstream response.

## Coverage
Do not chase a number. Cover behavior and error paths; skip generated code and trivial accessors. Never commit coverage artifacts.

## Anti-patterns (reject in review)
- Tests that assert implementation details or only that a mock was called.
- Shared mutable state between tests; order-dependent tests.
- `sleep` instead of waiting on a condition.
- A test that passes with the feature removed.
- One giant test covering many behaviors.
