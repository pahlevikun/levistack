---
name: color-kit
description: "Pick and prove the colors of a product. Choose a color strategy (feeling, harmony, contrast, dose), mix or anchor a palette, build OKLCH ramps and semantic roles, compose light, dark, high contrast, car night and TV modes, tune the result live with knobs, prove every text and control pair with measured contrast, build chart scales, audit the colors that already exist, and bind the theme to a stack (CSS and Tailwind, SwiftUI, Jetpack Compose, Flutter, React Native, Vue). Use when the user asks for a palette, brand colors, a theme, dark mode, color tokens, a contrast fix or a color audit. Not for buttons, layout or motion (ui-ux-kit), the full token file and DESIGN.md (design-system-kit), or logo art."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: product
  category: product-design
  department: product
  related_skills:
    - design-system-kit
    - ui-ux-kit
    - infographic
    - diagram
  tags:
    - color
    - palette
    - theme
    - contrast
    - tokens
    - dark-mode
  capabilities:
    - palette_strategy
    - contrast_proof
    - stack_binding
  languages:
    - en

---

# Color kit

Choose the colors, build them as roles, prove them, and bind them to the stack. This skill owns palette and mode decisions. It does not design buttons, layouts or motion, and it does not assemble the whole design system.

Work through every step in order. Keep a step short when the request is small, and write `Step N: skipped, because ...` instead of skipping silently.

The numbers come from a script, not from guesses. The script is `theme.py` in `design-system-kit` (`specialities/design-system/scripts/theme/`). Open a shell in that folder (`cd` there) and pass absolute paths for the brief and for `--out`, so your files land in the project and not inside the kit. If `design-system-kit` is not installed, follow the manual path in `references/ramps-and-roles.md` with a color library, and report only values you measured.

## Step 0: Frame

Ask only for what is missing, one question at a time, with your recommended answer:

- What is the product, and who uses it? (Picks the domain and the hue zones.)
- Which feeling, in two or three words?
- Which platforms and which modes? (Phone, tablet, desktop, web, TV, car. Light, dark, high contrast.)
- Is a brand color already fixed? Is it pinned or may it snap onto a ramp?
- Which stack gets the result? (Bind only that one.)
- Which region and language? (Color meanings change. See `data/locale-color-notes.csv`.)

## Step 1: Read what exists

Read the project's tokens, theme files and brand assets. Treat a confirmed brand color as fixed. If the product already has colors, audit them first: `python3 scripts/theme/theme.py audit <folder> --out color-audit.md`, then follow `references/audit-existing.md`. A greenfield product has nothing to read. Say so and go on.

## Step 2: Choose the strategy

Write four lines before any value: **feeling, relationship, contrast, dose**. Pick a method (anchor on a brand color, mix from a mood, extract and remix, sample an image). Decide whether the brand color is pinned or snapped. Choose one neutral. Guide: `references/strategy.md`. Words to flags: `data/mood-to-knobs.csv`.

## Step 3: Build the palette

1. Write the brief: copy `templates/color-brief.json` and fill it.
2. For a new palette, show three different directions: `python3 scripts/theme/theme.py explore --from-brief color-brief.json --count 3`. Let the user pick and refine with the knobs.
3. Keep the brief in the project as `design/brief.json` (copy the template there). If `design-system-kit` is in play it adds its own keys to this same file and rebuilds from it, so a pinned brand hue and chroma must be written in the brief, never only on the command line. Carry the chosen option into the build. Each option prints its seed (for example `1-0`). Put that seed in the brief (`"seed": "1-0"`) and keep every other key the same, or save the options with `explore --out recipes.json` and build with `--recipe recipes.json --pick N`. Without this, the build makes a different palette from the one the user picked.
4. Build: `python3 scripts/theme/theme.py build --from-brief color-brief.json --out design/`. For an existing site as inspiration, add `--from-extract extracted.json`.
5. If a brand color is fixed, pass its hue and chroma (`--hue`, `--chroma`). Check where it lands on the ramp.

The build writes `recipe.json`, `tokens.json`, `theme.css`, `platforms.css`, `tailwind-theme.css`, `DESIGN.md`, `report.md` and `preview.html`, and exits non-zero if a contrast or platform check fails. Never edit a failing color by hand and skip the re-run.

**Tune it live.** Add `--live` to also write `live.html`. It has knobs for color amount, neutral temperature and mode. Every position passed the contrast gate or says why not. Keep the choice by copying its two brief keys. Guide: `references/live-tuning.md`.

## Step 4: Roles and modes

Check the roles against `data/roles.csv`. Every role except `scrim` and the chart colors has a token in light and in dark (chart colors are CSS variables in `theme.css`, and the scrim is written by hand). The build emits two sets, light and dark. **Dimmed, high contrast, car night and TV are manual**: derive them from the dark set on purpose, make the app start in dark on TV and car, and measure them yourself. `--platform tv` or `car` only changes the default ground, the sizes and the contrast floor. Choose one switching mechanism. Guide: `references/ramps-and-roles.md` and `references/modes.md`.

## Step 5: Prove it

