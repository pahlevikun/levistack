# UI Critique

This is the core method for **Step 3** of the design-system-kit pipeline. It runs after the system exists (Step 2), so each fix points to a token. The full system-aware checklist, the platform lens (mobile, desktop, web, TV, car), the severity scale and the report shape are in [../../references/critique.md](../../references/critique.md).

Find why a screen feels wrong and fix the cause, not the symptom.

## Procedure
1. Squint test: what do you notice first, second, third? That order should match what matters most.
2. Check spacing: is it on one scale (4/8/12/16/24)? Do related items sit closer together than unrelated ones?
3. Check type: no more than two or three sizes and weights per screen, with clear contrast between levels.
4. Check states: empty, loading, error, disabled, long text, and very small and very large screens.
5. Check touch targets (44pt minimum on touch, larger on TV and in a car; see [platforms](../../references/platforms.md)) and contrast (4.5:1 for body text).
6. Check against the system: count hard-coded values and list each place that bypasses a token.
7. Report 3 to 5 fixes ordered by impact, each with the exact token or value to change. Add what to change in the system itself.

## Pitfalls
- Fix hierarchy before polish. Rounded corners will not rescue a bad layout.
- Prefer removing an element to restyling it.
