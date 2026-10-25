# Color meaning

Color carries meaning that the product did not choose. Read this before you pick a hue for a state or an audience.

## Conventions you keep

| Signal | Usual color | Also give |
|---|---|---|
| Error, danger, delete | Red | An icon and a word |
| Success, done | Green | A check and a word |
| Warning, caution | Amber | An icon and a word |
| Information, link | Blue | An underline or an icon |
| Disabled | Low-contrast gray | The disabled state in the control itself |

Convention beats invention for states. A user who has to learn that purple means error loses time.

## What changes by region and field

- Red can mean luck and celebration in East Asia, so an error shown only in red can look festive there.
- White can mean purity in one place and mourning in another.
- Finance apps in some markets show gain in red and loss in green.
- Green can carry religious or political meaning.
- Medical products have their own conventions for urgency. Follow the field's standard.

Use `data/locale-color-notes.csv` for the audience's region, and make anything regional a per-locale token. When unsure, ask a local reviewer and say that you asked.

## What to avoid

- Color as the only signal. Add an icon, a word or a shape.
- The blue-to-purple gradient on everything. It signals "template" faster than any other choice.
- A brand hue that is also a state hue, such as a red brand with red errors. Keep status colors separate from the brand.
- Red and green next to each other for good and bad.
- Reusing one color for two meanings (a green brand and green success).

## Brand colors carry recognition

People know a product by a few colors. A confirmed brand hue is fixed. Move the other colors around it. If the brand color fails contrast as text, keep it as a fill and use a darker step for text. Do not quietly darken the brand.
