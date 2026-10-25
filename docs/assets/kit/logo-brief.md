# Logo brief: levistack and Murk

## Routing

- **Mode:** `mark_only`. The mark is the existing mug, `docs/assets/murk.svg` (formerly `levi.svg`).
- **Kit tier:** `full`
- **Grill:** decisions asked one by one: mascot name, motion, kit tier, asset location.
- **Intent:** Animate the existing mascot and ship it as the levistack README hero. The four assets show Murk, a tired mug built from three stacked layers with a fish-hook handle, floating in dusky fog, beside the `levistack` wordmark and the seven-step `use-levistack` route. For people who install levistack. Tokens come only from the mascot's own colors. The banner keeps the 3-column blueprint.
- **Context sources:** `docs/assets/murk.svg` (every color token), `README.md` (tagline line, mascot copy), the GitHub repo description ("Agent skills for people tired of AI slop"), `skills/workflow/use-levistack/SKILL.md` (the seven steps), `docs/assets/levistack-routing-stack.svg` (the gold "prove" accent).
- **Unknown after lookup:** no theme file in the repo (looked: no CSS or token files). Tokens taken from the mascot SVG instead.
- **Banner column 3 mode:** `feature-summary` (the seven-step route)
- **Preview artifacts:** concept sheet, tiles boards, preview sheet, presentation board
- **Platform pack and social cards:** yes (required)
- **Gallery publish:** skip
- **Clichés avoided:** a smiling coffee mug, steam hearts, a robot or a brain, a purple-blue AI gradient, a face on the mascot.

## Decisions (user)

| Decision | Choice |
|---|---|
| Mascot name | Murk (replaces "Levi") |
| Motion | Tired float: slow bob with a lazy tilt, drifting fog, one steam wisp that rises and gives up, a glint on the hook |
| Kit tier | full |
| Location | `docs/assets/` and `docs/assets/kit/` |

## Brand and copy

- **Wordmark:** `levi` in `--fg` + `stack` in `--accent`. Cursor at `x=350` (measured from the render, the formula's 366 left a gap).
- **Tagline:** `for people tired of AI slop.` (28 chars, from the repo description)
- **Pill 1:** `37 skills` with dot, `width=92`. **Pill 2:** `proof before done`, `x=100`, `width=146`.
- **Motto:** `Meet Murk: overskilled and underslept.` (from the README line)
- **Column 3:** chip `/use-levistack <task>`, seven rows (route, prime, invoke, hunt, apply, prove, deliver), step 06 in gold, footer `37 skills · 11 agents · 42 rules · 5 hooks` and `+2 upstream`.

## Tokens (all from `docs/assets/murk.svg`)

| Role | Hex | Where it is in the mascot |
|---|---|---|
| `--bg` | `#17152e` | outline ink |
| `--surface` | `#3a3358` | dark fog |
| `--surface2` | `#4a4f7a` | main fog |
| `--line` | `#566782` | upper fog |
| `--fg` | `#e8e4f4` | layer highlights |
| `--muted` | `#98a2b6` | hook steel |
| `--dim` | `#6a6fa0` | mist |
| `--accent` | `#c99d48` | rim gold |
| accent chip border | `#b2853a` | top layer gold |
| extra | `#3c7f7c` teal, `#66589a` violet, `#c6cddb` hook shine | middle and bottom layers |
| `--del` / `--add` | not used | column 3 is not `diff-hunks` |

## Motion spec

- Icon loop `4.6s`, banner loop `6s`, cursor blink `1.1s steps(2, start)`.
- `.float` (translateY -7px, rotate -2deg, origin 160 190 in mug space), `.fog-drift` (translateX 6px), `.steam` (dash draw up, hold, fade and rise), `.glint` (hook shine pulse).
- Banner only: `.spine` draws, `.s1`…`.s7` dots light in turn, `.s6` and `.prove-row` go gold and hold to 88%.
- `prefers-reduced-motion: reduce` stops all motion and shows the full still.
