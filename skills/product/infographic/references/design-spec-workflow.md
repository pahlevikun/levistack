# Design spec workflow

Plan layout, hierarchy, and copy before build. Pair with evidence discipline and local exports.

## What this skill does and does not do

| Does | Does not |
|---|---|
| Plan layout, structure, hierarchy, and copy | Replace measured evidence with invented stats |
| Produce editable SVG/HTML and local PNG when tools exist | Claim image-model output is sourced proof |
| Write a design specification for designers or implementers | Ship scheduler posts without publishing gate |

## Step 1: Define goals

Capture in [visual brief](../templates/visual-brief.md):

- Topic and bounded takeaway
- Audience and tone
- Surface (social, print, web, slide) and dimensions
- Sourced data, quotes, or screenshots to include
- Rights and uncertainty

## Step 2: Choose layout type

Use [layout types](layout-types.md) (statistical, timeline, process, comparison, list, or composition tables for map/network/layers). Name why the type fits the evidence.

## Step 3: Produce the design specification

Fill [design specification](../templates/design-specification.md):

- Content outline by section
- ASCII wireframe
- Visual elements (icons, charts, images) with source or "decorative only"
- Color roles from project tokens when available
- Typography roles at delivery size
- Copy blocks ready to paste
- Export dimensions and production method

## Step 4: Build or hand off

- Charts from data: [data graphics](data-graphics.md) or `render_bars.py` when appropriate.
- Technical figures: [technical figures](technical-figures.md) and [technical figure package](technical-figure-package.md).
- Raster export: [figure exports](figure-exports.md).
- Review: [review](review.md). Publish: [publishing gate](publishing-gate.md).
