# Prove the contrast

Never report a ratio you did not measure. Never estimate a color you could compute. A pair that fails is a finding. A notation choice is not.

## Contents
- Thresholds
- Measure the pair as it renders
- Fix a failing pair
- What to check
- Color blindness and grayscale
- Chart colors
- Report format

## Thresholds

| Content | WCAG 2 (the gate) | APCA Lc (advice) |
|---|---|---|
| Body text | 4.5:1 | 75, 90 preferred |
| Large text, 24 px or 18.67 px bold | 3:1 | 60 |
| Labels and headlines | 4.5:1, or 3:1 when large | 60 |
| UI edges, icons, focus rings, solid fills | 3:1 | 45 for fine icons, 30 for solid shapes |
| Dividers that only need to be seen | no rule | 15 |
| Placeholder and disabled text | not required | aim for 30 so it stays findable |

Disabled controls and logos are exempt from WCAG, but keep them readable. APCA values have a sign: positive is dark text on light ground, negative is light on dark. Compare the absolute value.

WCAG 2 is the standard that conformance claims and linters use, so it is the gate. APCA predicts readability better, so it is advice. When they disagree, fix for the stricter one and say which one drove the fix.

## Measure the pair as it renders

- Identify the real ground. Text on a card is measured against the card, not the page.
- A color with **alpha** is composited over its real ground before it is measured. Prefer a solid token for anything that carries text.
- **Computed colors** (`color-mix()`, relative color syntax, opacity modifiers) resolve at render time. Measure the result, not the declaration.
- **Gradients.** Contrast changes along the gradient. Measure the worst stop, or place a scrim.
- **Text over images.** There is no single ground. Measure the worst region, or guarantee one with a scrim measured over the lightest and darkest areas.
- **Translucent surfaces** shift with what scrolls behind them. Test over the lightest and darkest content, or make the surface opaque enough.
- **Polarity.** Compare black and white text on the fill with the metric the project uses. WCAG's neutral crossover is near 56 percent OKLCH lightness. On a mid-lightness fill only one of black or white may pass.

Run the pair file through the gate. Each row names its own mode, so a single run measures every row. Use `--mode` only as the default for rows that give none.

```bash
python3 scripts/theme/theme.py contrast --pairs data/essential-pairs.csv --tokens design/tokens.json --mode light
python3 scripts/theme/theme.py contrast --pairs data/essential-pairs.csv --tokens design/tokens.json --mode dark
```

(The script lives in `design-system-kit`. Run it from that skill's `specialities/design-system/` folder and pass absolute paths.) The pairs file takes hex colors, hex with alpha, or role names. Add a row for every pair your product really draws.

## Fix a failing pair

1. **Change lightness first.** It is the channel that contrast responds to. Move the foreground away from the ground in OKLCH L and keep its hue and chroma. Then remeasure.
2. Keeping the hue fixed is what stops a contrast fix from becoming a palette change.
3. A mid-lightness ground caps what is possible. On a ground near L 0.75, even black text reaches only about Lc 60 to 70. Body text needs a ground near one extreme, so the ground is what must change.
4. Pushing lightness can push the color out of gamut. Lower chroma to keep it showable.
5. A brand color that fails behind white text stays the brand color. Use a darker step for the filled control.
6. Report the pair, the measured value and the threshold before you change a color, when the colors are a design decision. Change them only when asked or when the task says so.
7. Always remeasure after a change. Do not assume the fix landed.

## What to check

- Every pair, in every mode. A pass in light says nothing about dark.
- States: hover, pressed, focused, selected, disabled, placeholder, error.
- Status tints: text on its tint, and the solid against the page.
- Focus ring against the ground and against the control it surrounds.
- Increased contrast and forced colors where the platform has them.
- Overlays and scrims, composed over real content.

## Color blindness and grayscale

- Simulate protan and deutan vision. The kit does this for success and danger and for chart colors. If two are too close in color distance and in lightness, add an icon, a label or a pattern.
- Look at the screen in grayscale. The order of ground, surface, structure and accent must still show. Grayscale is a check of lightness separation. It is not an accessibility proof.
- Do not use red and green alone for gain and loss.

## Chart colors

- Give charts their own set, built around the brand hue with alternating lightness.
- WCAG wants 3:1 between neighbouring non-text elements. Finding six fills that hold 3:1 against each other is nearly impossible. Put a border on each mark and require 3:1 between each fill and its border. That is one rule per color, not many.
- Use direct labels. Use markers or patterns past four series.
- For a low-to-high scale, keep one hue and let lightness do the work. The perceptual step between neighbours should be flat, and the scale should still be ordered in grayscale.

## Report format

Group findings by the principle they break, ordered by severity, one row per root cause with every place it appears.

| Severity | Location | Before | After | Why |
|---|---|---|---|---|

- **HIGH:** text or control text fails its ratio, meaning carried by color alone, a semantic color used against its meaning.
- **MEDIUM:** a visible theme, token or gamut failure.
- **LOW:** isolated polish.

End with **Block** if any HIGH remains, **Approve** otherwise. Never approve what you did not inspect. List every check you could not run as **Not verified**. With nothing to report, say "No actionable color findings" and list what you verified. The template is `templates/contrast-report.md`.
