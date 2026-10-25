---
name: product-polish-workflow
description: "Use when an existing product needs a code or design audit, user-journey QA, UI/UX polish, design-system or theme refinement, branding or motion work, or a detailed next-feature implementation plan."
---

# Product polish workflow

Improve the actual product using current source, observed journeys and the user's scope. The procedures are embedded in this package. Read only the local guides relevant to the task, then work step by step. You may invoke other skills when useful.

| Task | Local procedure |
|---|---|
| Code, architecture, asynchronous state or maintainability | [Source audit and boundaries](references/architecture.md) |
| UI/UX, palette, design system, accessibility or motion | [Design and interaction](references/design.md) |
| Evidence-based design critique or refine/redesign decision | [Design audit](references/design-audit.md) |
| Broad feature inventory or end-to-end user-story testing | [Journey QA](references/journey-qa.md) |
| Create, audit or tune UI motion | [Motion](references/motion.md) |
| Logo, SVG assets or animated identity | [Branding](references/branding.md) |
| Runtime checks and evidence limits | [Verification](references/verification.md) |
| Detailed feature plan or handoff | [Planning and delivery](references/delivery.md) |
| Full product-polish result | [Minimum result and handoff template](references/minimum-result.md) |
| Optional project examples | [Eave](examples/eave.md), [Tabshelf](examples/tabshelf.md) |

## Workflow

1. **Establish scope.** Locate the repository, read governing instructions, current Git state, manifests and relevant design/architecture documents, then inspect affected source and callers. Name the audience, primary task, requested mode and acceptance conditions. Audit/plan-only work remains read-only. Preserve unrelated work and current authorization; old branch reports do not authorize Git or release actions.

2. **Audit the path.** Trace entry, state owner, rules and effects. Walk the real journey and required empty/pending/failure/recovery states. Record findings with severity, impact, source, evidence and closure condition. Distinguish reproduced defects, inferred risks and optional improvements. Use one canonical tracker when the request covers many user-visible features. Fix task/data/privacy/state failures before cosmetic drift.

3. **Choose a bounded direction.** Preserve the incumbent platform and useful conventions. Reuse tokens/components. For a novel interaction or architecture choice without precedent, compare two or three small prototypes against the same task before choosing. Inspect an available target before meaningful visual edits. Define semantic theme roles, component states, responsive behavior and motion/fallback rules. Keep generated concepts distinct from runtime evidence.

4. **Implement the authorized slice.** Reproduce behavioral defects first. Simplify at the correct owner; avoid speculative layers, dependencies and migrations. Model record, visit, editor and request lifetimes where needed. When delegation is authorized, give disjoint ownership, evidence, dependencies and acceptance; keep shared assets under one owner. Review specification compliance and quality, then fix and re-review material findings.

5. **Verify the real result.** Derive commands from the project's toolchain. Check behavior, production packaging, rendered states and motion on their matching surfaces. Inspect Light/Dark/System, supported sizes, focus and relevant accessibility preferences. Use isolated fixtures. Record command/observation, source state, outcome and artifact; distinguish passed, failed, skipped and unavailable checks. Historical results are not current proof.

6. **Leave a concrete continuation.** Update the design system and affected docs. Use the [minimum result](references/minimum-result.md) for a full polish engagement and scale it to narrower scope. Keep implemented work separate from proposed features; give requested plans files/contracts, states, dependencies, verification and delivery gates. Check the final diff. Report user-visible results, actual paths, checks, remaining limits and Git state.

## Done when

The authorized result is reviewable and its evidence supports the claims. Optional project examples do not constrain other repositories. Profile copywriting, greenfield stack selection and unrelated tasks fall outside this workflow. [Source provenance and adaptation notes](references/sources.md) provide attribution only.

## Related skills

- `design-system-kit`: design tokens, component library, UI critique or DESIGN.md in depth.
- `codebase-learner`: map the codebase before a broad source audit.
- `execution-ready-spec-plan` or `write-plan`: the next feature needs a full plan.
- `tdd`: fix a reproduced behavior defect test-first.
- `verify`: prove the polished result on the real surface.
