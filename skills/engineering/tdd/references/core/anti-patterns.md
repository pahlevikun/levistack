# TDD anti-patterns

Load with `legacy/catalog-anti-patterns.md` when mocks or test-only APIs appear. Links from [SKILL.md](../../SKILL.md).

## Horizontal slices

Do not treat RED as "write all tests" and GREEN as "write all code".

Bulk tests describe imagined shape (signatures, structs), not learned behavior. They pass when behavior breaks and fail when internals move.

Correct: vertical tracer bullets — one test, one implementation, repeat. Each cycle uses what the last one taught.

```
WRONG:  RED(test1..testN) then GREEN(impl1..implN)
RIGHT:  RED→GREEN per behavior
```

## Testing implementation

- Private methods, unexported helpers, SQL strings, mock `toHaveBeenCalledWith` on internals
- Tests that must change when you extract a function but users see the same result

Fix: move the assertion to the public seam (`core/seams.md`).

## Tests after, or tests that pass immediately

Passing on first run proves the test is insensitive or the behavior already exists. Watch fail first (`core/red-green-refactor.md`).

## Over-mocking

Mock setup longer than the act/assert, asserting on `*-mock` test ids, or mocking a method whose side effects the test needs.

Prefer real code, then fakes, then stubs. Interaction mocks last.

## Test-only methods on production types

Cleanup or inspectors that exist only for tests belong in test utilities, not the production type.

## Forced tests

A test that needs a huge harness, brittle mocks, production-only state, or unrelated fixture churn is worse than no new test. Skip with an explicit why and a closer check (`core/bug-fix-prove-it.md`).
