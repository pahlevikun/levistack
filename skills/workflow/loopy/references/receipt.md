# Loopy receipt

Return this in the reply after the loop stops. Keep it short. Include one action line per round that actually ran.

```markdown
## Loopy receipt

Conditions: [the observations that count as passed]
Scope: [files or systems inspected or changed]
Check: [the command or inspection, and the conditions it ran under]
Boundary: [user-supplied limit, or "no progress"]
Result: Passed | Clean no-op | Blocked | Approval required | Boundary reached | No progress

Rounds:
- [change, check, result]

Next: [nothing, the remaining failed condition, or the exact approval or blocker]
```

Do not include secrets. Do not call **Boundary reached** or **No progress** a pass.
