# Dress a look variant in a brand

Use this when the user says "in our brand", "use the company colors", or gives a brand page. A prototype may use a brand. It never invents one and never writes one down.

## Where the brand comes from

1. The repo's token file or `DESIGN.md`. Best case. Use its names.
2. A brand page, a style sheet or a logo file the user points at. Read it. Copy the values exactly.
3. Nothing. Then use the neutral prototype look in `templates/screen.html` and say so. Do not guess a palette. If the brand must be created, hand off to `color-kit` and `design-system-kit`.

## Map the brand to roles, then paint with roles

Read the brand into this small table before you draw anything:

| Role | What it is for | Rule |
|---|---|---|
| Ink | Main text and dark grounds | Highest contrast on the light ground |
| Paper | Main light ground and text on dark | Never pure white unless the brand says so |
| Mid | Secondary text and quiet shapes | Check it against paper |
| Wash | Subtle panels and rules | Barely different from paper |
| Accent 1 | The main action | One use per screen area |
| Accent 2, 3 | Other categories or non-text shapes | Only when they mean something |

Then write every color in the page as one of these role names (CSS variables). A variant then changes by swapping the role values, and a brand swap is one edit.

## Type with fallbacks

- Name the brand fonts for headings and body, then a safe fallback for each (a system sans for headings, a system serif or sans for body).
- Never link a web font. Self-host it next to the HTML (see `render-and-check.md`). If the file is missing, the fallback must still look sane.
- Apply the heading face from the size where the brand starts using it, and the body face below that. Do not mix a third face.

## Accents on shapes

For shapes that carry no text (bars, dots, dividers, chart marks), cycle through the brand accents in order. It keeps the screen alive without a new color. Text never sits on an accent unless the pair passes the contrast check.

## Check

- Contrast of every text and ground pair, from the real hex values (see `render-and-check.md`).
- The accent count. More than two accents on one screen area usually means the hierarchy is weak.
- Brand marks. Use the real logo file. Never redraw it.
