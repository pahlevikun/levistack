---
name: later-list
description: "Put a tangent on the later list (one line in LATER.md) and go back to the current task, then sort the list at a natural break (do now, schedule, drop). Applies to the user's ideas and to side issues the agent finds while working, such as an unrelated bug, refactor or doc gap. Use when the user says 'park this', 'note that for later', 'side quest', 'remind me', or when a new idea or unrelated fix shows up mid-task. Not for blockers of the current task (handle those now)."
---

# Later list

Tangents are fine. Chasing them mid-task is how the first task never gets finished.

## Steps

1. **Name the current task in one line**, so you know what you return to.
2. **Check it can wait.** If the current task cannot finish without it, it is a blocker. Say so and handle it now.
3. **Append one line** to `LATER.md` at the repo root (create it if missing; outside a repo, use the cwd):
   ```
   - [ ] 2026-10-25 · <idea or issue> · <why it might matter> · <file or link, if any>
   ```
   Keep it to one line. A long entry is a new task in disguise.
4. **Do not research, fix or start it.** Capturing it is the whole job. An agent that found an unrelated bug lists it and does not fix it in this diff.
5. **Go back** to the step you were on and say which step that is.

## Sort at a break

At a natural break (end of a round, before a handoff, end of the day), read `LATER.md` and decide for each open line:

| Decision | Do |
|---|---|
| Do now | It is small and related. Do it next, then tick it `[x]` |
| Schedule | Move it to a ticket, plan or handoff note, then tick it with a pointer |
| Drop | Delete the line |

Ticked lines older than a week can go.

## Pitfalls

- Do not ask the user before adding a line. Add it, tell them in one line, and continue.
- Do not commit `LATER.md` unless the user wants it tracked. Mention it once if it is untracked.

## Related skills

- `get-moving`: pick the next step after you list a tangent.
- `write-plan`: an item on the list grew into real work.
- `handoff`: carry open items into the next session.
