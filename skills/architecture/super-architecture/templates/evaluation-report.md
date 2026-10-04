# Architecture evaluation: <system>

**Date:** <YYYY-MM-DD>   **Scope:** <whole system | module | migration feasibility>   **Evidence:** <scan output, files read>

## Summary
<Three sentences: the style found, the overall health, the most important thing to fix.>

## Detected architecture
- Style: <primary>, variations: <...>   Confidence: high | medium | low
- Stack: <...>

## Quick diagnostic (0 to 7)
| Question | Yes or no | Evidence |
|---|---|---|
| Business rules testable without database, server or framework | | |
| All dependencies point inward | | |
| Database swappable without touching business logic | | |
| Use cases independent of delivery mechanism | | |
| Framework confined to the outer ring | | |
| Component graph has no cycles | | |
| One composition root builds dependencies | | |
**Score:** <n> of 7 -> <band>

## Maturity
Current level: L<n>. Target: L<n>. Key gaps: <...>

## Fitness (1 to 5)
| Dimension | Weight | Score | Evidence |
|---|---|---|---|
| Business alignment | 25% | | |
| Team fit | 25% | | |
| Technology fit | 20% | | |
| Evolution capability | 15% | | |
| Delivery efficiency | 15% | | |
**Weighted total:** <x.y>

## Debt
| Category | Weight | Score (0 to 100, higher is worse) | How counted |
|---|---|---|---|
| Structural | 0.5 | | |
| Design | 0.3 | | |
| Testing | 0.2 | | |
**Total:** <n> -> healthy | mild | moderate | severe

## Confirmed findings
| # | Finding | Where (file:line) | Severity | Fix |
|---|---|---|---|---|
| 1 | | | P0 | |

## Roadmap
| Phase | Actions | Effort | Exit check |
|---|---|---|---|
| 1. Stop the bleeding | | | |
| 2. Micro-refactor | | | |
| 3. Upgrade | | | |
| 4. Continuous | | | |

## Not assessed
<What could not be checked, and what would settle it.>
