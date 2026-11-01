# Playbook: feature

Matches "add", "build", "implement", "support X", a new endpoint, screen, command, or option.

| Step | Do | Skill |
|---|---|---|
| 1 Restate | Say the goal, the user-visible result, and how to tell it is done, in two or three sentences, before any edit. If done is not observable, ask once | — |
| 2 Ground | Read the subsystem the change touches when it is not already known in this chat | `codebase-learner` |
| 3 Shape | When the change adds a type, crosses a function boundary, or changes a module's public surface, settle the shape first | `shape-and-build` |
| 4 Plan | Only when the work spans more than one session or many files | `write-plan` |
| 5 Build | Failing test first when a cheap local test exists, then the smallest code that passes | `tdd` |
| 6 Prove | Run the gates and the user-visible check on the real surface | `verify` |
| 7 Review | When the change is wide, the design is contested, or the user asked | `second-opinion` |
| 8 Close | Unfinished or ending session: write the note. Commit and MR only when asked | `handoff`, `atomic-semantic-commit`, `write-mr-description` |

Build in small units and prove each before the next. Shared files serialize. Independent slices can go to `rumbling` Split through the `parallel` playbook.

**Reply:** what was built, the shape chosen and why, the proof output, and open decisions.
