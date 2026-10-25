# Color in the design system

Color decisions are owned by the `color-kit` skill. This guide says how the design system uses it. It does not repeat the ramp, role, mode or contrast rules. Those live in `color-kit`, so there is one place to fix them.

## Required call

At Step 2, load `color-kit` and run its steps for this product:

1. Frame the feeling, the platforms, the modes and the brand constraints.
2. Choose the color strategy (feeling, relationship, contrast, dose).
3. Build the palette with this kit's builder.
4. Check roles and modes.
5. Prove the contrast.
6. Bind to the stack that was asked for.

Then take its output into the system. Do not invent hex values here. Do not hand-edit a failing color.

## How the two skills share one build

One brief file feeds one build. Keep it as `design/brief.json`.

| Keys | Owner |
|---|---|
| `brief`, `seed`, `domain`, `mood`, `hue`, `accent_hue`, `chroma`, `temp`, `ground`, `harmony`, `neutral`, `color_amount`, `neutral_temp` | `color-kit` |
| `shape`, `voice`, `motion`, `signature`, `density`, `platform` | this kit (see the direction guide) |

```bash
python3 scripts/theme/theme.py build --from-brief design/brief.json --out design/
```

`color-kit` writes its keys (including a pinned brand `hue` and `chroma`) into `design/brief.json`. The kit adds its keys to that same file and rebuilds from it. Never rebuild from a brief that lacks the brand hue, or the proven palette is lost. Keep the seed the same. The seed makes the result reproducible.

## What the kit does with the result

| Output | Use in the system |
|---|---|
| `tokens.json` | The source of truth for color, space, type, radius, shadow and motion |
| `theme.css`, `platforms.css`, `tailwind-theme.css` | The CSS and Tailwind bindings |
| `DESIGN.md` | The prose and the front matter for agents and people |
| `report.md` | The contrast and platform checks |
| `preview.html` | A visual check |
| The `bind` output | Flutter, Compose, SwiftUI, React Native or Vue files, made by `theme.py bind` |

## Commands the color skill uses from this folder

| Command | Use |
|---|---|
| `theme.py explore` | Three different directions |
| `theme.py build` | Tokens, CSS, `DESIGN.md`, report, preview. Exits non-zero on a failed check |
| `theme.py contrast --pairs ... --tokens ...` | Measure any list of pairs, with alpha composited |
| `theme.py audit <folder>` | Inventory the colors a project already has |
| `theme.py bind --stack ...` | Write the stack's theme file |
| `theme.py build --live` | Also write `live.html`, a page with knobs for color amount, neutral temperature and mode |
| `theme.py scale categorical\|sequential\|diverging` | Chart scales with checks |
| `theme.py mix A B` | Blend two colors in four spaces and read the contrast |
| `theme.py name HEX...` | The nearest plain color name from our own list |

## When a site is the inspiration

Use `extract_site.py` (see the discover guide), then run `color-kit` with `--from-extract`. The result keeps hue, chroma and neutral and remixes the rest.

## Rules for this kit

- The kit never states a color rule that `color-kit` also states. If you need a rule, read it there.
- A token that the builder wrote is not edited by hand. Rebuild.
- If `color-kit` is not installed, say so, and follow the manual path described in its ramps guide if you have it. Otherwise report that color decisions were not reviewed.
