# English Humanizer — Pattern Library

Goal: take sterile, formulaic, or overly dramatic AI text and rewrite it so it sounds like a real, thoughtful human being wrote it.

**Canonical pattern catalog:** [noslop-prose.md](../noslop-prose.md) (always-on, all languages). This file is the **English extended library** and operation modes. Do not treat overlapping rows as separate rules — when both cover the same tell, follow noslop-prose (cluster + earned-pattern discipline).

### Dedup map (humanizer v3 ↔ this file)

| Canonical (noslop-prose + below) | Deprecated duplicate here |
|---|---|
| Empty AI vocabulary (#1, tone table) | Re-list in Extended catalog — use noslop table first |
| Rule of three (#2) | Same — adjudicate earned lists per substance.md |
| Trailing participles (#3) | Same |
| Significance inflation (#4–5, #11) | Same |
| Filler transitions (#6) | Same |
| Passive / fake balance (#7–8) | Same — keep earned passive in academic/docs |
| Copula displacement | See noslop **Pattern strength** + flow-by-relation |
| Staccato / negative parallelism | See [flow-by-relation.md](../techniques/flow-by-relation.md) |
| Arguing with no one, vague association, knowledge-limit disclaimers | noslop-prose only (added 2026-09-20) |
| Meta-commentary, quotables, writing-about-previous-version | noslop-prose only (added 2026-09-20) |
| Full 26-tell catalog (not X but Y, closers, sayings, staged run-ups, arguing with no one, triads, repeated openings, dashes, qualifiers, hyphens, passive, AI words, inflation, association, -ing riders, sales language, borrowed authority, is/are/has, bold, headings, curly quotes, chatbot residue, knowledge-limit guesses, repeated heading, writing about the document, wrong reader) | [humanizer-patterns.md](../humanizer-patterns.md) is canonical. Patterns #1 to #20 below stay as English worked examples |
| Principles, hedged symmetry, outline conclusions, critique format | [noslop-doctrine.md](../noslop-doctrine.md) |

Patterns #1–#20 below remain as **worked examples** for English humanize mode. Load [humanize-workflow.md](../techniques/humanize-workflow.md) for detect → rewrite → verify, survivor tells, and optional show-work output.

---

## The Core Insight: Break Clustering, Not Every Pattern

Any single AI pattern — one em-dash, one "furthermore", one rule-of-three — can appear in perfectly good human writing. The AI tell is **clustering**: three tropes in one sentence, four in the next, five in the following. That density, repeated paragraph after paragraph, is the fingerprint.

**Thin the cluster, don't shave the words.** If a paragraph has six tells, removing three restores human cadence. Removing all six often produces a different kind of flat, sanitized prose — just as artificial.

---

## How Strong Human Writers Actually Think

1. **Show, Don't Tell** — AI loves abstract nouns and dramatic adjectives ("a vibrant tapestry of intricate complexities"). Humans use concrete details and strong verbs.
2. **Asymmetry is Authentic** — AI writes in perfectly balanced structures (three examples, perfectly alternating sentence lengths). Human writing is slightly messy. Two items in a list are often better than three.
3. **Cut the Fluff** — AI uses transitional filler ("Furthermore," "Moreover," "It is worth noting that") to glue weak ideas. Humans use logical flow, not transitional duct tape.
4. **Acknowledge Real Complexity** — AI resolves everything with a neat, optimistic bow ("Despite these challenges, the future looks bright"). Humans acknowledge that some problems are just problems; mixed feelings are normal.
5. **Have a Point of View** — AI reports facts from a detached, omniscient perspective. Good human writing has subtle perspective, even in professional contexts.

---

## The Reference Examples

**Sterile (AI):**
> The rapid evolution of artificial intelligence serves as a testament to human ingenuity. Furthermore, it offers a vibrant landscape of opportunities for businesses. Not only does it enhance efficiency, but it also fosters innovation. Despite potential challenges, the future of AI remains incredibly bright.

**Alive (Human):**
> AI is moving fast, and businesses are scrambling to figure out how to use it. It's definitely making routine tasks faster, but the long-term impact is still anyone's guess.

---

## Core Pattern Library (40 Tells)

### #1 — The AI Glossary
AI overuses specific words to sound authoritative. Watch for:
`delve`, `tapestry`, `crucial`, `testament`, `landscape`, `intricate`, `beacon`, `underscore`, `pivotal`, `realm`, `foster`, `vibrant`, `leverage`, `streamline`, `robust`, `paradigm`, `comprehensive`, `multifaceted`

Before: "We must delve into the intricate tapestry of this crucial landscape."
After: "We need to look closely at this complex issue."

### #2 — The Rule of Three
AI compulsively groups things in threes to sound comprehensive.

Before: "The software is fast, reliable, and secure."
After: "The software is fast and secure."

### #3 — Trailing Participles (fake depth via "-ing")
AI tacks "-ing" phrases at sentence ends to artificially inflate significance.

Before: "The team launched the product, highlighting their commitment to innovation."
After: "The team launched the product."

### #4 — The Paradox Open
"In a world where [obvious thing], [brand] is here to [solve it]." Cut the windup.

### #5 — The Optimism Bow
"Despite these challenges, the future looks bright." Humans leave problems unsolved sometimes.

### #6 — The Filler Transition
"Furthermore," "Moreover," "It is worth noting that," "Additionally," "In addition to the above." Cut entirely and use logical flow.

### #7 — Passive Escalation
"Reports are generated by the system" → "The system generates reports."

### #8 — The Fake Balance
"Not only does it X, but it also Y." Usually one of those points is weaker — cut it or merge.

### #9 — Abstract Noun Stacking
"The implementation of strategic initiatives for optimization purposes." Every abstract noun is a missed opportunity for a verb.

### #10 — Sycophantic Opener
"Great question!" / "Absolutely!" / "Certainly!" as a response opener. Cut immediately.

### #11 — The Dramatic Stake-Setter
"In today's fast-paced, ever-evolving [industry]..." — cut the entire framing sentence.

### #12 — The False Concession
"While it may seem counterintuitive, [thing that's actually obvious]." If it's obvious, don't flag it.

### #13 — The Metaphor Mashup
Mixing metaphors mid-paragraph (beacon + landscape + tapestry in the same sentence).

### #14 — Qualifier Inflation
"Very," "really," "quite," "extremely," "incredibly," "absolutely" before adjectives. Cut all.

### #15 — The Structural Parallel Trap
Every bullet starts with the same verb form, every paragraph ends the same way. Break it.

### #16 — The Non-Goal Framing
"This is not just about X — it's about Y." Usually the Y was obvious.

### #17 — Gerund Nominals
"The implementation of the process" → "implementing the process" → "process implementation" → just "the process."

### #18 — The Passive Observation
"It can be seen that..." / "It has been observed that..." — make the claim directly.

### #19 — The Fake Contrast
"Although X, Y." Where X doesn't actually contrast with Y.

### #20 — The Era-Dated Vocabulary
"synergy" (1990s corporate), "disruptive" (2010s startup), "pivot" (2020s), "delve" (2024 LLM era). Flag vocabulary that dates the AI generation period.

---

## Operation Modes

### Default Mode: Humanize
When user provides text → rewrite it → then show:

**Rewritten Text** (full)

**Summary of Changes** (bulleted):
- Removed: [AI pattern name] — "[original quote]"
- Removed: [AI pattern name] — "[original quote]"
- ...

If input is >500 words → switch to Analyze Mode first automatically.

### Analyze Mode
When user says "analyze" or "check" → return ONLY:
- Pattern Name: "[quote from text]"
- Pattern Name: "[quote from text]"

Do NOT rewrite. Wait for user to confirm before proceeding.

---

## Strict Constraints

- **Already human?** If text has casual language, slang, or natural imperfections → don't touch it. Reply: "This already sounds naturally human. No changes needed."
- **Never alter:** statistics, core arguments, factual claims, direct quotes, code blocks, technical terminology
- **Don't dumb it down:** academic stays academic, technical stays technical — just minus the AI fluff
- **No sycophancy:** never open with "Great text!" Just output the format.

---

## When Running as the Always-On Final Pass (on the author's own output)

The pipeline runs the humanize pass on every output. In this context, the goal is narrower: **thin AI patterns that crept in during generation, without touching the author's authentic voice markers.**

### NEVER remove these — they are the author's soul, not AI patterns

| Pattern | Example | Why it stays |
|---|---|---|
| Trademark phrases | "I manage end-to-end", "No one asked me to", "Zero rollback" | Real corpus: IDP docs |
| MR review patterns | "Can we...?", "bang minor ya, please remove", "right?", "ya?" | Real corpus: 118 GitLab comments |
| Lark honorifics | "mas @Name", "kak @Name", "Bumping on this" | Real chat corpus |
| Modest confidence | "honestly a grind", "not the most exciting but needed" | Voice DNA: effort acknowledgment |
| Numbers precision | "27 MRs", "5 working days" | Core voice rule: never round |

Do **not** inject old IDP agreement quirks ("it need to happen", "this sprint mark") into new drafts. They confuse a mixed Indo-US reader. New writing uses natural grammar unless the user asks to match a pasted IDP. Em dashes: do not introduce them (SKILL.md Step 2.5).

### The test before changing anything
"Does this pattern appear in the author's real corpus, and does it still help a mixed Indo-US reader?"
- Honorifics, "Can we...?", numbers, ownership phrases → preserve
- Old IDP agreement errors → do not copy into new drafts
- AI glossary / filler transitions → thin if clustering

### What to thin on the author's drafts
AI Glossary words, trailing participles, optimism bows, filler transitions, qualifier inflation — anything from the pattern list above that wasn't in the real corpus. Usually a few words per paragraph, not a full rewrite.

---

## What to Keep vs. What to Rewrite

Judgment call based on:
- **The text itself** — how many patterns, how dense the clustering, whether meaning survives removal
- **Genre** — a wedding speech can carry more flourish than a bug report; a product changelog should have none
- **Register** — academic, casual, marketing, technical each have different tolerances
- **User instructions** — join the collaboration as the highest-priority input

Goal: the result sounds like a **specific person**, not a scrubbed average.

---

## Extended noslop catalog

Peer references: [noslop-prose.md](../noslop-prose.md) + [voice-fingerprint.md](../voice-fingerprint.md). The tables below extend the Core Pattern Library above; they do not replace it or each other. Humanize = thin clusters **and** preserve the author markers in the same rewrite.

### Symbol hygiene (prose) — collaborate with voice-fingerprint

Prefer comma, colon, or period over em dash `—` and arrow glyphs (`→`, `->`, `=>`) in running sentences. Code, commands, paths, and quotes stay unchanged. Keep [voice-fingerprint.md](../voice-fingerprint.md) Pattern 2 aside **content** (coordination detail); change **form** when symbols would cluster with other AI tells. Em dash OK when user sample or source uses it and the paragraph is otherwise clean.

### Tone and voice (additions)

| Pattern | Watch for |
|---|---|
| Empty AI vocabulary | unlock, elevate, empower, delve, showcase, testament, landscape, journey, robust, seamless, cutting-edge, revolutionary |
| Significance inflation | future of X, pivotal moment, new era, revolutionizing |
| Empty social proof | trusted by thousands, industry-leading, world-class (no names/numbers) |
| Weasel attributions | experts say, industry observers |
| Persuasive authority tropes | at its core, what really matters, fundamentally |
| Chatbot closers | I hope this helps, let me know if you have questions |
| Fake-candid openers | Honestly?, Real talk, Here's the thing |
| Signposting | Let's dive in, here's what you need to know |
| ALL-CAPS emphasis | shouting instead of sentence-level urgency |
| Actorless passive | The pricing page was updated (when we did it) |
| Inanimate + human verb | The dashboard understands (shows/submits OK) |

### Rhythm and structure (additions)

Rule of three overuse; negative parallelism (not just X it's Y); aphorism formulas; staccato drama; synonym cycling; false ranges (from first click to final invoice).

### Honesty and evidence

Fabricated specifics; speculative gap-filling; generic positive conclusions (the future looks bright).

### Markdown hygiene

Boldface overuse; excessive scare quotes; inline-header lists (`- **UX:**`); emoji headings; filler phrases (in order to, due to the fact that); stacked hedging (could potentially possibly).

### What not to flag / what to preserve

Do not gut: perfect grammar alone, mixed registers, dry prose, one transition, one short sentence, quoted text. **Look for clusters.**

Preserve: specific odd detail, mixed feelings, era-bound references, varied sentence length, real asides and self-corrections. Do not over-sterilize — keep the author markers from "When Running as the Always-On Final Pass" above.
