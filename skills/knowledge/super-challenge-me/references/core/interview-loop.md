# Interview loop

Shared by **grill**, **grill-docs**, and **brainstorm**. Challenge uses a shorter pass (`references/modes/challenge.md`). Router: `SKILL.md`.

## Before the first question

1. Name the subject in one line (what is being challenged).
2. Read what already exists: the artifact, nearby docs, and code the user is talking about. Do not ask for facts that a search would answer (`facts-vs-decisions.md`).
3. Apply session intensity from **calibrate** (`intensity.md`). Default: one question at a time, recommended answer, wait.
4. If many independent unknowns sit on the current frontier, offer one frontier round (`frontier.md`) instead of a 40-step serial interview.

## Each turn

1. Pick the highest-leverage undecided point (a branch in the design tree, a glossary clash, a hidden-work risk).
2. Emit using `templates/round.md` / `round-format.md`.
3. **Wait.** Do not auto-advance. If they answer several numbered items at once, consume all of them.
4. Look up anything they asserted that the tree can verify. Surface contradictions; do not silently "fix" the plan.
5. Record the decision (chat is enough; write `templates/decision-map.md` when they asked for a map or the thread will span sessions).
6. Recurse until the tree is covered or they stop.

## Past the first three

After the user (or you) names three obvious options, add **one** that is less obvious — a smaller slice, a different owner, a "do nothing / measure first" path, a boring alternative. Then recommend. Do not spawn extra agents or a 10-step ideation circus.

## When to stop

- The user says stop, "good enough", or asks to implement.
- Remaining questions are implementation trivia → hand off to `writing-plans` only if they want that file.
- Remaining work is refactor execution → `super-refactor`.
- Remaining work is a target stack → `super-tech-blueprint`.

## Do not

- Ask "what does this repo do?" when `super-codebase-learner` output or the tree already says.
- Batch-update glossary/ADRs in **grill-docs**; write them as terms resolve.
- Clone stores, run proprietary harnesses, or install interview scripts. The method is questions, recs, wait.
