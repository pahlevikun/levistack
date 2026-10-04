# Mode: decision-map

A compact, stateful markdown map so the next session does not re-litigate. Fill `templates/decision-map.md`. Optional mindmap aid: `mindmap.md`.

## When

User says decision map, tracking decisions, resume this planning later, or the thread already has more than a handful of locked trade-offs.

## Rules

- One file (or one section in an existing doc they name). Default path: `docs/decisions/<subject-slug>.md` unless they give a path. Create lazily.
- Three buckets only: **Decided**, **Open**, **Deferred**. Each row: id, choice or question, one-line why / blocker, date.
- Facts get a `Source:` path, not a decision row.
- Update in place as grilling continues. Do not fork versions.
- This is **not** an implementation-plan file. If they want tasks and test steps, `writing-plans`. If they want to pause the session, `handoff` can point at this map.

## Do not

- Encode owner/sprint/ticket fields unless they asked (that is `create-jira-story`).
- Dump the whole chat log into the file.
