# Technical figures in infographics

Implementation path for Mermaid, architecture SVG, and raster slots inside a poster, carousel, or page. This file is the **compose and export** checklist for infographic owners.

## Decide ownership

| Asset | Build here | Embed only |
|---|---|---|
| Bar or line chart from JSON/CSV | `render_bars.py` or app charts | — |
| Timeline from dates | [Composition](composition.md) | — |
| Mermaid, draw.io, Excalidraw, schema | — | After technical pass |
| PNG/GIF/motion on technical figure | — | Re-export size only |

Do not draw unverified Mermaid only inside the poster when the figure must match code or config.

## Technical pass (one per artifact)

Record in [visual brief](../templates/visual-brief.md):

- Question the figure answers
- Evidence anchors
- Required source format (`.mmd` preferred when user asked Mermaid)
- Exports: SVG, PNG, optional animated SVG or GIF
- Theme id if the poster slot needs a catalog theme

Accept back source file, static SVG, optional motion, and ledger. See [technical figure package](technical-figure-package.md).

## Place in layout

1. Import SVG at native aspect ratio. Do not stretch labels.
2. Prefer SVG for web and PDF vector paths. Use PNG when the host requires raster only.
3. Keep caption and source line outside the figure layer when possible.
4. For CSS-animated SVG, preserve `<style>` and `prefers-reduced-motion`. Ship a still sibling.

## Export commands

From the infographic skill directory or with absolute paths:

```sh
python3 scripts/png_from_svg.py layout.svg layout-1080.png --width 1080
python3 scripts/export_figure.py png-strict figure.svg figure.png --width 1200
python3 scripts/export_figure.py themes
python3 scripts/export_figure.py mermaid-theme flow.mmd flow-themed.mmd --theme harbor-slate
python3 scripts/export_figure.py mermaid-svg flow-themed.mmd flow.svg --theme harbor-slate
```

Set `LEVISTACK_DIAGRAM_SCRIPTS` when export scripts are not at the default sibling path.

## After technical receipt

Reuse commands from the technical receipt for GIF, batch PNG, or highlight animation. Do not reopen topology for the same artifact. For a new width only, use `png_from_svg.py` or `export_figure.py png`.

## Theming

- Poster field colors: [visual theming](visual-theming.md).
- Mermaid inside the slot: theme catalog from `export_figure.py themes`. Pick muted themes on busy posters.

## Receipt fields

Add to the infographic receipt:

- technical source path
- `theme_id` if used
- `mmdc` or `rsvg-convert` version when known
- PNG width and background
- Motion file path and still path when motion ships

See also [technical figure package](technical-figure-package.md) and [figure exports](figure-exports.md).
