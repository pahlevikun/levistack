# Verification during TDD

Peer skill `super-verify` owns completion claims. This file is the TDD-specific evidence. Load targets from [SKILL.md](../../SKILL.md).

## Per slice

- [ ] Watched this test fail for the intended reason (or documented skip + substitute check)
- [ ] Minimal production change; no extra behavior
- [ ] Same focused command now passes
- [ ] Assertion is on a public seam, not a mock graph

## Before "done"

- [ ] Ran the project's real test/lint/type gate (not a remembered earlier run)
- [ ] Reported every failure by name, including ones you did not cause
- [ ] Refactor (if any) stayed green and added no features
- [ ] Output is actually clean enough to ship, or residual warnings are listed

"Should pass" and "looks correct" are not evidence.

## Bug-fix extra

Revert-thought-experiment: the new test would fail if the fix were removed. If you cannot show RED-before, say so (`core/bug-fix-prove-it.md`).

## Stuck

| Problem | Move |
|---------|------|
| Do not know how to test | Write the wished-for public API and the assertion first; ask the user |
| Test is a novel | Interface is too wide; shrink the seam |
| Must mock everything | Coupling; inject the boundary, or test one level out |
| Huge setup | Helpers, then simplify the design |
