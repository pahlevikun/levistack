# Reduce complexity protocol

## Objective

Lower cognitive complexity of a named method or function to at or below a threshold (user-provided or default **15** when unspecified).

## Analyze

Sources of complexity:

- Nested conditionals and loops
- Long if/else or switch chains
- Repeated blocks
- Complex boolean expressions

## Extract

- Validation → `validate*` / guard helpers
- Case-specific logic → handlers
- Shared calculations → pure helpers
- Prefer static/private helpers when no instance state needed
- Keep helpers near the caller

## Simplify main flow

- Guard clauses early
- Orchestration reads top-down
- Preserve inputs, outputs, errors, and side-effect order

## Verify (mandatory)

1. Run tests covering the method and callers.
2. Read output; confirm **failed=0** (or document baseline failures unchanged).
3. Compile / typecheck.
4. Re-check complexity if tooling exists; otherwise justify by structure.

If tests fail, fix behavior before claiming done.
