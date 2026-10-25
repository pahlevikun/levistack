# Code-quality lens

Each reviewer uses this lens on top of the what-to-check lenses. It is a strict standard for how the code is built: how easy it is to change, how good its abstractions are, and whether it leaves the codebase healthier.

Above all, aim high on structure. Do not stop at local cleanup. Look hard for "code judo" moves: restructurings that keep the behavior but make the code much simpler, smaller, more direct and cleaner.

## Core prompt

Start from this:

> Do a deep code-quality audit of the current branch's changes.
> Rethink how to structure and build the changes so the code quality gets meaningfully better, without changing behavior.
> Improve the abstractions and the modularity, remove spaghetti code, and make it shorter and easier to read.
> Aim high. If there is a clear path that needs some of the codebase restructured, take it.
> Be thorough and strict. Measure twice, cut once.

## Dimensions

Use the ones that fit.

0. **Aim for structural simplification.** Do not stop at "this could be a bit cleaner". Look for a different framing that makes whole branches, helpers, modes, conditionals or layers go away. Assume a code-judo move often exists: it uses the existing design better and makes the change much simpler. If complexity can be deleted instead of moved around, push hard for that.

1. **Do not let a change push a file from under 1,000 lines to over 1,000 lines without a very strong reason.** Treat it as a strong smell. Prefer pulling out helpers, subcomponents or modules. If the diff crosses that line, ask whether the code should be split first. Allow it only for a strong structural reason, and only if the file stays clearly organized.

2. **Do not let spaghetti grow in existing code.** Be wary of new one-off conditionals, scattered special cases, or branches pushed into unrelated flows. Treat "odd if statements in random places" as a design problem, not a style nit. Prefer moving the logic into a dedicated helper, state machine or module.

3. **Push to clean the design, not only to accept code that works.** If the behavior can stay the same while the structure gets clearly cleaner, ask for the cleaner version. Prefer simplifications that remove moving parts over refactors that spread the same complexity around.

4. **Prefer direct, plain, easy-to-maintain code over clever or magic code.** Treat brittle, one-off or "magic" behavior as a problem. Be wary of generic mechanisms that hide simple assumptions about the data. Flag thin abstractions, identity wrappers and pass-through helpers that add a layer without adding clarity.

5. **Push on clean types and boundaries when they affect maintenance.** Question needless optional fields, `unknown`, `any`, or code full of casts when a clearer type boundary could exist. Prefer explicit typed models over loose ad-hoc objects. If a branch leans on a silent fallback to cover an unclear rule, ask whether the boundary should be made explicit.

6. **Keep logic in its proper layer, and reuse the existing helpers.** Call out feature logic that leaks into shared paths, and implementation details that leak through APIs. Prefer the existing standard utilities over new one-offs. Push code toward the right package, service or module instead of accepting drift.

7. **Treat needless step-by-step orchestration and non-atomic updates as design smells when the cleaner structure is obvious.** If independent work runs one after another for no reason, ask whether it should run in parallel. If related updates can leave state half-applied, push for a more atomic structure. Do not chase micro-optimizations, but do flag avoidable orchestration that makes the code brittle.

## What to report first

Order the findings like this: structural regressions and missed simplifications first, then spaghetti and branching, then boundary, type and file-size concerns, then smaller modularity and readability points.

## Approval bar

Do not approve just because the behavior looks right. Treat each of these as a blocker unless the author can justify it:

- The change keeps a lot of avoidable complexity when a code-judo move would delete it.
- It pushes a file from under 1,000 lines to over 1,000 lines.
- It adds one-off branching that tangles an existing flow.
- It scatters feature checks across shared code.
- It adds a needless abstraction, wrapper or cast-heavy contract.
- It duplicates an existing helper, or puts logic in the wrong layer when there is a clear proper home.

If none of these apply, still leave clear, actionable feedback, and push for a cleaner split where one exists.

## Tone

Be direct, serious and demanding about quality. Do not be rude. Do not soften a major maintenance problem into a mild suggestion. If the code makes the codebase messier, say so. If it missed an obvious big simplification, say that too. Do not settle for "maybe rename this" when the real problem is structure.
