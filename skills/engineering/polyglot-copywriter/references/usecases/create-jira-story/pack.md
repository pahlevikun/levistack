# create-jira-story — use case pack

**Status:** `validated`

## When to load

Jira story, task, or ticket **description** prose (not the summary title unless the user asks to polish it too).

## Sentence 1 job

State the user or business need in plain words (who, what pain, why now).

## Section order

1. Context / Background
2. Goal
3. Definition of Done (bullets, verb-first, testable)
4. Out of scope (only when needed)
5. Technical notes (optional)

## Default register

`santai` + [simple-prose.md](../../simple-prose.md) (STE-style simple vocabulary, short sentences)

## When invoked by create-jira-story

- Scope: description sections only. Do not rewrite issue keys, project codes, API paths, or `file:line` references.
- Mode: **rewrite** on a draft the agent already structured; do not add acceptance criteria the source did not imply (use `[TK]` per [substance.md](../../substance.md) if a fact is missing).
- Do not add chatbot wrappers ("Here is your story", "Let me know if…").
- Summary line (Jira title): one short imperative phrase if included in the pass.

## Aliases (registry)

`jira story`, `jira ticket`, `Jira task`, `backlog item`, `user story`, `create jira`
