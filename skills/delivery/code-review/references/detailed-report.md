# Detailed review report

Use this format only when the user asks for a full written review. Keep the same evidence and publication boundary as the normal preview.

```markdown
# Review of <MR or revision>

## Change and verdict

<What changed, which revision was checked, and the read-only verdict.>

## Findings

| # | Priority | File and line | Observed failure | Evidence | Suggested change |
|---|---|---|---|---|---|
| <number> | <severity> | <path:line> | <reproducible behavior> | <test, contract, or source> | <smallest supported fix> |

## Existing discussions

<Open threads, related findings, and threads still requiring a decision.>

## Verification

<Commands actually run, CI pipeline and job IDs checked, and gaps.>

## Next action

<Local fix, selected draft comments, or explicit publication request, as authorized.>
```

Leave out empty sections. Add a suggestion fence only for an exact drop-in replacement. Do not present the report as a posted review.
