# Core language rules

Read this before writing any Polyglot Voice prose. It covers **English and Bahasa Indonesia equally**. Skill instructions stay in English. User-facing output follows the selected `language`.

**Simple prose default (all languages):** [simple-prose.md](simple-prose.md) — common words, short sentences, active voice. Load on every draft; locale packs set *which* forms, not complexity for its own sake.

## What good output feels like (both languages)

Write like a coworker who is easy to follow. Casual. Simple words. Short, complete sentences. One intention per sentence. Natural grammar.

Stay literal on diagnosis, destructive actions, and security even when the rest of the text is casual. Upgrade to formal or a named use case only when the user asks. Light emoji is fine if it is rare.

**Good** = fits the situation, the reader, the channel, and the technical context.
**Correct** = follows the grammar of the chosen language and register without changing the meaning.

Default for both `english` and `indonesia`: casual, simple vocab, easy sentences. Load a use-case file only when the user asks for that format.

Do not write Indonesian that is English word-by-word. Do not write English that is Indonesian word-by-word, or a stiff US office memo.

---

## Shared: task target vs protected artifacts

Decide first whether an artifact is the user's change target:

1. **Task target** — code, identifiers, comments, docs, paths, or config the user asked to create or change. Edit those per the task and repo convention.
2. **Quoted reference** — technical material that is only cited, explained, or must match exactly. Copy it byte-for-byte.
3. **New artifacts** — create them for the technical need. Do not put dialect, speech level, or poetic style into syntax or names unless the user asked.

Protected material that is not the change target usually includes fenced and inline code; identifiers, config keys, function names, types, variables; paths, commands, flags, URLs, versions, hashes, issue numbers; error messages, stack traces, logs, program output, user quotes; product names, packages, APIs, and repo-fixed terms.

Style applies only to the prose around those artifacts. You may write “Coba jalankan lagi ya mas” or “Let me run this again,” but the command you point at must not change. Language rules must not freeze coding work the user actually asked for.

## Shared: technical terms

Follow `technical_terms`:

- `repo-natural` — default. Use the terms the repo and its docs already use.
- `indonesia-first` — natural Indonesian equivalents; keep the English term when it helps search or avoids ambiguity.
- `english-first` — keep English jargon; wrap it in natural sentences in the selected `language`.

Never translate official names or syntax tokens.

## Shared: sentence craft

Full cross-language bar: [simple-prose.md](simple-prose.md) (vocabulary, grammar, MUST/MUST NOT). This section is the short form.

Before drafting: **what should the reader know or do?** That answer is sentence 1.

- One intention per sentence. Extra facts go in the next sentence.
- Complete subject–verb–object. Correct agreement.
- Active voice. Specific numbers. No fabricated stats.
- Cut almost / very / really / quite / extremely.
- Avoid em dash (`—`) in casual/professional copy; prefer comma, period, colon, or parentheses. At most one per ~200 words in `santai`/`profesional`; zero preferred in chat and incident updates unless quoting. `baku` may use sparingly for apposition — still prefer a sentence break. Same restraint in every language.
- No en-dash asides or arrow glyphs (`→`, `->`, `=>`) in running prose. Say “to”, “then”, or split the sentence. Code, commands, paths, and quoted material stay as-is.
- Do not start with warmup (“I hope this finds you well”, “Perlu saya sampaikan bahwa”).
- Do not close with empty offers (“let me know if you have any questions”, “semoga membantu”) unless a real question is open.

Noslop catalog (tone, rhythm, honesty, markdown hygiene): [noslop-prose.md](noslop-prose.md) — apply **together with** [voice-fingerprint.md](voice-fingerprint.md), not instead of it. Same sentence: the author's job (voice) + slop-safe form (noslop). Operational humanize loop: [techniques/humanize-workflow.md](techniques/humanize-workflow.md).

## Technique routing

Load modular technique docs in this order (skip steps with no match):

1. **Language pack** — `references/languages/<id>/pack.md` (+ `registers.md`, `culture.md` as needed)
2. **Overlay** — when `regional_voice` is set; optional **profile** snapshot under `references/profiles/` (see [profiles/README.md](profiles/README.md))
3. **Use-case pack** — `references/usecases/<id>/pack.md`
4. **Generic technique** — use-case or rewrite module (table below)
5. **Locale technique** — `references/techniques/locales/<language_id>.md` when the active language has a locale file and the use case matches (see matrix)
6. **Humanize pass** — [noslop-prose.md](noslop-prose.md) + [techniques/humanize-workflow.md](techniques/humanize-workflow.md) when humanizing
7. **Substance** — [substance.md](substance.md) (truth, `[TK]`, least-invasive
   edit). Load in every mode. Interview and review load extra files from
   `SKILL.md`, not from this list.

Full index: [techniques/README.md](techniques/README.md) · [techniques/index.json](techniques/index.json).

### Generic techniques (all languages)

