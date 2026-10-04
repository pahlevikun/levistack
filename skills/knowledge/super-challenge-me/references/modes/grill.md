# Mode: grill

Walk the design tree of a plan, idea, design, or architecture. Manager in a review: numbered questions, a rec, wait. Loop: `interview-loop.md`. Shape: `round-format.md`.

## When

User says grill me, stress-test this plan, walk the decisions, design review questions. No existing domain docs required (if `CONTEXT.md` / ADRs exist, prefer **grill-docs** or combine).

## Do

1. One-line subject + constraints you already know.
2. Build an implicit tree: goals, non-goals, actors, success, failure, data, edges, rollout. Do not print the whole tree; ask the next highest-leverage node.
3. Cadence from **calibrate** (default one-at-a-time; frontier round if they asked).
4. After three obvious options on a node, add one non-obvious (`interview-loop.md`).
5. Stop at shared understanding. Offer a decision map if the thread will span sessions.

## Do not

- Invent a target stack (`super-tech-blueprint`).
- Write the implementation-plan file (`writing-plans`) or start the refactor (`super-refactor`).
- Ask trivia the repo answers (`facts-vs-decisions.md`).
