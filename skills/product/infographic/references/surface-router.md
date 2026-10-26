# Surface router

Pick the deliverable before layout work. Each surface has its own size rules, evidence bar, and export path.

| User intent | Primary guide | Evidence default |
|---|---|---|
| Poster, one-page explainer, landing figure | [Layout types](layout-types.md), [composition](composition.md) | Sourced facts in editable layers |
| Design spec only (no build yet) | [Design spec workflow](design-spec-workflow.md) | KPIs marked sourced or unknown |
| Slide deck (reading or scroll deck) | [Slide deck surfaces](slide-deck-surfaces.md) | Vector or HTML first when numbers must stay exact |
| Social carousel or single image post | [Formats](formats.md), [Social X surfaces](social-x-surfaces.md) | Recompose per frame, caveats on every panel |
| Article or post cover hero | [Cover hero surfaces](cover-hero-surfaces.md) | Title truthful, no invented stats in art |
| Template-driven chart poster (local renderer) | [Declarative infographic syntax](declarative-infographic-syntax.md) | Data block matches evidence ledger |
| Research-heavy stats or market brief | [Research quality bars](research-quality-bars.md) | Research pass before visual draft |
| Raster mood board or labeled synthetic mock | [Confirmation gates](confirmation-gates.md) | Mark synthetic, never ship as fact |
| Sequenced animated SVG (icons, stats, connectors) | [Animated SVG sequenced](animated-svg-sequenced.md) | Final numbers in markup, motion reveals only |

## Two production tracks

**Evidence track (default):** structured content → layout plan → SVG, HTML, or computed charts → exports via [figure exports](figure-exports.md). Use [technical figure package](technical-figure-package.md) for embedded topology.

**Raster draft track:** use only when the user wants a painted or generated look, or when the surface is inherently bitmap (some social covers). Require [confirmation gates](confirmation-gates.md). Save prompt files under the project folder. Do not fix wrong text by painting over the bitmap. Regenerate or simplify on-image text.

## Handoffs

- Technical topology and Mermaid: one technical pass per artifact ([technical figure package](technical-figure-package.md)).
- Palettes and contrast: use project token files and measured pair checks.
- Scheduled posts: [publishing gate](publishing-gate.md) after assets exist.