| Trigger | Technique doc |
|---|---|
| Use case `marketing`, `ads`, or `social` | [techniques/marketing-copy.md](techniques/marketing-copy.md) |
| Use case `email`, `letter`, or `announcement` | [techniques/email-comms.md](techniques/email-comms.md) |
| Use case `chat` | [techniques/chat-comms.md](techniques/chat-comms.md) |
| Use case `incident` or outage/status update | [techniques/incident-comms.md](techniques/incident-comms.md) |
| Use case `docs` or `technical-doc` | [techniques/docs-prose.md](techniques/docs-prose.md) |
| Use case `academic` | [techniques/academic-writing.md](techniques/academic-writing.md) |
| Use case `humanize` or user asks to de-AI / humanize | [techniques/humanize-workflow.md](techniques/humanize-workflow.md) |
| Paragraphs list-like, weak hinges, or decorative staccato closers | [techniques/flow-by-relation.md](techniques/flow-by-relation.md) |
| Any rewrite — stiff, unnatural, calque | [techniques/natural-writing.md](techniques/natural-writing.md) |
| User asks to translate or localize across languages | [techniques/translation-vs-voice.md](techniques/translation-vs-voice.md) |

### Locale techniques (load step 5 when language matches)

Full machine index: [techniques/index.json](techniques/index.json) (`locales` array). **97 locale files** — one per registry language (fictional fixtures in [fictional-catalog.json](fictional-catalog.json) have no locale file). Path pattern: `references/techniques/locales/<language_id>.md`.

Sample high-traffic triggers (full list in `index.json`):

| User says (examples) | `language` | Locale file |
|---|---|---|
| 文案, LP Mandarin | `mandarin` | [locales/mandarin.md](techniques/locales/mandarin.md) |
| 粵語, Cantonese, 廣東話 | `cantonese` | [locales/cantonese.md](techniques/locales/cantonese.md) — **not** `mandarin` |
| Hokkien, Taiwanese, Minnan | `hokkien` | [locales/hokkien.md](techniques/locales/hokkien.md) — separate from `mandarin` |
| ไทย, Thai email/marketing | `thai` | [locales/thai.md](techniques/locales/thai.md) |
| Nederlands, Dutch | `dutch` | [locales/dutch.md](techniques/locales/dutch.md) |
| فارسی, Farsi, Persian | `persian` | [locales/persian.md](techniques/locales/persian.md) |
| ελληνικά, Greek | `greek` | [locales/greek.md](techniques/locales/greek.md) |
| polski, Polish | `polish` | [locales/polish.md](techniques/locales/polish.md) |
| עברית, Hebrew | `hebrew` | [locales/hebrew.md](techniques/locales/hebrew.md) |
| Kiswahili, Swahili | `swahili` | [locales/swahili.md](techniques/locales/swahili.md) |
| iklan, landing page Indonesia | `indonesia` | [locales/indonesia.md](techniques/locales/indonesia.md) |
| copy en español, es-bo/pe/cl | `spanish` | [locales/spanish.md](techniques/locales/spanish.md) |

Indonesian the author default: [core.md](core.md) + [voice-fingerprint.md](voice-fingerprint.md). `english` locale file supplements overlay packs; the author fingerprint still applies to English by default.

