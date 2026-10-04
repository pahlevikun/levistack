# Facts vs decisions

## Facts (you look up)

Anything the repo, tickets, or docs can answer. Examples: what the code does today, what `CONTEXT.md` already names, which ADR is accepted, current stack versions, whether a test exists.

- Search first (`Read` / `Grep` / `Glob`). For a current-architecture inventory, load `super-codebase-learner` instead of guessing.
- Cite the file. If you cannot find it, say **unknown — looked, not found**, not a leading question dressed as ignorance.
- When the user states a fact that contradicts the tree, show both and ask which is canonical.

## Decisions (the user owns)

Trade-offs, scope cuts, naming when two terms are both new, risk they will accept, "is this worth it."

- Always attach a **recommended answer** and a one-line why.
- Do not implement the rec until they confirm (or they said "just pick and go").
- Do not invent a target stack, cloud, or framework set. That is `super-tech-blueprint`.

## Grey area

Estimates and "how hard is this" start as **challenge** material: you may label them as guesses, then the user decides whether to believe them. Hidden work (auth, migration, observability, i18n) is a fact if the code shows it, a decision if they will defer it.
