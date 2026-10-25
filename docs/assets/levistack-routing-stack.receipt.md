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
| Invoke picks from the intent map | verified | `playbooks/invoke.md` | The graphic shows 12 of the map's first picks. `how` was merged into `codebase-learner` (explain mode) |
| Hunt: at most three questions, chain of up to four, skills.sh only for a gap | verified | `skills/workflow/find-skills/SKILL.md` | |
| Prove: verify, then your yes for outward actions, then a re-check | verified | `playbooks/prove.md` | |
| 41 skills in 8 groups, with the per-group counts shown | verified | `skills/*/*/SKILL.md` | Nested skills (`noslop-code`, `output-savers` modes) not counted |
| 41 rules, 5 always on, per-topic counts | verified | `rules/*/*.md`, a line `alwaysApply: true` in the frontmatter of `rules/core/*.md` (the session-start hook uses the same test) | The graphic names seven core rules as examples |
| 11 agents | verified | `agents/*.md` | |
| 13 commands, and the five named in the graphic (`/start`, `/commit`, `/ship`, `/palette`, `/screen`) | verified | `commands/*.md` | The graphic names five of the 13 |
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
- Source line: 41 skills, 11 agents, 41 rules, 13 commands, 5 hooks, 2 upstream, 25 Oct 2026

## Receipt

- Final file: `docs/assets/levistack-routing-stack.png`
- Vector source: `docs/assets/levistack-routing-stack.svg`
- SVG SHA-256: `989e26bb710040dbf5559cd236fc333ca9f260f9ebd1bbdb5c2d173861b53452`
- PNG SHA-256: `844e954d5f88f8630a6e4d6ae2d6cdab0163c0a725d0ef33b5c771bc68853af8`
- QA score: 14 / 16 (mobile legibility 1, batch originality 1)
- Limitations: the title and the spine survive a thumbnail. Box detail needs the full image. The skeleton follows the-catalyst graphic on purpose, so the two read as one family.
- Last change: removed one core rule (rules 42 to 41, core 15 to 14), added the 13 commands and the `/start` entry line, and one commands line in the one-shot box.
- Update rule: when a count or step changes, edit the SVG, re-render the PNG, and update the hashes here.
