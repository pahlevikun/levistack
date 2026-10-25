# Step 1: Discover what exists

Find out what the product already looks like before you decide anything. The result is an **as-found sheet**: the colors, fonts, sizes, radii, shadows, spacing and motion that are really in use, with where each came from.

Do every source that applies. If none applies, write "greenfield, nothing to find" and go on.

## Contents
- Source A: code in the repo
- Source B: a live website
- Source C: a Stitch project
- Source D: screenshots or a design file
- The as-found sheet

## Source A: code in the repo

1. Look for token and theme files: `tokens.json`, `design-tokens.*`, `theme.*`, `tailwind.config.*`, CSS files with `:root { --... }`, SwiftUI `Color` assets, Android `colors.xml` and `themes.xml`, Flutter `ThemeData`.
2. Look for the components that use them: `Button`, `Input`, `Card`, the navigation.
3. Count hard-coded values: `node specialities/design-system/scripts/validate-tokens.cjs --dir src/`. A high count means the system exists in spirit only.
4. Note the stack (React, Vue, SwiftUI, Compose, Flutter, plain CSS). The output formats in Step 4 must fit it.

## Source B: a live website

Use this when the user gives a URL to learn from, or to document their own site. It works like a design extractor.

```bash
# 1. Static read of the HTML and CSS (no JavaScript is run)
python3 scripts/theme/extract_site.py https://example.com --out work/extracted.json --design-md work/as-found-DESIGN.md
```

- `extracted.json` holds clustered colors (with how each is used: text, background, border), fonts, sizes, weights, radii, shadows, spacing, durations, easings, CSS variables, and a `suggest` block (hue, chroma, neutral, shape, voice, motion, density, ground) that Step 2 can use.
- `as-found-DESIGN.md` is a faithful record with the exact values. It is **not** a target.

If the report says very few colors were found, the styles are built in the browser. Then:

1. Open the page in a browser (use the browser tool if one is connected).
2. Run `scripts/theme/extract-in-browser.js` on the page. It reads computed styles of what is on screen and prints one JSON string.
3. Save that JSON and run: `python3 scripts/theme/extract_site.py --browser-json browser.json --out work/extracted.json`.

Repeat in dark mode and at a phone width if the site changes. Take screenshots too, because numbers do not show composition.

Rules for extracting from someone else's site:

- Learn mechanics (a scale, a hierarchy, a spacing rhythm). Do not clone a brand's signature look, logo, copy or imagery.
- Only fetch pages the user is allowed to look at. The script reads public HTML and CSS and sends nothing anywhere.
- If the site is the user's competitor, say so in the as-found sheet and plan to remix, not copy.

## Source C: a Stitch project

If the Stitch MCP tools are connected, follow `stitch-design-md.md` to retrieve screens and write the semantic description. If they are not connected, say so. Do not guess a project's contents.

## Source D: screenshots or a design file

Read colors from the image with a picker, or ask the user for the file's styles. Mark every value "approximate, from a screenshot". Ask for the real tokens when they exist.

## The as-found sheet

Write this short sheet, from all sources:

```
Sources:      <repo path | URL | Stitch project | screenshots | none>
Platforms:    <what the product runs on today>
Colors:       <brand, neutrals, status, with counts or token names>
Type:         <families, sizes seen, weights>
Shape/depth:  <radii, shadows, borders>
Spacing:      <base unit and the steps in use>
Motion:       <durations, easings, anything animated>
Components:   <the ones that exist and how consistent they are>
Gaps:         <missing tokens, hard-coded values, dark mode, platforms not covered>
```

Do not judge yet. Step 2 builds the system, and Step 3 judges the screens against it.
