# Cross-check with a second tool

Our script gives the numbers. A second tool catches a mistake in a bad assumption (a wrong pair, a wrong ground). Use one of these for each job. Match the tool to the job, not the other way around.

| Job | What to use | What you are checking |
|---|---|---|
| Contrast ratio of one pair | The browser's color picker and its contrast row, or any WCAG checker | The pair, the ground and the ratio match `theme.py contrast` |
| Contrast of what really renders | The browser's rendering tools (computed styles and an eyedropper on the live page) | Alpha, gradients and images behind text |
| Color-blind view | The browser's rendering emulation for vision deficiencies | Series and states stay apart |
| Grayscale view | The browser's rendering emulation, or a grayscale filter on a screenshot | Hierarchy survives without hue |
| Out-of-gamut and OKLCH values | An OKLCH picker, or a color library that converts and reports gamut | The hex we wrote is the nearest one that fits |
| Dark mode and forced colors | The browser's emulation of the dark scheme and of forced colors | No role falls back to a bad default |
| Increased contrast | The device setting itself | Borders and text step up |
| Print | A proof from the printer | The brand colors in CMYK on the paper |
| Real devices | One phone, one laptop, one external display | Brightness and warmth differences |

Rules:

- When two tools disagree, find the cause before you pick a winner. The usual causes are a different ground, a different rounding or alpha.
- A tool is a check, not an authority. The pair file is the record.
- Write down which tool you used in the contrast report.
