# Safe execute protocol

Use in **safe-execute** mode.

## Boundary

Define what must not change:

- Public API signatures and documented behavior
- Error types, status codes, and failure ordering when observable
- External wire formats and persisted data (unless migration is explicitly scoped)
- Performance characteristics only when user named a budget

Keep feature work **out** of the refactor branch or commit.

## Before the first edit

1. Identify proof: tests, compile, lint, or scripted scenario the repo already uses.
2. Run proof; record baseline (pass/fail counts if tests).
3. Commit or stash unrelated WIP; work on a focused branch when the repo uses branches.

## During edits

- Move **one ownership boundary** at a time (function, type, module, package).
- Keep intermediate states buildable when possible.
- Do not add dependencies or config unless required for correctness.
- After each boundary: run proof again; stop on failure and fix or revert the last step.

## After

- Run the same proof as baseline; compare pass/fail explicitly (zero failures unless baseline already failed).
- Summarize structural change and what was verified.

See `legacy/legacy-steps-checklist-operations.md` for the classic five-phase checklist from the catalog `refactor` skill (linked from [SKILL.md](../../SKILL.md)).
