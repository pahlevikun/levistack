---
name: infographic
description: "Create evidence-based infographics, visual explainers, research posters, charts, timelines and social carousels, including layouts that embed Mermaid, technical figures, and CSS-animated SVG sequenced infographics (icon pop, staggered stats, draw-on connectors, tabular-nums, prefers-reduced-motion). Use when asked to make an animated infographic, sequenced reveal, stagger icons and stats, communicate a sourced claim visually, compose a data story, annotate authentic evidence, critique an infographic or adapt it for web, print, slides or social. Deliver motion as SVG only, not video or MP4. Bundled helpers cover PNG from SVG, optional themed Mermaid export, build_animated_svg.py, and raster prefs when API keys exist."
metadata:
  version: 1.4.0
  author: levistack
  license: MIT
  group: product
  category: editorial-visualization
  department: product
  related_skills:
    - diagram
    - color-kit
    - design-system-kit
    - polyglot-copywriter
    - logo-kit-svg
  invokes:
    - skill: diagram
      when: Mermaid, architecture, schema, or motion on a technical figure; one technical pass per artifact
    - skill: color-kit
      when: Palette roles, token mapping, or contrast proof on the composed poster or carousel
    - skill: design-system-kit
      when: Layout must match a shipped design system file in the repo
    - skill: polyglot-copywriter
      when: Headlines, captions, or social copy need plain-language polish without changing numbers or citations
    - skill: logo-kit-svg
      when: Logo mark in the layout needs SVG authoring or repair
  tags:
    - infographic
    - evidence-led
    - editorial
    - data-storytelling
    - poster
    - carousel
    - slide-deck
    - social-x
    - cover-hero
    - timeline
    - chart
    - technical-figure-embed
    - declarative-syntax
    - animated-svg
    - svg-export
    - accessibility
  capabilities:
    - evidence_ledger_and_claim_bounds
    - surface_router_poster_deck_cover_social
    - layout_mood_catalog_and_keyword_hints
    - structured_content_artifact
    - layout_planning_and_wireframes
    - design_specifications
    - composition_and_grid
    - data_graphics
    - technical_figure_package
    - figure_export_png_and_themed_mermaid
    - visual_theming
    - optional_declarative_infographic_syntax
    - build_animated_svg_script
    - research_quality_review_bars
    - raster_confirmation_gates
    - python_prefs_and_image_generate_cli
    - formats_print_web_social_motion
    - critique_and_review
    - publishing_gate_and_rights
  languages:
    - en

---

# Infographic

Give the reader a clear claim and a visible path to its evidence. Composition must clarify the relationship, not make weak evidence look certain.

Callable catalog skills are listed in frontmatter `metadata.invokes` (and `related_skills` for discovery). Load a companion skill when its `when` line matches the task. This skill still owns evidence, layout, and delivery.

Start with [surface router](references/surface-router.md) when the deliverable could be a poster, deck, cover, social package, or declarative DSL export.

Planning flow: [design spec workflow](references/design-spec-workflow.md) → [layout types](references/layout-types.md) → [design specification template](templates/design-specification.md). Long sources also use [structured content](references/structured-content.md) and [project artifacts](references/project-artifacts.md).

## Define and source the claim

Read the supplied material and existing brand guidance. Record the reader, bounded takeaway, surface, final reading size and output paths in [the brief](templates/visual-brief.md). Infer routine choices and proceed within the task. Ask only when a missing fact changes the claim. Keep project assets outside this installed skill.

Read [evidence](references/evidence.md) before designing. Record source locators, dates or revisions, transforms, uncertainty and reuse rights. Separate sourced facts, reproducible measurements, editorial inference, unknowns and synthetic examples. Put important limits beside the claim in the artifact. An unsupported factual claim must be corrected, sourced or marked unknown before factual delivery. Missing records do not mean zero or absence. association does not prove cause. Verify time-sensitive facts from current primary sources when available and disclose inaccessible evidence.

