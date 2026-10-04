# Noslop prose (always on)

Read this **together with** [core.md](core.md) and [voice-fingerprint.md](voice-fingerprint.md) for every mode, including casual. It pairs with Step 2.5 and Step 3.5 in `SKILL.md`. Overlap with [english-humanizer.md](usecases/english-humanizer.md) is intentional: each file covers a different lens on the same draft; none cancels the others.

Integrated into Polyglot Voice as **always-on cluster detection** (thin AI tells on every pass; full humanize mode also loads [humanize-workflow.md](techniques/humanize-workflow.md) and the humanizer use case). **Simple prose** ([simple-prose.md](simple-prose.md)) is the vocabulary/grammar floor — noslop thins AI clusters on top; it does not replace short sentences and common words.

## How references collaborate

These guides are **peers**, not a stack where one overrides another. Apply them in the same pass:

| Reference | Lens |
|---|---|
| [core.md](core.md) | Language bar, vocab, register, protected artifacts |
| [simple-prose.md](simple-prose.md) | Simple vocabulary and grammar default for every language |
| [voice-fingerprint.md](voice-fingerprint.md) | the author's real sentence shapes, trademark phrases, corpus markers |
| **This file** | AI cluster tells, symbol hygiene, honesty, markdown spam |
| [humanizer-patterns.md](humanizer-patterns.md) | The 26-tell catalog, strongest first, with before/after examples and file/embedded/pasted output modes |
| [noslop-doctrine.md](noslop-doctrine.md) | Principles ("sharp detail beats inflated significance"), extra detectors, critique format, rewrite self-check |
| [english-humanizer.md](usecases/english-humanizer.md) | Extended pattern library + analyze/humanize operation modes |
| [humanize-workflow.md](techniques/humanize-workflow.md) | Detect → rewrite → verify loop; detect vs edit modes |
| [regional.md](regional.md) / [configuration.md](configuration.md) | Overlays when the user picks a variety or style |

**Collaboration rules:**

1. **Voice + noslop together.** Thin AI clusters *and* keep the author markers. If a phrase is in the real corpus ([voice-fingerprint.md](voice-fingerprint.md)) and not an AI tell, keep it even while cutting nearby slop.
2. **Same job, different form.** When [voice-fingerprint.md](voice-fingerprint.md) calls for a coordination aside (Pattern 2), [noslop-prose.md](noslop-prose.md) prefers comma, colon, or parentheses over em dash — same rhetorical job, slop-safe punctuation. Arrows in prose (`→`) still become words ("to", "then") unless they are code or a quoted artifact.
3. **User sample is a third collaborator.** Match the sample's rhythm, punctuation habits, and markers. Still apply honesty rules (no new fabricated facts). Do not strip deliberate sample choices while thinning *unrequested* AI clustering in generated filler.
4. **Use-case files add format.** Email, MR review, RFC, and the rest layer channel rules on top; they do not replace core, voice, or noslop.
5. **Clusters, not veto.** One em dash, one "however", or one short fragment is not a failure by itself. Cross-check both files before cutting something that sounds like the author.
6. **Earned patterns stay.** A concrete list of three operational checks,
   an academic hedge the evidence requires, or a docs heading pattern is
   not slop. Adjudicate in context ([substance.md](substance.md)). Do not
   split, casualize, or "vary the shape" merely to look less like a model.

7. **Dash precedence.** [humanizer-patterns.md](humanizer-patterns.md) §8 sets the default: no em dashes, en dashes, or semicolons in final prose unless the user's sample uses them. This is the first principle. The budget table below is the upper limit for `baku` and for sample-matched voice, not a target for casual or `profesional` text.
8. **One catalog.** Rows in this file and numbered tells in [humanizer-patterns.md](humanizer-patterns.md) are the same tells. Use the numbered catalog for strength order and worked examples, and this file for the always-on cluster scan.

## Two global rules

