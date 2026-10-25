# Diagram and Mermaid in an infographic

Use this when the infographic needs a **technical figure**: process flow, sequence, architecture, schema, or API structure. Editorial charts and timelines built from data stay in this skill. Topology and labeled relationships belong to `diagram` in the same product group.

## When to hand off

| Need | Owner |
|---|---|
| Bar, line or other chart from a dataset | Infographic data graphics |
| Timeline from dated evidence | Infographic composition |
| Mermaid, draw.io, Excalidraw, or architecture SVG | `diagram` first |
| PNG, GIF, CSS-animated SVG (keyframes in file), or highlight-based motion | `diagram` (reuse its export tools) |
| Poster layout, headline, citations, carousel pages | Infographic after handoff |

Do not author Mermaid only inside the infographic workflow. Do not duplicate `diagram` scripts into this skill.

## Handoff to diagram (outbound)

Before calling `diagram`, record in the visual brief:

- bounded question the figure must answer;
- evidence anchors and fidelity limits;
- required editable source format (prefer Mermaid when the user asked for Mermaid);
- exports needed (SVG, PNG, animated SVG, GIF);
- whether motion is requested and the step order tied to evidence.

Load `diagram` and complete its workflow for the figure. Accept back:

- authoritative source (`.mmd`, native editor file, or SVG);
- static SVG at layout size;
- optional motion: CSS-animated SVG, highlight-based animated SVG or GIF, plus step plan or class-to-step map;
- evidence or fidelity ledger entries for every node and edge.

At most **one** handoff to `diagram` per artifact. Do not call `diagram` again after it returns unless the user opens a new task.

## Mermaid inside the poster

1. `diagram` writes and verifies Mermaid, renders to SVG, and compares semantics to the source.
2. Infographic places the SVG (or PNG) in the layout without distorting aspect ratio or cropping labels.
3. Preserve `diagram` labels, arrow direction and legend meanings. Editorial copy sits outside the figure or in captions, not overwritten on technical labels without agreement.
4. If the poster needs **motion**, request it from `diagram`: CSS keyframe SVG (loops, staggered steps, stroke reveals, with `prefers-reduced-motion`), or finite highlight GIF or animated SVG from a declared plan. Embed the **complete still** plus the motion file. Do not strip `<style>` or `@media (prefers-reduced-motion)` when inlining animated SVG. Follow motion rules in formats.md for the full page.

Infographic motion for the **whole page** (carousel transitions, emphasis) is separate from diagram's **semantic** figure animation. Both need a still that carries every factual claim.

## Inbound from diagram

When `diagram` sends an artifact here, do not call `diagram` back. Reuse documented export commands from the receipt if another raster size is needed. If a tool is missing, report the gap and keep the editable source.

Finish composition, review, and delivery here. The receipt must list both infographic exports and the diagram source path.
