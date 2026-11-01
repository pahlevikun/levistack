# Playbook: refactor

Matches "refactor", "clean up", "extract", "rename", "split this module", "migrate callers", "remove the old API". Behavior does not change.

| Step | Do | Skill |
|---|---|---|
| 1 Restate | Say what moves, what must stay the same, and how sameness will be checked, before any edit | — |
| 2 Safety net | When no test pins the current behavior, add characterization tests first | `tdd` |
| 3 Refactor | Small, reversible steps. Migrate every caller, then delete the old path in the same change | `safe-refactor` |
| 4 Prove | Same tests, same outputs, before and after | `verify` |
| 5 Outside the diff | When a public API, a serialized shape, or a config key moved | `blast-radius` |
| 6 Close | Unfinished: write the note. Commit only when asked | `handoff` |

A refactor that needs a behavior change is two changes. Stop and offer the `feature` or `bug-fix` playbook for the second.

**Reply:** what moved, the proof that behavior held, and any caller left on the old path with the reason.
