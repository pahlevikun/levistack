# Animated SVG (sequenced infographic)

Build a **static** infographic layout first, then choreograph reveals in a single self-contained SVG file. Editorial sequences: icons, key numbers, short labels, connectors. Heavy chart races belong in dedicated chart tooling, not here.

Levistack ships **CSS keyframes inside SVG** only. No video encode, no Remotion, no MP4 in this skill. Choreography craft: [sequenced infographic choreography](sequenced-infographic-choreography.md). Upstream lineage: [UPSTREAM.md](../UPSTREAM.md).

## When to use

- "Animate this infographic", "animated infographic", "sequenced reveal", "stagger icons and stats".
- User asks for infographic **animation** but the deliverable must stay **SVG**.
- Landing embed, docs hero, or carousel panel that must stay vector.
- You already have sourced numbers in the evidence ledger.

Stay on the **evidence track**: final values appear in the SVG text from the start. Motion controls opacity, scale, and connector draw only. Do not count up through wrong intermediate statistics.

For labeled synthetic mocks only (`synthetic: true`), you may hand-author a count-up in a separate prototype. Default builder does not interpolate numbers.

## Design order

1. Balance the full frame as if it were a poster ([layout mood catalog](layout-mood-catalog.md) or [composition](composition.md)).
2. Map reveal **tier** (importance), not layout scan order. See the tier table in [sequenced infographic choreography](sequenced-infographic-choreography.md).
3. Cap at five steps. One central insight plus supporting stats.

One loud motion at a time. Do not animate two headline numbers together.

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

1. Open the SVG in a browser. Scrub feels like a clear cascade, not a flash. Check title-only, mid-cascade, and final hold seconds from [sequenced infographic choreography](sequenced-infographic-choreography.md).
2. Toggle reduced motion: every label and number is visible.
3. Compare text to the evidence ledger (exact strings).
4. For a social still, use reduced-motion preview or a static duplicate. `png_from_svg.py` alone is not an end-of-timeline capture.

## Technical figure embeds

Embed a verified static or CSS-animated technical SVG as one panel inside a larger sequenced layout. Page-level carousel motion is separate ([formats](formats.md)).
