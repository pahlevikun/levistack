# fr-ca — Canadian French

**Type:** `regional` | **Status:** `validated`

## When to load

`language: french` + `regional_voice: fr-ca`. Québec/Canada lexicon and informatics terms.

## Particle and grammar jobs

| Form | Pragmatic job | Intensity |
|---|---|---|
| `tu (informal)` | Casual peer when register is santai | `sedang+` |
| `courriel` | Email (Canada) | `tipis+` |
| `fin de semaine` | Weekend (not week-end France) | `tipis+` |
| `magasiner` | Browse/shop — avoid in tech unless relevant | `tipis` |

## Examples (bug explanation)

- Il manque `API_TOKEN` dans `.env`, donc `loadConfig` retourne `undefined`. Lance `npm test -- config`.

## Caps

- Do not use France-only terms as default (e.g. e-mail vs courriel).

## What NOT to mix

- France tu/vous assumptions for Canadian formal client without check.

## Forbidden caricature

- France tu/vous assumptions for Canadian formal client without check.