Use synthetic values only for a requested mockup, visibly labeled in the asset. A model-generated chart, quote, screenshot or plausible curve is not evidence. Use real captures for product claims, retaining state and capture context. Generated illustration can explain a metaphor. Keep factual marks, exact text and numbers in deterministic editable layers.

## Choose the visual relationship

| Work | Read |
|---|---|
| Pick poster vs deck vs cover vs social vs declarative path | [Surface router](references/surface-router.md) |
| Keyword-led layout and mood for drafts | [Layout mood catalog](references/layout-mood-catalog.md), [data/layout-keywords.json](data/layout-keywords.json) |
| Multi-section source before build | [Structured content](references/structured-content.md) |
| Confirm before raster or painted output | [Confirmation gates](references/confirmation-gates.md) |
| Prefs, backends, API raster CLI | [Raster Python](references/raster-python.md) |
| Fresh stats or research poster | [Research quality bars](references/research-quality-bars.md) |
| Reading deck or raster slide batch | [Slide deck surfaces](references/slide-deck-surfaces.md) |
| Social post, thread, or article package | [Social X surfaces](references/social-x-surfaces.md) |
| Article or deck cover hero | [Cover hero surfaces](references/cover-hero-surfaces.md) |
| Optional declarative infographic DSL | [Declarative infographic syntax](references/declarative-infographic-syntax.md) |
| Sequenced animated SVG (no video encode) | [Animated SVG sequenced](references/animated-svg-sequenced.md), [Choreography](references/sequenced-infographic-choreography.md) |
| Layout type pick and wireframe planning | [Layout types](references/layout-types.md), [Design spec workflow](references/design-spec-workflow.md) |
| Comparison, evidence lanes, network, map, timeline or batch layout | [Composition](references/composition.md) |
| Mermaid, flow, architecture or schema figure inside the layout | [Technical figures](references/technical-figures.md), [Technical figure package](references/technical-figure-package.md) |
| Numeric marks, scales, denominators and transformations | [Data graphics](references/data-graphics.md) |
| Responsive web, poster, print, slides, social or motion | [Formats](references/formats.md) |
| Poster colors, Mermaid theme on embedded figures | [Visual theming](references/visual-theming.md) |
| PNG from SVG, themed Mermaid raster for layout slots | [Figure exports](references/figure-exports.md) |
| Critique, repair or final inspection | [Review](references/review.md) |
| Schedule copy with the image, scheduler payloads | [Publishing gate](references/publishing-gate.md) |
| Rights, attribution, public or client release | [Publication boundaries](references/publication-boundaries.md) |
| Example prompts and agent default | [Prompt recipes](references/prompt-recipes.md), [agents/openai.yaml](agents/openai.yaml) |

Choose a dominant relationship before styling. Comparable values need a common frame. Dates need honest spacing or an explicit categorical sequence. Links and spatial position need defined meanings. Explain the reading order and layout briefly, then build. A local preview is a review artifact, not an automatic permission gate.

Compute chart geometry from retained data and transformations. Check units, period, population, denominator, missing values, totals, rounding and uncertainty. Bars use a zero baseline. Area encodings scale area rather than radius. Preserve comparison scales across related panels. Keep raw and derived data distinct, and do not invent confidence intervals or missing values.

## Compose and produce

Reuse the project's fonts, semantic colors, and design tokens when the repo defines them. A single graphic can use a small local style. Keep copy plain and exact: preserve citations, quantities, units and uncertainty in labels and captions.

Build exact charts and labels with editable SVG, HTML, a plotting tool or an appropriate layout source. Keep its data and generator. Use existing local tools first. Follow the format guide and installed tool help. Do not depend on a remote renderer or guess helper APIs. Report the exact missing dependency, blocked export and check that could not run. Preserve useful source and accessible text. Do not upload private material as an automatic fallback.

