# Research quality bars

Use this guide when the user wants fresh market stats, scientific summaries, or a research poster with many numbers. It adapts a review-bar idea without tying you to any single paid image API.

## Research pass (before layout)

1. Gather candidate facts from primary or reputable secondary sources. Record locators in the evidence ledger.
2. Mark conflicts, ranges, and dates explicitly.
3. Fill [structured content](structured-content.md) only after the ledger stabilizes.
4. Optional: run a dedicated research tool if the user provides one. Treat its output as draft facts until sourced.

## Document-type review bar

Use these as **human** review targets before publish, not as model scores.

| Doc type | Bar (out of 10) | What must pass |
|---|---|---|
| Marketing | 8.5 | Compelling and still sourced, no hype beyond evidence |
| Report | 8.0 | Professional tone, denominators visible |
| Presentation / deck | 7.5 | Readable at distance, one idea per slide |
| Social | 7.0 | Survives single-panel crop, hook honest |
| Internal | 7.0 | Clear enough for teammates, caveats ok |
| Draft | 6.5 | Structure ok, facts may be incomplete if labeled |
| Default | 7.5 | General purpose |

If the piece is below its bar, fix claims and layout before shipping. Do not invent a numeric "quality score" in the receipt.

## Style presets (research visuals)

| Preset | Use when | Visual hint |
|---|---|---|
| Corporate | Business report, board slide | `flat-brand` mood, restrained palette |
| Healthcare / science | Clinical or public health | Conservative color, high label legibility |
| Academic poster | Conference print | `schematic-blue` or `editorial-clean`, small type for methods |
| Editorial | Magazine style | `watercolor-story` or `vintage-print` with strict fact boxes |

Pair presets with project palette rules. For colorblind-safe numeric charts, prefer Wong or Tol palettes when documented in the repo.

## Iteration

1. Build vector or DSL draft.
2. Review against the doc-type bar and [review](review.md).
3. Fix data and hierarchy before polish.
4. Regenerate raster only when the raster track is active.

Stop when the bar is met or the user accepts labeled unknowns. Keep versioned exports when you iterate raster drafts.
