# Bug-fix prove-it

Use in **bug-fix** mode. Do not start by patching production code.

## When a test is cheap

Make the broken behavior executable first.

1. **Understand.** Intended vs current behavior, path, smallest observable reproduction.
2. **Narrowest check.** Prefer an existing unit, component, or integration target for that path.
3. **Failing test first.** Encode intended behavior, not the current (wrong) implementation.
4. **Watch RED.** Confirm it fails for the bug, not setup. If it passes, the test does not reproduce; fix the test.
5. **Smallest fix.** Preserve nearby contracts.
6. **Watch GREEN** on that test.
7. **Nearby validation.** Adjacent tests, types, lint, or a scenario when the change has blast radius.

The regression should have caught the bug. Keep it focused. Do not expand coverage as a side quest.

## When a failing test is impractical

Do not force a test. Impractical means: broad harness, brittle mocks, slow E2E for a tiny fix, production-only state, vague repro, or large unrelated fixture churn.

**Do not skip silently.** Before fixing, say why a new failing test is not worth it, then use the closest executable check: focused script, manual repro command, browser automation, snapshot, log assertion, or existing integration test.

Prefer no new test over a bad one (mocks-as-subject, timing, global state, disposable after the fix).

## Guardrails

- Do not change tests to match a wrong implementation.
- Do not weaken assertions unless the expected behavior actually changed.
- Flaky bug: make the check deterministic if you can; say what signal you locked.
- Broader class of failures: land the focused regression first, then consider siblings.

## Report

- Failing-before evidence (command + why it failed).
- Passing-after evidence and nearby validation.
- If RED could not be shown: the why, and the substitute check.
