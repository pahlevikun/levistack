---
name: gap-analysis
description: "Find where the code, the product spec, the tech spec, and the docs do not match, or isolate a failure from an error or a stack trace. Use when asked what is missing before a release, whether the change still matches the spec, or to debug a hard bug or a slowdown. Not for why the code was shaped this way (trace), what a diff can break outside itself (blast-radius), or writing the spec (ready-spec, write-adr, write-plan)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: knowledge
  category: knowledge
  department: knowledge
  related_skills:
    - trace
    - blast-radius
    - ready-spec
    - write-adr
    - write-plan
    - verify
    - second-opinion
    - tdd
  invokes:
    - skill: blast-radius
      when: A gap can break behavior outside the diff
  tags:
    - gap
    - spec
    - debug
  capabilities:
    - spec_gap_list
    - failure_isolation
  languages:
    - en

---

# Gap analysis

Two modes. Pick one. Do not blend them.

| They ask | Mode |
|---|---|
| What is missing, what diverged, does this change still match the spec | Gap |
| An error, a stack trace, a hard bug, or a slowdown | Debug |

## Gap

1. Read the code that the claim is about.
2. Read the product spec (`ready-spec` if one exists: behavior, errors, compatibility) and the tech spec (`write-adr` for the decision, `write-plan` for the file list).
3. Read the docs that describe the same behavior.
4. List each mismatch: what the code does, what the spec or the docs say, and the file that shows it. A mismatch with no file is not a finding.
5. If a mismatch can break behavior outside the diff, name `blast-radius` for that item. Security findings on a diff go to `second-opinion`.
6. Do not write a new spec. Hand a draft of missing behavior to `ready-spec` only when they ask.

## Debug

1. Quote the error or the stack frame you will follow. Do not guess a cause first.
2. State one hypothesis.
3. Read the frames and the inputs that reach them. Stop when the hypothesis is confirmed or dropped.
4. If it is dropped, state the next hypothesis. Do not pile up guesses.
5. Report the isolated failure: the line, the input, and the check that would catch it. Hand the fix to `tdd` when they ask to change code.

## Related skills

- `trace`: why the code is shaped this way.
- `blast-radius`: what a change can break outside the diff.
- `ready-spec`: the product spec.
- `write-adr`: the decision.
- `write-plan`: the file-by-file plan.
- `verify`: fresh proof that a claim is true.
- `second-opinion`: a security finding on a diff.
- `tdd`: the test that locks the fix.

## Done when

- Gap mode lists mismatches with a file for each one.
- Debug mode ends on one confirmed failure, or says the hypothesis was dropped.
- [evals/evals.json](evals/evals.json) covers a spec mismatch, a stack trace, and a request that belongs to trace.
