# Sequenced infographic choreography (SVG)

Craft reference adapted from [iart-ai animated-infographic](https://github.com/iart-ai/data-animation-skills/tree/main/skills/animated-infographic). Levistack delivers **one SVG file** with CSS inside `<defs><style>`. No Remotion project, no MP4, no GIF encode in this skill.

## Static frame first

Lay out the full composition in final positions before any motion. Animation only controls **when** each placed element appears. Scope to one central insight and **3–5** supporting points. More competing motion reads as noise.

Optional JSON field `insight` holds the tier-1 line when it differs from `title`.

## Hierarchy is reveal order

| Tier | Element | Motion in SVG |
|---|---|---|
| 1 | Title or `insight` | fade and slight rise |
| 2 | Icon or glyph | scale pop with overshoot |
| 3 | Key number | fade at final `value_display` (sourced) |
| 4 | Caption | fade under the number |
| 5 | Connector | stroke draw toward the next item |

Reveal by importance, not layout scan order. Only one headline number should **move** at a time. For sourced evidence, the number string is correct from the first frame it becomes visible. Motion is opacity and scale, not an odometer.

## Timing (30 fps mental model)

Defaults match `build_animated_svg.py`. Override with a `timing` object in JSON (see [animated-infographic.json](../templates/animated-infographic.json)).

| Beat | Default (s) |
|---|---|
| Title hold before steps | 1.0 |
| Per item (icon → value → label) | 1.55 stride |
| Stagger between siblings | ~0.27 (8 frames @ 30 fps) |
| Connector draw | ~0.45, overlaps next item |
| Final hold (all visible) | 2.5 (`hold_seconds`) |

End on a **complete static frame** held still for 2–3 seconds. The takeaway is the assembled poster, not mid-cascade.

## Motion craft

- **Icon pop:** cubic-bezier overshoot (not linear scale).
- **Values:** `font-variant-numeric: tabular-nums` on monospace stats so labels do not jitter when digits change width in hand-authored variants.
- **Connectors:** `pathLength="100"` plus `stroke-dashoffset` keyframes so draw-on works without measuring path length in script.
- **Pictogram fills:** reveal discrete units on the same stagger; clip partial units with a mask instead of scaling a fraction glyph.

## Template × data

Keep layout and theme fixed; swap `steps`, `title`, `source`, and `insight` per dataset. Validate 1–5 steps, nonempty strings, and ledger-matched `value_display` before build.

```bash
python3 scripts/build_animated_svg.py data/q2.json out/q2.svg
python3 scripts/png_from_svg.py out/q2.svg out/q2-hold.png --width 1200
```

`png_from_svg.py` captures the **first painted frame**, not an animation midpoint. For a hold-frame PNG, pause at end of the timeline in a browser or export a static sibling SVG with all elements visible.

## Verify (SVG, not video)

1. Build from the shipped JSON, not a stale template default.
2. Open the SVG in a browser. Scrub the timeline: title alone, mid-cascade, final hold.
3. Toggle `prefers-reduced-motion`: every tier is visible without animation.
4. Compare every `value_display` and caption to the evidence ledger.
5. Optional: rasterize after forcing the reduced-motion stylesheet for a social still.

Heavy chart races and CSV-driven chart animation belong outside this sequenced layout path.
