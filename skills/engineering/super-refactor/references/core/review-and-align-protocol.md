# Review and align protocol

## Role

Senior maintainer pass: find structural and clarity issues, propose refactors that preserve behavior, align with **this repository's** rules (AGENTS.md, `rules/`, linters, and any `.github/instructions` or copilot instructions if present).

## Task

1. Read applicable project instructions and rules before judging style.
2. Review the scoped code carefully. Prefer small, local refactors over file splits unless the user asked to split.
3. **Do not split files** unless the user requested or the plan mode already approved splits.
4. If tests exist, run them after changes; do not assume green without reading output.

## Output

- List findings with path:line when possible.
- Separate **must-fix** (correctness, contract break risk) from **should-fix** (clarity, smell).
- Apply output-savers review one-liner style for each finding when writing review text.

Execute fixes only when the user asked for implementation, not review-only.
