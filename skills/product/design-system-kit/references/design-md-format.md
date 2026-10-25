# DESIGN.md

`DESIGN.md` describes a visual identity for people **and** for coding agents. It has two layers: machine-readable tokens in YAML at the top, and prose that explains the why. The tokens are the rule. The prose says how to apply them.

The format is an open alpha spec, so check the current spec before you rely on a detail: the `google-labs-code/design.md` repository, or `npx @google/design.md spec`.

## Contents
- Shape of the file
- Front matter
- Value types and references
- The sections, in order
- Components
- Rules the linter applies
- How we write ours
- The three DESIGN.md files you may make

## Shape of the file

````markdown
---
version: alpha
name: <name>
description: <one sentence>
colors: { ... }
typography: { ... }
rounded: { ... }
spacing: { ... }
---

## Overview
...
## Colors
...
````

Components may be in the front matter, or in a fenced `yaml` block inside the Components section. Each top-level key may appear **once** in the whole file.

## Front matter

| Key | Holds |
|---|---|
| `version` | `alpha` |
| `name` | The system name |
| `description` | One sentence |
| `colors` | Named colors |
| `typography` | Named text styles |
| `rounded` | Radius scale |
| `spacing` | Spacing scale |
| `components` | Component tokens, with references |
| `omitted` | Sections you leave out on purpose |

Recommended color names: `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`. Other names are accepted. Typography names like `body-md` and `label-sm` are recommended. Most systems have 9 to 15 text levels.

## Value types and references

- **Color**: any valid CSS color. `#RRGGBB` is recommended. The linter converts to sRGB to check contrast.
- **Dimension**: a number with `px`, `em` or `rem`.
- **Typography**: `fontFamily`, `fontSize`, `fontWeight`, `lineHeight` (a bare number is a multiple of the font size), `letterSpacing`, `fontFeature`, `fontVariation`.
- **Reference**: `"{colors.primary}"`. Outside `components`, a reference must point to a plain value. Inside `components` it may also point to a whole style such as `"{typography.label-md}"`.

## The sections, in order

All use `##`. You may leave sections out, but the ones you keep must follow this order. An unknown section (for example Motion) is kept and does no harm.

1. Overview (also "Brand & Style")
2. Colors
3. Typography
4. Layout (also "Layout & Spacing")
5. Elevation & Depth
6. Shapes
7. Components
8. Do's and Don'ts

Duplicate headings are an error.

## Components

Each component maps property names to values or references. The properties are `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`. A variant such as hover or pressed is its own sibling key with a shared prefix (`button-primary`, `button-primary-hover`).

## Rules the linter applies

| Finding | Level |
|---|---|
| Broken reference | Error |
| Duplicate section or top-level key | Error |
| Contrast below 4.5:1 for a component's text on its background | Warning |
| Sections out of order | Warning |
| A missing section that is not in `omitted` | Warning |
| An unknown component property | Warning |

Run it: `npx @google/design.md lint DESIGN.md`. Compare two versions: `diff`. Export tokens: `export --format css-tailwind|json-tailwind|dtcg`.

Our own quick check, which needs no network: `python3 scripts/theme/theme.py check DESIGN.md`.

## How we write ours

- Light-mode names are plain (`primary`, `surface`). Dark-mode counterparts add a `-dark` suffix (`primary-dark`). The spec has no mode concept, so suffixes keep every value a plain color.
- Names describe **roles**, and the prose names the **look** ("Deep muted teal, `#2F6F73`").
- Every color has a reason in the prose: what it is for and what it is not for.
- The prose has a Motion section after Components, and a **Platform** paragraph in Layout for each platform.
- Do's and Don'ts hold the domain's "avoid" notes, so the next person does not repeat a known mistake.
- Never put raw hex in components. Use references.

## The three DESIGN.md files you may make

| File | Made by | Use |
|---|---|---|
| `design/DESIGN.md` | `theme.py build` | The **target** system, with checked contrast and platform rules |
| `work/as-found-DESIGN.md` | `extract_site.py --design-md` | A faithful record of an existing site, with its exact values. Not a target |
| A Stitch-derived file | the Stitch guide | A semantic description of a Stitch project's screens |

When there is an existing system to keep, the as-found file becomes the base of the target, and you fix its gaps. When there is not, the built file is the target.
