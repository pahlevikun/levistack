# Playbook: bug-fix

Matches "fix", "broken", "regression", "fails when", a stack trace, an error report, a flaky test.

Every shipped line traces to evidence. A change that "might help" is a hypothesis. It does not ship. When the evidence refutes a hypothesis, revert what it motivated.

| Step | Do | Skill |
|---|---|---|
| 1 Restate | Say the expected behavior, the observed behavior, and where it shows, before any edit | — |
| 2 Reproduce | Make it fail on the surface the user saw. If it will not reproduce, tighten the conditions or add logging until it does. Ask the user only with a named reason the surface cannot be reached | `verify` (investigate first) |
| 3 Root cause | Form the candidate causes, cut the most problem space each pass, and confirm the surviving mechanism with evidence | `trace` (root-cause mode) |
| 4 Fix | The smallest change the evidence justifies. Failing test first when a cheap local test exists. A fix that crosses a function boundary gets its shape settled first | `tdd`, `shape-and-build` when needed |
| 5 Loop | Only when the user asked to keep going until it passes | `loopy` |
| 6 Prove | The original repro now passes on the same surface. A green unit test alone does not prove the bug is gone | `verify` |
| 7 Outside the diff | When the fix touches shared code, a wire format, or a cache | `blast-radius` |
| 8 Close | Unfinished: write the note. Commit and MR only when asked | `handoff` |

**Reply:** what was broken, the root cause with `file:line`, the fix, and the failing-then-passing output pasted as it ran.
