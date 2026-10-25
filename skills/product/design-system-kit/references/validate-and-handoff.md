# Steps 6 and 7: Validate, then hand off

Nothing is done until it has been checked by a tool and looked at by eyes. Then the user gets files they can use and a plan for adopting them.

## Contents
- Step 6: validate
- Step 7: hand off
- The final report

## Step 6: validate

Run every check that applies. Name each one in the report with its result.

| Check | How | Pass rule |
|---|---|---|
| Token build | `python3 scripts/theme/theme.py build ...` exits 0 | No contrast or platform failures |
| DESIGN.md structure | `python3 scripts/theme/theme.py check design/DESIGN.md` | 0 errors |
| Official lint (if online) | `npx @google/design.md lint design/DESIGN.md` | 0 errors, review warnings |
| Hard-coded values in code | `node scripts/validate-tokens.cjs --dir src/` | Count goes down, and no new ones |
| Generated slide HTML (if slides) | `python3 scripts/html-token-validator.py <file>` | No raw values |
| CSS builds from tokens | `node scripts/generate-tokens.cjs --config design/tokens.json -o out.css` | Output matches `theme.css` roles |
| Visual check | Open `design/preview.html` in light and dark, at the platform's width | Nothing clipped, overlapping or unreadable |
| Contrast spot check | Read `design/report.md`, then run `python3 scripts/theme/theme.py contrast --pairs <color-kit>/data/essential-pairs.csv --tokens design/tokens.json` for light and for dark, adding a row for every pair the product draws | All rows pass |
| Color literals in code | `python3 scripts/theme/theme.py audit <src folder> --out color-audit.md` | Literals outside token files go down, with no new ones |
| Acceptance rows | `node <ui-ux-kit>/scripts/check-acceptance.mjs ux-acceptance.csv` when `ui-ux-kit` wrote rows | File is valid and every row has an anchor |
| Platform check | `report.md`, Platform checks | All rows pass. Do the manual checks in `platforms.md` |
| Motion check | Reduced motion on, then off | Meaning survives both |

Look at pictures, not only numbers. If a browser tool is available, render `preview.html` at the lead platform size (for example 1920 x 1080 for TV, 390 x 844 for mobile) and ask a precise question per image: "Is any text clipped or overlapping? Is the focus state clear? Does the primary button stand out from the rest?"

If something fails, go back to the step that owns it: a contrast problem is Step 2, a screen problem is Step 3, a component gap is Step 4.

## Step 7: hand off

1. **Files.** List what was made and where. Suggested layout in the user's repo:

   ```
   design/
     DESIGN.md           the system, for people and agents
     tokens.json         source of truth (W3C style)
     theme.css           CSS variables, light and dark
     platforms.css       overrides per platform
     tailwind-theme.css  if the project uses Tailwind v4
     recipe.json         every choice and why (rebuild from this)
     report.md           checks
     preview.html        a visual check
   ```
2. **How to load it.** Two lines of code for the stack in use (an import, a `data-theme` or `data-platform` attribute).
3. **Adoption plan.** Order of work: tokens first, then primitives (button, input, text), then the screens with the worst hard-coded counts from Step 3. Name the first three tasks.
4. **Governance.** Who changes tokens, how a new color is added (rebuild from the recipe, do not hand-edit), how a new component is proposed. See `specialities/design-system/references/library-and-governance.md`.
5. **Open questions and assumptions.**
6. **Rebuild command**, with the seed, so the result can be reproduced:

   ```bash
   python3 scripts/theme/theme.py build --brief "<brief>" --seed <seed> --platform <list> --out design/
   ```

Do not commit or push. Hand the files to `atomic-semantic-commit` when the user asks.

## The final report

Keep it short:

```
Direction:    <name>, <moods>, <domain>. Seed <seed>.
Platforms:    <lead> + <others>
Made:         design/ (list)
Checks:       contrast 0 failing of N | platform 0 of M | DESIGN.md lint 0 errors | preview looked at (light, dark)
Critique:     <count> findings (B blockers, M major, m minor), top three fixes
Not done:     <what was skipped and why>
Next:         <the first three tasks>
```
