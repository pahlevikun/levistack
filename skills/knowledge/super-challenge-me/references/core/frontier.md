# Frontier rounds

Use when **calibrate** is set to frontier-round, or when serial one-at-a-time would stall (many independent unknowns, user said "batch", "grill me faster").

A **frontier** is every question that can be answered *now* without depending on an unanswered sibling. Dependent questions wait for the next round.

## How to run a round

1. List open decision points. Drop any that a file already answers (look them up; do not ask).
2. Keep only independent items (answering A does not require B). Cap at **5–7** per round. If more remain, pick the highest leverage and park the rest for round N+1.
3. Emit them as one numbered block using `templates/round.md`. Each item still has a recommended answer.
4. Wait for the batch. Accept partial answers; unanswered items roll forward.
5. After answers, recompute the frontier (new dependents may unlock). Repeat.

## vs one-at-a-time

| | One-at-a-time | Frontier-round |
|---|---|---|
| Default | Yes | Only on request or after calibrate |
| Wait | After every question | After the round |
| Risk | Slow | Overwhelming if you dump dependents too |

Do not mix: if they asked for one-at-a-time, do not sneak a five-question dump. If they asked for a frontier round, do not drip one question after they already said batch.
