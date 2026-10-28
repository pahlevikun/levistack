# levistack routing stack

## Source

- Topic: the `use-levistack` seven-step route and what wraps the session
- Model: the-catalyst routing stack (same left spine and right envelope, new content and palette)
- Audience: people who install levistack and want to know where to start
- Platform: README image. SVG 1480 x 1440, PNG export 2960 x 2880 (2x)

## Evidence pack

| Claim or asset | Status | Source | Limitation |
|---|---|---|---|
| Seven steps: route, prime, invoke, hunt, apply, prove, deliver | verified | `skills/workflow/use-levistack/SKILL.md` | Hunt is skipped for a named skill |
| Prime and deliver use `output-savers`, deliver also uses `polyglot-copywriter` | verified | `playbooks/prime.md`, `playbooks/deliver.md` | `polyglot-copywriter` is an upstream plugin |
| Invoke picks from the intent map | verified | `skills/workflow/use-levistack/playbooks/invoke.md` | The graphic shows 12 of the map's first picks. It does not list every mode or skill |
| Hunt: at most three questions, chain of up to four, skills.sh only for a gap | verified | `skills/workflow/find-skills/SKILL.md` | |
| Prove: verify, then your yes for outward actions, then a re-check | verified | `playbooks/prove.md` | |
| 51 skills in 8 groups, with the per-group counts shown | verified | `skills/catalog-metadata.json`, `skills/*/*/SKILL.md` | Nested skills (`noslop-code`, `output-savers` modes) not counted |
| Parallel work is coordinated by `rumbling`; completed work is judged by `evidence` | verified | `skills/workflow/rumbling/SKILL.md`, `skills/workflow/evidence/SKILL.md` | The graphic names the relation, not every mode |
| 42 rules, 5 always on, per-topic counts | verified | `rules/*/*.md`, a line `alwaysApply: true` in the frontmatter of `rules/core/*.md` (the session-start hook uses the same test) | The graphic names seven core rules as examples |
| 11 agents | verified | `agents/*.md` | |
| 15 commands, including the four named in the graphic (`/start`, `/evidence`, `/rumbling`, `/ship`) | verified | `commands/*.md` | The graphic names four of the 15 |
| 5 opt-in hooks and what each does | verified | `hooks/*.mjs`, README Hooks table | |
| 2 upstream plugins installed as dependencies | verified | `upstream.json`, test install with an isolated Claude config | Claude Code only; skills CLI users install them separately |

## Five-second takeaway

After seeing this image for five seconds, the viewer should understand that every task takes the same seven steps, and the path ends at proof and your yes.

## Visual decision

- Primary job: map
- Layout family: convergence (one spine narrows to the human gate), with a side envelope
- Dominant element: the spine from `use-levistack` down to YOUR YES
- Accent colors: slate indigo for the agent's path, gold for the human gate (both from Murk, the mascot, in `docs/assets/murk.svg`)
- Production method: hand-written deterministic SVG, rendered with `rsvg-convert -w 2960`

## Final overlay copy

- Title: Every task takes the same seven steps.
- Supporting line: Nothing counts as done without proof. Nothing leaves the session without your yes.
- Entry line: Type /start (or /use-levistack) and your task. It picks the skill, runs it, proves it and shapes the reply.
- Steps: Route, Prime, Invoke, Hunt, Apply, Prove, Deliver
- Envelope: rules, hooks, one-shot, agents, focus, upstream plugins
- Source line: 51 skills, 11 agents, 42 rules, 15 commands, 5 hooks, 2 upstream, 28 Oct 2026

## Receipt

- Final file: `docs/assets/levistack-routing-stack.png`
- Vector source: `docs/assets/levistack-routing-stack.svg`
- SVG SHA-256: `8b0965ed71da47104a3443a3f879b5d229d263399eb0a17b5ab2ee2dca474ea8`
- PNG SHA-256: `25a023cb3a36bc7dfe7ca35140bd4928869312b4b479ac0b3a4c9246f55499ad`
- Current check: re-rendered at 2960 x 2880 and visually inspected. Counts and the evidence/rumbling relation fit the existing boxes without clipping. No numeric quality score was assigned.
- Limitations: the title and the spine survive a thumbnail. Box detail needs the full image. The skeleton follows the-catalyst graphic on purpose, so the two read as one family.
- Last change: renamed `evidence-workflow` to `evidence`, added `rumbling` and two commands, and corrected the group counts after the delivery/knowledge moves and documentation additions. Footer date 28 Oct 2026.
- Update rule: when a count or step changes, edit the SVG, re-render the PNG, and update the hashes here.
