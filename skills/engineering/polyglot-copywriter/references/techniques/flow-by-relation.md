# Flow by relation

Load when development is weak: locally clear paragraphs that sit beside each
other, list-like sections, or conclusions that state a generic thesis without
returning to a concrete carrier. Pairs with [substance.md](../substance.md)
rewrite order step 3 and [humanize-workflow.md](humanize-workflow.md).

**Multilingual note:** relation forms below are English examples. Translate
connectives (`because`, `although`, `once`, `if`, `which`) per the active
language pack — the job is to **name the relation**, not import English syntax.

## Rule

> Flow improves when each paragraph makes the next question possible.

Paragraphs should not merely sit in plausible order. Each paragraph should
answer the prior question or make the next one necessary.

## Relations table

| Relation | Useful forms (adapt per language) |
|---|---|
| Cause | `Because X, Y.` |
| Contrast | `Although X, Y.` |
| Dependency | `Without X, Y cannot happen.` |
| Time / state change | `Once X is visible, Y becomes inspectable.` |
| Condition | `If X changes, Y no longer means the same thing.` |
| Scope / level | `At that level, Y changes from A into B.` |
| Inference | `Which means …` / `So Y follows from X.` |
| Carrier-to-claim | `Because this example is small and inspectable, it can carry the larger claim.` |

## Hinge repair

A section needs a hinge when:

- headings do all the organizing work;
- each paragraph is locally clear but the sequence feels like a list;
- the piece jumps from example to general claim without naming what transfers;
- the conclusion states a thesis but does not return to the concrete object;
- every section closes on the same two-part contrast (document-level parataxis).

**Repair:**

1. Name the level or relation that connects the next section.
2. Add one factual hinge sentence before the list or section shift.
3. Prefer `because`, `although`, `without`, `once`, `where`, `if`, `which` over decorative contrast.
4. Do not subordinate every clause into one connective-heavy sentence — keep readable beats.

### Example

Weak:

```txt
The Climb ranks the models. Head-to-Head is a filmstrip viewer. Runbook Diffs compares versions.
```

Better:

```txt
The site exposes the run at three resolutions. The Climb shows the aggregate trajectory, Head-to-Head shows round-by-round lineage, and Runbook Diffs drops to the source level where the prompt and seed SVG changed.
```

## Carrier-bound endings

Weak ending (generic thesis):

```txt
A benchmark is stronger when you can inspect the run that produced it.
```

Better (returns to carrier, states transferable structure):

```txt
Because the pelican project is small enough to inspect and strange enough to remember, it works as a compact carrier for the larger claim: a benchmark is stronger when you can inspect the run that produced it.
```

Reject outline templates such as "Despite challenges, X continues to thrive"
unless a specific challenge and next step are named.

## Staccato contrast

Do not treat every short contrast as slop. Classify before editing:

| Type | Test | Action |
|---|---|---|
| **Earned antithesis** | Both sides evidenced in prior sentences; contrast lands a distinction the reader can verify | **keep** or use once at document level |
| **Compressed antithesis** | One side evidenced; other side is a leap | Expand — name the unsupported relation |
| **Decorative antithesis** | Neither side evidenced; cadence supplies closure | **cut** or replace with named relation |

**Emphasis-source test:** flatten the line (remove contrast shape). If the
residual claim still names actor, mechanism, or limit, keep it. If it
collapses to a generic statement, cadence was carrying it.

**Document-level lens:** one earned staccato line can work; four section
closers on the same `Not X. Y.` rhythm is parataxis density — convert most
instances to hypotaxis (`because`, `although`, `once`) and keep at most one
earned paratactic line for effect.

Typical repair moves:

```txt
Although X, Y.
Because X, Y.
When X changes, Y no longer means the same thing.
Where X only shows final state, Y records process.
```

See [noslop-prose.md](../noslop-prose.md) pattern strength and
[review-prose.md](../review-prose.md) `Rewrite check:` when suggesting fixes.
