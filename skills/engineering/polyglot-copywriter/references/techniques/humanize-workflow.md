# Humanize workflow

Operational humanize loop. **Extends** [noslop-prose.md](../noslop-prose.md) with detect → rewrite → verify — do not duplicate the full pattern tables; cross-link instead.

Load when use case is `humanize`, or user asks to de-AI, humanize, rewrite stiff copy, or audit for AI tells.

The tell catalog is [humanizer-patterns.md](../humanizer-patterns.md): 26 patterns, strongest first. Principles and the critique format are in [noslop-doctrine.md](../noslop-doctrine.md). This file is the loop that applies them.

## Two modes

| Mode | User intent | Output |
|---|---|---|
| **Edit** (default) | Fix a draft | Rewritten text + short "what changed" |
| **Detect** | Audit only | Named patterns, quoted lines, fix hint — no rewrite until asked |
| **Review** | User asked to critique / check / detect | [review-prose.md](../review-prose.md) — no file edits |

If no draft, ask for one. If audience/format unclear, ask once: who is this for and where will it publish?

### Output shape by input

| Input | Return |
|---|---|
| Pasted text (default) | Draft, short list of remaining patterns, final rewrite. Short drafts: edited text plus "what changed" is enough |
| A named file | Write only the final text to the file. Change prose only. Keep code blocks, inline code, commands, paths, YAML metadata, data and link targets. Then give a short summary |
| Another task (PR, commit, MR comment, doc) | Only the final text, no commentary |
| A reply in a thread | Check §26 first: does it lead with the decision? |

## Loop: detect → rewrite → verify

```
1. READ full draft, note voice traits to keep (cadence, bluntness, humor, uncertainty). If the user gave a sample, read it first and match it
2. DETECT: mark tells strongest first (§1 to §5 act on one sighting, weak-alone tells need company). Look at paragraph shape too, not only sentences. Scan [noslop-prose.md](../noslop-prose.md) clusters + checklist below
3. REWRITE — minimum effective edit; preserve meaning and personal markers
4. VERIFY — re-read aloud; run quick score from [evaluation.md](../evaluation.md) § Self-check rubric
5. SURVIVOR TELLS — scan the rewrite for patterns you just cut (see checklist below)
6. REWRITE SELF-CHECK — would you flag your own rewrite under [noslop-prose.md](../noslop-prose.md)? If yes, revise again
7. DELIVER — edited draft + what changed (edit mode) or findings list (detect mode)
```

**Fact check on every rewrite:** compare against the source for any added or dropped fact, name, number, date, quote, citation, ranking, or "these happen at once" claim. Shape edits (triads, bold-label lists, merged sentences) drop these most often. An unsupported addition is an error. A lost claim is an error unless a pattern calls for cutting it.

**Rule:** Look for **clusters**, not isolated tells. One em dash or one "however" is fine. Em dash + rule of three + empty vocabulary + generic kicker in one paragraph is a cluster.

## Core rewrite principles

0. **Substance first** — follow [substance.md](../substance.md) order
   (truth → substance → development → sentences → craft). If the draft
   has no source material, stop and offer [interview.md](../interview.md)
   instead of inventing color.
1. **Preserve the writer's real voice** — Do not sterilize into generic polished prose.
2. **Minimum effective edit** — Strong human sentences stay.
3. **Lead with the point** when setup adds nothing; keep asides that create context or character.
4. **Never invent** claims, stats, examples, or sources.
5. **Portability test** — If a sentence could move unchanged to another company/product, cut or replace with a specific fact.
6. **Show, don't tell importance** — Cut "the key point is" / "this matters because" when the prose already shows it.
7. **Trust the reader** — Skip softening, hand-holding, and interpretive metadiscourse.

## Pattern quick reference (audit)

Use [noslop-prose.md](../noslop-prose.md) for full tables. High-signal audit list:

