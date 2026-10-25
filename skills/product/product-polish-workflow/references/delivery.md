# Concrete plans and delivery

## Keep the current contract clear

Use existing project documentation as the canonical home for architecture, design, verification and plans. Update the affected documents rather than creating competing sources of truth. Label implemented behavior, observed defects, assumptions, decisions and proposed capabilities separately. Historical reports and screenshots remain dated evidence rather than current execution claims.

For a bounded change, a short task note can be enough. For a requested detailed plan, make the work implementable and reviewable with the contract below. Add only artifacts relevant to the product: a UI polish does not automatically need a schema migration or API.

## Detailed implementation slice

| Required field | Content |
|---|---|
| Problem and outcome | Concrete trigger, affected user, current behavior and intended result |
| Source grounding | Current paths/contracts inspected; confirmed facts, unknowns and assumptions |
| Scope | In-scope work, non-goals and compatibility constraints |
| Domain/state | Entities, owners, identity/lifetimes, events, guards and terminal/error/recovery states |
| Journey | Entry → primary action → pending/result → Back/Cancel/retry; draft, focus, selection and scroll behavior |
| Implementation | Real modules/files to change or add; boundary, signatures and integration points |
| Data/storage | Only when needed: schema/table/field constraints, indexes, versions, privacy, migration/backfill and rollback |
| API/protocol | Only when needed: route/command, authentication, validation, idempotency, request/response/error examples and partial failure |
| Design | Semantic roles, component states, layouts, long/empty content, accessibility and native platform behavior |
| Motion | Trigger, property, timing/easing, interruption, final state and Reduced Motion fallback |
| Dependencies | Task prerequisites, external decisions, shared assets and owners |
| Verification | Behavior regressions, production build and real-surface checks; fixtures, evidence and unavailable prerequisites |
| Delivery gate | Observable acceptance, review closure, rollout/reversibility and any approval explicitly required by the user |

Use concrete request/response examples or state/sequence diagrams where they clarify the contract. Keep Mermaid in ordinary fenced Mermaid blocks. Do not add decorative diagrams for a one-step edit. A state machine must describe actual guards and transitions, not rename a linear checklist.

## Sequence useful phases

Order by dependencies and risk, not by file type. A practical sequence is establish/reproduce → correct ownership/data contract → implement one end-to-end slice → refine interface/states → verify/review → update delivery docs. Each phase has an input, owned output and a check that closes it. Shared contracts precede parallel consumers; coupled writers serialize or use isolated copies.

For next-feature exploration, prioritize the user problem, prerequisites and acceptance. Describe one recommended first slice and credible alternatives where they change risk or cost. Keep proposals distinct from authorized current implementation. New accounts, permissions, services, storage, deployment platforms or architectural migrations require an actual product need and current authorization; historical examples do not supply it.

Record a meaningful technology decision with the incumbent option, alternatives, deciding evidence, consequences, migration/rollback and what would change the recommendation. Do not replace a stack because a design tool defaults to another one. Avoid arbitrary maturity/beauty scores, fabricated estimates or promises of perfect pixel/security/accessibility results.

## Handoff a reviewable result

Report the user-visible result first, followed by the ownership/implementation detail needed to maintain it. Include actual repository paths, affected design/architecture documents, verification commands/results and evidence, remaining limits and observed Git state. Mention commits or publishing only as actually authorized and performed.

For a full product-polish engagement, use the [minimum result and handoff template](minimum-result.md). Its deliverables are drawn from the [Eave](../examples/eave.md) and [Tabshelf](../examples/tabshelf.md) examples. Scale the result to the authorized scope; a single-screen fix does not require a project-wide plan or new documents.

For multiple repositories, give each a separate result and keep shared assets/evidence under one owner. A future session rereads source and status rather than inheriting an old pass. Preserve useful checkpoints for long work, including completed work, open decisions, failed approaches that shaped the result and concrete next steps.

A compact handoff contains:

- Implemented slice and who benefits.
- Changed behavior, state/ownership and documentation paths.
- Checks actually run, source/build provenance and inspected artifacts.
- Unverified behavior and the exact missing environment or evidence.
- Current branch and committed/uncommitted state, when relevant.
- Proposed next slice with its acceptance gate, only when requested or needed for continuation.

Do not end a requested implementation at a plan or an offer to continue. Complete the authorized reversible work, fix material review findings and leave any genuine blocker explicit. Audit-only and plan-only requests finish with their requested documents rather than source edits.