Recompose each requested aspect ratio instead of stretching it. Keep caveats and sources attached when panels reflow or a carousel page is shared alone. Verify current platform limits before claiming compliance. A familiar aspect ratio alone proves nothing about current upload rules.

## Check and deliver

Run the review against the actual source and delivered file. First repair claims, calculations and inaccessible essential information. Then refine the layout. Inspect at the expected feed width, presentation distance or physical print size. For web, check narrow layouts, zoom and keyboard/touch access to interactive detail. Use measured contrast evidence before claiming a contrast pass. Supply labels or patterns alongside hue and an accessible description or data table.

For motion, keep every claim and caveat available in a complete still. Follow [sequenced infographic choreography](references/sequenced-infographic-choreography.md) for tier order, pacing, and final hold. Declare step order and timing, avoid rapid flashes, and inspect the encoded first/final frames and meaningful steps. Test reduced motion in SVG/HTML and provide controls for long or interactive playback. Pair animated SVG with a still. Motion cannot be the only way to read a fact. Do not ship MP4 or GIF as the primary deliverable from this skill.

Inspect the exact exports: SVG structure and live text, PNG dimensions and background, PDF page size and fonts, or the actual native source in its editor where relevant. A parser pass cannot prove visual quality or editor behavior. After repairs, regenerate and inspect the affected file. For compression, preserve originals and compare bytes and readability.

Deliver editable source, data and generator where used, requested exports, accessible text, the source/transform ledger and a receipt listing dimensions, versions, render commands, checks run and remaining limits. Report critique findings as observed problems with concrete fixes, not invented quality scores. Keep delivery local unless publication was requested. An authorized publishing flow receives the exact asset, copy, alt text and destination for its own checks. When copy ships with the image, run [publishing gate](references/publishing-gate.md) and [publication boundaries](references/publication-boundaries.md).

## Tools and examples

- `scripts/render_bars.py INPUT.json OUTPUT.svg` builds an original zero-baseline bar figure with sources and a text equivalent. It supports nonnegative comparable values only. Use it for that chart, not as a template for every infographic.
- `scripts/png_from_svg.py INPUT.svg OUTPUT.png --width 1200` rasterizes a layout or bar SVG with local `rsvg-convert`.
- `scripts/export_figure.py png|png-strict|mermaid-theme|mermaid-svg|themes` delegates themed Mermaid and strict static SVG checks to optional export scripts when `LEVISTACK_DIAGRAM_SCRIPTS` or the default sibling path is set. `scripts/sibling_diagram.py` resolves that path.
- `scripts/image_generate.py` loads `infographic.prefs.json` / `infographic.extend.md`, lists raster backends, resolves `preferred_raster_backend`, and calls image APIs when keys are set. Use `agent-native` when the host should call its own image tool. See [raster Python](references/raster-python.md).
- `scripts/build_animated_svg.py INPUT.json OUTPUT.svg` writes a self-contained sequenced infographic with CSS keyframes and `prefers-reduced-motion`. See [animated SVG sequenced](references/animated-svg-sequenced.md) and [UPSTREAM.md](UPSTREAM.md).
- `evals/sample-bars.json` is visibly synthetic sample data. `evals/cases.json` covers research, archival, timeline, chart, screenshot, carousel and critique requests, plus boundary cases.
- `examples/cfo-capacity/brief.md` is a fictional worked campaign brief (convergence layout, optional technical figure).
- `references/prompt-recipes.md` lists starter prompts. `agents/openai.yaml` and `agents/README.md` package the default prompt for agent hosts.

Run `python3 -m unittest discover -s <infographic-skill>/scripts -p 'test_*.py'` for checks in `scripts/test_render_bars.py`, `scripts/test_export_figure.py`, `scripts/test_image_generate.py`, and `scripts/test_build_animated_svg.py`. Exercise the request cases against the selected workflow and record observed checks separately from pending tool checks.
