# JS/TS/React TDD track

Apply the core loop from [SKILL.md](../../SKILL.md). Discover Jest vs Vitest vs `node:test` vs `bun:test` from `package.json` — they are not interchangeable.

**Use when:** `.ts`/`.tsx`/`.js`, Jest, Vitest, React Testing Library, or "write a failing test" in a JS app.

## Runner

Prefer the repo script (`npm test`, `pnpm test`, `npx vitest run path`). `bun test` is not `bun run test`.

Focused file during the loop; full `test` script before done.

## Seams

- Pure modules: exported functions.
- HTTP: the handler or request helper the app already uses.
- React: user-facing behavior via Testing Library roles, labels, and text — not `data-testid` on mocks, not internal hook state.

## Mocks

Mock network and time at the boundary. Do not assert that a mocked child rendered. Prefer wrapping the real component.

## Green / refactor

YAGNI in the implementation. After green, peer `super-refactor` React track for splits; stay on the public component contract.
