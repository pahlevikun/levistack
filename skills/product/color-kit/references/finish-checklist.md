# Before you finish

Run this on the result. Each row is a pattern to find and what to do about it.

| Pattern | Fix |
|---|---|
| A hex, `rgb(` or `oklch(` literal in a component where a token exists | Use or add the role token in the project's own notation |
| One `oklch(` value in a codebase written in hex | Use the established notation unless a migration was asked for |
| A primitive such as `blue-600` used in a component | Point a semantic role at it and use that |
| A role named for a hue or a place (`blue-button`, `sidebar-gray`) | Rename it for its job |
| `primary` used both for the brand and for the main text | Rename the brand token `accent`, or keep `primary` for the brand only |
| A border token used as text color or a text token as a ground | Add a token for the missing role |
| A ramp made of HSL values that differ only in lightness | Rebuild it in OKLCH with a constant hue |
| Steps 50 to 200 as far apart as mid-ramp steps | Tighten the light end to about 0.04 to 0.05 in L |
| One chroma number copied to every hue | Use the same share of each hue's own maximum |
| A status hue within 15 degrees of the accent | Move it, or give the destructive action another treatment |
| Success and danger at the same lightness | Move them at least 0.12 apart in L |
| Dark values equal to the light ramp in reverse | Lower accent chroma, widen the dark end and remeasure |
| Color tokens set under both `prefers-color-scheme` and a class | Pick one mechanism |
| A contrast fix that changes hue and leaves lightness | Change lightness |
| One `prefers-contrast` block shared by light and dark | Give each appearance its own value |
| Text on a color with alpha | Measure the composed result or use a solid token |
| White label on a mid-lightness fill | Measure it. Move the fill to a darker step or use dark text |
| Chroma beyond sRGB with no sRGB value first | Declare the sRGB value, then the vivid one under `color-gamut: p3` |
| A gradient behind text | Measure the worst stop or add a scrim |
| Hue picked from the category cliché | Pick it from the product's meaning |
| Red as the only error signal | Add an icon and words |
| A new ramp nothing uses | Delete it |

## Final checks

- Every pair in `data/essential-pairs.csv` passes in every mode, or each failure has a stated reason.
- Light, dark and any special mode were measured separately.
- The brand color is recognizable in every mode.
- A grayscale view still shows the order of ground, surface and accent.
- Success and danger are told apart without color.
- Zero hex outside theme files.
- The recipe, the seed and the rebuild command are written down.
- Everything not measured is listed as Not verified.
