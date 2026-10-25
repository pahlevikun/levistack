# SVG and explanatory motion

Use native vector shapes, live text and named groups for an editable diagram. Keep a separate static source. Preserve a supplied raster as evidence when appropriate, but do not claim a raster embedded in SVG became editable vector art.

## Compose the static view

Set the final aspect ratio and `viewBox` before laying out the nodes. Use stable group IDs for semantic elements. Draw boundaries behind their members and connectors behind the boxes. Give labels enough space and keep a connector from passing through an unrelated node.

Use a small visual vocabulary. Shape, line style and text should distinguish a service, store, boundary, decision and optional path. Explain custom notation in a legend. Pick one dominant reading direction and keep attached labels close enough that their meaning is clear.

Use a real `<title>` and `<desc>`, with unique IDs referenced by `aria-labelledby` on a root `role="img"` SVG. Include a nearby relationship table for dense content. Keep decorative overlays out of the accessibility tree.

Set explicit font fallbacks. Check the fonts available to the renderer. Keep live text in the source even if a separate print export outlines it. Resolve theme variables for a renderer that cannot read external CSS. Do not remove IDs, accessible text or grouping during optimization.

Validate XML, `viewBox`, unique IDs and referenced markers, masks and clips. Then render and inspect. XML checks cannot prove labels fit, text remains legible or a connector points at the right node.

## Motion plan

Use motion when the user asks for it or it explains ordered change. Choose a semantic purpose first:

| Purpose | Treatment |
|---|---|
| Follow a request through a graph | Highlight explicit node and edge IDs in execution order |
| Explain a decision or policy trace | Step through labeled outcomes and branches |
| Show accumulation or state change | Keep values sourced and provide a complete final snapshot |
| Show optional data movement | Add a decorative token while the base edge remains visible |

Never infer execution order from top-left coordinates or DOM order. A left-to-right graph may contain branches, retries and parallel work. Write the step order explicitly and label a selected path as an example if other paths exist.

Keep the complete static figure meaningful without JavaScript. Add motion as a presentation layer. Do not make an error branch, caveat or terminal outcome disappear from the only available view.

For short standalone SVG, use a finite CSS animation with a complete base frame. Put the reduced-motion rule after the animation rules and disable the decorative layer. Keep print static. For looping icons, stroke reveals, staggered step emphasis, and brand-style motion authored entirely in SVG, follow the CSS SVG motion guide named in `SKILL.md` (keyframes in `<defs>`, class-based delays, dashoffset paths). For interactive HTML, provide native Play/Pause and Replay controls, visible focus and a readable step status. Keep controls scoped to their figure and stop playback when hidden. `ui-ux-kit` owns more involved product controls.

Avoid rapid flashes. Do not encode outcomes only in hue, movement or opacity. Provide a still alongside GIF because the file cannot respond to `prefers-reduced-motion`.

## Original local highlight helper

The bundled helper supports one narrow pattern: highlight rectangular focus areas in a declared order. The underlying nodes, text and edges stay visible. The plan references actual source IDs:

```json
{
  "step_ms": 900,
  "steps": [
    {"id": "gate", "label": "Validate request", "box": [300, 100, 180, 100]},
    {"id": "store", "label": "Store accepted request", "box": [560, 100, 180, 100]}
  ]
}
```

Boxes use the SVG's own coordinate system. Choose boxes from the rendered geometry, with padding, and keep them inside the `viewBox`. A step is a focus region, not a generated claim about causality.

```sh
python3 <diagram-skill>/scripts/export_svg.py animate source.svg motion.svg --plan walk.json
python3 <diagram-skill>/scripts/export_svg.py gif source.svg walk.gif --plan walk.json --width 1000
```

The animated SVG plays one highlight pass and ends with the complete unhighlighted view. The GIF shows the same steps and a final still. Total playback is at most five seconds. Use interactive playback for a longer explanation. The script uses no network and makes no changes to the source. It is not a general Mermaid animation engine or an arbitrary CSS timeline capture tool.

Check every step, the final frame, reduced motion and no-animation support. For an animated source from another tool, use that tool's explicit frame API or export a declared frame sequence. Do not take screenshots after guessed wall-clock delays.
