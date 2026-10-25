# Testing anti-patterns (catalog)

**Load when:** writing or changing tests, adding mocks, or tempted to add test-only methods to production code. Retained from the prior `test-driven-development` skill. Router: [SKILL.md](../../SKILL.md).

Tests must verify real behavior, not mock behavior. Mocks isolate; they are not the subject.

## Iron laws

1. Never test mock behavior.
2. Never add test-only methods to production classes.
3. Never mock without understanding dependencies.

## 1. Testing mock behavior

```typescript
// Bad: asserting the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

The test passes when the mock is wired and says nothing about the page.

```typescript
// Good: real UI contract
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});
```

If you must mock a child for isolation, do not assert on the mock. Assert on the parent’s behavior.

**Gate:** before asserting on a mock element, ask whether you are testing real behavior. If not, delete the assertion or unmock.

## 2. Test-only methods in production

```typescript
// Bad: destroy() exists only for tests
class Session {
  async destroy() {
    await this._workspaceManager?.destroyWorkspace(this.id);
  }
}
```

Production types stay free of test lifecycle. Put cleanup in test utilities.

**Gate:** if a method is only called from tests, do not add it to the production type. If the type does not own the resource lifecycle, the method is on the wrong type.

## 3. Mocking without understanding

Mocking a high-level method can remove a side effect the test depends on (config write, cache fill). The duplicate-detection test then never fires.

**Gate:** list the real method’s side effects. If the test needs one of them, mock a lower layer (the slow I/O) or use a fake that still performs the needed write. If unsure, run once with the real implementation, then mock the actual bottleneck.

Red flags: "mock to be safe", "it might be slow".

## 4. Incomplete mocks

Partial response objects hide fields downstream code reads. Mirror the real schema, not the fields this one test mentions.

**Gate:** check docs or a recorded payload; include fields the system might consume.

## 5. Integration tests as afterthought

Claiming "ready for testing" after implementation is skipping TDD. RED then GREEN then refactor, then complete.

## When mocks are too complex

Setup longer than the act, missing methods the real type has, tests that fail when you remove a mock you cannot explain. Prefer a narrower integration test with real components.

If TDD shows you are testing mock behavior, you added mocks without watching fail against real code first.
