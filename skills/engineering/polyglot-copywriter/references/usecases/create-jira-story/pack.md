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

## Problem first

Every story needs a problem to solve, told from the user's side. If the request holds only implementation steps ("move the export to a queue worker"), ask once: "What problem does the user have today?" Do not invent one. If you cannot ask, write `[TK: what problem does this solve for the user?]` under Context.

Write the what and the why. Add the how only when the team has already decided it. Do not turn raw brainstorming into a ticket unless the user asks.

Before:

> Exports over 20k rows time out after 30 seconds and users just get an error. We should probably move the export job off the request thread and put it on a queue, maybe with a worker pool, and then store the file somewhere and email a link.

After:

> Context. Exports of more than 20k rows time out after 30 seconds, so users get an error and no file.
>
> Goal. Users can export any size and get the file when it is ready.
>
> Definition of Done.
> - An export above 20k rows finishes without a timeout.
> - The user gets a link when the file is ready.

## Default register

`santai` + [simple-prose.md](../../simple-prose.md) (STE-style simple vocabulary, short sentences)

## When invoked by create-jira-story

- Scope: description sections only. Do not rewrite issue keys, project codes, API paths, or `file:line` references.
- Mode: **rewrite** on a draft the agent already structured; do not add acceptance criteria the source did not imply (use `[TK]` per [substance.md](../../substance.md) if a fact is missing).
- Do not add chatbot wrappers ("Here is your story", "Let me know if…").
- Summary line (Jira title): one short imperative phrase if included in the pass.

## Aliases (registry)

`jira story`, `jira ticket`, `Jira task`, `backlog item`, `user story`, `create jira`
