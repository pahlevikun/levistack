# Design document and RFC

Use this job for a proposal that needs a broader review than one architecture decision record. Follow the repository's existing RFC or design-doc format. Do not turn the proposal into an accepted ADR without decision evidence.

## Establish the proposal

1. Identify the reader, decision to be made, scope, document status, and authorized file. Continue within an already authorized docs request without another approval pause.
2. Read the current implementation, tests, constraints, related decisions, plans, and available Git history. Record the revision or release checked. Separate present behavior and contractual requirements from proposed behavior, estimates, and unknowns.
3. State the problem, goal, meaningful exclusions, proposed behavior, and owner or reviewer when known. Define domain terms that change the requirements.
4. Compare the strongest realistic alternative for a consequential choice. Name each option's cost, limitation, and reason for the recommendation. Do not invent alternatives for a trivial choice.

## Make review possible

Describe interfaces, data ownership, dependencies, failure handling, and compatibility where they affect the choice. Include measurable acceptance conditions and the evidence that would satisfy them. Address rollout, rollback, and operational impact when the proposal changes them. Assign unresolved questions to a known owner, or leave ownership visibly open.

Use `super-architecture` if the architecture choice still needs evaluation. It returns a recommendation and evidence to this document. Keep coding tasks with `write-plan`; do not implement endpoints, migrations, or configuration merely to finish the proposal.

For a useful figure, invoke `diagram` for a technical relationship or `infographic` for an audience-facing comparison. Keep current facts and proposed behavior distinct. Pass sources, uncertainty, and requested formats. An infographic may embed one verified diagram. Allow one handoff between the visual skills and no callback; avoid duplicate unsolicited visuals.

## Output and check

Use the local format. Otherwise include the proposal's status and audience, problem and current evidence, goals and scope, proposed behavior, alternatives and trade-offs, acceptance and rollout, rollback, and open decisions. Use exact wire names, units, paths, and interfaces.

Reopen the finished document. Check present-state claims against the named revision, links, example commands, unresolved placeholders, unsupported guarantees, and contradictions between prose and figures. A target is not a measured result. Label illustrative or unrun examples and report missing evidence. Edit documentation only unless the user separately asked for implementation.
