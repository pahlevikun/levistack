---
name: lane-lead
description: "Run several lanes of work under one controller. Each lane owns a disjoint set of files and returns a done block. The controller writes one digest and integrates locally. Lanes do not merge, push, or ship. Use when the user says run the lanes, one controller and several workers, or a crew that reports back and does not merge. Not for independent parallel tasks with no controller (rumbling), a long open-ended run (figure-it-out), or merging a request (code-review prep)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: workflow
  category: workflow
  department: workflow
  related_skills:
    - rumbling
    - figure-it-out
    - verify
    - handoff
    - code-review
  invokes:
    - skill: rumbling
      when: The lanes can run together
    - skill: verify
      when: The combined tree needs a check
  tags:
    - lanes
    - controller
    - digest
  capabilities:
    - lane_coordination
    - done_block
    - local_integration
  languages:
    - en

---

# Lane lead

One controller. Several lanes. One digest. A lane finishes its files and reports. It does not merge.

## Steps

1. **Name the lanes before any of them start.** For each lane write the goal, the files it owns, and the check that counts as done. Two lanes do not own the same file. Shared files stay with the controller.
2. **Run the lanes.** Use `rumbling` Split when the host can run them together. Otherwise run them one after another and say so. A lane does not read another lane's uncommitted work.
3. **Accept only a done block.** A lane is done when it returns the goal, the full head SHA, the checks it ran and their results, and what it did not prove. A chat message that says the work looks good is not a done block. Send that lane back.
4. **Write the digest.** One short note: what each lane did, what is accepted, what is blocked, and the SHA the digest describes.
5. **Integrate locally.** Combine the accepted lanes into one tree. Run the checks that cover the combination. Push, merge, and ship wait for a yes.

## Do not

- Let a lane merge, push, or open a request.
- Stamp a version, run a merge train, or schedule a later flake pass.
- Call a lane done because its own summary says so. Read the checks.

## Output

The lane table, each done block or the reason it was sent back, the digest, and the result of the combined check. Say if you are waiting for a yes to push.

## Related skills

- `rumbling`: run the lanes together when they are independent.
- `figure-it-out`: the lanes are one phase of a larger run. That skill designs the run. This skill runs the lanes.
- `verify`: the combined check after integration.
- `handoff`: the digest needs to outlive this session.
- `code-review`: a request needs watch or prep. This skill does not merge it.

## Done when

- Every lane has a done block or a named reason it was sent back.
- The digest names what is accepted and what is blocked.
- Nothing was pushed or merged without a yes.
- [evals/evals.json](evals/evals.json) covers a two-lane run, a lane that reports without checks, and a request to merge.
