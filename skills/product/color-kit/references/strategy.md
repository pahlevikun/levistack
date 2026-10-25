# Choose a color strategy

Pick the plan before you pick a hue. A plan has four parts: the feeling, the relationship between the colors, the contrast range and the dose of color.

## Contents
- Say the plan in four lines
- What drives the feeling
- Pick a method
- A brand color that already exists
- Neutrals
- Position and price
- Hue, region and meaning
- Make it fit this product

## Say the plan in four lines

Write these down before any value:

```
Feeling:       <two or three words, for example quiet, warm, unhurried>
Relationship:  <similar hues for calm | contrasting hues for pop | one accent on neutral>
Contrast:      <soft | standard | high>, and why
Dose:          <how much of the screen is color>, for example 60% ground, 30% surfaces, 10% accent
```

If the user cannot name a feeling, ask for two words and a product they like. Do not start from a hue.

## What drives the feeling

- **Chroma and lightness beat hue.** A muted palette often reads as calm across many hues. A vivid one reads as lively across many hues. Set chroma and lightness first, then choose the hue.
- **Character first.** Think in groups: pale, muted, deep, vivid, dark. Pick a character for the ground, a character for the brand and a character for the accent.
- **Similar hues are calm. Contrasting hues are loud.** Close hues look harmonious together. A foreground color gets more attention against a ground of a different hue, even when the pair is not "harmonious". Use similarity for the page and contrast for the one thing that must be found.
- **Temperature is a joint shift.** Warming a palette makes reds and oranges more vivid, turns blues grayer and pushes greens toward yellow. Cooling does the reverse. It is not a hue rotation.
- **Hue geometry is a weak rule.** Triads, complements and tetrads do not guarantee balance, because the hue plane is not even. Compute the opposite from the real color (hue plus 180) and then judge it by eye and by contrast.
- **Lightness does legibility.** Same hue with varied lightness reads well. Same lightness across hues reads badly.

## Pick a method

| Situation | Method | How |
|---|---|---|
| A brand color is given | Anchor the ramp on it | Put the brand on the solid step (or snap it, see below). Build everything else around it |
| New product, only a feeling | Mood-led mix | Run `explore` to get three different directions. Each differs in harmony, neutral and signature, not only hue |
| A site or product to learn from | Extract, then remix | Read its colors with the extractor. Keep hue, chroma and neutral. Change the rest so it is a remix, not a copy |
| An image or a photo drives the palette | Sample, do not eyeball | Measure real pixels in OKLCH. Keep a small vivid accent that averaging would hide |
| Expressive or generative work | Constrain, then vary | Few hues in a narrow band of lightness and chroma. Weighted choice. Small hue jitter |

When you show options, show real differences: different harmony, different neutral, different dose. Four recolors of one palette are one option.

## A brand color that already exists

Two decisions before any ramp:

1. **Which step does it take?** A brand color meant for buttons and links sits on the solid step. Then the primary button is the actual brand color.
2. **Pinned or snapped?** Pin a contractually fixed color: it stays exact and the ramp grows around it, with one slightly uneven step. Otherwise snap it onto the ramp so the spacing stays regular. Snapping looks better almost every time.

A brand color that fails contrast under white text is still the brand color. Keep it, then use a darker step for filled controls. Never quietly darken the brand. Say what you did.

## Neutrals

- One neutral ramp. Do not mix warm and cool grays.
- Pure gray sits under any accent and never needs a rework when the brand changes.
- A tinted neutral (OKLCH chroma 0.005 to 0.02 at a chosen hue) puts the grays in a family. Warm tints feel approachable and editorial. Cool tints feel precise and technical.
- Neutrals carry 80 to 90 percent of the interface, so they get at least as many steps as the accent.

## Position and price

- Price tier shows in restraint. Low chroma, warm neutrals and one accent read as high price. Many saturated primaries read as low price and high volume. Match the position on purpose.
- Use 60-30-10 for hierarchy: about 60% dominant, 30% support, 10% accent.
- Calming products: low chroma, soft contrast, no pure white or black, no red unless it is an error.
- Food and warmth: warm hues raise appetite. Keep the ground warm. Photos do the heavy lifting.
- Money and trust: blue is the default and blends in. Move the hue, the neutral or the type to stand out.
- Do not choose a hue from the category cliché. Choose it from the product's own meaning.

## Hue, region and meaning

Color meanings change by region and even inside one language. Treat them as questions for local users. See `data/locale-color-notes.csv` for the common ones. Never guess a person's region from their name.

- Do not rely on red for errors or green for success alone. Add an icon and plain words.
- Where gain and loss colors differ by market (some markets show gains in red), make them per-locale tokens.
- Right-to-left languages mirror layout and direction cues. Brand marks and numerals usually do not mirror.

## Make it fit this product

- Name the cliché for the domain and avoid it. The most common AI-made palette is indigo on a light gray with a purple gradient.
- Change the neutral and the signature move before changing the hue. They are what people remember.
- Use one accent for one meaning. Spend it once per view on the main action.
- When palette and brand voice disagree, the voice wins. A palette is easier to change.
