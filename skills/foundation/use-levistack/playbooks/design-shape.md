# Playbook: design-shape

Matches "design this", "how should we structure", "what should the types be", "sketch the API", "which architecture", "write the ADR for this choice".

| Step | Do | Skill |
|---|---|---|
| 1 Restate | Say the problem, the constraints, and what the design must make easy, before sketching | — |
| 2 Ground | Read every system the new code touches. Add `trace` when the design moves ownership or layering | `codebase-learner`, `trace` |
| 3 Style | Only when the system-level style is undecided | `super-architecture` |
| 4 Shape | Types, signatures, and module boundaries with stub bodies, at least two whole-shape candidates, then one pick | `shape-and-build` |
| 5 Behavior question | When the open question is how it feels or flows, answer it with a throwaway build | `prototype-wireframe` |
| 6 Grill | When the user wants pressure on the pick before code | `challenge-me` |
| 7 Record | When the decision needs a record or the repo keeps ADRs | `write-adr` |

`shape-and-build` implements right after the pick. Add "with checkpoint" to stop and show the design first.

**Reply:** the candidates, the pick and why, the stub files or sketch, and the decision record path when one was written.
