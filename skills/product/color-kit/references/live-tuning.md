# Live tuning

Use this when the user wants to try the palette and tune it, and does not want to wait for a rebuild each time. The build can write one page, `live.html`, with knobs that change the colors on screen at once.

## Build it

```bash
python3 scripts/theme/theme.py build --from-brief /abs/design/brief.json --out /abs/design/ --live
```

The page needs no server. Open the file in a browser.

## The knobs

| Knob | Values | What it does |
|---|---|---|
| Color amount | 0, 0.25, 0.5, 0.75, 1 | How much of the color strategy shows. 1 is the recipe. 0 is a gray product. The brand ramps scale fully, the neutral tint scales less, and status colors do not scale |
| Neutral temperature | cool, as built, warm | Moves the neutral hue 60 percent of the way toward cool or warm |
| Mode | light, dark | Shows the matching token set |

Each position is a full build. Every one has passed through the same contrast gate. The page shows one line: all checks pass, or how many fail and which pairs.

A position that fails stays selectable. Show it to the user as a warning. Do not ship it.

## Keep a choice

1. Press **Brief keys**. The page prints `{"color_amount": 0.5, "neutral_temp": "warm"}`.
2. Add those two keys to `design/brief.json`.
3. Rebuild without `--live`, or keep `--live` so the page matches the files.

`color_amount` and `neutral_temp` are normal brief keys. They also work as flags: `--color-amount 0.5 --neutral-temp warm`.

**CSS variables** prints the current mode as one `:root` block. Use it to try the colors on a running page. Open the browser tools on the real page, paste the block into a style rule, and look at the real screens. Do not paste it into source until the rebuild is done.

## Rules

- The knobs change the palette only. They never change type, space or motion.
- Use at most two extra knobs when a direction needs its own (for example, how strong the surface tint is). Name each one, give it a range and a default, and keep every position gated.
- Never tune by editing a hex in the page. Change a knob or the brief, then rebuild.
- Say which position the user chose, and put it in the recipe.