1. **Never invent facts.** No fabricated numbers, testimonials, names, dates, quotes, or citations. Specificity comes from the source or the user. If a sentence needs real detail to work, ask for it or write the plain version without it.
2. **Do not over-sterilize.** Scrubbing AI tells but killing voice is also a tell. Keep the author markers ([voice-fingerprint.md](voice-fingerprint.md), `SKILL.md` Step 3.5). When the user supplies a writing sample, collaborate with it: match voice habits and still thin AI clusters that were not in the sample.

## Symbol and punctuation hygiene (prose)

In user-facing prose (all modes), avoid decorative symbols that read as AI formatting or slide-deck copy:

| Avoid in prose | Use instead |
|---|---|
| Em dash `—` or spaced ` - ` as an aside | Comma, colon, parentheses, or a new sentence |
| Semicolon `;` joining two clauses | A period, or a plain connective (`because`, `so`, `but`) |
| En dash `–` as a connector between clauses | Comma, colon, or split into two sentences |
| Arrow glyphs in running text (`→`, `->`, `=>`, `⇒`) | "to", "then", "leads to", or a short list sentence |
| Unicode bullets or ornament arrows mid-sentence | A normal list, or "first … second …" |
| ALL-CAPS clauses for emphasis | Write urgency into the sentence |
| Emoji in headings or bullets as decoration | Plain heading; emoji only if the user asked and it is rare |

**Allowed without change:** fenced code, commands, paths, URLs, issue numbers, log lines, quoted material, tables that are the deliverable format, and artifacts that are the task target.

**With [voice-fingerprint.md](voice-fingerprint.md) (symbols):** Pattern 2 uses em-dash asides for coordination detail in the historical corpus. Collaborate: keep the **aside job** (who else was involved, scope note) using comma, colon, or parentheses first. An em dash is OK when (a) the user pasted source text and asked to preserve shape, (b) the user's sample uses em dashes at a natural frequency, or (c) a comma/colon would blur two independent clauses — and it is **not** part of an AI cluster (rule of three, filler, signposting in the same paragraph). IDP/management reports: comma form per both files.

### Em dash overuse (AI tell)

In daily coworker copy, em dashes (`—`) are rare. Models overuse them as a default rhythm. Treat **em-dash density** like other cluster tells.

| Default | Rule |
|---|---|
| Casual / `profesional` | Avoid em dash; prefer comma, period, colon, or parentheses |
| Budget | At most **one** em dash per ~200 words; **zero** preferred in chat and incident updates unless quoting |
| `baku` / formal | May use sparingly for apposition; still prefer a sentence break |
| Cross-language | Same restraint in every language — locale packs may use different punctuation; do not import English em-dash habit into other langs |

**MUST NOT:**

- Chain ideas with em dashes instead of periods (`fact — explanation — conclusion`)
- Use em dash as the default "AI rhythm" or slide-deck aside
- Stack multiple em dashes in one paragraph when comma/period/colon would read naturally

**Cluster signal:** em dashes plus rule of three, signposting, or empty vocabulary in the same block is a confession — split sentences and thin the tells.

## Tone and voice patterns

| Pattern | What to watch for |
|---|---|
| **Empty AI vocabulary** | game-changer, navigate the landscape, unlock, elevate, empower, delve, showcase, testament, landscape (abstract), journey, robust, seamless, cutting-edge, revolutionary |
| **Significance inflation** | "future of X", "pivotal moment", "new era", "revolutionizing" |
| **Empty social proof** | "trusted by thousands", "industry-leading", "world-class" with no names or numbers |
| **Weasel attributions** | "experts say", "industry observers" — name the source or cut |
| **Persuasive authority tropes** | "at its core", "what really matters", "fundamentally", "the deeper issue" |
| **Chatbot closers** | "I hope this helps!", "Let me know if you have any questions", "Would you like me to expand on this?" |
| **Fake-candid openers** | "Honestly?", "Real talk", "Here's the thing" as a theatrical pause |
| **Signposting** | "Let's dive in", "Here's what you need to know", "Without further ado" |
| **ALL-CAPS emphasis** | Shouting instead of writing urgency into the sentence |
| **Actorless passive** | "The pricing page was updated" when we did it — name the actor when known |
| **Inanimate subject + human verb** | "The dashboard understands…" — product verbs (`shows`, `submits`, `filters`) are fine; mind verbs (`understands`, `decides`, `wants`, `believes`) are not |

