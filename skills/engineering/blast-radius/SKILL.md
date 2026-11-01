---
name: blast-radius
description: "Find what a change could break outside its own diff before it ships, and prove the one fact it is safe because of by running real code. Looks where grep stops: library source at the pinned version, timing and teardown, wire formats, DB columns, feature flags, other languages reading the same bytes, code several hops away. Use for 'blast radius of X', 'what could this break', 'is this small diff safe', 'is this pull request unsafe to merge', or a change you do not trust yet. Not for running the ordinary gates (verify), an adversarial review of the diff itself (second-opinion), or fixing what it finds (tdd)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: engineering
  category: engineering
  department: engineering
  related_skills:
    - verify
    - second-opinion
    - trace
    - rumbling
    - tdd
    - gap-analysis
  invokes:
    - skill: trace
      when: The intent behind the change is unclear and needs the PR and commit history
    - skill: rumbling
      when: A wide change needs a Council of reviewers looking for outside-the-diff breakage
  tags:
    - blast-radius
    - risk
    - safety
    - impact
  capabilities:
    - outside_diff_risk_analysis
    - safety_fact_proof
  languages:
    - en

---

# Blast radius

Find what a change breaks somewhere else, before it ships. Listing callers is not the job: grep does that in a second. The job is the breakage grep will not show.

A writeup that sounds right reads the same whether or not it is true. So the deliverable is the one or two facts the change's safety depends on, proven by running code.

## How sure

For each fact the safety depends on, push it as far down this ladder as is cheap, and say where it stopped.

| Level | Evidence |
|---|---|
| 1 Said so | A claim. Worth nothing alone |
| 2 Pointed | A real `file:line`, or the library's own source at the pinned version |
| 3 Walked | The failure path traced step by step, and it does not reach |
| 4 Ran | A script or test that calls the real code and fails loudly if the fact is wrong |
| 5 Reproduced | The case exercised in the running app |

Level 4 is usually one small script that imports the library the app ships and calls the exact function in question.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes, and deletes, and what now behaves differently, including what the diff does not spell out. Use `trace` to pull the PR and commits when the intent is unclear.
2. **Find the one fact.** Most risky-looking changes are safe because of a single fact, such as "this call only drops entries that are already expired". Find it. If it holds, most risks clear at once. Spend the time here.
3. **Look where grep stops.** Read the library source at the pinned version and any local patch. Work out when things run: async ordering, teardown, retries, caches. Follow what a symbol search misses: API response JSON, a DB column, a serialized format, a config key, a feature flag, another service or language reading the same data, code three hops downstream.
4. **Weigh each risk honestly.** A real chance and a real cost. Keep the confirmed ones. List the checked-and-cleared ones apart. Cite a real `file:line`. A search that finds nothing is an answer; say what was searched. Never invent a caller or an API.
5. **Prove the one fact.** Write the script or test, run it, and paste the output. Keep it out of the reviewed files unless the user asks to add it.
6. **Wide change.** When the change spans many modules, run the question as `rumbling` Council so different reviewers can catch different breakage, then judge the merged list.
7. **Merge.** Say whether this pull request is unsafe to merge. Unsafe means a confirmed risk whose safety fact is unproven. A cleared risk is not a merge block.

## Output

- **What it does.** The change, including the part that is not obvious.
- **The safety fact.** Stated, its ladder level, and the proof output. If it could not be proven, write **unproven**.
- **Risks.** Each with how it breaks, `file:line`, likelihood and cost, and how to check it.
- **Cleared.** What was checked and why it is fine.
- **Before merge.** The cheapest test or repro that would catch the real bug, including the script written in step 5.

Strip anything private before the writeup goes anywhere public.

## Related skills

- `verify`: ordinary gates, and the general prove-it-is-safe reference.
- `second-opinion`: adversarial review of the diff itself.
- `trace`: the history and intent behind the change.
- `rumbling`: Council for a wide change.
- `tdd`: turn a confirmed risk into a failing test and a fix.

## Done when

- The safety fact is stated with its ladder level and proof output, or marked unproven.
- Every confirmed risk cites a real location, and cleared items are listed apart.
- No reviewed file was edited without a request.
- [evals/evals.json](evals/evals.json) covers a small risky diff, a request for the ordinary gates, and a request for an adversarial review.
