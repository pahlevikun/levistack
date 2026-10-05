# <Plan name>

Plan <phase>-<n>. Two or three tasks, one subsystem, about half a context window. Delete any row that does not apply.

## Objective
<What this plan delivers and why it matters.>
Output: <the artifacts it creates or changes>.

## Context
Read before starting:
- `<path/to/brief-or-roadmap.md>`
- `<path/to/findings-or-previous-summary.md>`
- `<path/to/relevant/source.ext>`

## Tasks

### Task 1: <action-oriented name>
- **Type:** auto
- **Files:** `<exact/path.ext>`, `<exact/other.ext>`
- **Action:** <what to do; what to avoid and why; the technology choice and its reason>
- **Verify:** <a command, test or observable behavior>
- **Done:** <testable acceptance state>

### Task 2: <action-oriented name>
- **Type:** auto
- **Files:** `<exact/path.ext>`
- **Action:** <...>
- **Verify:** <...>
- **Done:** <...>

### Checkpoint: <verify | decision>
- **What was built:** <what the agent automated> (verify only)
- **How to verify:** <numbered steps with exact URLs or commands> (verify only)
- **Decision:** <what is being decided, why it matters, options with pros and cons> (decision only)
- **Resume with:** <"approved", or the option id>

## Verification
- [ ] <build or type check passes>
- [ ] <the test command passes>
- [ ] <end-to-end behavior is observed>

## Success criteria
- Every task is done and its verification passed.
- <Measurable, plan-specific outcome.>

## Rules while executing
- Fix bugs, add missing security or correctness code, and fix blockers yourself; record each in the summary.
- Stop and ask before an architectural change.
- Log nice-to-haves to the issues log and keep going.
- On a failed verification, stop and report expected and actual.

## Output
When finished, write `<path>/<phase>-<n>-SUMMARY.md` with: a one-line result that says what shipped, accomplishments, files changed, decisions, deviations (rule, task, issue, fix, files, verification, commit), issues, and what the next plan can rely on.
