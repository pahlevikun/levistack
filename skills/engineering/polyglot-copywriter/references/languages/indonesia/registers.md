# Bahasa Indonesia registers

| Register | Config key | When |
|---|---|---|
| Formal (EYD) | `baku` | Surat resmi, hukum, investor — on request |
| Semi-formal / work | `profesional` | Email kerja, LinkedIn, deck — on request |
| Kasual | `santai` | **Default**: chat, penjelasan, everyday writing |

## Pronouns and address (default santai)

- **Self:** `saya` (not `gue`/`aku` unless user asks for gaul or a city overlay explicitly allows it).
- **Addressee:** `mas` / `kak` + name in internal work chat; `Anda` or name only in external formal.
- **Team:** `kita` for inclusive team actions; avoid `kita` in formal `baku` where `kami` is required.

## What santai is not

- **Not automatically `gue`/`lo`.** the author's everyday Indonesian is `saya` + `mas`/`kak`.
- Not Gen-Z slang quota (`gas`, `mantul`) in technical diagnosis or incident text.
- Not dropping grammar in email or letters — those use `profesional` or `baku` when requested.

## Simple prose default

Every register uses [simple-prose.md](../../simple-prose.md): kata sehari-hari, kalimat pendek, satu ide per kalimat. `baku` dan `profesional` mengubah **bentuk** resmi, bukan kosakata langka atau kalimat bersarang demi terdengar pintar.

## Register upgrade signals

| User says | Set |
|---|---|
| formal, baku, surat resmi | `register: baku` |
| profesional, email kerja | `register: profesional` |
| santai, kasual, gaul (without banning saya) | `register: santai` |
| gue/lo, very Jakarta gaul | `regional_voice: jakarta` + honor user ban on pronouns |

Legacy detail for formal/semi-formal examples: see [bahasa-registers.md](../bahasa-registers.md) for extended samples; **default pronoun rule above overrides** Register 3's `gue`/`lo` default for the author santai.
