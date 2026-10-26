# Hand off to infographic

Use when the user wants an **editorial** deliverable (poster, carousel, research graphic, social frame) that **includes** a verified technical figure, not a diagram alone.

## Outbound package

Pass to `infographic`:

| Item | Content |
|---|---|
| Editable source | Mermaid, draw.io, Excalidraw, or SVG path |
| Static export | SVG or PNG at a stated width |
| Motion | Optional GIF or animated SVG, step plan JSON, and a still frame |
| Ledger | Evidence anchors, confirmed vs inferred edges, open gaps |
| Brief | Reader, bounded question, formats, and note that diagram completed its pass |

Do not call `infographic` back after it accepts the package. At most one handoff between these two skills per artifact.

## Mermaid and animation

Author and verify Mermaid in this skill. Render to SVG before any infographic layout. For animation:

1. Keep a complete static SVG.
2. Choose **CSS keyframe animation in SVG** for loops, mascot motion, stroke reveals, and staggered step pulses (see the CSS SVG motion guide in `SKILL.md`). Deliver `*-animated.svg` with `prefers-reduced-motion` and a static sibling when both are needed.
3. Or build a **finite semantic highlight** plan from evidence and export with `export_svg.py animate` or `gif` when installed.
4. State which pattern was used. Highlights are rectangular focus steps; CSS motion is authored classes and keyframes, not timeline capture from a browser.

`infographic` owns page composition, copy, citations and multi-format crops. It may embed your exports without re-deriving topology. For poster-sized PNG or another levistack theme on the same `.mmd`, it can call `export_figure.py` in its skill (sibling to this one) without a second topology pass.

## Stay in diagram

Remain here when the task is only to create, repair, convert or export a technical figure with no editorial poster or story layout.
