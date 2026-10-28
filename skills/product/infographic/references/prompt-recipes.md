# Prompt recipes

Example invocations for humans and agents. Replace bracketed paths with the project. Load the `infographic` skill first.

## Plan a design specification only

```text
Load the infographic skill. Follow design-spec-workflow and layout-types.
Return a filled design-specification template with wireframe, copy, and color/type roles.
No invented statistics. Mark unknowns.
```

## Design from research notes

```text
Load the infographic skill. Turn these research notes into a source-led editorial infographic.
Return: bounded claim, evidence ledger, reading order, grid rationale, visual system, caveats, and verification checklist.
```

## Redesign a data page

```text
Load the infographic skill. Critique and redesign this data page.
Keep the content. Fix hierarchy, evidence traceability, source labels, and responsive behavior.
Order findings by severity.
```

## Web research poster with charts

```text
Load the infographic skill. Implement a web research poster for this dataset.
Reuse local design tokens. Build an auditable chart sequence with method and source notes.
Complete a technical figure pass for Mermaid or architecture figures if needed.
```

## Static editorial poster

```text
Load the infographic skill. Design a static poster for this archive topic.
Show data hierarchy, uncertainty, and source rights. Include export dimensions for print or PDF.
```

## Review before publication

```text
Load the infographic skill. Review this infographic before publication.
Focus on overclaiming, hidden uncertainty, mixed source types, and broken reading path.
Then run the publishing transport gate if copy schedules with the image.
```

## Carousel from one dataset

```text
Load the infographic skill. Build a mobile carousel from this dataset.
One bounded takeaway per panel. Recompose aspect ratio per frame. Keep sources on every panel that can be shared alone.
```

## Technical figure plus poster

```text
Load the infographic skill. Complete technical-figure-package for a verified Mermaid payment-flow figure (SVG and PNG).
Compose a research poster with citations around that figure. One technical pass only.
Record theme id and export commands in the receipt.
```

## Adapt the method to a new brand

```text
Load the infographic skill. Adapt the editorial method for [subject] without copying any existing project's visual identity.
Keep evidence discipline. Propose new palette roles in the visual brief.
```

## Structured content then vector poster

```text
Load the infographic skill. Fill structured-content.md from the template.
Pick layout from layout-mood-catalog or layout-types. Build editable SVG or HTML.
No raster until I confirm. Evidence ledger beside the claim.
```

## Reading deck (raster slides)

```text
Load the infographic skill. Follow slide-deck-surfaces.
Outline one idea per slide. Save prompts/slide-NN.md for each slide before batch PNG generation.
Confirm layout and aspect unless I said skip confirm.
```

## Social thread package

```text
Load the infographic skill. Follow social-x-surfaces and formats.
Recompose carousel frames for X width. Draft alt text and thread copy.
Run publishing-gate on the scheduler payload. Do not post without my OK.
```

## Sequenced animated SVG (no video)

```text
Load the infographic skill. Follow animated-svg-sequenced and sequenced-infographic-choreography.
Fill templates/animated-infographic.json with exact value_display strings from the ledger.
Optional insight line and timing overrides for stagger and hold.
Run build_animated_svg.py. Deliver SVG only. Optional static hold via reduced-motion preview.
Do not encode MP4 or Remotion in this skill path.
```

## Declarative DSL export

```text
Load the infographic skill. Map structured-content sections to declarative-infographic-syntax.
Emit a renderer DSL file only. I will render locally.
```

## Agent default (OpenAI-style hosts)

See [agents/openai.yaml](../agents/openai.yaml) for `display_name`, `short_description`, and `default_prompt`.
