---
name: design-system-kit
description: "Build a design system step by step, then critique with it. Discover what exists (code, a live website, Stitch, screenshots), set the direction from a wide reference library, assemble tokens for type, space, shape, elevation and platform sizes, write DESIGN.md, critique the real screens against the new system, record component specs, set up the library and governance, validate and hand off. It calls color-kit for every color decision and ui-ux-kit for components, motion and UX. Fits mobile, desktop, web, TV and car. Use when the user wants a design system, token file, DESIGN.md or governance, to extract a site's design, or brand slides. Not for choosing a palette (color-kit), building one screen (ui-ux-kit) or brand identity."
when_to_use: "Use when the user asks for a design system, a token file or DESIGN.md, to audit or govern a component library, to extract the design of a website, to review a UI against a system, or to make slides that follow a brand. Also use it when the user mentions Stitch, CSS variables, spacing or type scales. For only a palette or dark mode, use color-kit. For one screen or component, use ui-ux-kit."
metadata:
  version: 3.0.0
  author: levistack
  license: MIT
  group: product
  category: product-design
  department: product
  related_skills:
    - color-kit
    - ui-ux-kit
    - prototype-wireframe
  invokes:
    - skill: color-kit
      when: Any color, mode, or contrast decision
    - skill: ui-ux-kit
      when: Components, motion, or platform UX decisions
  tags:
    - design-system
    - tokens
    - DESIGN.md
    - governance
  capabilities:
    - design_system_pipeline
    - token_assembly
    - critique_against_system
  languages:
    - en

---

# Design system kit

A pipeline, not a menu. Every request goes through the same steps in the same order: **find what exists, decide the system, then critique with it**. The system comes first, so every critique is a check against a rule instead of a matter of taste.

This skill owns the system: token layers, type, space, radius, elevation, platform sizes, `DESIGN.md`, governance and the critique against the system. It **calls two other skills** instead of doing their work:

- `color-kit` for every color decision: strategy, palette, roles, modes, contrast proof and stack binding.
- `ui-ux-kit` for every component, state, motion and UX decision, on every platform.

`product-polish-workflow` audits a shipped product and `prototype-wireframe` answers one open question with a throwaway. Neither is a step here.

Run all steps. A step can be short (a line or two for a small request), but never skip one silently. If a step does not apply, write `Step N: skipped, because ...` and move on.

Paths are relative to this folder. Run scripts from `specialities/design-system/`.

## The pipeline

| Step | Name | Output | Guide |
|---|---|---|---|
| 0 | Frame | One paragraph: product, users, platforms, region, what exists | below |
| 1 | Discover | The as-found sheet | [discover](references/discover.md) |
| 2 | Direction and tokens | `design/` with tokens, CSS, `DESIGN.md`, report, preview. **Calls `color-kit`** | [direction](references/direction.md), [color](references/color-craft.md) |
| 3 | Critique | Findings against the system, with exact fixes | [critique](references/critique.md) |
| 4 | Components and motion | Component records in system format. **Calls `ui-ux-kit`** | [components](references/components.md), [motion](references/motion.md) |
| 5 | Library and governance | Structure, docs, tests and the change process | [library and governance](specialities/design-system/references/library-and-governance.md) |
| 6 | Validate | Every check run, with results, and the preview looked at | [validate and handoff](references/validate-and-handoff.md) |
| 7 | Hand off | Files, adoption plan, rebuild command | [validate and handoff](references/validate-and-handoff.md) |

Steps 2 and 3 are the heart of it. Do not critique before Step 2 has produced a system. If the user only asked for a critique, still do Steps 0 to 2 first (the system can be the as-found one, read from their code), and keep them short.

### Step 0: Frame

Say in a few lines, and ask only for what is missing, one question at a time with your recommended answer:

- What the product is and who uses it.
- **Platforms**: mobile, desktop, web, TV, car. Which one leads. Read [platforms](references/platforms.md).
- Region and language (it changes color cautions and layout direction).
- What exists: a repo, a live site, a Stitch project, screenshots, or nothing.
- What the user wants at the end: a system, a critique, a theme, a `DESIGN.md`, slides, or all of it.

