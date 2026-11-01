---
name: visual-art
description: "Create original static canvas art, reproducible generative art, and short animated GIFs from a visual brief. Use when asked for a poster or art object, seeded procedural artwork, interactive generative parameters, or a chat-sized GIF. Not for factual charts/infographics (infographic), technical diagrams (diagram), product interfaces (ui-ux-kit), or logo identity (logo-kit-svg)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: product
  category: product-design
  department: product
  related_skills:
    - file-toolkit
    - color-kit
    - design-system-kit
    - infographic
    - diagram
    - logo-kit-svg
  invokes:
    - skill: file-toolkit
      when: Render scene sources, convert image formats or encode GIF frames
    - skill: design-system-kit
      when: Artwork must bind supplied brand assets and tokens
  tags:
    - canvas
    - art
    - generative
    - seeded
    - gif
    - animation
  capabilities:
    - static_canvas_composition
    - seeded_art_sources
    - interactive_canvas_exploration
    - frame_animation_composition
  languages:
    - en

---

# Visual art

One owner for non-data artwork. Pick a mode and preserve an editable source,
rebuild settings and the actual exported artifact. Do not invent data graphics
or force a fixed vendor style onto a project.

## Route the output

| Request | Procedure |
|---|---|
| Static canvas, poster or composition | Write a small visual brief, then a file-toolkit image scene JSON. Render with its create command. |
| Seeded generative art | Use the bundled scene generator, record seed/palette/parameters, then render with file-toolkit. |
| Interactive exploration | Generate a self-contained canvas HTML with seed/count controls and PNG export. |
| Short animated GIF | Prepare equal-sized ordered image frames, then call file-toolkit animate through the helper. |

Read [composition and verification](references/composition.md) for brief, layout,
motion and accessibility checks. Read [the helper contract](references/helpers.md)
for commands, bounds and dependencies. File-toolkit owns format conversion;
this skill owns artistic choices and reproducibility.

## Procedure

1. Identify the purpose, subject, target surface, dimensions, allowed text, supplied
   assets and output type. Use design-system-kit for a supplied brand and color-kit
   for palette decisions. Resolve consequential missing inputs; infer reversible
   routine choices and proceed within the task.
2. Choose one visual idea with hierarchy, spacing and deliberate contrast. Leave
   enough negative space for the actual display size. Use the requested style or
   source assets without copying a supplied artist's specific work.
3. Create editable scene JSON, generated parameters or original frame sources.
   Preserve the seed for procedural work. Do not silently rasterize editable text
   or represent generated decoration as factual evidence.
4. Use the helpers instead of generating another conversion pipeline. Inspect
   available backends with file-toolkit capabilities. Missing codecs are explicit
   prerequisites; do not rename a file extension and claim conversion.
5. Render and inspect the actual output at its intended size. For a GIF, check
   dimensions, duration, loop and file size, and inspect several frames. Prefer
   gentle low-frequency motion; avoid flashing and provide a static alternative.
6. Deliver source, final asset, parameters, rebuild command, checks performed and
   any backend or visual-inspection limits. Publishing is a separate action.

## Related skills

- `file-toolkit`: parse/create/convert assets and encode animated frames.
- `color-kit`: palette roles and contrast.
- `design-system-kit`: binding to supplied brand rules.
- `infographic`: evidence-led visual explanations.
- `diagram`: technical figures with source-backed relationships.
- `logo-kit-svg`: logo and identity work through its existing upstream owner.

Use [eval cases](evals/evals.json) for modes and near misses.
