# Mode: decision-map

A compact, stateful markdown map so the next session does not re-litigate. Fill `templates/decision-map.md`. Optional mindmap aid: `mindmap.md`.

## When

User says decision map, tracking decisions, resume this planning later, or the thread already has more than a handful of locked trade-offs.

## Rules

- One file (or one section in an existing doc they name). Default path: `docs/decisions/<subject-slug>.md` unless they give a path. Create lazily.
- Three buckets only: **Decided**, **Open**, **Deferred**. Each row: id, choice or question, one-line why / blocker, date.
- Facts get a `Source:` path, not a decision row.
- Update in place as grilling continues. Do not fork versions.
- This is **not** an implementation-plan file. If they want tasks and test steps, `write-plan`. If they want to pause the session, `handoff` can point at this map.

## Huge work (more than one session)

Use this when the job is too big for one session and you cannot see the way to the end yet. The map helps you **find the way**. It does not do the work. You can run it with plain files. No issue tracker is needed.

**Start with the destination.** Write one or two lines on what "done" looks like: a spec to hand off, a decision to lock, or a change to make in place. It sets the scope, so settle it first.

**Add three lists to the map file:**

| List | Holds |
|---|---|
| **Settled** | One line per closed decision, with a short gist and a link to the file that holds the detail. Each decision lives in one place only. |
| **Unclear yet** | Decisions you can feel coming but cannot phrase sharply. Test: can you state the question precisely now? If yes, it is a decision to schedule. If not, it stays here. Do not cut this list into ticket-sized pieces. |
| **Parked** | Work you chose to leave out of this effort, with one line on why. It only comes back if the destination changes. |

**Make one file per decision,** small enough for one session. Give each a clear title, and refer to it by title, never by a bare number.

**Tag each decision with how it gets settled:**

| Kind | How it is settled |
|---|---|
| **Look it up** | You read docs, code or sources. No person needed. |
| **Try it rough** | You build something cheap and rough for people to react to. |
| **Talk it through** | A live conversation with the user. Never answer your own questions for them. |
| **Do a chore first** | Manual work that must happen before anyone can decide, such as signing up for a service so its API can be judged. |

**Write what each decision waits on.** The **ready list** is every open decision whose waits are all settled. Work from the ready list, in order. Settle one decision per session, except look-it-up ones.

**After each decision:** record the answer, close the file, add a line to Settled, and move anything that is now sharp from Unclear yet to its own decision file. Move anything now past the destination to Parked.

**No unclear areas at all?** Then the way is clear and the job fits one session. Skip the map and use `write-plan`.

## Do not

- Encode owner/sprint/ticket fields unless they asked (that is `create-tickets`).
- Dump the whole chat log into the file.
