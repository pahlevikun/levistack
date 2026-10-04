# Domain: tests

Test files, fixtures, mocks, and assertion style in the diff.

## Checklist

- [ ] Tests prove behavior change — not weakened asserts or skips to green broken code (pair with MR `tests` dimension).
- [ ] Fixtures obviously synthetic or labeled — not realistic production-shaped rows presented as real (R-18).
- [ ] Mocks match repo style; no in-memory stand-in smuggled onto prod wiring (R-22).
- [ ] Table-driven or focused cases cover new error branches — not only happy path.
- [ ] Comment noise in tests follows [super-noslop-code](../../skills/super-noslop-code/SKILL.md) if cleaning comments.

## Out of scope

Choosing test framework or TDD workflow — use project TDD rules and **super-tdd** when the user asks for red-green-refactor.
