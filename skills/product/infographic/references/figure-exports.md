# Figure exports for infographics

Raster and themed exports for layout. Technical verification stays with the technical source. This skill owns **sizes and crops** for poster, slide, and social surfaces.

## PNG from SVG

| Tool | When |
|---|---|
| `scripts/png_from_svg.py INPUT.svg OUTPUT.png --width 1200` | Fast raster of a trusted layout or `render_bars.py` SVG |
| `scripts/export_figure.py png ...` | Same as above |
| `scripts/export_figure.py png-strict ...` | Static SVG checks via optional export scripts when installed |

Requires local `rsvg-convert`. Refuse to overwrite an existing output path.

## Themed Mermaid for a poster slot

When optional Mermaid export scripts are on the path (`LEVISTACK_DIAGRAM_SCRIPTS` or default sibling resolution):

```sh
python3 scripts/export_figure.py themes
python3 scripts/export_figure.py mermaid-theme flow.mmd flow-themed.mmd --theme golden-platform
python3 scripts/export_figure.py mermaid-svg flow-themed.mmd slot-flow.svg --theme golden-platform
```

Needs `mmdc` on PATH for `mermaid-svg`. Record `theme id` in the receipt.

## GIF, batch PNG, and highlight motion

Use the technical receipt commands for GIF, batch PNG, terminal ASCII, or highlight animation when those tools are installed. After the technical pass, reuse commands from the receipt instead of re-deriving topology.

## Sizes

Set width from the destination guide in [formats](formats.md). Common starting points:

| Surface | SVG width (px) |
|---|---|
| Slide 16:9 | 1920 |
| Social square | 1080 |
| Feed portrait 4:5 | 1080 (height from layout) |
| Print poster at 300 dpi | width = inches × 300 |

Recompose aspect ratios. Do not stretch a single PNG.

## Compression

Keep originals. Compare bytes and readability after lossy steps.
