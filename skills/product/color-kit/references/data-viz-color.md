# Color for charts

Charts have their own rules, because the marks must tell apart, not just look nice. Build the scales with the script, then read the checks.

```bash
python3 scripts/theme/theme.py scale categorical --n 6 --hue 250 --mode light --out /abs/chart-categorical.md
python3 scripts/theme/theme.py scale sequential --hue 250 --n 7
python3 scripts/theme/theme.py scale diverging --hue 250 --hue2 40 --n 9
```

Use `--mode dark` and `--ground <hex>` for the real surface. Add `--json` for a file the code can read. The command exits 1 when a check fails.

## Pick the kind

| The data is | Use | Rule |
|---|---|---|
| Groups with no order | Categorical | At most 6 marks for a safe result. Past that, label marks directly |
| Low to high | Sequential | One hue. Lightness moves one way in even steps |
| Below and above a middle (zero, a target) | Diverging | Two hues and a neutral middle. Mirrored steps have the same lightness |

## What the script checks

- **Categorical:** every mark is visible on its ground (3:1), and the closest pair stays apart in the normal view and in the red-green and blue-yellow views.
- **Sequential:** each step is at least 0.03 lighter or darker than the last, and lightness never reverses.
- **Diverging:** mirrored steps match in lightness, so the scale still reads in grayscale.

A failing check is a finding. Say it. With 8 or more marks on a light ground the closest pair is usually too close. Group the small ones, label directly, or add shapes and patterns.

## Rules for a chart

1. **Separate touching marks.** Draw a 1 to 2 px stroke in the ground color between bars, slices and areas.
2. **Label directly.** Put the name on or beside the mark. A legend is a fallback.
3. **Color groups, not values.** Show exact numbers with position, length and labels.
4. **Never use red against green as the only cue.** Add an icon, a sign or position.
5. **One highlight.** Gray everything except the series that matters, then give that one the accent.
6. **Both modes.** Build the scale for light and for dark. Marks that pass on white often fail on near-black.
7. **Name the colors** in the legend text only when the reader must say them aloud. `theme.py name` gives a plain word.
