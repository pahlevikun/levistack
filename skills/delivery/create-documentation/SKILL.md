---
name: create-documentation
description: "Write source-checked technical documentation and client API handovers. For handovers, reads Bruno first, creates a missing collection, then reconciles code, Git history, plans, existing docs, and available Swagger/OpenAPI for supported response variants and states. Use when asked for technical writing, a README, API reference, PDF/HTML/DOCX API handover, endpoint and field explanations, full error responses, lifecycle states, process or payload documentation, doc comments, or a docs check after a diff. Not for an ADR, design doc, or RFC (write-adr), runbook (write-runbook), postmortem (write-postmortem), changelog or release notes (write-changelog), repo map (codebase-learner), implementation plan (write-plan), MR description (write-mr-description), or prose polish alone (polyglot-copywriter)."
metadata:
  version: 1.4.0
  author: levistack
  license: MIT
  group: delivery
  category: delivery
  department: delivery
  related_skills:
    - diagram
    - infographic
    - codebase-learner
    - create-bruno-collection
    - write-adr
    - write-changelog
    - write-postmortem
    - write-runbook
    - polyglot-copywriter
  invokes:
    - skill: diagram
      when: Docs need technical figures
    - skill: infographic
      when: Documentation needs an evidence-based visual explainer, comparison, or timeline, optionally embedding a verified technical figure
    - skill: codebase-learner
      when: Module map is unknown
    - skill: create-bruno-collection
      when: API handover requires a missing collection or missing supported variant cases before drafting or final delivery
    - skill: polyglot-copywriter
      when: Documentation prose needs plain-language revision while preserving technical meaning
  tags:
    - documentation
    - technical-writing
    - api
    - handover
    - bruno-first
    - response-variants
    - process
    - contract
  capabilities:
    - feature_documentation
    - api_reference
    - client_api_handover
    - bruno_prerequisite
    - api_variant_and_state_coverage
    - complete_error_responses
    - process_documentation
    - contract_documentation
    - documentation_freshness
  languages:
    - en

---

# Create documentation

Write documents readers can use and maintainers can check. Identify the reader's task and choose one job below. Follow that job's evidence order. Load only its reference and the shared writing guidance.

For technical writing across all jobs, read [writing-style.md](references/writing-style.md). `polyglot-copywriter` can refine prose while preserving code, commands, paths, wire names, and meaning.

## Pick the job

| The user wants | Job | Read |
|---|---|---|
| Pages for a feature, module or project | **write** | [pages.md](references/pages.md) |
| An API reference | **api** | [api-reference.md](references/api-reference.md) |
| A client HTTP API document to share as PDF, HTML or DOCX | **handover** | [api-handover.md](references/api-handover.md) |
| A business process, handoff, workflow or state machine | **process** | [processes.md](references/processes.md) |
| An event, webhook, message, file or shared payload contract | **contract** | [contracts.md](references/contracts.md) |
| Doc comments inside the code | **comments** | [code-comments.md](references/code-comments.md) |
| To know which docs a change made wrong | **check** | [check-after-change.md](references/check-after-change.md) |

For **handover**, also load [api-glossary.md](references/api-glossary.md) and start from [the handover template](templates/api-handover.md). The glossary explains API parts. The handover reference covers HTTP outcomes and business lifecycle states separately.

ADRs, design documents, RFCs, runbooks, postmortems, and changelogs have independent owners: `write-adr`, `write-runbook`, `write-postmortem`, and `write-changelog`. Invoke the matching skill directly for those requests instead of treating them as modes here.

If the request mixes jobs, check existing documentation first and write only the gaps. A handover package may contain a quick start, an explanation, and reference sections. Keep those sections distinct so a reader can find each kind of information.

When a visual helps, use `diagram` for technical relationships or `infographic` for an evidence-based visual explainer, comparison, or timeline. An infographic can embed a verified technical figure. Pass the sources, uncertainty, requested formats, and any completed technical pass. Allow at most one handoff between the visual skills for an artifact; the receiving owner finishes without calling back. Keep figures within the requested document scope.

## Rules for every job

