# Simple prose (always on)

Global default for **every language**. Read with [core.md](core.md) on every draft. Locale packs choose *which* words and forms fit the register — not *how complicated* the sentence should be.

English and Indonesian examples live in [core.md](core.md). Noslop cluster detection stays in [noslop-prose.md](noslop-prose.md). This file is the **vocabulary and grammar bar** those files assume.

---

## Simple vocabulary

- Prefer words a tired teammate already knows. If you would stop to explain a word, pick a shorter common synonym.
- Avoid Latinate and corporate jargon (`utilize`, `leverage`, `facilitate`, `commence`, `endeavor`, `streamline`, `holistic`) unless the domain, repo, or quoted artifact already uses that exact term.
- One idea per sentence when explaining. Extra facts go in the next sentence.
- Define each acronym once on first use, then use the short form. Never assume the reader knows internal abbreviations.
- Keep technical terms the repo already uses (`repo-natural`, `english-first`, or `indonesia-first` per [core.md](core.md)). Simple prose does not mean dumbing down official names, syntax, or product terms.

## Simple grammar

- Short, complete sentences. If you run out of breath reading aloud, split the line.
- Active voice. Name the actor when known (`We deployed`, `Tim infra`, `I merged`).
- Avoid nested clauses, stacked passives, and connector soup (`furthermore`, `moreover`, `in order to`, `due to the fact that`).
- Match the requested register with the right **forms** (honorifics, pronouns, channel layout) — not with rare words or long sentences.
- Formal (`baku`, legal, academic) still prefers clarity over ornament. Complete sentences ≠ complicated sentences.

## Punctuation

- **First principle:** no em dash (`—`), en dash (`–`), or semicolon (`;`) in prose you write. Use a period, comma, colon, or parentheses, or split the sentence. A user's own sample is the only override. Code, commands, paths, URLs and quoted text stay as they are.
- Default: avoid em dash (`—`) in casual/professional coworker copy; use comma, period, colon, or parentheses.
- Budget: at most one em dash per ~200 words in `santai` / `profesional`; zero preferred in chat and incident updates unless quoting.
- `baku` may use an em dash sparingly for apposition; still prefer splitting into two sentences.
- Cross-language: same restraint in every language — do not copy English em-dash rhythm into other langs.
- Do not chain ideas with em dashes (`fact — explanation — conclusion`); that is an AI rhythm tell. See [noslop-prose.md](noslop-prose.md).

## Cross-language

These rules apply in **every** registry language — not only English and Indonesian.

- Do not "sound formal" by reaching for rare literary words or multi-clause sentences.
- Do not "sound professional" by copying English corporate calques into another language.
- Thai, Japanese, Arabic, Spanish, and every other pack: load register examples from `references/languages/<id>/registers.md`, then keep vocabulary and grammar **simple within that register**.
- When the pack is thin or uncertain, fall back to plain coworker clarity and state limits honestly — do not inflate complexity to hide uncertainty.

## Plain writing procedure

Merged from the `plain-writing` skill. Say the thing in the fewest words that stay clear.

1. **Lead with the point.** If the reader stops after one sentence, they should still have the answer.
2. **Cut filler.** `in order to` becomes `to`. `it is important to note that` becomes nothing.
3. **Concrete verbs over noun phrases.** `We decided`, not `a decision was made`.
4. **Split long sentences.** Over about 25 words, or any line that needs two breaths.
5. **Drop stock AI phrasing.** `delve`, `tapestry`, `navigate the landscape`, `game-changer`, `unlock`, and a closing summary that repeats the body.
6. **Read it aloud.** Rewrite anything you would not say to a colleague.

Pitfalls:

- Plain is not cold. Keep warmth, thanks, and a real greeting where the channel has one.
- When you edit someone else's text, keep their voice. Fix clarity, not style.

## STE casual (the daily recipe)

Simplified Technical English (ASD-STE100) was built so non-native readers can follow technical text on the first read. Borrow its habits, then loosen them for chat, MR and PR comments, email, and docs. This is the default for every draft. It is a style bar, not a rulebook to quote at the user.

1. **One word, one meaning.** Pick one term per thing and keep it. Do not cycle `job`, `task`, `run` for the same object.
2. **Short sentences.** About 20 words or fewer for steps and instructions, about 25 or fewer for explanations. Over that, split.
3. **One idea per sentence.** One instruction per step. Put the command first (`Run the test.`), then the reason.
4. **Simple tenses.** Present for how things work, past for what happened, `will` for what comes next. Avoid stacked forms like `would have been being`.
5. **Keep the small words.** Keep `the`, `a`, `that`, `is`. Do not write headline grammar or telegram style, except in a fixed format such as a commit subject or a table cell.
6. **Verbs over noun stacks.** `Check the pump pressure`, not `pump pressure check`. Three nouns in a row is the limit. Split before four.
7. **Plain verbs.** Prefer one clear verb over a phrasal verb with many meanings (`install`, not `set up` when you mean install). Skip idioms, sports and war metaphors, and jokes in steps.
8. **Warning first.** Put the warning or the destructive-action note before the step it covers, and say the consequence.
9. **Same shape for the same job.** Steps look like steps. Results look like results.
10. **Casual layer on top.** Contractions are fine. `I`, `we` and first names are fine. One light emoji is fine if the channel uses them. Casual changes tone, not sentence difficulty.

