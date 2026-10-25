# The ingredient library

The theme builder does not pick one palette from a list. It **mixes ingredients**: a domain, one to three moods, a harmony, a neutral, a shape, a type voice, a motion profile and a signature move. Each ingredient has its own file, and the seeded mixer combines compatible ones. This keeps every result specific to the brief.

Run scripts from `specialities/design-system/`. The data lives in `data/theme/`.

## Contents
- What is in the library
- How the mixer chooses
- Domain notes
- Mood notes
- Color rules that hold across domains
- Region and culture cautions
- Adding or changing an ingredient

## What is in the library

| File | What it holds | Count |
|---|---|---:|
| `domains.json` | Kinds of product, with hue zones, default moods, preferred shapes, voices, motion and signatures, and "avoid" notes | 35 |
| `moods.json` | Feelings, with chroma, temperature, contrast, ground and preferred or forbidden ingredients | 24 |
| `harmonies.json` | Ways to place the secondary and tertiary hues (calm kinds and pop kinds) | 8 |
| `neutrals.json` | Tinted gray families (paper, stone, mist, slate, plum, moss...) | 15 |
| `shapes.json` | Radius scales, border weight, elevation style, control padding | 8 |
| `voices.json` | Type pairings with scale, weights, tracking and case (all free fonts) | 15 |
| `motion.json` | Motion profiles with durations, easings, travel, press scale, stagger | 6 |
| `signatures.json` | One recognisable device per project | 15 |
| `platforms.json` | Mobile, desktop, web, TV and car profiles | 5 |
| `rules.json` | Extra forbid lists that stop clashes | - |
| `names.json` | Plain color names, not an ingredient. Read by `theme.py name` and by the report | about 100 |

List any of them: `python3 scripts/theme/theme.py list domains` (and `moods`, `harmonies`, `shapes`, `voices`, `motion`, `signatures`, `neutrals`, `platforms`).

## How the mixer chooses

1. Match the brief to one or two **domains** (or take `--domain`). The first gives the primary hue zones. A second gives the accent.
2. Match **moods** from words in the brief (or take `--mood`). If none, use the domain's default moods, and sometimes add a neighbour.
3. Pick the **primary hue** inside the domain's hue zones, with a small jitter. Scale **chroma** by the moods. Apply **temperature**, which moves hue and chroma together: warming boosts reds, oranges and yellows and quiets blues, and cooling does the reverse.
4. Pick the **harmony**, the **neutral**, the **shape**, the **voice**, the **motion** and the **signature** by weighted chance. An ingredient listed in `want` of the domain or a mood gets more weight, one in `forbid` is removed, and the rest still has a small chance. That small chance is what makes unexpected but valid mixes.
5. Apply the lead **platform** profile (ground, contrast floor, sizes).
6. The seed is a hash of the brief and the seed text. Same input gives the same output.

## Domain notes

These are the working notes behind the data, grouped by what the product feels like. The hue words use the OKLCH wheel: red about 25, orange 55, amber 75, yellow 100, lime 125, green 145, teal 185, cyan 210, sky 235, blue 255, indigo 275, violet 295, magenta 335, pink 355.

**Calming and caring** (meditation, sleep, mental health, therapy, journaling)
- Low chroma, soft lightness steps, hues that sit back: teal, sage, dusk blue, lavender. Similar hues feel calm together. Use one gentle warm accent for the main action.
- No pure white and no pure black. Use warm off-white or deep blue-green for the ground.
- Avoid red unless it is a true error, avoid ticking counters, and keep motion slow with no bounce.
- Keep soft palettes readable: pair muted grounds with near-dark text.

**Health and medical**
- Calm blues and teals with a lot of white space read as safe. Red must keep its meaning, so use it only for errors and urgent states.
- Large touch targets, very clear status, and no reliance on color alone. People may be anxious or in pain.

**Food and drink** (delivery, restaurants, cafes, recipes)
- Warm reds, oranges and yellows raise appetite. Photography is the main color, so the interface steps back and lets the food be the brightest thing.
- Keep the ground warm. A cool blue-black base mutes food. Green as the main color reads as diet food unless the brand is about health.
- Big prices in tabular numerals. Pill shapes and a little bounce feel friendly and fast.

**Money** (banking, payments, insurance, investing)
- Blue means trust, green means growth, and a refined violet or teal stands out in a crowded blue field. Plain blue blends in, so change the neutral, the type or the hue to be remembered.
- Show amounts large and tabular. Never use only red and green for gain and loss.

**Tools and work** (SaaS, productivity, developer tools, analytics)
- People live in the UI all day, so chroma stays modest and the neutral is chosen carefully. Spend color on state and on the single primary action.
- Default indigo with Inter is the look of a thousand templates. Change at least one of hue, neutral or type voice.
- Developer tools lean dark with mono accents and fast motion. Analytics keep the chrome gray so data can carry color, with a separate checked palette for charts.

