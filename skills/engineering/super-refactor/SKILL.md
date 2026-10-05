---
name: super-refactor
description: "Behavior-preserving refactoring across languages and stacks: plan multi-file work, execute one safe boundary at a time, review-and-align to project standards, cut method complexity, apply smell/pattern catalogs, and run scoped tracks for Go, Elixir (via super-elixir), Terraform modules, React components, web UI, and mobile placeholders. Always pairs with output-savers for minimal diffs. Use when the user asks to refactor, clean up, extract, rename, reduce complexity, split a component, refactor a Terraform module, plan a safe refactor, or fix UI hierarchy — not for new features or repo rebuilds."
metadata:
  version: "1.0.0"
---

# Super refactor

One router for behavior-preserving structural improvement. Gradual evolution, not rewrite. Feature work stays out of scope unless the user explicitly combines them.

**Simplicity:** Before editing code, apply [output-savers](../output-savers/SKILL.md) via [references/core/output-savers-integration.md](references/core/output-savers-integration.md). Missing tests on the path you will move: load [super-tdd](../super-tdd/SKILL.md) first, then return here.

Research notes: [references/core/research-synthesis.md](references/core/research-synthesis.md). Stack index: [references/tech/README.md](references/tech/README.md).

## Step 0: detect the job

Do this first; do not announce it. Full signal table: [references/core/auto-detect.md](references/core/auto-detect.md).

| If the user is doing this | Mode | Load |
|---|---|---|
| Plan, sequence, or scope multi-file refactor | **plan** | [refactor-plan-protocol.md](references/core/refactor-plan-protocol.md) |
| Execute extract/rename/move/cleanup with tests | **safe-execute** | [safe-refactor-protocol.md](references/core/safe-refactor-protocol.md) |
| Review against repo rules then refactor | **review-and-align** | [review-and-align-protocol.md](references/core/review-and-align-protocol.md) |
| Cut cognitive complexity of one method | **reduce-complexity** | [reduce-complexity-protocol.md](references/core/reduce-complexity-protocol.md) |
| Smells, duplication, Fowler patterns | **patterns/smells** | [refactoring-patterns-overview.md](references/core/refactoring-patterns-overview.md), [legacy-code-smells.md](references/legacy/legacy-code-smells.md) |
| Textual / structural / conceptual dupes | **duplication-levels** | [duplication-levels.md](references/core/duplication-levels.md) |
| Go files, gopls, import cycles | **language: Go** | [refactoring.md](references/tech/golang/refactoring.md) |
| Elixir / OTP / Ecto idioms | **language: Elixir** | [elixir.md](references/tech/elixir.md) → `super-elixir` |
| Terraform module extraction | **language: Terraform** | [module-refactor.md](references/tech/terraform/module-refactor.md) |
| React/TSX split, huge components | **language: React** | [component-refactor.md](references/tech/react/component-refactor.md) |
| Visual hierarchy, spacing, Tailwind | **ui-refactor** | [refactoring.md](references/tech/web-ui/refactoring.md) — only when UI is in scope |
| Kotlin, Swift, Android/iOS mobile | **language: mobile** | [android.md](references/tech/android.md) |

Precedence: missing tests on critical paths → [super-tdd](../super-tdd/SKILL.md) first; then explicit user mode; then detected signals.

## Golden rules (short)

From the prior catalog `refactor` skill ([legacy-principles.md](references/legacy/legacy-principles.md)):

1. Behavior preserved — change how, not what (unless scoped).
2. Small steps; verify after each boundary.
3. One purpose per change set — no mixed features.
4. Tests or agreed proof bracket structural edits.
5. Skip refactor when code is stable, untested-critical, or deadline-blocked without a plan.

## Default pipelines

**Large change:** plan → user confirms → safe-execute (repeat verify) → optional review-and-align.

**Single-file cleanup:** safe-execute; add reduce-complexity when one function dominates.

**Go at scale:** plan (inventory) → execute one atomic change per step per [golang track](references/tech/golang/refactoring.md).

**Elixir:** [elixir track](references/tech/elixir.md) → load `super-elixir`; do not duplicate BEAM guides here.

## Legacy catalog depth

Retained content from `refactor` (examples and checklists):

| Topic | Reference |
|---|---|
| Principles and when not to | [legacy-principles.md](references/legacy/legacy-principles.md) |
| Ten smells with diffs | [legacy-code-smells.md](references/legacy/legacy-code-smells.md) |
| Extract method, typing | [legacy-extract-and-types.md](references/legacy/legacy-extract-and-types.md) |
| Strategy, chain patterns | [legacy-design-patterns.md](references/legacy/legacy-design-patterns.md) |
| Steps, checklist, operations table | [legacy-steps-checklist-operations.md](references/legacy/legacy-steps-checklist-operations.md) |

## Layout

| Path | Holds |
|---|---|
| [references/core/](references/core/auto-detect.md) | Mode routing, protocols, patterns overview, duplication, output-savers bridge, research |
| [references/legacy/](references/legacy/legacy-principles.md) | Prior catalog `refactor` body |
| [references/tech/](references/tech/README.md) | Per-stack tracks (Go, Elixir pointer, Terraform, React, web UI, mobile stub) |

## Old skill name

| Old | Use |
|---|---|
| `refactor` | This skill (`super-refactor`) |

## Related skills

- `super-tdd`: add a test first.
- `super-verify`: prove behavior is the same.
- `output-savers`: keep the diff small.
- `super-codebase-learner`: find the smells.
- `atomic-semantic-commit`: commit each step.

## Done when

- Correct mode(s) ran; only needed references were loaded.
- Behavior preserved per boundary definition; proof run before and after execute modes with failures explicitly checked.
- Diffs stay minimal per output-savers; no scope creep into features.
- Plan mode produced a plan and waited for confirmation before code (unless user waived).
