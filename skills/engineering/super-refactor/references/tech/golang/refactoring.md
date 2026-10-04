# Go refactoring mode

For naming, layout, modernize, and style details, follow this repository's Go rules and skills; this file is the levistack gate.

## Modes (map to super-refactor)

| super-refactor | Go skill mode |
|----------------|---------------|
| plan | Plan — map blast radius, inventory, user sign-off before edits |
| safe-execute | Execute — one atomic change, green tests, small PR mindset |
| review-and-align | Review — structure/behavior separation, preservation |

## Iron rules

- Never change structure and behavior in the same step.
- Keep tests green; read failure counts explicitly.
- Prefer gopls rename/extract and `gofmt -r` over hand edits when available.
- Stack small changes; parallel only when files are disjoint.

## Simple sweep

Single mechanical transform tree-wide (e.g. one modernize fixer) may run as one step with full test pass after.

## Prerequisites

`go`, tests, and ideally `gopls`. Do not invent a second Go refactor workflow here.
