# React component refactor mode

## Triggers

- User asks to split a component, reduce React complexity, or extract hooks
- Analyzer signals (when present): complexity **> 50** or line count **> 300**
- Many useEffects, mixed data + presentation, prop drilling across unrelated concerns

## Approach

1. Identify **behavior owner** and public props contract.
2. Extract presentational subcomponents without changing rendered output.
3. Extract hooks for state, data fetching, and effects — one concern per hook.
4. Keep types with the owner; avoid circular imports.
5. Verify: lint, typecheck, and component tests or story if the repo has them.

## Boundaries

- Not for styling-only polish → use **ui-refactor** when the issue is visual hierarchy, not structure.
- Not for wholesale design system creation.

For Dify-specific UI packages, follow that repo's component guides when working inside Dify; this file is generic React/TSX.