1. **Read-only on application code.** Edit docs and doc comments. For an API handover, collection creation or completion runs through `create-bruno-collection` as a prerequisite. This does not authorize implementation changes or live writes.
2. **Research before writing.** Read entry points, types, serializers, tests, config, and relevant records. For a wide area, use `codebase-learner` in explain mode first. Record source locations and the revision or snapshot checked.
3. **One purpose per section.** Separate tutorials, how-to guides, references, and explanations. Link them or package them as distinct sections when one deliverable needs several.
4. **Verify examples honestly.** Prefer safe local tests or a disposable environment. Do not execute destructive commands or contact production merely to verify documentation. Label examples that were not run and distinguish syntax, schema, fixture, and live checks.
5. **No invented behavior.** Tie implemented behavior to code, a test, or a run. Tie history to records. Mark proposals, inference, unknowns, and conflicting evidence. Private internals are not public contracts.
6. **Use the repo's own places.** Follow its docs folder, README sections, and doc-comment style. If no convention exists, use `docs/` for a requested document or present a draft when the write destination matters.
7. **State the file list before writing.** Proceed when the user's request already authorizes those docs. Ask only for missing scope or required approval. A review-only request stays read-only until edits are requested.
8. **Review the whole result.** Apply the writing guidance, open links, check inventories against sources, and inspect exported artifacts. Keep accepted historical records intact and make corrections traceable.

## API handover prerequisites

Inspect the target Bruno collection before drafting. If it is absent, invoke `create-bruno-collection` to create it first from the available contracts and code. Read the resulting collection, then study the codebase, relevant Git history, available plans and docs, and Swagger/OpenAPI. Reconcile these sources for the target release. Historical or proposed behavior is not proof of current behavior.

Build an operation inventory and a scenario matrix. Cover every evidenced success and error branch, payload variant, business state, and allowed transition. Each supported error scenario needs the complete HTTP response with status, headers, and body, plus its trigger and caller action. A list of error codes or a shared schema alone is insufficient.

For each operation, include a copyable cURL command and the matching sample request JSON when it accepts JSON. Show complete sample response JSON for each supported JSON success, error, and conditional outcome, alongside HTTP status and relevant headers. State explicitly when a request or response has no JSON body. Derive samples from the reconciled contract and label anything not run.

Complete missing collection cases through `create-bruno-collection` before final handover. An unrun case is not a missing case; label its verification honestly. If required definitions, fixtures, or write access are unavailable, report the gap and keep the result a draft. If the user forbids collection edits, honor that scope and name any prerequisite that remains incomplete.

## Done when

- The document fits the requested audience, job, and authorized write scope.
- Claims and inventory coverage have source evidence. Unknowns and contradictions remain visible.
- Examples, commands, links, and exports were checked at the stated level. Unrun examples and unresolved checks are named.
- Sections have clear purposes. External readers can use the deliverable without access to private source files.
- For **check**, report the coverage map and preserve review-only scope unless fixes were requested.
- For **handover**, Bruno was read or created first, all available evidence sources were reconciled, and each supported variant has a collection case and complete document entry or an explicit unresolved gap. Do not claim complete coverage with gaps outstanding.
- Exercise the matching scenarios in [evals/evals.json](evals/evals.json), including a request that belongs elsewhere.

## Related skills

- `codebase-learner`: understand an area first (explain), or write one `ARCHITECTURE.md` of what exists (summarize).
- `create-bruno-collection`: required first when a handover collection is missing, and used to complete missing cases before final delivery.
- `write-runbook`: operational procedures with checks, recovery, and escalation.
- `write-adr`: architecture decisions, design proposals, RFCs, and their review or supersession history.
- `write-postmortem`: evidence-based incident and near-miss records after stabilization.
- `write-changelog`: release records and consumer migration notes.
- `diagram`: create and render a process, state, or architecture diagram when it answers the reader's question.
- `infographic`: compose an evidence-based visual explainer, comparison, or timeline for the document, retaining source facts and uncertainty.
- `write-plan`: turn an accepted design into implementation steps.
- `polyglot-copywriter`: simple words and short sentences for every page.
- `write-mr-description`: describe the change in the MR. Docs for readers of the product come here.
- `verify`: prove a documented command or claim by running it.
- `atomic-semantic-commit`: commit the docs separately from the code.