### Step 1: Discover

Read what exists. Use every source that applies: code, a website (static extractor and in-browser extractor), a Stitch project, screenshots. Write the **as-found sheet**. Greenfield means "nothing found", and that is a valid result. See [discover](references/discover.md).

### Step 2: Direction and tokens

1. Choose the non-color ingredients with the user: shape, type voice, motion profile, signature move, density and platform. Use the [ingredient library](references/ingredient-library.md).
2. **Load `color-kit` and run it** for the color decisions. It frames the feeling, picks the strategy, builds the palette with this kit's builder, composes the modes, proves the contrast and binds the stack. Share one `design/brief.json` (see [color](references/color-craft.md)). Do not state color rules here and do not invent hex values.
3. Build everything in one pass: `python3 scripts/theme/theme.py build --from-brief design/brief.json --out design/`. It writes light and dark tokens, per-platform overrides, a `DESIGN.md`, a report and a preview, and exits non-zero on a failed check.
4. If a system already exists and should stay, build from the as-found values instead of re-mixing. If a site is the inspiration, remix from the extraction. Never copy a brand's signature look.

Details: [direction](references/direction.md), [color](references/color-craft.md), [motion](references/motion.md), [DESIGN.md format](references/design-md-format.md).

### Step 3: Critique

Judge the real screens against the system from Step 2, top-down: purpose and hierarchy, spacing, type, color, shape, states, content, motion, accessibility, and fit for each platform. Every finding names the element and the exact token or value to change. Include what to change in the system itself. See [critique](references/critique.md) and `specialities/ui-critique/GUIDE.md`.

### Step 4: Components and motion

**Load `ui-ux-kit`** for each screen or component the system must serve. It specifies states, geometry, motion, UX and platform behavior (including the car and the TV). Record each component here in the system format: variants, sizes, states supported, component tokens that alias semantic tokens, platform mapping and status. See [components](references/components.md), [motion](references/motion.md) and the token specs in `specialities/design-system/references/` (`token-architecture`, `component-specs`, `states-and-variants`, `tailwind-integration`).

### Step 5: Library and governance

Decide how the system lives: where tokens are the source of truth, how components are built and documented, how changes are tested (visual regression, accessibility linting) and who approves them. See [library and governance](specialities/design-system/references/library-and-governance.md). Brand slides use the slide tooling in `specialities/design-system/` (strategies, layouts, color logic, token validator).

### Step 6: Validate

Run every check from [validate and handoff](references/validate-and-handoff.md) and name each with its result. Look at the preview in light and dark at the lead platform's size. A failure sends you back to the step that owns it.

### Step 7: Hand off

List the files, how to load them, the first three adoption tasks, the governance note, the assumptions and the rebuild command with the seed. Do not commit.

## Rules that hold in every step

1. **System first, critique second.** No judgment of a screen without a system to judge it by.
2. **Use the system that exists.** Read the project's tokens, theme and components before proposing values. Keep what works.
3. **Every value comes from a scale.** Spacing, type, color, radius and motion come from named tokens, not typed ad hoc.
4. **Accessibility is built in by the owners.** Contrast comes from `color-kit` and is checked by the builder in both modes. Targets, states and gestures come from `ui-ux-kit`. This skill records the result and runs the gates.
5. **Each platform is its own input and distance.** Tokens are shared. Sizes, focus, motion and layout are set per platform.
6. **Be specific and distinct.** Mix ingredients to fit the brief. Do not start from indigo, Inter and a purple gradient. Pick one signature move.
7. **Give exact fixes.** Name the element and the value, ordered by impact.
8. **Learn from sites, do not clone them.** Take mechanics, not a brand's identity.
9. **Report what you ran.** Every script and check is named with its result.
10. **One owner per decision.** Color goes to `color-kit`. Components, motion and UX go to `ui-ux-kit`. This skill records their output and does not restate their rules. Never invent a hex or a motion time here.

## What is in this folder

