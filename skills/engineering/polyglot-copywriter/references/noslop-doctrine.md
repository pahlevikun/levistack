# Noslop doctrine

Principles, detectors and critique format for important prose.

Load for a full prose review, for essays, talks, launch copy, README and docs text, or when a draft is clean at sentence level but still reads generic. The pattern catalog is [humanizer-patterns.md](humanizer-patterns.md). The always-on scan is [noslop-prose.md](noslop-prose.md). Relation and flow work is in [techniques/flow-by-relation.md](techniques/flow-by-relation.md). This file adds the principles and the checks those files do not hold.

Examples are English. In other languages, translate the job, not the words (see [natural-writing.md](techniques/natural-writing.md)).

## Core principle

> Sharp detail beats inflated significance.

AI writing often fails by doing this: less detail, more importance. Fix it by doing this: more detail, earned importance.

## Before writing or rewriting

Answer these four. If they are unclear, ask or inspect the source before drafting.

1. What is the exact point?
2. What concrete detail proves it?
3. What sentence machinery is making it feel true?
4. What should the reader remember?

## Extra detectors

Use these on top of the 26 patterns.

| Detector | What to check |
|---|---|
| Rhetorical drift | Noun-heavy abstractions, nominalizations, phrasal coordination, and dense information without a mechanism. |
| Symmetry | Paragraphs of the same length, parallel headings, and bullet + bold header + colon blocks. |
| Hedged symmetry | "Whether you're X or Y", "While X, Y is also important". They address every reader and every value at once. Keep the form only when it names a real branch with different downstream behavior. Example that earns it: "Whether the worker crashes before or after the receipt is written decides if recovery retries the job or marks it complete." |
| Outline conclusions | "Despite ongoing challenges, X continues to thrive." "Looking ahead, X will play an increasingly pivotal role." Cut, or return to a concrete carrier from the body and a specific next step. |
| Copula displacement | `serves as`, `stands as`, `features`, `marks`, `represents` where `is` or `has` would do. Keep the verb when it enumerates, defines or locates: "The retry policy serves three failure modes: timeout, oversized payload, dependency outage." |
| Dash and semicolon clusters | Several dashes or semicolons in a paragraph used for emphasis or to skip choosing a connector. The output rule is stricter than the detector: no dashes or semicolons in final prose unless a sample uses them (§8 in [humanizer-patterns.md](humanizer-patterns.md)). |
| Staccato contrast | Classify first. Earned: both sides were shown before. Compressed: one side is a leap. Decorative: neither side was shown. Details in [flow-by-relation.md](techniques/flow-by-relation.md). |
| Hypotaxis | When the relation matters, say it: because, although, when, where, once, so that. |
| Conclusion | Return to the concrete carrier, admit the limit if there is one, state what transfers. A last line that could end any essay in the category is weak. |
| Unseeing | Strip the polished sentence down to the machinery that made it feel true: cadence, contrast, the missing relation, the scope of the evidence. |
| Emphasis source | Flatten the line (no cadence, same claim). If the claim still names an actor, mechanism or limit, the idea carried it. If it goes generic, the rhythm did. |
| Syntax-relation | Restate the implied relation with a connective. If you cannot supply one without inventing it, the syntax was standing in for a relation that was not there. |
| Contribution bar | Length must be earned by judgment, framing or depth. Add one of those, or cut. |
| Durable prose | Long-lived writing needs judgment, evidence, runnable artifacts and taste. |

## Default editing pass

1. Delete the generic opening.
2. Find prestige-vocabulary clusters.
3. Replace abstract nouns with concrete mechanisms.
4. Remove "not just X but Y" unless it is the exact point.
5. Cut "highlighting" and "underscoring" clauses.
6. Check every claim of importance against evidence.
7. Replace vague actors with a named source, named uncertainty, or an `ask-author` note. Never invent a name, count, tool or timing to fill a rewrite.
8. Collapse redundant bullets.
9. Vary sentence rhythm on purpose.
10. Name the hidden relation behind staccato contrast: contrast, evidence scope, cause, consequence, exception, or scope control.
11. Prefer subordination to side-by-side clauses when the relation matters.
12. Check paragraph flow. Add a hinge sentence when a section reads like a list.
13. Check the conclusion (see the table above).
14. Replace rhythm with relation when a line sounds good but names no mechanism.
15. Fix displaced copulas, hedged symmetry and outline conclusions.
16. Remove dashes and semicolons (first principle).
17. End on a concrete line the reader will remember.

## Avoid by default

Phrases to avoid unless there is a specific reason:

```txt
In today's rapidly evolving landscape
In the realm of
When it comes to
At its core
Let's dive into
It's worth noting that
It's important to note that
A testament to
Not just X, but Y
Not only X, but also Y
Same X. Same Y. Different Z.
Not X. Y.
This is where X comes in
Whether you're X or Y
While X, Y is also important
Despite ongoing challenges, X continues to thrive
Looking ahead, X will play an increasingly pivotal role
In conclusion
Overall
Ultimately
I hope this helps
```

