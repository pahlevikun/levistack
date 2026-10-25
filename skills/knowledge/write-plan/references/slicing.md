# Slice the work

Use this when a plan is large, crosses several layers, or will become tickets for more than one person or agent. Skip it for a one-file change.

## Contents
- What a slice is
- Rules
- An example
- A slice card
- Check the cut with the user
- Where the slices go
- Do not

## What a slice is

A slice is a thin piece of the work that goes all the way through: data, API, screen and tests. When it is done, you can show it or check it by itself. It is the opposite of "do all the database work first, then all the API work".

## Rules

- **Cut end to end.** Each slice touches every layer it needs, and nothing more.
- **Fit one session.** A slice should be small enough for one fresh agent session, or one human review.
- **Make room first.** If the code needs reshaping before the feature fits, that reshaping is slice 1. It changes no behavior. Use `safe-refactor`.
- **Say what each slice waits on.** Write the slices that must finish first. Only list a real reason: data flows from it, a contract must exist first, or a shared interface is missing. Do not add order just to look tidy.
- **Find the ready slices.** A slice is ready when everything it waits on is done. A slice that waits on nothing can start now. A simple chain runs top to bottom.
- **Use the project's words.** Titles use the repo's glossary and respect its ADRs.
- **One exception: sweeping mechanical changes.** A rename or a type change that touches the whole codebase breaks everything until it is done, so a split by feature will not compile. Plan it as one slice. Or plan a tool that makes the change, one run of the tool, and a compiler check.

## An example

The goal: "users can export their orders as CSV."

| Slice | What it delivers | Blocked by |
|---|---|---|
| 1. Make room | Order data is read through one function, behavior unchanged | None |
| 2. Export one order | A user downloads a CSV of a single order | 1 |
| 3. Export a date range | A user picks a range and downloads one CSV | 2 |
| 4. Big exports | Exports over 10,000 rows run in the background and arrive by email | 3 |

Each slice works on its own. Slice 3 and slice 4 could be built by different people, but slice 4 waits on 3.

## A slice card

```markdown
### Slice <n>: <short title in plain words>

**What it delivers:** the result a user can see or check, not a list of layers.

**Blocked by:** the slices that gate this one, or "None, can start now".

**Done when:**
- [ ] <a check anyone can run>
- [ ] <a check anyone can run>
```

Leave file paths and code out of the card. They go stale fast. One exception: a short snippet that states a decision more exactly than prose can, such as a state machine, a schema or a type. Keep only the part that carries the decision.

## Check the cut with the user

Show a numbered list: title, blocked by, what it delivers. Then ask one question at a time, each with your recommendation:

1. Is the size right, or are some slices too big or too small?
2. Is each "blocked by" real, or does a slice wait on something that does not gate it?
3. Should any slices be merged or split?

Change the list until the user agrees. Do not write full plan tasks before that.

## Where the slices go

- **A plan file:** each slice becomes a task, or a small group of tasks. The task gets a "Blocked by" line (see the task template in `SKILL.md`).
- **Tickets:** give the approved slices to `create-tickets`. It turns "Blocked by" into links between stories.
- **Too big to see the end:** do not slice yet. Use the huge-work section of the decision map in `challenge-me` first.

## Do not

- Make one ticket per layer.
- Slice a sweeping mechanical change by feature.
- Edit or close the parent issue the slices came from.
- Add a blocker just to force an order.
