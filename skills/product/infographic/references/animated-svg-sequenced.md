# Animated SVG (sequenced infographic)

Build a **static** infographic layout first, then choreograph reveals in a single self-contained SVG file. This path is for editorial sequences (icons, key numbers, short labels, connectors). Heavy chart races belong in dedicated chart tooling, not here.

Levistack ships **CSS keyframes inside SVG** only. No video encode in this skill.

## When to use

- "Animate this infographic", "sequenced reveal", "stagger icons and stats".
- Landing embed, docs hero, or carousel panel that must stay vector.
- You already have sourced numbers in the evidence ledger.

Stay on the **evidence track**: final values appear in the SVG text from the start. Motion controls opacity, scale, and connector draw only. Do not count up through wrong intermediate statistics.

For labeled synthetic mocks only, you may hand-author a count-up in CSS. Prefer `build_animated_svg.py`, which does not interpolate numbers.

## Design order

1. Balance the full frame as if it were a poster ([layout mood catalog](layout-mood-catalog.md) or [composition](composition.md)).
2. Map reveal **tier** (importance), not layout scan order.

| Tier | Element | Motion |
|---|---|---|
| 1 | Title / central insight | fade and slight rise |
| 2 | Icon or pictogram | scale pop with overshoot |
| 3 | Key number | fade in at final string (no odometer unless synthetic) |
| 4 | Caption | fade under the number |
| 5 | Connector | stroke draw into the next item |

One loud motion at a time. Do not animate two headline numbers together.

## Timing (30 fps mental model)

| Beat | Seconds |
|---|---|
| Title hold | 0.8–1.2 |
| Per item (icon → number → label) | 1.2–2.0 |
| Connector draw | 0.4–0.6, overlaps next item |
| Final hold (all visible, no motion) | 2–3 |

Stagger siblings by about **0.25–0.35 s** (roughly 8–10 frames at 30 fps). Keep one enter curve across the set.

## Accessibility

- `role="img"`, `<title>`, and `<desc>` with the bounded claim and source line.
- `@media (prefers-reduced-motion: reduce)` must show the **complete** static infographic.
- Pair animated SVG with a static sibling for feeds that block motion ([formats](formats.md)).

## Build helper

```bash
python3 scripts/build_animated_svg.py data.json OUTPUT.svg
python3 scripts/build_animated_svg.py data.json OUTPUT.svg --width 1200
```

Input schema: [../templates/animated-infographic.json](../templates/animated-infographic.json). Example: [../examples/animated-steps/steps.json](../examples/animated-steps/steps.json).

## Verify

1. Open the SVG in a browser. Scrub feels like a clear cascade, not a flash.
2. Toggle reduced motion: every label and number is visible.
3. Compare text to the evidence ledger (exact strings).
4. Rasterize a hold frame with `png_from_svg.py` for social if needed.

## Technical figure embeds

Embed a verified static or CSS-animated technical SVG as one panel inside a larger sequenced layout. Page-level carousel motion is separate ([formats](formats.md)).
