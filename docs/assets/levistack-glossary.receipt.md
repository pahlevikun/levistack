# levistack glossary

## Source

- Topic: how to start, the words around a run, the nine groups, and every catalog skill
- Audience: someone installing levistack who needs the words, not the route picture
- Platform: README image, next to the same glossary in text. SVG 1040 x 3894, PNG export 2080 x 7788 (2x)

## Evidence pack

| Claim or asset | Status | Source | Limitation |
|---|---|---|---|
| Three ways to start: full route (`/use-levistack` or `/start`), one-shot, bare skill | sourced | `skills/foundation/use-levistack/SKILL.md` (One-shots), `commands/start.md` | A bare `/skill` skips prime, hunt, and deliver |
| Seven steps and what each does | sourced | `skills/foundation/use-levistack/SKILL.md` | The chips are short labels. The sentence under them is the definition |
| Words: playbook, chain, your yes, loaded, file-only, skills.sh, upstream, group, catalog, agent, rule, command, hook | sourced | `use-levistack` SKILL.md, `find-skills` SKILL.md, `commands/start.md`, `hooks/README.md` | One sentence each. The owning file has the rest |
| 68 skills in 9 groups, plus 2 upstream | measured | top-level `skills/<group>/<name>/SKILL.md` on 1 Nov 2026, `upstream.json` | foundation 3, workflow 9, knowledge 6, engineering 8, architecture 7, delivery 15, product 8, focus 3, agent-authoring 9 |
| Modes inside a skill are not catalog entries | sourced | `skills/engineering/output-savers/concise/`, `principles/`, `skills/engineering/noslop/skills/noslop-code/` | concise, concise-light, concise-heavy, principles, noslop-code |
| Each skill line | sourced | that skill's `description`, shortened to one clause | The line is an index. The skill file owns the detail |
| 97 languages, facts unchanged | sourced | `upstream.json` description of `polyglot-copywriter` | Count is the upstream skill's own claim |

## Five-second takeaway

A task starts one of three ways, then a group, then a skill. The list under that is every skill.

## Visual decision

- Primary job: lookup
- Layout family: containment. Ways to start, then the step sequence, then words, then groups that contain skills
- Dominant element: the skill list, grouped
- Accent: slate indigo for the full route and group names, gold for Prove and "Your yes". Both sit on the paper background of the routing graphic
- Production method: one list laid out to SVG, rendered with `rsvg-convert -w 2080`. The same list is the markdown in `README.md` and `skills/foundation/help-levistack/SKILL.md`

## Contrast (computed, sRGB, on `#F3F1EC` unless noted)

| Pair | Ratio |
|---|---|
| `#17152E` ink on paper | 15.72 |
| `#4F5A8F` blue on paper | 5.83 |
| `#4F5A8F` blue on `#ECEDF4` chip | 5.64 |
| `#7A5410` gold on paper | 6.00 |
| `#5E6275` muted on paper | 5.35 |

Body glosses are ink. Muted is for roles, eyebrows, and the closing line. All five pairs are at or above 4.5:1.

## Receipt

- Final file: `docs/assets/levistack-glossary.png`
- Vector source: `docs/assets/levistack-glossary.svg`
- Text equivalent: the Glossary section in `README.md`, and the same section in `skills/foundation/help-levistack/SKILL.md`. The PNG has no text layer
- SVG SHA-256: `3a56acaaa22c0c95616c5db9156b2b5f99abc29813256e3848240d9154988018`
- PNG SHA-256: `a7b03ac9a1dcc4bba21c28d35016229a1d89927d623d0e34047bfe10f78d02f3`
- Current check: rendered at 2080 x 7788 and inspected in slices (header, knowledge and engineering, delivery, agent-authoring through the footer). `gap-analysis`, `qa`, and `create-readme` are in their groups. `setup-pack` is not listed. The footer is on the canvas. No numeric quality score was assigned
- Limitations: at a README width near 900px, 15px source type is about 13px. The markdown under the image is the copy to search. Not checked in print
- Update rule: when a skill is added or renamed, change the line in both markdown glossaries and in the SVG, re-render the PNG, and update the hashes here
