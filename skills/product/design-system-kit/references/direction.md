# Step 2: Set the direction and build the tokens

This is where the design system is decided, **before any critique**. You choose the non-color ingredients here, call `color-kit` for every color decision, show a few options, let the user pick, then build contrast-checked tokens and a `DESIGN.md` in one pass.

**Split of work.** This skill owns shape, type voice, motion profile, signature move, density and platform. `color-kit` owns the feeling, the palette, the roles, the modes and the contrast proof. Both write into one `design/brief.json` (see `color-craft.md`) and one `theme.py build`.

The goal is a result that fits this product, not the most common answer. Two briefs for the same kind of app should not come out the same.

## Contents
- Intake
- Three ways in
- Explore, pick, refine
- Words to knobs
- Build
- Making it unique
- What to hand the user

## Intake

Ask only what the as-found sheet and the brief do not already say. One question at a time, with your recommended answer.

| Ask | Why it matters |
|---|---|
| What is it, and who uses it? | Picks the domain and the hue zones |
| Which feeling should it give? Name 2 or 3 words | Picks the moods. `color-kit` asks this too, so ask once and share the answer |
| Which platforms? Which one matters most? | Sets the lead platform (see `platforms.md`) |
| Light, dark or both? Any brand color already fixed? | Sets ground and anchors the hue |
| Which region and language? | Raises color and layout cautions (see `ingredient-library.md`) |
| Any color, font or look to avoid? | Becomes a forbid or an override |

If the user gives a single sentence ("a calming meditation app for iOS and TV"), infer what you can, say your assumptions, and go on.

## Three ways in

| Situation | Start from |
|---|---|
| **Greenfield** | The brief. Mix everything from the library. |
| **Existing system, keep it** | The as-found values as the tokens. Build ramps and checks around them, fix gaps, write `DESIGN.md` from what is true. Do not re-mix. |
| **Existing site or product to learn from** | `extracted.json` as a seed: `theme.py build --from-extract work/extracted.json`. It keeps the hue, chroma, neutral and rough shape, voice and motion, and mixes the rest so the result is a remix, not a copy. |

## Explore, pick, refine

1. **Explore.** Make three different directions, not three recolors:

   ```bash
   python3 scripts/theme/theme.py explore --brief "<brief>" --platform <lead[,others]> --count 3 --out work/directions.json
   ```

   Each direction differs in harmony, shape, type voice, motion and signature move. Show them as a short table with the swatches and one line on why each fits.
2. **Pick.** Ask which one the user wants, with your recommendation. Ask what to keep and what to change.
3. **Refine** with knobs (below). Re-run `explore` with the same seed to keep the base, or change `--seed` for a fresh set.
4. **Lock.** When the user says yes, build.

## Words to knobs

Turn what people say into flags.

| The user says | Do this |
|---|---|
| Calmer, softer, quieter | `--mood calm` or `gentle`, lower `--chroma`, `--ground soft` |
| More premium, less cheap | `--mood premium`, `--chroma low`, one accent, fewer colors, `--signature one-loud-accent` |
| Warmer / cooler | `--temp 0.5` / `--temp -0.5` (hue and chroma move together) |
| More energy, punchier | `--mood energetic`, `--chroma high`, `--harmony complement` |
| Friendlier, rounder | `--shape pebble` or `soft`, `--voice friendly-humanist` |
| More serious, formal | `--shape sharp` or `crisp`, `--voice classic-serif`, `--motion still` |
| More modern | `--voice geometric-modern`, `--shape pill` or `crisp` |
| Darker | `--ground dark` |
| Looks too generic | Change the **neutral**, the **signature** and the **type voice** first, then the hue |
| Keep my brand color | `--hue <degrees>` from the brand color (read it with the extractor or the OKLCH of the hex) |
| Different accent | `--accent-hue <degrees>` or `--harmony <id>` |
| Fewer / more dense | `--density airy|balanced|dense` |

List all ids with `python3 scripts/theme/theme.py list <domains|moods|harmonies|shapes|voices|motion|signatures|neutrals|platforms>`.

## Build

```bash
python3 scripts/theme/theme.py build --brief "<brief>" --seed <seed> --platform <lead[,others]> --out design/
```

It writes: `recipe.json` (every choice and why), `tokens.json`, `theme.css`, `platforms.css`, `tailwind-theme.css`, `DESIGN.md`, `report.md` and `preview.html`. It exits with an error if any contrast or platform check fails. Fix the cause (usually a brand hue that needs a different step) and run it again. Never edit a failing color by hand without re-running the checks.

Then run `python3 scripts/theme/theme.py check design/DESIGN.md`, and the official linter if the network allows: `npx @google/design.md lint design/DESIGN.md`.

Open `preview.html` (or render it to PNG with the browser) and look at it in light and dark before you show the user.

If the project is native (SwiftUI, Compose, Flutter), port `tokens.json` into the platform's theme files by hand or with the project's own tool. Keep the names the same.

## Making it unique

The library has many ingredients on purpose. These habits keep results distinct:

1. **Never start from the default.** Indigo + Inter + rounded cards + a purple gradient is the template look. If the draft lands there, change the neutral, the type voice and the signature before the hue.
2. **Choose one signature move** and repeat it (tinted shadows, hairline rules, oversized numerals, one loud accent). A system with one clear device is remembered. A system with five is noise.
3. **Constrain, then vary.** Use few hues in a narrow band of lightness and chroma, and get variety from the neutral, the type and the shape.
4. **Use hue similarity for calm and hue contrast for pop.** Similar hues feel harmonious together. A foreground color pops most against a background of a different hue.
5. **Let the second domain lend an accent.** A food app with a wellness side can take its accent from the wellness zone.
6. **Keep luxury quiet and discount loud.** Low chroma, warm neutrals and one accent read as high price. Many saturated primaries read as low price. Match the positioning on purpose.
7. **Seed on purpose.** The same brief and seed always gives the same result. Change the seed to explore, and write the chosen seed down.
8. **Check against a cliché list** for the domain (see the `avoid` lines in the library). Fixing one cliché is enough to make a result stand out.

## What to hand the user

- The three directions and which one was chosen, in a few lines.
- `design/` with the files above, and a line on how to load `theme.css`.
- The assumptions you made and the checks that passed.
