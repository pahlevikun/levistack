# After-mode audit template

Use when the user chose **AFTER** super-noslop (audit first; fix approved finding numbers only).

Save as `anti-slop/audit-001-YYYY-MM-DD.md`.

```markdown
# Super-noslop audit — YYYY-MM-DD

**Diff scope:** `<paths or PR summary>`
**Mode:** AFTER (user selects finding numbers to fix)

## Findings

| # | Priority | Rule | One-line reason | Location |
|---|----------|------|-----------------|----------|
| 1 | HIGH | R-02 | Generic CLI error without code | `path:line` |
| 2 | MEDIUM | R-01 | Extra service layer for single query | `path:line` |

Priority map: Hard Gate = HIGH, Purpose-Gate = MEDIUM, Quality locks = LOW.

## Delivery gate snapshot

- Hard Gate: FAIL (finding 1)
- Purpose-Gate: PASS with reasons documented
- Craftsmanship: PASS
- Quality locks: PASS

## User-approved fixes

- [ ] Fix #1 only (user requested)

Do not fix unapproved numbers in AFTER mode.
```
