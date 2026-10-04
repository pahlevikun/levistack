# Language selection

Read when the user asks for a language other than English or Bahasa Indonesia, sets `language` to a registry id, or asks for a regional *language* (not just Indonesian city style).

Language, dialect, regional voice, sociolect, and speech level are different axes. See [configuration.md](../configuration.md).

## Registry

[registry.json](../registry.json) is the plug-in index for **real** languages and use cases (schema v2). Fictional honesty fixtures (`atlantis`, `klingon`, `elvish`, `navi`) are in [fictional-catalog.json](../fictional-catalog.json) (schema v1). Neither catalog is the 718-language Peta Bahasa dump. Search matching entries only:

```bash
python3 scripts/find_language.py <name|alias|region>
```

Each language row has:

- `id` — config key
- `name`, `aliases`, `iso`
- `support.status` — always `validated` (load the pack)
- `support.pack` — `references/languages/<id>/pack.md`
- `overlays[]` — typed rows (`regional`, `slang`, `mix`) with `file` paths
- `speech_levels[]` — when the language has level systems (Jawa, Sunda, Bali, Japanese, Korean)
- `umbrella` — if true, ask for a more specific language before thick prose

Legacy [languages.json](languages.json) mirrors ids for backward compatibility — prefer `registry.json`.

## Capability

All registry languages are **validated**. Load `pack.md` + `registers.md` for everyday writing; add `culture.md` and one overlay when the user asks for cultural colour, slang, city, or speech level.

Honesty still applies when:

- The language is **umbrella** (`arabic`, `dayak`) — ask which variety.
- The pack is **limited** (`abui`, `kashmiri`, `quechua`, `guarani`, `latin`, `hokkien`, …) — follow `pack.md` honesty; do not invent forms.
- The pack is **fictional** — resolve id in [fictional-catalog.json](../fictional-catalog.json); honesty fixture only; fall back to Indonesian or English; do not invent vocabulary.
- The name is **not in either catalog** — state the limit; offer English or Indonesian, or ask for examples.

## Resolution

1. Match name or alias in registry (case-insensitive). Use `find_language.py` when you can run it.
2. If one name hits several entries and the difference changes output, ask which language or variety.
3. Load `support.pack`, `registers.md`, and `culture.md` when needed.
4. For umbrella or limited packs, follow `pack.md` before drafting thick prose.

Egyptian Arabic (`arz`) is not MSA (`arabic`). Malay is not Indonesian. `language: makassar` is not `regional_voice: makassar` on Indonesian.

## Language vs regional voice

```yaml
farhan_voice:
  language: indonesia
  regional_voice: jakarta
```

```yaml
farhan_voice:
  language: makassar   # Makassarese language pack
  regional_voice: netral
```

## Coverage

97 real languages, 4 fictional fixtures, 163 overlays, 18 use cases — see [README.md](../../README.md) for the full matrix and counts.
