# Domain tracks

Optional stubs loaded **after** the mode. They add question lenses, not new skills.

## Add a track

1. Create `references/domains/<slug>.md` (hyphen slug, same idea as the skill name).
2. Include: when to load, typical artifacts, 5–8 lenses (questions you always consider), and a **Do not** that points at a peer skill instead of duplicating it.
3. Add one row to the domain table in `SKILL.md` and mention the new filename there (lint requires the basename to appear in some markdown file of this skill).
4. Do not add a mode. Do not paste an industry playbook. Keep the stub under ~40 lines.

## Existing stubs

| File | Load when the subject is… |
|---|---|
| `product.md` | Offering, marketplace, packaging, new vs existing product |
| `engineering.md` | Services, APIs, architecture of a system (not stack shopping) |
| `design-ui.md` | UI/UX, layout, flows, visual design |
| `writing.md` | Prose, specs, narrative or policy docs |

Generalize vertical grilling (health, fiction, etc.) into `writing.md` or `grill-docs.md` via whatever domain docs the repo already has.
