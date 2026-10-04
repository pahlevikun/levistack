# Academic writing techniques

Load when use case is **`academic`**, or user asks for paper, abstract, thesis section, literature summary. All languages.

**Boundary:** this skill helps *write* academic prose structure — not peer-review critique (see `peer-review` use case separately).

## Sentence 1 job

Contribution, claim, or recommendation — not flattery opener.

## Section order (typical)

1. **Contribution / thesis** — what this work adds
2. **Evidence** — methods, results (user-supplied)
3. **Limitations** — honest scope
4. **Conclusion / recommendation** — if requested

## Register

Default `baku`. No the author slang, marketing superlatives, or chat particles unless user quoted them.

## Cross-language rules

- Citations and bibliography format: follow user/journal — do not invent references
- Passive voice OK where discipline expects it; still prefer clear agent when possible
- Technical terms: discipline-standard; protected symbols unchanged
- No fabricated p-values, sample sizes, or author names

## Locale routing

| Language | Locale file |
|---|---|
| japanese | [locales/japanese.md](locales/japanese.md) § Academic |
| indonesia | [locales/indonesia.md](locales/indonesia.md) § Academic |

Other languages: follow [languages/<id>/pack.md](../languages/) `register: baku` examples.

## Good vs bad

| Bad | Good |
|---|---|
| This groundbreaking study revolutionizes the field | We measure latency under 10k RPS using the setup in Section 3 |
| The authors did amazing work | The method in Table 2 controls for selection bias via … |

## Related

- [usecases/academic/pack.md](../usecases/academic/pack.md)
- [docs-prose.md](docs-prose.md) — when doc is internal guide not paper
