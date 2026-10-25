# Wireframe and flow

Use this for "where is the wireframe" and "show me every screen and how they connect". The result is a layout proof, not a polished screen. Say the point of the picture first and pick the family from the relationship (see `layout-by-relationship.md`).

## Contents
- Shape wireframe
- Flow map
- Checks

## Shape wireframe

- **Grayscale on warm paper.** Base `#F7F7F5`, ink `#2B2B2B`, rules `#C9C9C9`, a 24 px grid background, monospace labels, no brand color. The user reads structure and does not argue about taste.
- **Three labels** keep it from being reviewed as a design:
  1. A kicker: `WIREFRAME v0.1`.
  2. One line saying what the frame claims: "shape, not look".
  3. A footer naming what is still undecided.
- **Show state, do not describe it.** For a tool rail, draw the active tool raised, show its effect on the canvas, and add a small callout at the cursor. Add a legend under the canvas (`solid = sync`, `dotted = async`).
- **Phone frame:** 390×844, a 44 px status bar, content in a flex column, the bottom bar pinned with `margin-top:auto`. A bar pinned with `position:absolute` takes no space, so give the content `padding-bottom` of the bar height plus a margin.
- **Bottom-anchor** calls to action and input rows, or every frame ends two thirds empty.

## Flow map

One canvas, drawn in one `<svg>`:

- Rows are phases of the journey. Each screen is a frame with an ID badge (`S1`, `S2`).
- One drawn arrow per transition, in the same coordinate space as the frames, so arrows do not drift when a frame moves.
- A transition table below the canvas: from, to, trigger.
- Each frame carries the requirement it proves.
- Generate it from one script with shared tokens, so a fix is one edit and a re-render.

For a very large journey, inspect one frame at a time (clip each frame at scale 2). A tall board shrunk into one image cannot be read.

## Checks

- Count frames, arrows and badges after every regeneration. Compare with the expected numbers.
- Run the overlap and overflow checks in `render-and-check.md`, then the gate in `variant-gate.md`.
- Label any number or name that is sample data as "sample".
- Every control you draw must work in the real design. Delete a decoration you will not build.
