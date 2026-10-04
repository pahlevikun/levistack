# output-savers during refactor

Every **execute** mode applies the peer skill [output-savers](../../output-savers/SKILL.md). Do not paste the full noslop corpus here.

## Call pattern

Tell output-savers the job is **writing or changing code** (minimal scope) plus **cleaning duplication** when smells are in scope (DRY rule of three).

## Refactor-specific rules

1. **Smallest behavior-preserving diff.** Prefer extract/rename/move over new abstractions. No speculative interfaces.
2. **Delete first.** Dead code, unused imports, commented blocks — remove before extracting.
3. **One purpose per commit/step.** Refactor commits contain no feature flags or behavior tweaks.
4. **Comments.** Follow output-savers comment hygiene: no narrating comments; rename instead.
5. **Review output.** If reporting a refactor review, use output-savers review one-liner format for findings.

## When output-savers wins over refactor zeal

- User asked only to rename for clarity → ladder says stop after rename; do not introduce patterns.
- Third duplication not present → do not extract shared helper (YAGNI).
- Refactor would add dependency → reject unless required for correctness.

If principles and safe-refactor conflict, **safe-refactor** (tests, boundaries) wins over brevity; **output-savers** wins over clever structure.
