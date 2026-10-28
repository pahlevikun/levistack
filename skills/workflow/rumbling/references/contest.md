# Contest candidate solutions

Use Contest when choosing one solution shape matters and parallel candidates can implement or sketch the same task independently.

1. Give every candidate the same problem, input evidence, constraints, target artifact, and acceptance criteria. Optional approach assignments may explore named alternatives; they must not change the success bar.
2. Put each candidate in an isolated worktree or output folder. Ask for the artifact, its checks, a short rationale, and the tradeoff it rejected. Dispatch all candidates together.
3. Wait until all candidates finish or fail. Read every artifact end to end. Score each against the criteria, including maintenance cost and the actual checks. A candidate's own score is not evidence. Ask a separate read-only `evidence` Judge to compare the completed candidates before choosing a base; give it every artifact and the common criteria.
4. Compare the Judge verdict with your own inspection, then choose one base. Resolve a disagreement by reproducing the disputed check. Take only specific useful ideas from other candidates and adapt them into the base's design; do not paste whole solutions together. If candidates converge, keep the clearest implementation. If they diverge because the task was under-specified, reframe the contract before another round.
5. Verify the synthesized artifact, then hand it to the shared `evidence` Judge gate in [SKILL.md](../SKILL.md). Include the score rationale, rejected candidates, and any grafts so Judge can test the selection claim.