## Rhythm and structure patterns

| Pattern | What to watch for |
|---|---|
| **Em-dash chaining** | `fact — aside — punch` or multiple `—` per paragraph where periods or commas would do |
| **Rule of three overuse** | Forced trios everywhere when two items (or four) fit the content |
| **Negative parallelism** | "It's not just X, it's Y", clipped "no guessing", "no wasted motion" — see pattern strength; keep when severity or mechanism is named |
| **Aphorism formulas** | "X is the language of Y", "Efficiency becomes a trap when…" |
| **Staccato drama** | Chains of short fragments for fake punch; see [flow-by-relation.md](techniques/flow-by-relation.md) § Staccato contrast |
| **Synonym cycling** | fast → quick → speedy to dodge repetition |
| **False ranges** | "from first click to final invoice, and everything in between" |
| **Arguing with no one** | Fake objections, straw alternatives, "some say… but we…" with no named opponent |
| **One-line closers** | Mic-drop aphorism or pull-quote line whose force is cadence, not prior evidence |
| **Quotables / emphasis inflation** | Self-contained line engineered to be tweeted; bold label + colon + punch |
| **Meta-commentary** | "As we'll see", "the rest of this essay", "this section will explore" |
| **Copula displacement** | `serves as`, `boasts`, `features`, `stands as`, `represents` where plain `is` or a specific verb would do — keep when enumerating, defining, or locating |
| **Writing about previous version** | Docs prose that narrates what was replaced (non-changelog); state what *is* now |
| **Explain-the-example closer** | A line after a scene, number or example that names what it showed ("This shows the importance of…", "The message was clear:"). Cut unless it adds a fact the example does not show |
| **Repeated openings** | Several sentences in a row with the same subject. Merge, change the subject, or lead with the action |
| **Hedged symmetry** | "Whether you're X or Y", "While X, Y is also important" with no real branch |
| **Outline conclusions** | "Despite challenges, X continues to thrive", "Looking ahead, X will play a pivotal role" |
| **Writing about the document** | "generated from…", "the table below compares…", "anything unconfirmed is flagged". Describe the subject, not the page |
| **Wrong reader** | A reply that rebuilds background the reader already has and puts the decision last. Lead with the decision ([humanizer-patterns.md](humanizer-patterns.md) §26) |

## Honesty and evidence

| Pattern | What to watch for |
|---|---|
| **Fabricated specifics** | Fake stats, quotes, customer names (worse than vague copy) |
| **Speculative gap-filling** | "likely founded in the 1990s" when unknown — state the gap or omit |
| **Knowledge-limit disclaimers** | "While details are limited…", "though records are scarce…" followed by a guess — mark `[TK:]` or omit |
| **Vague association** | "associated with", "in connection with", "linked to" without naming the relation or evidence |
| **Generic positive conclusions** | "The future looks bright", "exciting times ahead" — end on the last concrete fact |

## Hygiene and markdown

| Pattern | What to watch for |
|---|---|
| **Boldface overuse** | Every keyword bolded — emphasis nowhere |
| **Excessive quotation marks** | Scare quotes as default emphasis |
| **Inline-header lists** | `- **UX:** The UX improved` — merge into prose or plain bullets |
| **Emoji headings** | 🚀 Launch, ✅ Next steps |
| **Filler phrases** | "in order to", "due to the fact that", "it is important to note that" |
| **Stacked hedging** | "could potentially possibly" — one qualifier is enough |
| **Title Case headings, rules, `# Title` repeated** | Sentence case, no `---` between every section, title appears once |
| **Heading restated in line 1** | `## Performance` then "Speed matters." Delete the restating line |
| **Hyphen after the noun** | `the report is high-quality` → `high quality`. Keep `third-party`, `cross-functional` as spelled. Weak alone |
| **Curly quotes** | Use straight quotes where the target format does. Weak alone |

