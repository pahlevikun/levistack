# Look variants

Use this when the question is "how should this screen look?" or "find a better theme". The answer is two to four variants of the **same** screen, so the user can point at one. Default to three. Past five, the differences turn to noise.

## Where the variants live

Decide this first. It changes how honest the comparison is.

| Home | Use it when | How |
|---|---|---|
| **In the app (preferred)** | A page or flow already exists, or the new part would sit inside one | Render the variants on the same page, picked by `?v=a`, `?v=b`. Keep the real data, header, sidebar and density. Only the drawn part swaps |
| **Standalone** | There is no nearby page, or no app code is available | One HTML page in `prototypes/<topic>/` with the switcher. Use real-looking content and the project's tokens |

Variants alone on an empty page always look fine. Next to the real header and the real data they often do not. That is why the in-app home is better.

In-app rules:

- Work on a **throwaway branch**. The change never merges. Say so in the first line of the branch name or the PR.
- Keep all data loading, auth and params as they are. Only the drawn part switches.
- Variants may read the real data. They must not write. Point any write at a stub.
- Show the switcher only outside production. Use the project's own dev check, so a stray merge cannot show it to users.
- Use the project's routing and styling system. Do not invent a new top-level structure.

## Steps

1. **Write the question and the number.** One line: "Three variants of the settings page behind `?v=`, on the existing `/settings` route."
2. **Read any reference into devices, not adjectives.** "Cute and friendly" cannot be built. Pull out the parts that transfer, with numbers: corner radius, number of stacked tonal bands, where the one dark element sits, how status is shown. Each device is something to use or reject.
3. **Check where the reference came from.** If it is a competitor, take the mechanics and leave the signature look, or it reads as a clone. Tell the user plainly.
4. **Keep the user's palette and words.** A reference gives structure, not colors. If a brand is given, follow `brand-dress.md`.
5. **Write a direction for each variant** (see `directions.md`). Name, idea, structure.
6. **Make the variants differ by structure.** A different layout, a different information hierarchy and a different main action. Then vary at least three of: number face, rule style, corner radius, button fill, label voice. Four recolors of one design are one option shown four times. If two drafts come out alike, redo one with a hard rule such as "no card grid".
7. **Share little between variants.** A shared header component is fine. A shared layout wrapper is not, because each variant must be free to throw the layout away.
8. **Put them behind one switch.** Start from `templates/variant-switcher.js`. It sets the URL param, so a variant can be shared and survives a reload.
9. **Hold content identical.** Same headline, same items, same counts. If one variant needs an extra element, add it to all or cut it from all. Assert the counts.
10. **Render each variant** and check it (see `render-and-check.md`), then run the gate in `variant-gate.md`.
11. **End with a ranked verdict.** Say which wins and why, in mechanisms: hierarchy, contrast, what happens when content grows, how many illustrations a new screen costs. Say what each loser is still good at. The most useful feedback is often "the header from B with the list from C". Offer a compromise only when it is real.

## After a pick

- Write the answer first: which variant, and the one reason.
- Fold the winner into the real code properly. Prototype code is not production code, so rewrite it with the states, tests and error handling the real thing needs (use `ui-ux-kit`).
- Delete the losers and the switcher from the main branch. If someone may want them again, keep the whole set on the throwaway branch and note the branch in the receipt. Do not leave variants beside product code.

## Notes

- Warm, soft palettes (warm near-black, a muted accent) read as pleasant. Saturated neon on cold blue-black reads as harsh.
- For a real product, draw a small set of its own icons. The default icon library reads as generic.
- A number on screen must equal what is drawn. "3 waiting" over four drawn items makes the whole mockup look invented.
- Dead space between the last content and the bottom bar is the most common defect. Extend the content or move it down. Do not decorate a hole.
