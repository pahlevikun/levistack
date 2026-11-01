---
name: qa
description: "Write a test plan, the cases, and a defect note. Use when asked for QA, a test plan, test cases, or a defect report. Not for writing the code tests (tdd) or for proving a claim with a fresh run (verify)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: engineering
  category: engineering
  department: engineering
  related_skills:
    - tdd
    - verify
    - ready-spec
    - gap-analysis
  invokes:
    - skill: tdd
      when: A case should become a code test, or a defect should be fixed
  tags:
    - qa
    - test-plan
    - defect
  capabilities:
    - test_plan
    - defect_note
  languages:
    - en

---

# QA

Plan the tests. `tdd` writes them. Do not replace `tdd`.

## Test plan

1. Read the product spec if one exists (`ready-spec`: behavior, errors, compatibility). If none exists, read the code and say the plan is based on the code.
2. List what must be tested, what is out of scope, and the environment.
3. Write cases a person can run: setup, action, expected result. One case per behavior.
4. Mark the cases `tdd` should turn into code tests. Do not write those tests here.

## Defect note

When a case fails, write a defect note: what you did, what you saw, what you expected, and the smallest input that shows it. Hand the fix to `tdd` when they ask to change code.

## Related skills

- `tdd`: one failing test, the smallest pass, then refactor.
- `verify`: fresh proof that a claim is true.
- `ready-spec`: the product spec the plan should follow.
- `gap-analysis`: a mismatch or a stack trace, before this plan.

## Done when

- The plan names scope and cases with expected results.
- Code tests are left to `tdd`.
- [evals/evals.json](evals/evals.json) covers a test plan, a defect note, and a request that belongs to tdd.
