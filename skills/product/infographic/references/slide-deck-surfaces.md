# Slide deck surfaces

Decks here mean **reading decks**: slides meant to be scrolled or shared, not only spoken once in a room.

## Plan before pixels

1. Outline: title, section breaks, one idea per slide.
2. For each slide record: headline, bullets (sourced), visual type (chart, diagram, photo, icon grid), and speaker notes if needed.
3. Save outline beside other artifacts ([project artifacts](project-artifacts.md)).

Complete a technical figure pass for slides that need Mermaid or architecture figures. Import the export into the deck composition.

## Production choice

| Track | When | Output |
|---|---|---|
| Vector / HTML slides | Numbers, citations, or frequent edits | SVG, PDF from vector, or HTML scroll deck |
| Raster slide images | User wants painted slides or social-native deck posts | PNG per slide under `exports/slides/` |

Raster track requires [confirmation gates](confirmation-gates.md). Save one prompt file per slide before batch generation.

## Batch policy for raster slides

- Finish all prompt files for the selected slides first.
- Generate in batches of up to four parallel jobs when the runtime supports it, unless the user names another batch size.
- Retry failed slides once without redoing successful ones.
- Merge to PDF or PPTX only after all selected images exist.

Do not fix slide text by drawing over a generated PNG. Regenerate with shorter on-slide copy.

## Density and type

- Large type for headlines. Fewer than eight lines per slide when possible.
- Put sources in footer or notes, not scattered microtype.
- Animated builds: provide a complete still per slide for accessibility ([formats](formats.md)).

## Aspect

Default `landscape-wide` (16:9). Portrait decks are valid for mobile scroll. Record the choice in the receipt.
