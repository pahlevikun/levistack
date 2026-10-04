# Natural writing techniques

Operational guide for natural-sounding prose. Applies to **all languages** via the active language pack.

Always cross-check [core.md](../core.md). Load for any rewrite, humanize, or "sounds stiff / unnatural" request.

## Design principle

**Detect mechanically, judge in context.** Suspect patterns are flags, not automatic deletes. The active pack decides what "natural" means for that language.

**Prefer constraints at generation time** over heavy post-hoc scrubbing: one intention per sentence, conclusion first, common words — then inspect.

## Plain sentence rules

1. **Conclusion first** — Sentence 1 = what the reader should know or do. No warmup.
2. **One intention per sentence** — Split overloaded lines.
3. **Complete grammar** — Subject–verb–object; correct agreement for the register.
4. **Active voice** — Name the actor when known.
5. **Common words** — If you would explain the word to a teammate, pick a simpler one (see [core.md](../core.md) tables).
6. **Read-aloud test** — If you stumble or run out of breath, shorten or split.

## Calque avoidance

Do not write Language B as word-for-word Language A:

| Signal | Fix |
|---|---|
| Idiom translated literally | Rewrite natively or drop |
| Wrong preposition / particle habits | Check language pack + culture |
| Stiff nominalization chains | Use verbs the pack prefers |
| English connector soup (furthermore, moreover) | Cut; use logical flow |
| "It is important to note that" | State the fact |

Indonesian calques: see [core.md](../core.md) § Bahasa Indonesia. Japanese 翻訳調: see [locales/japanese.md](locales/japanese.md) + japanese pack.

## Register match

- Output must match requested `register` (baku / profesional / santai) and channel.
- Agent comms default: coworker clarity, not essay or ad unless use case says so.
- Do not upgrade formality to sound "professional" — that often adds slop.

## Dialect honesty

- One overlay at a time unless user named a mix.
- If pack is umbrella or limited coverage, state bounds — do not invent forms.
- Regional flavor is overlay, not costume (see [regional.md](../regional.md)).

## Lightweight score rubric (0–100, optional self-check)

Use before delivery on important drafts. **Not** a user-facing grade unless they asked to score.

| Axis | What to check | Weight |
|---|---|---|
| **AI-smell** | Cluster density per [noslop-prose.md](../noslop-prose.md) | 25% |
| **Calque / translationese** | Sounds translated or stiff for the target lang | 20% |
| **Register match** | Fits baku/pro/santai + channel | 20% |
| **Clarity** | Sentence 1 job, scannable facts, no buried lead | 20% |
| **Dialect honesty** | Overlay used correctly; no fake regional mix | 15% |

**Bands (informal):**

- **85+** — Ship; spot-check only
- **70–84** — One more pass on worst axis
- **Below 70** — Rework lead + thin clusters before sending

Full harness: [evaluation.md](../evaluation.md).

## Depth modes

| Mode | When | Depth |
|---|---|---|
| **Quick** (default) | Chat, email, short copy | Read-aloud + noslop checklist + register check |
| **Full** | External, legal-adjacent, long docs | Above + structure review (headings carry message) + [humanize-workflow.md](humanize-workflow.md) verify loop |

**Score-only:** User asks "how AI does this sound?" — list findings and axis scores; do not rewrite until asked.

## Clarity audit

Terse pass on the draft:

- First sentence states the point?
- Jargon undefined for this audience?
- Passive voice hiding the actor?
- Long sentences doing multiple jobs?
- Em dashes (`—`) doing the work of periods or commas? Scan and split per [noslop-prose.md](../noslop-prose.md) em-dash rules.
- Headers are messages, not labels ("Background" → state the conclusion)?

## Long-form rhythm (light touch)

For docs, essays, long posts only — not ads or chat:

- Vary paragraph length; avoid identical section shapes three times in a row.
- Each section should earn the next (chain rule: line N exists so they read line N+1).
- Do not force setup/payoff beat sheets; use when the piece feels flat.

## Related

- [humanize-workflow.md](humanize-workflow.md) — operational rewrite loop
- [marketing-copy.md](marketing-copy.md) — persuasion structure
- [translation-vs-voice.md](translation-vs-voice.md) — not a translation pipeline
