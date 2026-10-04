---
name: super-challenge-me
description: "Stress-test a document, plan, idea, design, or architecture by grilling like a critical manager: numbered questions with recommended answers, glossary and ADR alignment, blunt challenge of estimates and hidden work, plus structured brainstorming and a compact decision map. Use when the user says grill me, grill this doc, stress-test this plan, challenge this idea, poke holes, decision-map, or brainstorm a design before coding. Not for executing a refactor (super-refactor), writing implementation-plan files (writing-plans), or inventing a target stack (super-tech-blueprint)."
metadata:
  version: "1.0.0"
---

# Super challenge me

One interview skill for a **document, plan, idea, design, architecture, or anything else** that needs shared understanding. Act like a manager: critical questions, then brainstorming, then a locked map of decisions. Stop there unless the user asks to write a plan artifact or tickets.

Research notes: [research-synthesis.md](references/core/research-synthesis.md). Question shape: [round-format.md](references/core/round-format.md), [templates/round.md](templates/round.md).

## Principles

1. **Facts vs decisions.** Look up what the repo or docs already answer. Only the user decides trade-offs. See [facts-vs-decisions.md](references/core/facts-vs-decisions.md).
2. **Numbered question + recommended answer, then wait.** Never dump an interrogation without a rec. Default one-at-a-time; switch to a frontier round when the user asks or after **calibrate**.
3. **Attack the work, not the person.** Intensity is a dial. Thermonuclear is off unless they opt in ([intensity.md](references/core/intensity.md)).
4. **Past the first three.** Do not stop at the obvious answers; force at least one non-obvious option, then pick. Not a multi-agent loop.
5. **Stop at shared understanding.** Do not execute a refactor, invent a stack, or write `docs/superpowers/plans/*.md` unless the user asks. Then hand off (peers below).
6. **Language-agnostic.** The round format works in any language; do not load a second language pack.

## Step 0: pick a mode

Do this first; do not announce it. Load only that mode file plus the core files it names.

| If the user wants… | Mode | Load |
|---|---|---|
| Walk a design tree, grill me, stress-test this plan/idea/architecture | **grill** | [grill.md](references/modes/grill.md) |
| Grill against CONTEXT.md, glossary, ADRs, existing docs | **grill-docs** | [grill-docs.md](references/modes/grill-docs.md) |
| Blunt advisor: estimates, hidden work, overcomplication | **challenge** | [challenge.md](references/modes/challenge.md) |
| Ideas → design before implementation (new or existing product) | **brainstorm** | [brainstorm.md](references/modes/brainstorm.md) |
| Compact stateful map across sessions | **decision-map** | [decision-map.md](references/modes/decision-map.md) |
| Softer/harder, one-at-a-time vs frontier-round | **calibrate** | [intensity.md](references/core/intensity.md) |
| Mermaid/PlantUML as an aid, not a diagram takeover | **mindmap** | [mindmap.md](references/core/mindmap.md) |

**Precedence:** explicit mode → artifact (docs present → **grill-docs**; "too big"/"hidden work" → **challenge**; "just an idea"/no design yet → **brainstorm**; resume later → **decision-map**) → default **grill**. Combine **grill** + **grill-docs** when they bring a plan *and* domain docs. Run **calibrate** whenever they say softer, harder, batch, or one-by-one; keep the setting for the session.

Loop mechanics: [interview-loop.md](references/core/interview-loop.md). Frontier rounds: [frontier.md](references/core/frontier.md).

## Domain tracks (optional)

Subject is not a mode. After the mode, load at most one stub if the artifact is clearly in that world. Index and how to add a track: [domains/README.md](references/domains/README.md).

| Subject | Stub |
|---|---|
| Product / marketplace / new vs existing offering | [product.md](references/domains/product.md) |
| Engineering / architecture / APIs | [engineering.md](references/domains/engineering.md) |
| UI, UX, visual design | [design-ui.md](references/domains/design-ui.md) |
| Prose, specs, narrative docs | [writing.md](references/domains/writing.md) |

## Peers (do not duplicate)

| Job | Skill |
|---|---|
| Current-repo facts, smells, `ARCHITECTURE.md` | `super-codebase-learner` (diagnose pairs with **grill-docs**) |
| Target stack / migration blueprint | `super-tech-blueprint` — do not invent stacks here |
| Execute a refactor | `super-refactor` |
| Write the implementation-plan file | `writing-plans` |
| Pause/resume the session | `handoff` |
| Tickets after grilling | `create-jira-story` |

Do not absorb `do` / `make-plan` orchestrators. If they want subagent execution, point at `writing-plans` then `handoff`.

## Layout

```
super-challenge-me/
├── SKILL.md
├── references/core/      # loop, frontier, facts vs decisions, intensity, round rules, mindmap, research
├── references/modes/     # grill, grill-docs, challenge, brainstorm, decision-map
├── references/domains/   # optional stubs + contribution README
└── templates/            # round.md, decision-map.md, context.md
```

Templates: [round.md](templates/round.md), [decision-map.md](templates/decision-map.md), [context.md](templates/context.md).

## Old skill name

| Old | Use |
|---|---|
| `grill-with-docs` | This skill, usually **grill-docs** |

## Done when

- The matching mode ran; only needed references were loaded.
- Every asked question had a number and a recommended answer; the user made the decisions.
- Facts cited a file, doc, or "unknown — looked, not found."
- Shared understanding is written (answers, glossary/ADR updates if **grill-docs**, or a decision map if they asked).
- No implementation-plan file, refactor, or invented stack unless they explicitly asked for that handoff.
