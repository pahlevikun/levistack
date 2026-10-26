---
name: prototype-wireframe
description: "Answer one design question with a throwaway prototype or a wireframe before real code. A logic question gets one HTML playground, a look question gets several structurally different variants of one screen behind a URL switch (in the real page when one exists), a shape question gets grayscale wireframes, and a flow question gets one navigation map. Can dress a variant in a given brand. Renders screens to PNG with headless Chrome, scores them with a short gate, and keeps a receipt. Use when the user says prototype this, try it, show me options, where is the wireframe, wire up every screen, or how should this behave. Not for polishing a shipped UI (product-polish-workflow) or tokens and component libraries (design-system-kit)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: product
  category: product-design
  department: product
  related_skills:
    - ui-ux-kit
    - design-system-kit
  tags:
    - prototype
    - wireframe
    - throwaway
  capabilities:
    - rapid_prototype
  languages:
    - en

---

# Prototype and wireframe

Answer one design question with the cheapest thing that can answer it. Draw it or run it, look at it, decide, and throw it away.

Use this before real code when the user says "try it", "prototype this", "show me options", "where is the wireframe", "how should this behave" or "which layout is better".

## Step 1: name the question

A prototype answers **one** question. Write it down in one line and show it to the user. If you have two questions, make two prototypes.

| The question is about | Kind | What you build | Read |
|---|---|---|---|
| How a rule, state machine or flow **behaves** | **Logic** | One HTML file the user can click through | [logic-playground.md](references/logic-playground.md) |
| How a screen should **look** | **Look** | Several variants of one screen on one page, switched by `?v=a`, `?v=b`. Each has a written direction | [look-variants.md](references/look-variants.md), [directions.md](references/directions.md) |
| How a screen is **laid out**, before style | **Shape** | Grayscale wireframe, marked as unfinished | [wireframe.md](references/wireframe.md), [layout-by-relationship.md](references/layout-by-relationship.md) |
| How screens **connect** | **Flow** | One canvas with every screen and every arrow | [wireframe.md](references/wireframe.md), [layout-by-relationship.md](references/layout-by-relationship.md) |

If the user is stuck on what to ask, ask one question first: "What decision will this help you make?"

## Rules for every prototype

1. **It is throwaway, and it says so.** Put a visible "PROTOTYPE" label on the page and a comment at the top of the file. Do not harden it, test it or ship it. Keeping it is a new request. The one thing that outlives it is the answer, and for a logic prototype the pure rule block.
2. **One command runs it.** Open a file, or run one line. No install, no build, no server unless the question needs one.
3. **No persistence.** State lives in memory. A reload resets it.
4. **No polish.** Skip animation, accessibility work, error handling and edge cases the question does not ask about.
5. **Reuse the project's tokens and copy** when the repo has them: read its token file or `DESIGN.md` and use the names, glossary and strings. Never invent a design system when one exists. When the user gives a brand, follow [brand-dress.md](references/brand-dress.md). A prototype never writes a `DESIGN.md`, a palette or a QA tracker. If the answer needs those, hand off (see Related skills).
6. **Pick one home.** Default: a scratch folder (`prototypes/<topic>/`), outside the app's source tree, touching no product code. Exception for a look question: when the screen already exists, put the variants on that page, on a **throwaway branch** that never merges, with the switcher shown only outside production. Variants may read real data and never write it.
7. **Hold content identical across variants.** Same text, same counts. Only the thing being compared changes.
8. **Look at it before you show it.** Render, check, fix. See [render-and-check.md](references/render-and-check.md).
9. **Be different, not just decorated.** Variants must disagree about structure. See [directions.md](references/directions.md).
10. **Show only true content.** A drawn number equals what is on screen. Sample data is labeled as sample data. No invented quotes, sources or fake product screens.

## Step 2: build, render, check

1. Build the smallest version that can answer the question.
2. Render it to PNG (looks and wireframes), or run it once (logic). Follow [render-and-check.md](references/render-and-check.md).
3. Check it with measured tests first, then a targeted look (never "does this look good").
4. Fix and re-render only what failed. Two or three rounds is normal.
5. Run the short gate in [variant-gate.md](references/variant-gate.md) (score, thumbnail check, red-team questions). Fix the lowest line first. When a round is only polish, **refine what is there. Do not add more.**

## Step 3: hand back the answer

Give the user the answer, not just the artifact:

```
Question: <the one line>
What I built: <path, and how to run it>
What it showed: <2 to 4 lines, in mechanisms: what grows, what breaks, what is unclear>
My pick: <option or rule>, because <one reason>
Still undecided: <what the prototype could not answer>
Next: keep it (new request) | throw it away | build the real thing with <skill>
```

Then close it out:

1. Write the answer where the team will find it: the plan, the issue or the design doc. A logic prototype also hands over its confirmed rule block.
2. Fill the receipt (`templates/receipt.md`) and keep it with the prototype.
3. Delete the prototype. If someone may want the full set again, keep it on a clearly named throwaway branch and put the branch name in the receipt and the issue. Never leave it beside product code.

For a look prototype, rank the variants and say what each losing one is still good at. Offer a compromise only when it is real.

## Templates

- `templates/playground.html`: a working state-machine playground. Replace the `MACHINE` table.
- `templates/screen.html`: a fixed-size phone screen to start a look or shape prototype from. Swap its tokens for the app's.
- `templates/variant-switcher.js`: one script that switches variants by `?v=`, with arrow keys, hidden outside local pages.
- `templates/receipt.md`: the record to keep: question, home, how to run, gate score, answer.

## Do not

- Build the real feature "while you are at it".
- Change product files, except on a throwaway branch in the in-app look shape.
- Show a wireframe without its "unfinished" labels, or it gets reviewed as a design.
- Draw a control that does not work (a drag handle on a sheet that cannot be dragged).
- Make four recolors of one design and call them four options.
- Write a `DESIGN.md`, a color palette or a test tracker. Those belong to the skills named below.

## Related skills

- `product-polish-workflow`: improve a UI that already ships. It also holds the audit and QA routes.
- `design-system-kit`: carry the winning look into the token system, or write a DESIGN.md. A prototype may read its tokens.
- `color-kit`: the look question is really about color. Take the winning direction there and prove it.
- `ui-ux-kit`: build the winning screen or component for real, with all states and platform behavior.
- `challenge-me`: the question itself is still fuzzy. Settle it before you build anything.
- `write-plan`: the question is answered and the real build needs a plan.
- `verify`: prove a behavior by running it once the real code exists.
- `polyglot-copywriter`: clean the copy shown on a screen.
