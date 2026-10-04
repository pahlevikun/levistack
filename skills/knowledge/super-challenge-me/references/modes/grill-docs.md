# Mode: grill-docs

Grill a plan or idea **against existing domain docs**, then update those docs as names crystallize. This is the former `grill-with-docs` skill. Pairs with `super-codebase-learner` **diagnose** for in-place deepening (same stack, deeper module). Loop: `interview-loop.md`.

## When

User says grill this doc, stress-test against CONTEXT, glossary, ADRs, domain model, or they have `CONTEXT.md` / `docs/adr/` and a plan.

## 1. Explore domain context first

Read before the first question:

- `CONTEXT.md` — existing domain terminology
- `docs/adr/` — prior architectural decisions
- Relevant source files for current behavior
- `CONTEXT-MAP.md` at repo root when it exists (monorepo: each context has its own `CONTEXT.md` and `docs/adr/`)

Create those files **lazily** — only when you have something to write. Snippet: `templates/context.md`.

If current-architecture facts are missing, load `super-codebase-learner` rather than guessing.

## 2. Three stress-test mechanisms

**Glossary alignment** — User term conflicts with CONTEXT.md:

> Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?

**Precision sharpening** — Vague or overloaded words; propose a canonical name:

> You're saying 'account' — do you mean the Customer or the User? Those are different things.

**Scenario probes** — When they discuss relationships, hit the boundary with a concrete scenario (partial vs whole, retry vs duplicate, guest vs user).

Generalize to **whatever domain docs this repo uses** (not a health, SRHR, or fiction-writing pack). Specs, glossaries, tone guides, and ADRs all count.

## 3. Update docs inline

When a term is resolved, update `CONTEXT.md` immediately. Do not batch.

**ADRs** — create only when all three are true:

1. Hard to reverse (meaningful cost to change later)
2. Surprising without context (a future reader would ask "why?")
3. Result of a real trade-off (genuine alternatives existed)

If any condition is missing, skip the ADR. ADR shape: title, status, context, decision, consequences.

## 4. Cross-reference with code

When they state how something works, verify the code. Surface contradictions:

> Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?

## File formats

- `CONTEXT.md`: terms meaningful to domain experts (no implementation details)
- After diagnose: if they reject a deepening with a **load-bearing** reason, offer an ADR so a future diagnose pass does not re-suggest it (skip ephemeral "not now")

## Do not

- Choose a target stack (`super-tech-blueprint`).
- Write implementation tickets (`create-jira-story` after they ask).
- Run general code review (use the review skill the repo uses).