Legacy stub: [techniques/jp-marketing.md](techniques/jp-marketing.md) → [locales/japanese.md#marketing](techniques/locales/japanese.md#marketing).

---

## English

Default register maps to casual spoken-complete English. `profesional` and `baku` are on request. `baku` in English means complete, careful sentences — not legal English.

### Grammar

- “It needs to happen,” not “it need to happen.”
- “This sprint marks…,” not “this sprint mark…”
- Do not copy old IDP agreement quirks into new drafts unless the user pastes an old IDP and asks to match it.
- Chat may be short, but it is still a real sentence: “Standup moves to 10:00 WIB from Monday.”
- Email and letters never use telegram fragments: not “Need review. Tomorrow. Thanks.”

### Simple vocab

English-specific examples of [simple-prose.md](simple-prose.md). Prefer: ask, tell, need, send, check, start, stop, wait, join, share, fix, delay, cancel, today, tomorrow, next week, blocker, owner, deadline, update, meeting, file, link, please, thanks.

If you would explain a word to a teammate, do not use it.

| Never write | Write instead |
|---|---|
| utilize / leverage | use |
| facilitate | help / run |
| commence / endeavor | start / try |
| unlock / elevate / empower / delve / showcase | use plain verbs; say what happens |
| streamline / optimize / innovative / robust / holistic / seamless / cutting-edge / revolutionary | say what is faster, new, or what it handles |
| testament / landscape (abstract) / journey (hype) | cut or replace with a concrete fact |
| kindly / please revert / please be informed | please / reply / just state the fact |
| circle back / loop in / touch base | I'll reply / I'll add [name] / let's talk |
| bandwidth (for people) | time / too busy this week |
| going forward / as per | from [date] / as we agreed |
| whilst / amongst / aforementioned | while / among / this |

`revert` means undo to US readers. Write **reply**. `out of pocket` and `table this` mean different things in US vs other English. Say **away** or **delay this**.

### Indo-US tone

- US: first sentence is the point. No warmup. Concrete verbs.
- Indonesian warmth: name people. Thank once when it is real. Internal chat may keep `mas` / `kak`. External English email uses the person's name only.
- Both: common words. Natural grammar. One intention per sentence.
- Dates and times with timezone (`Tue 16 Sep, 14:00 WIB`).

### Pronouns (English)

- `I` for personal ownership. `we` for team decisions.
- `you` is fine. Do not stack `I` on 3+ sentences in a row.
- Do not use `one` as a fake-formal person (“one might consider”).
- If `self_reference` or `addressee_reference` is set, honor it. `omit` means drop the pronoun when the referent is clear. Never print the word `omit`.

### English spelling in prose

- US spelling by default: `color`, `behavior`, `analyze`, not British `colour` / `behaviour` / `analyse`, unless the repo already uses British.
- Numbers, dates, and units in human prose only. Never rewrite program literals.
- Contractions are fine in casual (`it's`, `don't`). Spell out in `baku` if the user asked for formal English.

Email, letter, and announcement layout still lives in [plain-comms.md](usecases/plain-comms.md). This file is the English **language** bar for every mode, including casual.

---

## Bahasa Indonesia

For `register: baku`, follow [EYD V](https://ejaan.kemendikdasmen.go.id/eyd/). `profesional` and `santai` may use consistent spoken forms. Those forms are not wrong just because they are not official. Default is `santai`. The other two registers are on request. See [bahasa-registers.md](languages/bahasa-registers.md).

Natural Indonesian words like *aplikasi*, *pengguna*, *jaringan*, *data*, *unduh*, *unggah* are fine when they match the repo.

### Calques to avoid

| Stiff | Natural |
|---|---|
| hal ini dikarenakan oleh | ini terjadi karena |
| dapat dilakukan dengan cara | caranya |
| Anda dapat mencoba untuk | coba |
| pada saat ini | sekarang |
| dalam rangka untuk | untuk |
| terdapat sebuah | ada |
| melakukan pengecekan | mengecek |
| melakukan penambahan | menambahkan |
| memberikan penjelasan | menjelaskan |

Do not use `yang mana` or `di mana` as a translation of *which/where*. Split the sentence, or use `yang`, `tempat`, `ketika`, or the real relation.

### Pronouns (Indonesian)

- Honor `self_reference` and `addressee_reference` when set.
- If `auto`, follow the user's existing address, or drop the pronoun when the referent is clear.
- Default work chat: `saya` / omit, plus `mas` / `kak` on names. Do not jump to `gue/lo` or `aing/maneh` first.
- `Pak`, `Bu`, `Kak`, `Mas`, `Mbak`, `Bang` only when the context supports them.
- Do not mechanically rewrite every pronoun in the text.

### Indonesian spelling in prose

- Preposition `di` (`di folder`) vs prefix `di-` (`disimpan`).
- Hyphen mixed forms when needed: `di-deploy`, `commit-nya`.
- Number, date, and unit format in human prose only. Never rewrite program literals.
- Spoken spellings (`udah`, `nggak`) only when register and profile allow.

---

## Style axes (keep them separate)

- `language` — main output language (`english`, `indonesia`, or a registry id)
- `variety` — dialect inside that language; never guess
- `regional_voice` — prose overlay for the **active** language. Indonesian: `jakarta`, `bandung`, … English: `netral`, `us`, `uk`, `jaksel`, `singlish`, `au`, `nz`, `ca`, `us-slang`, `in-en`, `ph-en`, `ie`, `za`. Not a language switch. See [regional.md](regional.md).
- `speech_level` — Indonesian social speech level (Sunda `loma`/`cohag`, Jawa `ngoko`/`krama`). English uses `register` instead.
- `register` — default `santai`. `baku` / `profesional` only on request. Applies to both languages.
- `prose_style` — `lugas` or `puitis`

Do not use one axis to guess another. Bahasa Makassar is not Indonesian-with-Makassar-particles. Poetic prose is not automatically formal. `ngoko` is not an insult. A city name is not an ethnicity. Jakarta particles do not belong in English sentences unless the user asked for mixed chat.

## Coding-agent answer shape

- Start from the result or diagnosis, not small talk.
- Name the location, symbol, or command in concrete terms.
- Separate fact, guess, and suggestion.
- Keep warnings and consequences in plain words.
- Do not add “semoga membantu” / “hope this helps” if it adds nothing.

If `prose_style: puitis`, facts, diagnosis, actions, and warnings stay literal and scannable. Imagery frames the warning. It does not replace it.

## Anti-caricature

- Particles and slang need a job. Do not sprinkle `ya`, `sih`, `like`, or `basically`.
- Do not tie a dialect or an accent to a personality (rough, funny, lazy, smart).
- Do not fake an accent with mocking spelling. Do not write broken English to “sound Indonesian,” and do not write stiff English to “sound professional.”
- If you cannot explain why a regional or fancy form is in that sentence, drop it. Accurate simple language beats a confident fake.
