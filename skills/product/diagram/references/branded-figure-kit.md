# Branded figure kit

HTML or SVG figures with editorial tokens. This does not replace `design-system-kit`.

## First figure gate

Before the first branded figure in a project:

1. Check for design tokens or `DESIGN.md`.
2. If only defaults exist, ask once: customize from site URL, `color-kit` build, `design-system-kit`, pasted tokens, or keep the neutral scaffold.
3. Record the choice in the diagram brief.

Skip the gate when the repo already has custom tokens.

## Build

1. Pull roles from `color-kit` when you can (surface, on-surface, accent, muted, danger).
2. Use inline SVG or HTML with semantic groups, live text, and `viewBox`. Do not use a raster image as the only source.
3. For embedded Mermaid, apply a presentation theme with `mermaid_render.py`.
4. Export PNG for slides or wikis when needed.

## Style gate checklist

- One or two accent focal nodes per view.
- Measured contrast on text pairs when `color-kit` ran.
- Legend when color carries meaning.
- Static frame for any motion. See SVG motion guides in `SKILL.md`.

## Handoffs

| Need | Skill |
|---|---|
| Full token file and governance | `design-system-kit` |
| Palette only | `color-kit` |
| Multi-panel story | `infographic` |
| Logo or mark | `logo-kit-svg` |

`theme-factory` slide themes can inspire mood words. Map that mood to `color-kit` brief knobs. Do not copy hex tables from slide packs.
