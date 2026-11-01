---
name: shape-and-build
description: "Sketch types, signatures, and module boundaries with stub bodies before code, compare at least two whole-shape candidates, pick one, then implement against it and scrap it when the friction says the shape is wrong. Use when the user says 'design this', 'shape this first', 'what should the types be', 'architect this', or before non-trivial code that adds a type, crosses a function boundary, or changes a module's public surface. Add 'with checkpoint' to stop before implementing. Not for choosing a system-level architecture style (super-architecture), recording a decision (write-adr), or an implementation plan for someone else (write-plan)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: architecture
  category: architecture
  department: architecture
  related_skills:
    - codebase-learner
    - trace
    - super-architecture
    - rumbling
    - tdd
    - write-adr
    - prototype-wireframe
  invokes:
    - skill: codebase-learner
      when: Ground the systems the new code touches before sketching
    - skill: rumbling
      when: A wide or contested design needs candidates run as a Contest
    - skill: tdd
      when: Implement each stub test-first when a cheap test exists
  tags:
    - design
    - types
    - signatures
    - module-shape
  capabilities:
    - caller_first_type_sketch
    - candidate_shape_comparison
    - implement_against_sketch
  languages:
    - en

---

# Shape and build

Settle the shape of a change before its logic: the types, the function signatures, the module boundaries, and who owns which state. Then implement against that shape and stay with it until the code is in. The shape is the contract. A deviation is a signal to examine.

## When to use

- The change adds a type or a module, crosses a function boundary, or changes a public surface.
- Jumping to code would lock in a shape nobody chose.
- Not for one-line fixes, mechanical renames, or a shape already settled in this chat.

## Steps

1. **Ground.** Read every system the new code touches with `codebase-learner`. When the design moves ownership or layering, run `trace` on the current shape so its reasons become constraints. Skip only for greenfield code with nothing around it.
2. **Write the caller first.** Sketch how a caller will use the new code, as real code at the call site. The types follow from that usage.
3. **Sketch at least two candidates.** Each is a whole shape: types, signatures with `not implemented` bodies, and a module map. Two variations of one shape count as one candidate. For a wide or contested design, run the candidates as `rumbling` Contest.
4. **Screen each candidate** against [references/red-flags.md](references/red-flags.md). Assume the next contributor sees only the file they opened and copies the nearest example. Prefer the shape where an edit that looks right in one file is right for the whole repo.
5. **Pick one.** Prefer the shape that hides more behind a smaller public surface. Write a short rationale with [references/rationale.md](references/rationale.md).
6. **Checkpoint, only when asked.** "With checkpoint", "show me before you build": show the pick and the rationale, and wait. Otherwise continue. Pushback on the shape is new grounding: go back to step 1.
7. **Implement against the sketch.** Replace stubs with code, test-first through `tdd` when a cheap test exists. When a function needs something the sketch did not foresee, decide whether the sketch was wrong, a requirement was missed, or the code is overreaching, and say which.
8. **Scrap when the shape is wrong.** See below.

## Scrap

One awkward edge case does not condemn a shape. A pattern does:

- The same workaround shows up in unrelated places.
- Several unrelated cases each need a special branch.
- Types need escape hatches to compile: `any`, casts, optional fields that are always set.
- A lock appears where the sketch said state was not shared.
- Callers must know the module's internal rules to use it.
- Two or more step 7 deviations have the same shape.

When it is a pattern: re-read what was built, remove what the new design will not need, redesign as if today's constraints were known on day one, and return to step 3. The new sketch starts smaller than the old.

## Output

- Small change: one file of new types and signatures, then the code.
- Larger change: a module map plus the type definitions, then the code.
- The rationale: the caller sketch, the candidates, the pick and why, and what was scrapped if anything.

## Related skills

- `codebase-learner`: step 1 grounding.
- `trace`: why the current shape exists, before moving ownership.
- `super-architecture`: the system-level style is undecided.
- `rumbling`: Contest for wide or contested candidates.
- `tdd`: implement each stub test-first.
- `write-adr`: the pick needs a decision record.
- `prototype-wireframe`: the open question is how it behaves or feels, not its types.

## Done when

- At least two whole-shape candidates were compared and one was picked with a written reason.
- The code matches the sketch, or each deviation is named with its cause.
- A scrapped shape, if any, is recorded with the pattern that condemned it.
- [evals/evals.json](evals/evals.json) covers a cross-boundary change, a checkpoint request, and a request that belongs to `super-architecture`.
