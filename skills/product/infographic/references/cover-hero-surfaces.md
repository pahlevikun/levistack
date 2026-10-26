# Cover hero surfaces

Covers sit above articles, decks, and posts. They sell attention, not new facts.

## Six axes

Confirm or infer each axis before raster hero work. Defaults are safe starting points only.

| Axis | Values | Default |
|---|---|---|
| Frame type | hero scene, concept metaphor, type-led, minimal band, environment scene | concept metaphor |
| Palette family | warm, cool, dark, earth, vivid, pastel, mono, duotone | from project palette brief |
| Render style | flat vector, hand line, paint wash, pixel, chalk, screen print | flat vector |
| Text depth | none, title only, title plus subtitle, rich labels | title only |
| Contrast level | quiet, balanced, loud | balanced |
| Type voice | clean sans, handwritten, serif, display | clean sans |

## Evidence rules

- Do not paint statistics into the hero unless they appear in the ledger.
- Prefer title-only text on art. Put numbers in the body or caption layers.
- Reference images: store under `source/refs/` with a one-line note on what each ref controls.

## Sizes

Match the host surface. Common starting points:

| Host | Starting ratio |
|---|---|
| Blog header | 16:9 or 3:2 |
| Deck title slide | 16:9 |
| X card image | 16:9 or 1.91:1 per current [formats](formats.md) check |
| Vertical story | 9:16 |

Verify live platform limits before claiming compliance.

## Workflow

1. Read article or brief. Set axes via [confirmation gates](confirmation-gates.md) when raster is planned.
2. Write `prompts/cover-{slug}.md` with axes, aspect, and forbidden elements (no fake UI, no logos you lack rights to).
3. Generate or illustrate. For vector covers, build editable SVG/HTML instead of raster when text may change.
4. Deliver still plus source. Run [publication boundaries](publication-boundaries.md) when the cover is public.
