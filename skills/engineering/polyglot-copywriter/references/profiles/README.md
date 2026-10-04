# Voice profiles index

Short (~30–50 line) snapshots agents can load when an overlay matches — **163 profiles**, one per registry overlay. Fictional fixtures in [fictional-catalog.json](../fictional-catalog.json) have no overlays or profiles. **Authoritative rules** stay in `references/languages/<lang>/overlays/<id>.md` — profiles summarize when to load and what not to do.

Machine index: [index.json](index.json) (full list). Schema: [schema/profiles.schema.json](../schema/profiles.schema.json). Coverage enforced by `tests/test_profiles.py`.

## When profile vs overlay pack

| Load | When |
|---|---|
| **Language pack** | Always — `references/languages/<id>/pack.md` |
| **Overlay pack** | `regional_voice` set — full dialect rules |
| **Profile** (this folder) | Quick orientation after overlay id resolved; optional if overlay already loaded |

Profiles do not replace overlay files. Use both when the agent needs a fast reminder without re-reading the full overlay.

## Profile → language + overlay id

| Profile file | `language_id` | `overlay_id` |
|---|---|---|
| [english-netral.md](english-netral.md) | `english` | `us` / `netral` |
| [uk.md](uk.md) | `english` | `uk` |
| [au.md](au.md) | `english` | `au` |
| [in-en.md](in-en.md) | `english` | `in-en` |
| [us-slang.md](us-slang.md) | `english` | `us-slang` |
| [singlish.md](singlish.md) | `english` | `singlish` |
| [jaksel.md](jaksel.md) | `english` | `jaksel` |
| [jakarta.md](jakarta.md) | `indonesia` | `jakarta` |
| [surabaya.md](surabaya.md) | `indonesia` | `surabaya` |
| [bandung.md](bandung.md) | `indonesia` | `bandung` |
| [yogyakarta.md](yogyakarta.md) | `indonesia` | `yogyakarta` |
| [medan.md](medan.md) | `indonesia` | `medan` |
| [makassar.md](makassar.md) | `indonesia` | `makassar` |
| [tokyo.md](tokyo.md) | `japanese` | `tokyo` |
| [kansai.md](kansai.md) | `japanese` | `kansai` |
| [seoul.md](seoul.md) | `korean` | `seoul` |
| [busan.md](busan.md) | `korean` | `busan` |
| [zh-cn.md](zh-cn.md) | `mandarin` | `zh-cn` |
| [zh-tw.md](zh-tw.md) | `mandarin` | `zh-tw` |
| [es-mx.md](es-mx.md) | `spanish` | `es-mx` |
| [es-ar.md](es-ar.md) | `spanish` | `es-ar` |
| [es-bo.md](es-bo.md) | `spanish` | `es-bo` |
| [es-pe.md](es-pe.md) | `spanish` | `es-pe` |
| [es-cl.md](es-cl.md) | `spanish` | `es-cl` |
| [it-it.md](it-it.md) | `italian` | `it-it` |
| [it-ch.md](it-ch.md) | `italian` | `it-ch` |
| [ta-in.md](ta-in.md) | `tamil` | `ta-in` |
| [ta-lk.md](ta-lk.md) | `tamil` | `ta-lk` |
| [pa-in.md](pa-in.md) | `punjabi` | `pa-in` |
| [pa-pk.md](pa-pk.md) | `punjabi` | `pa-pk` |

See [index.json](index.json) for all 163 profiles. See [configuration.md](../configuration.md) for aliases that set `regional_voice`.