Run the pair file once. Every row names its own mode, so one run measures light and dark. The second line is only for a pair file whose rows give no mode:

```bash
python3 scripts/theme/theme.py contrast --pairs <this skill>/data/essential-pairs.csv --tokens design/tokens.json --mode light
python3 scripts/theme/theme.py contrast --pairs <this skill>/data/essential-pairs.csv --tokens design/tokens.json --mode dark
```

The pairs file lists the mode of each row, and `--mode` is the default for rows that give none. Add a row for every pair the product really draws. Measure composed alpha and gradient stops. Check success against danger and the chart colors for color blindness. Fix a failing pair by changing lightness only, and remeasure. Write `templates/contrast-report.md`. Guide: `references/contrast-proof.md`.

Charts need their own scales: `theme.py scale categorical|sequential|diverging`. Guide: `references/data-viz-color.md`. For a hover, tint or gradient color use `theme.py mix` (`references/mixing-and-gradients.md`). For a plain word for a color use `theme.py name` (`references/naming-colors.md`).

## Step 6: Bind to the stack

`python3 scripts/theme/theme.py bind --tokens design/tokens.json --stack <flutter|compose|swiftui|react-native|vue> --out <folder>`. Plain CSS and Tailwind come from the build. Guide and rules per stack: `references/stack-bindings.md`.

## Step 7: Hand off

Give the user: the files and where they live, how to load them, the switching mechanism, the recipe and seed with the rebuild command, what was not measured, and what `ui-ux-kit` needs next (the role names, the focus ring role and the status roles). If the user wants the whole system, hand the build output to `design-system-kit`. Then run `references/finish-checklist.md`.

## Rules

1. **Roles, not swatches.** Components use roles. Themes override roles.
2. **Measure, never guess.** Report only measured ratios. List the rest as Not verified.
3. **Chroma and lightness before hue.** Feeling comes from them first.
4. **One neutral, one accent, status only where shown.**
5. **One color, one meaning.** One filled action per view.
6. **Dark is composed, not inverted.** Measure it separately.
7. **Never carry meaning by color alone.**
8. **Keep the brand color.** Pin or snap it on purpose. Never darken it quietly.
9. **No raw hex outside the palette and theme files.**
10. **Fix contrast by lightness.** Do not change hue to fix a ratio.

## What is in this folder

| Path | Use |
|---|---|
| `references/strategy.md` | Pick the feeling, the relationship, the method and the neutral |
| `references/ramps-and-roles.md` | OKLCH ramps, roles, names, rules of use, the manual path |
| `references/modes.md` | Light, dark, high contrast, dimmed, car, TV, brand themes, switching |
| `references/contrast-proof.md` | Thresholds, measuring the rendered pair, fixes, color blindness, charts, report |
| `references/stack-bindings.md` | CSS, Tailwind, SwiftUI, Compose, Flutter, React Native, Vue, desktop, car, TV |
| `references/audit-existing.md` | Inventory and merge the colors a product already has |
| `references/live-tuning.md` | The live page: knobs, keeping a choice, trying colors on a running page |
| `references/data-viz-color.md` | Categorical, sequential and diverging chart scales and their checks |
| `references/mixing-and-gradients.md` | Tints, hover and disabled colors, gradients, and which space to mix in |
| `references/naming-colors.md` | Role names for code and plain words for people |
| `references/color-meaning.md` | Conventions, regional meanings and what to avoid |
| `references/print-and-brand-handoff.md` | Print, spot inks and the brand sheet |
| `references/color-science-for-products.md` | How to use the facts base that explains the rules |
| `references/check-tools.md` | Which second tool to use to cross-check each job |
| `references/finish-checklist.md` | Patterns to find and fix before you finish |
| `data/roles.csv` | Every role with its light and dark rule and its contrast need |
| `data/essential-pairs.csv` | The pairs to measure in light and dark |
| `data/mood-to-knobs.csv` | What people say, and the flags that answer it |
| `data/locale-color-notes.csv` | Color meaning cautions by region |
| `data/color-facts.csv` | 50 short facts (perception, spaces, mixing, print, meaning, charts, access) each with a use and a check |
| `templates/color-brief.json` | The brief the script reads |
| `templates/contrast-report.md` | The proof, written down |
| `templates/role-inventory.md` | The audit of an existing palette |

## Related skills

- `design-system-kit`: owns the builder scripts and assembles tokens, type, space and `DESIGN.md`. It calls this skill at its color step.
- `ui-ux-kit`: builds the components, motion and UX that consume these roles.
- `product-polish-workflow`: audits and changes a shipping product. It calls this skill for any palette or mode work.
- `prototype-wireframe`: grayscale first. Bring color here after the structure is agreed.
- `challenge-me`: stress-test the direction before you build it.
- `verify`: prove the rendered result on the real surface.

## Done when

- The four-line strategy is written and the user agreed to it.
- `tokens.json` exists with every role in light and dark, built from a recorded seed.
- Every pair in the pair file passes in every mode, or each failure has a stated reason.
- The contrast report lists what was measured and what was not.
- The binding for the named stack exists, or none was asked for.
- No raw hex sits outside the palette and theme files.