| Category | Examples |
|---|---|
| **Empty vocabulary** | delve, leverage, robust, seamless, tapestry, landscape (abstract), foster, elevate |
| **Binary contrasts** | "It's not X, it's Y" / "Not just X but Y" — state Y directly |
| **Colon reveals** | "The detail that matters: a separate agent grades it" — use plain sentences |
| **Trailing -ing** | "…highlighting their commitment" — cut or replace with mechanism |
| **Significance inflation** | pivotal moment, testament, new era, revolutionizing |
| **Weasel attribution** | experts say, studies show — name source or cut |
| **Fake-profound kickers** | Mic-drop metaphor at end — end on last concrete fact |
| **Summary recap** | "In conclusion…" / restating the whole piece |
| **Formatting slop** | emoji headings, bold every keyword, bullets where prose fits |

## Inject soul (not just scrub)

After thinning clusters, check the draft is not **technically clean but lifeless**:

- Mixed sentence length (not robotic rhythm)
- Specific detail or honest uncertainty where appropriate
- Point of view when the channel allows
- Do not make every paragraph equally tidy

## Collaboration with other refs

| Reference | Role in humanize pass |
|---|---|
| [noslop-prose.md](../noslop-prose.md) | Pattern catalog + symbol hygiene |
| [voice-fingerprint.md](../voice-fingerprint.md) | Keep the author markers (EN/ID) |
| [core.md](../core.md) | Register, vocab, protected artifacts |
| [english-humanizer.md](../usecases/english-humanizer.md) | Extended EN pattern library |
| [natural-writing.md](natural-writing.md) | Plain sentence + calque pass (all langs) |
| [humanizer-patterns.md](../humanizer-patterns.md) | The 26 numbered tells, examples, output modes |
| [noslop-doctrine.md](../noslop-doctrine.md) | Principles, extra detectors, critique format |
| [simple-prose.md](../simple-prose.md) | STE casual bar: the rewrite must end simpler, not fancier |

## Detect-mode output shape

For each hit:

```
- **Pattern:** {name from noslop or table above}
- **Quote:** "{line}"
- **Fix:** {one-line direction}
- **Verdict:** keep | revise | ask-author | cut
```

When the user asked for a critique, map each hit to review verdicts from
[review-prose.md](../review-prose.md). Offer to run edit mode after detect.

## Survivor tells (post-rewrite scan)

After rewrite, re-scan the output for these high-recurrence tells (the first five survive most rewrites):

- [ ] **Negative parallelism** — `not X but Y`, `not just X`, clipped `Not X. Y.` without named mechanism
- [ ] **One-line closer** — mic-drop aphorism or pull-quote ending; flatten and test (emphasis-source)
- [ ] **Dash or semicolon** — any em dash, en dash, or `;` reintroduced while fixing other tells (first principle, §8)
- [ ] **Rule of three** — forced triad where two items (or a concrete list) fit the content
- [ ] **Bold label + punch** — `- **Label:** generic claim` or inline-header list slop
- [ ] **Chatbot wrapper**: a greeting, offer or "let me know" left around real content
- [ ] **Reply order**: in a reply, the decision comes first and background the reader already has is gone

If any survive, run one more minimum-effective pass or escalate to detect mode.

## Rewrite self-check

Before delivery, ask: **Would I flag this rewrite if it were source text?**

Check your rewrite for the same detectors you used on the source: staged openers, prestige vocabulary, `not just` without mechanism, invented facts, decorative staccato, meta-commentary, copula displacement without enumeration job. If the rewrite would earn `revise` on review, fix it or mark `[TK:]` — do not ship a sterile swap of AI patterns.

## Show-work output (optional)

When the user pastes a long draft for humanize (not incident/chat/file-edit tasks), you may use this shape:

```txt
Flagged patterns:
- {pattern}: "{quote}" → {fix direction}

Draft rewrite:
{minimum effective edit}

Final (after survivor scan + self-check):
{delivered text}

What changed:
- …
```

Default remains **edited draft + what changed** unless the user asked to see the intermediate steps.
