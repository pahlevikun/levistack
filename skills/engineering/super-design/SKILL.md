---
name: super-design
description: "Use for UI and design-system work: critique a screen or component, set up design tokens and a component library, write component specs, document accessibility and governance, generate brand-compliant slides, or synthesize a Stitch project into DESIGN.md. One skill with four specialities. It detects the job and loads only the guide it needs."
when_to_use: "Use when the user says a screen 'feels off', asks to review a UI, set up or audit design tokens, build or govern a component library, write a DESIGN.md, or make slides that follow a brand; or mentions Stitch, CSS variables, spacing or type scales, theming or WCAG contrast."
metadata:
  version: "1.0.0"
---

# Super Design

One skill, four specialities. Call it once. It picks the speciality from the job and loads only that guide.

The guides are kept whole. Each is a full, separate skill that was merged in.

## Step 0: detect the job

Do this first and do not announce it.

| If the user is doing this | Speciality | Load |
|---|---|---|
| A screen or component "feels off", review a UI, fix hierarchy, spacing, type or states | ui-critique | [ui-critique](specialities/ui-critique/GUIDE.md) |
| Token files: primitive, semantic and component tokens, CSS variables, Tailwind integration, component specs, validating tokens, brand slides | design-system | [design-system](specialities/design-system/GUIDE.md) |
| Building or governing a component library: foundations, component architecture, accessibility, documentation, theming, process and governance | design-systems | [design-systems](specialities/design-systems/GUIDE.md) |
| A Stitch project, or writing a `DESIGN.md` from one | design-md | [design-md](specialities/design-md/GUIDE.md) |
| Setting up a design system end to end | design-systems for the process, then design-system for the token files | both, in order |

`design-system` (singular) is the tokens, specs and slide tooling, with scripts. `design-systems` (plural) is the library and governance guidance, with no scripts. When a request fits both, start with `design-systems` for decisions and use `design-system` to produce files.

Not for: designing a new screen from nothing, brand identity, or illustration. Say so and ask what the user wants.

`design-md` needs the Stitch MCP tools. If they are not connected, say so instead of guessing at a project's contents.

## Pipeline: critique, then systematize

1. **Critique** the screen with [ui-critique](specialities/ui-critique/GUIDE.md). Fix hierarchy before polish.
2. **Name the system** the fixes imply: the spacing scale, type scale and colors in use. [design-systems](specialities/design-systems/GUIDE.md) for the rules.
3. **Write it down** as tokens with [design-system](specialities/design-system/GUIDE.md), and run its validation scripts from `specialities/design-system/scripts/`.

## Rules that hold across all guides

1. **Use the system that exists.** Read the project's tokens, theme and components before proposing new values.
2. **Every value comes from a scale.** Spacing, type and color are chosen from a named scale, not typed ad hoc.
3. **Accessibility is not a polish step.** Contrast (4.5:1 for body text) and touch targets (44pt) are checked in every critique and every component spec.
4. **Give exact fixes.** Name the element and the value to change, ordered by impact.

## Bundled helpers (design-system)

Run from `specialities/design-system/`. Token scripts: `embed-tokens.cjs` embeds tokens into CSS. Slide scripts: `generate-slide.py` builds a slide, `slide_search_core.py` is the search engine behind `search-slides.py`, and `html-token-validator.py` checks generated HTML for hard-coded values. `scripts/tests/test_validate_tokens.py` tests the token validator.

## Done when

- The guide matching the job was opened, plus a second only when the job needs it.
- Proposals use values from the project's own scales or name the scale they add.
- Any script that was run is named with its result.
