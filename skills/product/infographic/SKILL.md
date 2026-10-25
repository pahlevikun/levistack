---
name: infographic
description: "Create evidence-based infographics, visual explainers, research posters, charts, timelines and social carousels, including layouts that embed Mermaid, diagram figures, and CSS-animated SVG (keyframes, stroke reveals, staggered steps, prefers-reduced-motion). Use when asked to communicate a sourced claim visually, compose a data story, annotate authentic evidence, critique an infographic or adapt it for web, print, slides or social. Pair with diagram (same product group) for technical structure, Mermaid source, and PNG, GIF or animated SVG exports. Use color-kit for palettes, design-system-kit for shared tokens, and create-documentation for full documentation."
---

# Infographic

Give the reader a clear claim and a visible path to its evidence. Composition must clarify the relationship, not make weak evidence look certain.

## Define and source the claim

Read the supplied material and existing brand guidance. Record the reader, bounded takeaway, surface, final reading size and output paths in [the brief](templates/visual-brief.md). Infer routine choices and proceed within the task. Ask only when a missing fact changes the claim. Keep project assets outside this installed skill.

Read [evidence](references/evidence.md) before designing. Record source locators, dates or revisions, transforms, uncertainty and reuse rights. Separate sourced facts, reproducible measurements, editorial inference, unknowns and synthetic examples. Put important limits beside the claim in the artifact. An unsupported factual claim must be corrected, sourced or marked unknown before factual delivery. Missing records do not mean zero or absence. association does not prove cause. Verify time-sensitive facts from current primary sources when available and disclose inaccessible evidence.

Use synthetic values only for a requested mockup, visibly labeled in the asset. A model-generated chart, quote, screenshot or plausible curve is not evidence. Use real captures for product claims, retaining state and capture context. Generated illustration can explain a metaphor. Keep factual marks, exact text and numbers in deterministic editable layers.

## Choose the visual relationship

| Work | Read |
|---|---|
| Comparison, evidence lanes, network, map, timeline or batch layout | [Composition](references/composition.md) |
| Mermaid, flow, architecture or schema figure inside the layout | [Diagram handoff](references/diagram-handoff.md) |
| Numeric marks, scales, denominators and transformations | [Data graphics](references/data-graphics.md) |
| Responsive web, poster, print, slides, social or motion | [Formats](references/formats.md) |
| Critique, repair or final inspection | [Review](references/review.md) |

Choose a dominant relationship before styling. Comparable values need a common frame. Dates need honest spacing or an explicit categorical sequence. Links and spatial position need defined meanings. Explain the reading order and layout briefly, then build. A local preview is a review artifact, not an automatic permission gate.

Compute chart geometry from retained data and transformations. Check units, period, population, denominator, missing values, totals, rounding and uncertainty. Bars use a zero baseline. Area encodings scale area rather than radius. Preserve comparison scales across related panels. Keep raw and derived data distinct, and do not invent confidence intervals or missing values.

## Compose and produce

Reuse the project's fonts and semantic colors. `color-kit` owns palette decisions and measured contrast. `design-system-kit` owns shared tokens. A single graphic can use a small local style. `ui-ux-kit` owns application controls and interactions, `create-documentation` owns full pages, and `logo-kit-svg` owns logo work. Apply `polyglot-copywriter` to copy while preserving exact citations, quantities, units and uncertainty.

Build exact charts and labels with editable SVG, HTML, a plotting tool or an appropriate layout source. Keep its data and generator. Use existing local tools first. Follow the format guide and installed tool help. Do not depend on a remote renderer or guess helper APIs. Report the exact missing dependency, blocked export and check that could not run. Preserve useful source and accessible text. Do not upload private material as an automatic fallback.

Recompose each requested aspect ratio instead of stretching it. Keep caveats and sources attached when panels reflow or a carousel page is shared alone. Verify current platform limits before claiming compliance. A familiar aspect ratio alone proves nothing about current upload rules.

## Related skills

- `diagram` (sibling under `product/`) owns Mermaid, draw.io, Excalidraw, SVG, architecture and process figures, plus local PNG, GIF and animated SVG exports. Use its [workflow](../diagram/SKILL.md) when the infographic needs a technical figure or motion on that figure. Follow [diagram handoff](references/diagram-handoff.md) for the package to send and receive.

Pass the bounded question, sources, required formats and a note that the handoff is used. Accept the editable figure and evidence/fidelity ledger, then finish the editorial composition here.

Allow at most one handoff between these two skills for the same artifact. If diagram sent the artifact here, do not call it back. Reuse its documented export mechanics directly when needed, or use the project's renderer and report a missing capability. Editorial arrangement must preserve the supplied technical relationships and known limits.

## Check and deliver

Run the review against the actual source and delivered file. First repair claims, calculations and inaccessible essential information. Then refine the layout. Inspect at the expected feed width, presentation distance or physical print size. For web, check narrow layouts, zoom and keyboard/touch access to interactive detail. Use measured contrast evidence before claiming a contrast pass. Supply labels or patterns alongside hue and an accessible description or data table.

For motion, keep every claim and caveat available in a complete still. Declare step order and timing, avoid rapid flashes, and inspect the encoded first/final frames and meaningful steps. Test reduced motion in SVG/HTML and provide controls for long or interactive playback. Pair GIF with a still. Motion cannot be the only way to read a fact.

Inspect the exact exports: SVG structure and live text, PNG dimensions and background, PDF page size and fonts, or the actual native source in its editor where relevant. A parser pass cannot prove visual quality or editor behavior. After repairs, regenerate and inspect the affected file. For compression, preserve originals and compare bytes and readability.

Deliver editable source, data and generator where used, requested exports, accessible text, the source/transform ledger and a receipt listing dimensions, versions, render commands, checks run and remaining limits. Report critique findings as observed problems with concrete fixes, not invented quality scores. Keep delivery local unless publication was requested. An authorized publishing flow receives the exact asset, copy, alt text and destination for its own checks.

## Tools and examples


- `scripts/render_bars.py INPUT.json OUTPUT.svg` builds an original zero-baseline bar figure with sources and a text equivalent. It supports nonnegative comparable values only. Use it for that chart, not as a template for every infographic.
- `evals/sample-bars.json` is visibly synthetic sample data. `evals/cases.json` covers research, archival, timeline, chart, screenshot, carousel and critique requests, plus boundary cases.
- The `diagram` skill provides local SVG/PNG/GIF exports. If it is unavailable, use the project's renderer and report the gap. Do not copy its helpers into this skill.

Apply `polyglot-copywriter` to headings, labels, captions and the handoff. Keep citations, numbers, units and uncertainty exact.

Run `python3 -m unittest discover -s <infographic-skill>/scripts -p 'test_*.py'` for the focused checks in `scripts/test_render_bars.py`. Exercise the request cases against the selected workflow and record observed checks separately from pending tool checks.

