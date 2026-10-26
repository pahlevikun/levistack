# Technical figure package

Use when the infographic needs a **technical figure**: process flow, sequence, architecture, schema, or API structure. Editorial charts and timelines built from data stay in this skill.

## Scope split

| Need | Where it lives |
|---|---|
| Bar, line or other chart from a dataset | [Data graphics](data-graphics.md) |
| Timeline from dated evidence | [Composition](composition.md) |
| Mermaid, draw.io, Excalidraw, or architecture SVG | Technical figure pass first |
| PNG, GIF, CSS-animated SVG, or highlight motion on that figure | Same pass, export tools |
| Poster layout, headline, citations, carousel pages | Infographic composition after the figure is verified |

Author topology in a dedicated technical pass. Do not paste unverified Mermaid only inside the poster layout.

## Outbound brief (before the technical pass)

Record in the visual brief:

- bounded question the figure must answer;
- evidence anchors and fidelity limits;
- required editable source format (prefer Mermaid when the user asked for Mermaid);
- exports needed (SVG, PNG, animated SVG, GIF);
- whether motion is requested and the step order tied to evidence.

## Inbound package (after the technical pass)

Accept:

- authoritative source (`.mmd`, native editor file, or SVG);
- static SVG at layout size;
- optional motion: CSS-animated SVG, highlight-based animated SVG or GIF, plus step plan or class-to-step map;
- ledger entries for every node and edge.

At most **one** technical pass per artifact. Do not reopen topology after composition starts unless the user opens a new task.

## Mermaid inside the poster

1. Verify Mermaid, render to SVG, and compare semantics to the source.
2. Place the SVG (or PNG) in the layout without distorting aspect ratio or cropping labels.
3. Preserve technical labels, arrow direction and legend meanings. Editorial copy sits in captions, not over technical labels without agreement.
4. For figure motion, use CSS keyframe SVG (with `prefers-reduced-motion`) or a finite highlight export. Embed the **complete still** plus the motion file. Do not strip `<style>` when inlining animated SVG. Page-level carousel motion is separate; both need a still that carries every factual claim.

## Re-export without redoing topology

Reuse commands from the technical receipt if another raster size or theme is needed. For SVG width changes, use [figure exports](figure-exports.md) (`png_from_svg.py` or `export_figure.py`). For themed Mermaid on the same source, use `export_figure.py mermaid-theme` when optional export scripts are installed (`LEVISTACK_DIAGRAM_SCRIPTS`). If a tool is missing, report the gap and keep the editable source.

Finish composition, review, and delivery here. The receipt must list infographic exports and the technical source path.
