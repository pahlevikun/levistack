# Confirmation gates

Raster drafts and some social surfaces are costly to redo. Confirm choices before generation unless the user clearly opts out in the current message (for example "skip confirm" or "use defaults").

## When the gate applies

- Any labeled synthetic or model-generated raster image.
- Slide deck images generated as bitmaps.
- Cover hero art that will carry text baked into pixels.
- Optional external image backends the user must supply.

The gate does **not** block vector SVG, HTML figures, or `render_bars.py` output when data is sourced.

## Questions (batch when the runtime allows)

| Priority | Topic | Options |
|---|---|---|
| 1 | Layout and mood | Three or more pairs from [layout mood catalog](layout-mood-catalog.md) with short rationale |
| 2 | Aspect | Named preset or custom ratio |
| 3 | Production track | Evidence vector vs raster draft |
| 4 | Language | Only if source language differs from delivery |
| 5 | Image backend | Only when multiple backends exist and none is pinned in project prefs |

State assumed defaults in the next message when the user skipped confirmation.

## After confirmation

1. Write or update `structured-content.md` when the topic has multiple sections.
2. Save the full final prompt under `prompts/` before calling any image tool.
3. Generate. Retry a failed item once. Do not repaint text on an existing bitmap.
4. Run [review](review.md) at display size. For raster, treat misspelled on-image text as a regenerate, not a patch.

## Preferences file (optional)

Projects may keep `infographic.prefs.json` or `infographic.extend.md` (see [raster Python](raster-python.md)). Run `python3 scripts/image_generate.py prefs show --project .` to see merged values. Preferences recommend only. They do not replace this gate unless `skip_confirm` or `quick_mode` is true in prefs or the user opts out in the current request.