## What not to flag

Sanity-check before editing. These are **not** reliable AI tells on their own:

- Perfect grammar and consistent style
- Mixed casual and formal registers
- Dry or bland prose without the tells above
- Precise formal vocabulary (AI overuses *specific* empty words, not all fancy words)
- A single "however", "additionally", or transition word
- Curly quotes from the editor or CMS
- One em dash, one short punchy sentence, or unsourced claims in isolation
- Text inside quotations, titles, proper names, or examples being discussed

**Look for clusters, not isolated tells.** One em dash means little. Two or more em dashes in a short block, or em dashes plus rule of three plus "vibrant tapestry" plus a generic conclusion, is a confession.

## Pattern strength

Treat detector hits as hypotheses, not verdicts. Adjudicate with [substance.md](substance.md) earned-pattern rule.

| Strength | Examples | Action |
|---|---|---|
| **Strong** (edit on one sighting) | Staged opener ("In today's landscape…"); fake-candid throat-clearing; meta-commentary; arguing-with-no-one; knowledge-limit guess; decorative one-line closer; quotable pull-quote with no surviving claim when flattened; copula displacement with no enumeration/locating job |
| **Medium** (flag; revise when clustered or hollow) | `not just X but Y` without mechanism; rule of three; staccato contrast; copula displacement; vague association; writing-about-previous-version |
| **Weak** (cluster only — never blanket ban) | One adverb, one passive, one Wh- opener, one `however`, one em dash, one short fragment, one `robust` in engineering context |

**Emphasis-source test:** flatten cadence on a suspect line (remove contrast shape, dashes, parallel clauses). If the residual claim still names an actor, mechanism, or limit, keep it. If it collapses to a generic statement, cadence was carrying it.

**Do not add blanket bans** on all adverbs, all passive voice, zero em dashes, or all Wh- openers. Academic, docs, and quoted material may require them.

## What to preserve (human signals)

Lean toward leaving prose alone when you see:

- Specific, unusual, hard-to-fabricate detail
- Mixed feelings and unresolved tension
- Era-bound references and in-jokes
- Variety in sentence length
- Genuine asides and self-corrections

## Draft → audit → final (copy work)

When the task is prose for people to read, follow [humanize-workflow.md](techniques/humanize-workflow.md) (detect → rewrite → verify). Short form:

1. **Draft** — apply the tables above; vary sentence length; prefer specific detail and simple constructions.
2. **Audit** — briefly answer: "What makes this obviously AI generated?" and "Does it state any fact, name, number, date, or citation that is not in the source?"
3. **Final** — revise for both answers; re-check symbol hygiene (em dashes, arrows in prose).

## Checklist (run with `SKILL.md` Step 4 — collaborate with voice-fingerprint)

- [ ] No fabricated numbers, testimonials, names, dates, or claims
- [ ] Empty AI vocabulary and significance inflation thinned or replaced with specific language
- [ ] Symbols slop-safe: comma/colon preferred; em dash / arrows only when sample, source, or Pattern 2 job needs them and paragraph is not a cluster
- [ ] No excessive scare quotes, ALL-CAPS emphasis, or emoji decoration in headings
- [ ] Actors named where known; no abstraction given a human mind verb
- [ ] No dense AI-rhythm clusters (rule of three, negative parallelism, staccato drama, aphorisms, false ranges)
- [ ] the author markers from [voice-fingerprint.md](voice-fingerprint.md) still present — not a sterile scrub
- [ ] Read aloud: sounds like the author wrote it, not a model padded it

---

**Vocabulary watch lists drift.** Words such as `delve`, `robust`, and `landscape` peak and fade with model generations. Re-profile against current output; a single word on the list is not a veto when nearby prose supplies mechanism, measurement, or boundary ([substance.md](substance.md)).