Words to review (beyond §12 in [humanizer-patterns.md](humanizer-patterns.md)):

```txt
realm, multifaceted, nuanced (as filler), foster, bolster, emphasize,
encompass, utilize, facilitate, transformative, groundbreaking, seamless,
robust (outside an engineering claim)
```

Both lists are time-dated. Words enter and leave with each model generation (`delve` peaked in 2023 and 2024 output and fell sharply after). Re-profile against current human and model text instead of keeping the list by taste. Do not quote a precise drop figure.

`serves as` and `stands as` stay out of the word list on purpose, because the verdict depends on context.

## False-positive restraint

A detector hit is a hypothesis, not a verdict. If the same sentence or the lines around it supply the mechanism, failure mode, measurement or boundary that earns the term, keep it and say why.

> Keep: "The queue is robust because each job has an idempotency key, a retry receipt, and a dead-letter cutoff."
> Why: `robust` is an engineering claim earned by the dedup, retry tracking and dead-letter mechanisms.

Do not offer a synonym-only rewrite just because a watch-list word appears.

## Better replacements

Replace the thought, not the word.

| Instead of | Write |
|---|---|
| This underscores the importance of durable execution. | The workflow can fail on step 4, retry only that step, and keep the previous outputs. |
| Cloudflare is not just a CDN, but a platform. | Cloudflare turns the network boundary into a programmable runtime. |
| This empowers teams to build seamless experiences. | The team can ship a WebSocket room without running a room server. |
| The point is not the pelicans. The point is the process. | The pelican is useful because it gives the process a small, inspectable carrier. |
| A benchmark is stronger when you can inspect the run that produced it. (as a last line) | Because the pelican project is small enough to inspect and strange enough to remember, it works as a compact carrier for the larger claim: a benchmark is stronger when you can inspect the run that produced it. |

Section hinge. Weak: three one-line paragraphs, one per page of the site. Better: "The site shows the run at three levels. The Climb shows the overall trend, Head-to-Head shows round-by-round lineage, and Runbook Diffs drops to the source where the prompt changed."

Earned compression stays. "The pelican is the surface. The inspectable run is the point." works when the earlier text already drew that distinction.

## Rewrites must pass their own detectors

A rewrite is prose too. Rule-of-three, X-not-Y cadence, dash antithesis, prestige adjectives and decorative closers are slop in the fix as much as in the source. Run the same scan on your rewrite before you ship it.

Two common failures:

1. An `ask-author` verdict is right, but the fallback invents specifics ("most hallway talk was about moderation tooling") and reuses the cadence it flagged. Fix: ask for the missing fact, or offer a cut. Do not invent the fallback.
2. A closing rewrite that decorates instead of carrying, such as a last line "That was the point." Fix: end on the mechanism ("A standard.site post is a record on a PDS, so the URL keeps working if any one piece of the stack goes away.").

## Critique output format

For a review that does not rewrite, use the block below. It extends the passage format in [review-prose.md](review-prose.md).

```txt
Verdict: keep / revise / ask-author / reject
Slop tells:
Specificity missing:
Inflated claim:
Flow break:
Concrete rewrite:
Rewrite check:
Remembered line:
```

- Use `ask-author` when the line can be fixed only with a fact the source does not give (a tool, a person, a count, a timing, a named mechanism). Say what to ask in the `Concrete rewrite` slot and offer a fallback (cut it, or let the next sentences carry it). A fallback that invents is worse than none.
- `Rewrite check` is mandatory. State whether your rewrite contains a triad, X-not-Y, dash antithesis, an avoid-by-default phrase, a prestige adjective, a decorative closer ("That was the point", "In conclusion", "Overall", "Ultimately"), or an invented fact. If it would earn `revise` as source text, rewrite it or move to `ask-author`. If it passes, write `passes self-detectors`.
- Before grading a contrast as compressed or decorative, read the sentence before it. If that sentence supplies the mechanism the contrast points at, the contrast is earned.

## Final self-check

- Did I answer the actual request: review, rewrite, draft, or all three?
- Did every flagged tell get a concrete rewrite or a reason to cut?
- Does each rewrite name a mechanism, a relation, an actor and result, or a concrete carrier?
- Did I keep earned compression instead of expanding it into bland explanation?
- Did I avoid new prestige words and avoid-by-default phrases?
- Did I run on my rewrite the detectors I ran on the source?
- Where a rewrite needed a fact the source lacks, did I ask or cut instead of inventing?

For high-stakes prose, do one bounded judge-and-refine pass: score specificity, evidence fit, relation clarity and rhythm from 1 to 5, then improve the weakest one once.

## Tone target

Prefer: specific, source-grounded, direct, varied rhythm, concrete mechanisms, named tradeoffs, one memorable line.
Avoid: safe essay voice, prestige abstraction, balanced filler, fake profundity, marketing fog.