**Shopping and marketplaces**
- Warm accents push action, a calm base keeps products readable. Reserve one color for price and sale and one for the buy button. If everything shouts, nothing converts.

**Premium and fashion**
- Price tier shows up as restraint: low chroma, warm neutrals, one controlled accent, a lot of space and large quiet type. Many colors read cheap. Use the 60-30-10 rule (60% dominant, 30% support, 10% accent).
- No bouncy motion and no sticker shapes.

**Playful, kids and learning**
- Bright, clear hues on a calm ground, big touch targets, friendly shapes, and rewards for progress. Playful is not low contrast: text stays strongly readable. Use at most four hues at once.
- Serious learning (university, research) goes the other way: deep blues, burgundy or green, serif text, quiet motion.

**Travel and real estate**
- Open, airy and warm. Let photography set the palette: a sea trip leans teal, a desert trip leans clay. Property uses deep green or navy with warm neutrals, and price and place lead.

**Media, music and creative**
- News is type-led: a serif for text, a sans for UI, one accent for links. Music and video use a dark canvas so artwork glows and pull accents from the cover. Photo and video tools keep the canvas neutral so color judgments stay honest.

**Sport, fitness and games**
- Saturated, high contrast, expressive. Numbers (reps, pace, score) are the product, so type them large. Use one hot accent for effort and a cooler color for recovery. Do not use red for progress.

**Civic, legal and faith**
- Plain, readable and sober. Strong contrast, a visible grid, no playful shapes. For faith and cultural communities, follow the community's own visual language, avoid sacred colors or symbols as decoration, and support right-to-left layouts and local numerals when needed.

**Nature and impact** (eco, farming, non-profit)
- Plain bright green looks like a template. Shift toward olive, moss or sea green, and add a soil or sun accent. Real photos and honest type.

**TV and car** use the same domain notes with the platform rules in `platforms.md`: darker grounds, larger type, higher contrast.

## Mood notes

| Mood | What it does to the system |
|---|---|
| calm, gentle, serene-night | Lower chroma, soft contrast, slow motion, rounded shapes, tinted neutrals |
| appetizing, wholesome, earthy | Warm temperature, warm neutrals, soft shapes, photo-led |
| trustworthy, clinical, focused | Higher contrast, crisp shapes, restrained motion, one accent |
| playful, festive, social | Higher chroma, pop harmonies, pebble or pill shapes, springy motion |
| premium, editorial, mysterious | Low chroma, high contrast, mixed or sharp shapes, theatrical or slow motion |
| energetic, sporty, bold, rebellious | High chroma, complement or triad, hard shapes, big type |
| futuristic, technical | Dark ground, cool temperature, sharp shapes, mono labels, fast motion |
| nostalgic | Warm, faded, paper neutrals, serif voices |
| optimistic, fresh | Sunny, clean, mid-high chroma, bright neutrals |

Mix two or three. Opposite pulls (calm + energetic) are allowed, but say which one wins.

## Color rules that hold across domains

1. **Hue similarity is for calm. Hue contrast is for pop.** A foreground color gets more attention against a background of a different hue, even when the pair is not "harmonious".
2. **Lightness does the hierarchy.** Separate roles (ground, surface, structure, detail, accent) by lightness first, and by hue second. A grayscale test must still show the order.
3. **Temperature is a joint shift of hue and chroma**, not a hue rotation. When you warm a palette, reds and oranges get more vivid, blues get grayer, greens lean yellow.
4. **Keep the semantic status hues recognisable.** Success, warning, error and info keep their usual hue families, tuned to the palette's chroma. Always add an icon or a label.
5. **A color has to pass its job.** Text 4.5:1, large text and UI edges 3:1, in both modes.

Details and the math are in `color-craft.md`.

## Region and culture cautions

Color meanings change by region and even inside one language. Treat these as questions to test with local users, not rules.

- Red can mean luck, joy and celebration in many East and South Asian settings, so a red used only for "error" may feel odd or may soften the warning. Give errors an icon and plain words, and consider a different hue for promotions.
- Green can mean growth and also carry religious or political meaning in some places. Do not rely on green alone for "success" or "go".
- White can mean purity or mourning. Gold and yellow can mean prosperity or caution.
- In warm, bright places, higher-chroma warm colors may read better on screen in daylight. Test outdoors.
- Do not guess a person's region from their name. Ask, or use the product's market.
- Right-to-left languages mirror layout and direction cues. Arrows, progress bars and carousels flip. Numerals and brand marks may not.

## Adding or changing an ingredient

1. Copy an existing entry in the right file and give it a new `id` in kebab-case.
2. Fill every field. `describe` is a plain sentence used in `DESIGN.md`.
3. Add its id to the `want` lists of the domains and moods it suits, and to `forbid` where it would clash.
4. Run `python3 scripts/theme/theme.py list <file>` to see it. Then run `explore` for a brief that should pick it.
5. Run the tests: `python3 -m unittest discover -s scripts/tests -p "test_theme*.py"`.
6. Only use free fonts (Google Fonts), so the output works anywhere.
