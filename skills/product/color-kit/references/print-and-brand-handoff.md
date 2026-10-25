# Print, spot colors and brand sheets

Use this when a color must leave the screen: a printed card, a package, a sign, a slide that gets printed, or a brand sheet for a vendor.

## What changes

- **Gamut.** Print inks (CMYK) cannot show some bright blues, greens and oranges. A vivid screen color is dulled in print. Ask early.
- **Spot inks.** A spot color (for example a Pantone number) is a mixed ink. Its screen swatch is an approximation. A CMYK conversion is a second approximation.
- **Paper.** Coated paper keeps color strong. Uncoated paper makes it softer and darker.
- **Light.** A screen gives off light. Paper reflects it. The same hex looks different on each.

## What to write in the brand sheet

For each brand color, one row:

| Field | Example |
|---|---|
| Plain name | Harbor |
| Master | Which value wins when they disagree (screen hex or spot ink) |
| Hex (sRGB) | `#3B6A8C` |
| P3 value | Optional. Only when it was designed, not auto-converted |
| CMYK | The converted values, marked as converted |
| Spot | The ink name, if any |
| Use | Where it appears and where it must not |
| Minimum contrast pairs | The text colors that may sit on it |

## Rules

1. Name which value is the master. Two masters means two brands.
2. Never say a CMYK value matches the screen. Say it is the nearest the process can print.
3. Ask the printer for a proof on the real paper before a full run.
4. Keep a pure-black-on-white version of the mark for one-color jobs.
5. A dark full-bleed background uses a lot of ink and may show banding. Ask before you plan one.
6. For slides that may be printed, check the light theme too.
