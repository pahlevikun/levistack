---
name: figure-it-out
description: "Design an auditable run when no narrower route fits: a large migration, an ambitious multi-part change, or work a person reviews after stepping away. Frames done as a check that can fail, sets the rigor to the stakes, writes the phase list before code, runs each unit as a hypothesis, and keeps a decision log. Use when the user says 'figure it out', 'figure out how to do X', or hands over a large open-ended goal. Not for an accepted spec someone else will build (write-plan), a single feature or bug (use-levistack playbooks), or repeating one fix until checks pass (loopy)."
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: workflow
  category: workflow
  department: workflow
  related_skills:
    - write-plan
    - shape-and-build
    - rumbling
    - evidence
    - handoff
    - verify
    - use-levistack
    - lane-lead
    - compare-models
  invokes:
    - skill: shape-and-build
      when: A one-way-door design decision inside the run
    - skill: rumbling
      when: Work fans out across real seams
    - skill: lane-lead
      when: The run needs a controller and lanes that report done and do not merge
    - skill: compare-models
      when: A step is a question of which model to use
    - skill: evidence
      when: Delegated work needs a Judge
    - skill: handoff
      when: Keep the decision log, or pause the run
    - skill: verify
      when: Check the whole against done on the real product
  tags:
    - open-ended
    - migration
    - audit-trail
    - decision-log
  capabilities:
    - auditable_run_design
    - hypothesis_loop
    - decision_log
  languages:
    - en

---

# Figure it out

When the task fits no narrower playbook, design one. The first deliverable is the run itself: phases that scale rigor to the stakes, test each step against evidence, and leave a decision trail a person can audit after stepping away.

## Steps

### 1. Frame

Ground first, then commit. Do not start until these are written:

- **Done** as a check that can fail, observed on the real product.
- **Scope**, sized: rough units and effort, and the blockers grounding found.
- **Rigor**, biased high. One-way doors and wide reach get more gates and artifacts. Reversible, low-stakes steps get fewer.

Show the frame and its tradeoffs. Reversible work proceeds. A multi-hour run gets one checkpoint for a yes first.

### 2. Design the run

- Split into small units that each land and prove on their own. Riskiest unknown first. Scaffold and the check come before features.
- Build the check before the work, with a baseline from the pre-change state, so each result reads "old value, new value".
- A one-way-door design decision goes to `shape-and-build`. Mechanical work with a settled shape skips it.
- Fan out only across real seams, through `rumbling` Split, with each worker owning disjoint files. Do not over-fan. When the lanes must report back to one controller and must not merge, use `lane-lead`. When a step is a question of which model to use, use `compare-models`.
- Write the phase list down. That list is what the person reviews.

Then run the list. Each phase uses the `use-levistack` playbook that fits it: feature, bug-fix, refactor, design-shape, or parallel.

### 3. Run each unit as an experiment

State the hypothesis, make the smallest change, measure it against done on the real artifact, keep it if it moved forward, revert it if it did not. Prove each unit before the next.

- Check the artifact, never a self-report. When something passes too easily, suspect the check first.
- Pair delegated work with a judge (`evidence` Judge). A worker that games the check gets a reset and a tighter contract. A wrong check gets fixed in its own change.
- A verdict is **verified**, **not verified**, or **inconclusive**. Inconclusive is not a pass. Report every negative.

### 4. Keep the decision log

Use `handoff` Write with its decision log: one row per decision as it lands (what, why, evidence, result). Commit the log with the work when the person will review it in the MR, and only when asked to commit.

### 5. Prove the whole and hand back

Check the whole against done on the real product with `verify`, not only the harness. A correction that kept recurring becomes a check or a test, named in the reply.

## Output

The phase list, the rigor level and why, the decision log path, what is verified against done, and what is still open.

## Related skills

- `write-plan`: an accepted spec for someone else to build.
- `shape-and-build`: one-way-door design decisions inside the run.
- `rumbling`: fan-out across real seams.
- `lane-lead`: a controller and lanes that report done and do not merge.
- `compare-models`: the open question is which model should do a step.
- `evidence`: Judge on delegated work.
- `handoff`: the decision log and the note when the run pauses.
- `verify`: the final check against done.
- `use-levistack`: the playbooks each phase runs.

## Done when

- Done was written as a check that can fail before any code.
- The phase list was written and shown before the run.
- Every unit has a verdict, and the decision log has a row per decision.
- [evals/evals.json](evals/evals.json) covers a large migration, a request for a plan only, and a single bug that belongs to a playbook.