| Path | What it holds |
|---|---|
| `references/` | The step guides above, plus [platforms](references/platforms.md) and the [ingredient library](references/ingredient-library.md). The color and motion guides here only say how to call `color-kit` and `ui-ux-kit` |
| `specialities/design-system/` | The scripts, data, templates and token references. `scripts/theme/` has the mixer, builder, extractor and DESIGN.md writer. `data/theme/` has the ingredient library. `scripts/` also has the token generators and the slide tools |
| `specialities/design-system/references/` | Token architecture, component specs, states, Tailwind, library and governance, the Stitch DESIGN.md guide |
| `specialities/ui-critique/` | The core critique method used in Step 3 |

Bundled helpers, from `specialities/design-system/`:

| Script | Use |
|---|---|
| `scripts/theme/theme.py` | `list`, `explore`, `build`, `check`, `contrast`, `audit`, `bind`. The command line for the steps. `--from-brief` reads a JSON brief |
| `scripts/theme/check_pairs.py` | The one contrast gate: measures pairs, composites alpha, reads role names from `tokens.json` |
| `scripts/theme/audit_colors.py` | Inventories color literals in a project and groups near duplicates |
| `scripts/theme/bind.py` | Writes the stack's color file: Flutter, Compose, SwiftUI, React Native, Vue |
| `scripts/theme/scales.py` | Chart scales (categorical, sequential, diverging) with color-blind checks: `theme.py scale` |
| `scripts/theme/mixing.py` | Blends two colors in sRGB, linear, OKLab and OKLCH: `theme.py mix` |
| `scripts/theme/names.py` | Names a color with the nearest plain word: `theme.py name` |
| `data/theme/names.json` | Our own list of about 100 plain color names (OKLCH values) that `names.py` reads |
| `scripts/theme/mixer.py` | Seeded mixer: brief, domains, moods and platform to one recipe |
| `scripts/theme/build.py` | Recipe to ramps, light and dark roles, per-platform sizes, and every contrast check |
| `scripts/theme/emit.py` | Writes `tokens.json`, `theme.css`, `platforms.css`, `tailwind-theme.css`, `DESIGN.md`, `report.md`, `preview.html` |
| `scripts/theme/oklch.py` | Color math: OKLCH, gamut fit, WCAG and APCA contrast, color-blindness simulation |
| `scripts/theme/extract_site.py` | Read a website's design into JSON and an as-found `DESIGN.md` |
| `scripts/theme/extract-in-browser.js` | Read computed styles from a page that builds its CSS in the browser |
| `scripts/generate-tokens.cjs` | CSS or Tailwind from a token JSON file |
| `scripts/validate-tokens.cjs` | Find hard-coded values in code |
| `scripts/embed-tokens.cjs` | Embed tokens into CSS |
| `scripts/generate-slide.py`, `search-slides.py`, `slide_search_core.py`, `html-token-validator.py` | Brand slides |
| `scripts/tests/test_theme.py`, `scripts/tests/test_validate_tokens.py` | Tests for the theme tools and the token validator |
| `templates/stitch-example-DESIGN.md` | A sample `DESIGN.md` written from a Stitch project |

## Related skills

- `color-kit`: required at Step 2. Owns palette, roles, modes, contrast proof and stack binding.
- `ui-ux-kit`: required at Step 4. Owns components, states, motion and UX on every platform.
- `challenge-me`: stress-test the direction before you build it.
- `prototype-wireframe`: sketch or prototype a screen before specifying it.
- `product-polish-workflow`: audit and change a shipped product and run its journey QA. It calls this skill for the system.
- `write-plan`: turn the adoption plan into tasks.
- `verify`: prove accessibility or visual claims by running them.
- `polyglot-copywriter`: clean the prose in `DESIGN.md` and the report.
- `handoff`: pause the work and keep the state.

## Done when

- Every step ran, or has a one-line reason for being skipped.
- A system exists (built, or read from the code) before any critique was written.
- `color-kit` ran for the color decisions and `ui-ux-kit` ran for the components, or each has a reason it was skipped.
- The tokens, `DESIGN.md` and report exist, and all contrast and platform checks pass.
- Findings name the element and the exact token or value to change.
- Every script that ran is named with its result, and the preview was looked at.