Reader test: could a teammate who reads English as a second language follow this on one read, without a dictionary? If not, shorten it.

## Plain-word swaps

Use the left word only when the repo, the domain or a quote already uses it. Outside protected terms, prefer the right.

| Instead of | Write |
|---|---|
| utilize, leverage | use |
| facilitate | help, let, allow |
| commence, initiate | start |
| terminate | end, stop |
| endeavor, attempt (noun) | try |
| ascertain | find out, check |
| demonstrate | show |
| obtain, acquire | get |
| purchase | buy |
| require | need |
| assist | help |
| ensure | make sure |
| approximately | about |
| additional | more, extra |
| numerous | many |
| sufficient | enough |
| in order to | to |
| due to the fact that, owing to | because |
| prior to / subsequent to | before / after |
| in the event that | if |
| with regard to, regarding | about |
| at this point in time | now |
| a number of | some, several |
| is able to | can |
| implement | build, add (name the change) |
| optimize | name the gain: faster, smaller, cheaper |

Indonesian (`santai` and `profesional`, while `baku` keeps the formal form):

| Instead of | Write |
|---|---|
| menggunakan | pakai (santai), menggunakan (profesional) |
| mengimplementasikan | membuat, menambah |
| melakukan pengecekan / perbaikan | cek / memperbaiki |
| dalam rangka untuk | untuk |
| disebabkan oleh | karena |
| oleh karena itu | jadi, makanya (santai) |
| pada saat ini | sekarang |
| sehubungan dengan | soal, tentang |
| sebagaimana | seperti |
| dapat | bisa |

A swap list is not a filter. Replace the word only when the shorter one keeps the exact meaning in that sentence.

## Before and after (casual)

| Before | After |
|---|---|
| We would like to take this opportunity to inform you that the deployment has been successfully completed. | The deploy is done. |
| In order to facilitate a smoother onboarding experience, we have implemented a number of enhancements. | We made onboarding easier. (Then name the actual changes. If you do not have them, ask or mark `[TK:]`.) |
| It is recommended that the configuration be reviewed prior to the commencement of the migration. | Check the config before you start the migration. |
| Sehubungan dengan adanya kendala pada sistem, dimohon untuk melakukan pengecekan ulang. | Ada masalah di sistem. Tolong cek lagi. |

## When complexity is OK

Keep simple prose as the default even here; add complexity only when the task requires it:

| Situation | Guidance |
|---|---|
| Legal, compliance, or contract text | Use required legal terms; still prefer short sentences where the format allows |
| Academic use case (`usecases/academic`) | Follow discipline conventions; avoid empty jargon that adds no precision |
| Quoted technical terms, error messages, API names | Copy byte-for-byte; simplify only the prose around them |
| User explicitly asks for formal / `baku` register | Use correct formal forms; do not add rare vocabulary or nested grammar for show |
| Domain terms the repo already uses | Keep them; wrap in simple sentences |

---

## Agent rules (MUST / MUST NOT)

### MUST

- Default to common words and short, complete sentences in every language.
- Put the main point in sentence 1 when explaining, warning, or updating.
- Use active voice and name the actor when known.
- Define acronyms once, then use the short form.
- Match register with appropriate **forms**, not with inflated vocabulary or grammar.
- Apply this bar before noslop thinning — simple draft first, then cut AI clusters.

### MUST NOT

- Replace a plain verb with corporate jargon when a common word works in that language.
- Stack subordinate clauses, passives, or hedges to sound "smart" or "professional."
- Pick rare, literary, or dictionary-heavy words just because the register is formal.
- Treat formal register as a license for long, nested sentences.
- Leave acronyms undefined on first mention in user-facing prose.
- Write prose that needs a second read to find who did what or what happens next.
- Bulk-edit protected artifacts (code, commands, paths, quoted errors) to "simplify" them.
- Default to em dash for asides, chaining, or punch — use comma, period, colon, or parentheses instead.

---

## Quick self-check (with [evaluation.md](evaluation.md))

Before delivery on important prose:

1. Could a tired teammate parse this in one read?
2. Is any word replaceable with a shorter common synonym without losing meaning?
3. Does each sentence carry one main idea (or one clear list job)?
4. Would reading aloud require a breath mid-clause? Split it.

See also [techniques/natural-writing.md](techniques/natural-writing.md) for rewrite and calque passes.
