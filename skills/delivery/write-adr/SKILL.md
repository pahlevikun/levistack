---
name: write-adr
description: "Write evidence-based architecture decision records, design documents, and RFC, using current code, decision history, realistic alternatives, documents, attachments, image, mermaid, diagram, infographic, brainstorm output, user discussion, and clear review conditions. Use when asked to draft, review, consult, accept, or supersede an ADR, or to write or revise a technical proposal, design document, or RFC. Not for implementing the design, an implementation plan (write-plan), choosing an architecture style (super-architecture), or documenting an existing API contract (create-documentation)."
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - super-architecture
    - write-plan
    - create-documentation
    - diagram
    - infographic
    - polyglot-copywriter
  invokes:
    - skill: super-architecture
      when: The architecture choice still needs evaluation
    - skill: write-plan
      when: An accepted decision or design needs implementation steps
    - skill: diagram
      when: A technical relationship or flow needs a verified figure
    - skill: infographic
      when: A proposal needs an audience-facing visual comparison or explainer with current and proposed evidence kept distinct
  tags:
    - adr
    - architecture-decision-record
    - decision-history
    - design-doc
    - rfc
    - proposal
  capabilities:
    - adr_authoring
    - adr_review
    - decision_lifecycle
    - design_documentation
    - proposal_evidence_and_acceptance
  languages:
    - en

---

# Write an ADR or design document

Write a reviewable design proposal or record one consequential decision. Preserve the target repository's document format and accepted decision history.

## Pick the job

| Request | Job |
|---|---|
| Draft or revise a broad design document, technical proposal, or RFC | **Proposal**: [design-doc.md](references/design-doc.md) |
| Draft a formal architecture decision record | **ADR draft**: use the ADR procedure below |
| Check a proposed ADR | **ADR review**: use the ADR procedure below |
| Find the decision that governs a change | **ADR consult**: use the ADR procedure below |
| Accept, reject, deprecate, or replace an ADR | **ADR lifecycle**: [lifecycle.md](references/lifecycle.md) |

ADR review and consultation are read-only unless the user also asks for edits. A proposal does not become an accepted ADR by being well written.

## ADR procedure

1. Find existing ADRs, their index, filename or numbering scheme, status terms, and template. Follow that convention. If none exists, use [the small fallback template](templates/adr.md) in the existing docs tree without creating a fake initial decision or index.
2. Read the affected code, tests, plans, related ADRs, and available decision notes. Inspect relevant Git history when it explains a prior choice. Separate current implementation from a proposal and an approved decision. Code presence alone does not prove acceptance.
3. For a new record, check that an earlier ADR has not already made the decision. Cite or link the record when it has. Use `super-architecture` when the architecture choice still needs evaluation; it returns the recommendation and evidence here without authoring the record. For a broader proposal, use this skill's Proposal job before recording an accepted choice.

### Write or review the decision

State DARCI roles when known, context, and a distinct problem statement. Document each realistic approach in **Approaches** with a mermaid or diagram figure, pros, cons, and consequences; omit alternatives the evidence does not support. Name the decision in one sentence and tie it to the chosen alternative. Add reversibility or a revisit trigger when useful. Do not manufacture options merely to fill [templates/adr.md](templates/adr.md).

Keep one decision per record. Label unknown rationale, missing authority, and open questions. Do not set `accepted` just because a draft is well written or implementation exists. When the repo requires a decision owner or date, use an evidenced value or leave a visible gap. Link the governing code and related records when available.

For **Review**, check the problem statement, DARCI gaps, decision, evidence, each approach (figure, pros, cons, consequences), status, links, and whether the record conflicts with another accepted decision. Report concrete gaps. Do not silently edit accepted history. For **Consult**, identify the governing accepted record and its scope; if records conflict or are superseded, show the chain and current uncertainty.

## Verify the document

For an ADR, check the actual file and index for unique numbering, status consistency, links, source-backed claims, and bidirectional supersession links where the repo uses them. For a design proposal, check present-state evidence, acceptance conditions, unresolved decisions, and consistency between prose and visuals. A proposal with open questions is a valid draft, but it is not an accepted decision. Report what was checked and what remains unknown. Use [evals/evals.json](evals/evals.json) to exercise both jobs and routing boundaries.

## Related skills

- `super-architecture`: evaluate and choose a software architecture before recording it.
- `write-plan`: turn an accepted decision into implementation steps.
- `create-documentation`: document the implemented behavior that results from a decision.
- `diagram`: show an evidence-backed technical relationship or flow.
- `infographic`: show a sourced visual comparison or explanation while preserving current and proposed labels.
- `polyglot-copywriter`: refine the prose without changing technical facts.
