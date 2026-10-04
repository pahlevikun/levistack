# Mode: brainstorm

Ideas → a design the user agrees with **before** implementation. Tracks (not separate skills): new product vs existing product. Loop: `interview-loop.md`.

## When

User says brainstorm, ideate, think through this, design this before we code, new product, existing product feature.

## Tracks

Pick one; say it in a line.

| Track | Signal | Extra lenses |
|---|---|---|
| **New product** | Greenfield, 0→1, "what should we build" | Who is it for, why now, what "working" means, what you will not build |
| **Existing product** | Feature on a live system | Current behavior (look it up), who already depends on it, migration/compat, what not to break |

Other subjects (architecture sketch, UI concept, writing outline) stay on the matching domain stub after this mode.

## Do

1. **Do not implement.** No production patches, no "quick spike in the repo" unless they explicitly want a spike and you labeled it disposable.
2. Explore constraints: users, success, failure, time, non-goals. Numbered Q + rec + wait.
3. Put **at least four** approaches on the table when the shape is still open (the "past three" rule plus the obvious). Rec one.
4. Converge to a short shared design: problem, chosen approach, non-goals, open questions. Chat is enough; write `templates/decision-map.md` if they asked or the thread will span sessions.
5. If they then want an implementation-plan file → `writing-plans`. Tickets → `create-jira-story`. Target stack → `super-tech-blueprint`. Current-repo inventory → `super-codebase-learner`.

## Independent subsystems

If the idea is several products glued together, split them before anyone writes a plan. `writing-plans` expects that split already happened.

## Do not

- Duplicate subagent orchestration from `do` / `make-plan`.
- Ship a novel-length spec nobody asked for.
- Treat "brainstorm" as permission to skip grilling hard decisions — switch to **grill** when the tree is the job.
