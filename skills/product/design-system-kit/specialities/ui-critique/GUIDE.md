> **Speciality `ui-critique`**, merged from the `ui-critique` skill. Original description: Use when a screen or component feels off: critique hierarchy, spacing, type and states, then propose concrete fixes.
> Paths such as `references/`, `scripts/` and `assets/` are relative to this folder.


# UI Critique

Find why a screen feels wrong and fix the cause, not the symptom.

## Procedure
1. Squint test: what do you notice first, second, third? That order should match what matters most.
2. Check spacing: is it on one scale (4/8/12/16/24)? Do related items sit closer together than unrelated ones?
3. Check type: no more than two or three sizes and weights per screen, with clear contrast between levels.
4. Check states: empty, loading, error, disabled, long text, and very small and very large screens.
5. Check touch targets (44pt minimum) and contrast (4.5:1 for body text).
6. Report 3 to 5 fixes ordered by impact, each with the exact value to change.

## Pitfalls
- Fix hierarchy before polish. Rounded corners will not rescue a bad layout.
- Prefer removing an element to restyling it.
