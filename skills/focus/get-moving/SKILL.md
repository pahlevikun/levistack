---
name: get-moving
description: "Get moving when stuck, overwhelmed or avoiding a task: name what kind of stuck it is, shrink the goal to one physical next action, and run one 25-minute round with a finish line. Use when the user says they are stuck, overwhelmed, do not know where to start, have too much to do, keep putting something off, or asks 'what should I do next'. Not for picking a skill (use-levistack) or planning a whole project (write-plan)."
---

# Get moving

When everything feels equally urgent, pick one physical action and start it. One round, one finish line.

## Steps

1. **Read before asking.** Check the cwd, `git status`, the latest handoff note and `LATER.md` if they exist. They often already say what the goal and the last step were.
2. **Name the kind of stuck.** Pick one. Say it in one line.

   | Kind | Sign | Move |
   |---|---|---|
   | Too many things | Three or more goals compete | Ask "which one hurts most if it waits a day?" Put the rest on `later-list` |
   | Vague goal | The goal needs more than one sentence | Split it. Pick one half. If it is still unclear, use `challenge-me` |
   | Blocked | Waiting on a person, an answer or access | The next action is the message that unblocks it. Draft it now |
   | Avoiding | The task is clear but does not start | Shrink the action until it feels too small to skip |
   | Lost the thread | Came back after a break | Read the handoff note or the last commit, then take the next unchecked step |

3. **Write one next action.** It starts with a verb, takes under 25 minutes, and can start right now. "Open `auth.ts` and write the failing test for expired tokens", not "work on auth".
4. **Set the finish line.** One line: what exists when this round is done.
5. **Run the round.** Do only that action for 25 minutes. A tangent goes to `later-list`, not into the work.
6. **Close the round.** Continue, switch or stop. Before you leave, write the next action down (in the handoff note, `LATER.md` or the reply).

## Output

```
Stuck: <kind> — <one line why>
Next action (25 min): <verb + object + where>
Done for this round: <finish line>
```

## Pitfalls

- If the action is still vague, shrink it again. "Open the file" counts.
- Do not plan the whole project. One step.
- Do not ask more than one question. If the workspace answers it, do not ask.

## Related skills

- `later-list`: a tangent shows up during the round.
- `challenge-me`: the goal is too vague to name a first step.
- `write-plan`: the goal is large and needs a real plan.
- `handoff`: you stop for the day.
- `use-levistack`: you know the task but not which skill fits.
