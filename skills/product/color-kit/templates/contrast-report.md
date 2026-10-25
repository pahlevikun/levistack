# Contrast report: <theme name>

Date: <YYYY-MM-DD>
Tokens: `<path to tokens.json>` built from seed `<seed>`
Pairs file: `<path to the pairs csv>`
Modes measured: light, dark, <high contrast>, <car night>, <TV>

## Result

<One line: "All N pairs pass in M modes" or "K pairs fail, listed below".>

## How it was measured

- WCAG 2 ratio on the color as it renders. A color with alpha was composited over its real background first.
- APCA Lc is listed as advice. Body text wants Lc 75 or more.
- Command: `python3 scripts/theme/theme.py contrast --pairs <pairs.csv> --tokens <tokens.json> --mode <light|dark> --out <this file>`

## Failures

| Pair | Mode | Ratio | Need | Fix chosen | Remeasured |
|---|---|---:|---:|---|---:|
| <name> | <mode> | <x.xx> | <4.5> | <what moved: lightness only> | <x.xx> |

## Not measured

- <Text over photos. Needs a scrim measured over the lightest and darkest region.>
- <Gradients. Measure the worst stop.>
- <Anything that needs a device: Increased Contrast, forced colors, OLED, glare.>

## Color blindness and grayscale

- Success against danger: <distance, lightness gap, pass or add icon and label>
- Chart colors: <worst pair under deuteranopia>
- Grayscale view keeps the order of ground, surface, structure, accent: <yes or no>

## Verdict

<Approve, or Block with the one thing that must change.>
