# Translation vs native voice rewrite

Honesty boundaries for voice rewrite vs translation. **Polyglot Voice is not a translation skill.**

## What this skill does

| Task | Polyglot Voice | Dedicated translation workflow |
|---|---|---|
| Write new copy in target language | Yes | Sometimes (mode-dependent) |
| Rewrite stiff / AI text in one language | Yes | No |
| Source → target faithful transfer | **No** | Yes |
| Glossary / TM / chunk pipeline | **No** | Yes |
| Register + dialect overlays | Yes | Rare |

**Voice rewrite** = generate or polish prose **as if a fluent writer drafted in the target language**, with register, overlay, and use-case structure.

**Translation** = preserve source meaning, terminology, and often sentence mapping across languages.

## When to refuse translation framing

User says "translate this to Japanese" with a source block:

1. **Clarify intent:**
   - **Faithful transfer** (legal, UI strings, cited quotes) → recommend a translation skill or human translator; the author can only do *style* pass on already-translated text if they insist on voice polish **without** changing meaning.
   - **Marketing / comms for JP audience** → transcreation: load [locales/japanese.md](locales/japanese.md) + japanese pack; rewrite for outcome, not word alignment.
   - **"Make this sound natural in Indonesian"** → voice rewrite in `indonesia` + register — not EN→ID pipeline.

2. **State the boundary once**, then proceed with the allowed mode.

## Terminology and consistency (adapted from translation workflows)

When user supplies a **glossary** or **forbidden terms** for a rewrite (not full translation):

| Step | Action |
|---|---|
| 1 | Extract product names, approved terms, banned calques |
| 2 | Apply glossary to **new prose only** — never rename code/API identifiers unless task target |
| 3 | One term → one choice per document (no synonym cycling for "variety") |
| 4 | Flag ambiguous terms; ask once instead of guessing |

No TM database, no chunk-by-chunk source alignment — manual consistency only.

## Transcreation (marketing)

For cross-locale campaigns:

- Preserve **intent, emotion, CTA level** — not headline word count or English rhythm.
- Reload [marketing-copy.md](marketing-copy.md) spine + target [culture.md](../languages/) + [locales/](locales/) file when listed in [core.md](../core.md).
- Proof points must stay factually identical; claims cannot be invented in any locale.

## Polish-after-translate (edge case)

If user already ran an external translator and wants "sound human":

- Treat pasted target text as **draft in that language**
- Run [humanize-workflow.md](humanize-workflow.md) + language pack
- **Do not** silently re-translate from a hidden source language
- If meaning drift is suspected, say so and ask for source only if they want fidelity check (outside skill scope)

## Honesty lines (templates)

- "I rewrite in natural {language} — I don't run EN→{language} translation pipelines."
- "For legal or UI string parity, use a translation tool; I can humanize the result if you paste the target text."
- "This is transcreation: same offer, native Japanese structure — not word-for-word."

## Related

- [locales/japanese.md](locales/japanese.md) — JP transcreation patterns
- [natural-writing.md](natural-writing.md) — calque avoidance
