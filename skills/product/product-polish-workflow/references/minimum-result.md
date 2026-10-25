# Minimum result for a full product-polish engagement

Use this when the user authorizes a broad audit, product polish and next-development plan. The [Eave](../examples/eave.md) and [Tabshelf](../examples/tabshelf.md) examples show the result shape on different platforms. Their names, architecture, colors, commands and test counts are not defaults for a new product.

## Deliver the product and its evidence

| Result | Minimum content | Check |
|---|---|---|
| Current product map | Primary user task, entry points, state owners, effects, storage and privacy boundaries, and source anchors | Each material claim points to current code or an observed journey |
| Prioritized audit | Reproduced defects and inferred risks separated by severity, impact, evidence and closure condition | The first implementation slice addresses the highest-impact in-scope failure |
| Implemented polish | Working primary journey and affected first-use, populated, empty, pending, failure and recovery states; correct focus, selection and data preservation | Exercise the changed behavior and its relevant races on the actual product boundary |
| Design system | Consumed color/type/spacing roles, Light/Dark/System where supported, component states, responsive or native layout, accessibility and motion behavior | The implementation uses the documented tokens and states; rendered samples match the chosen direction |
| Identity and assets | Brand/copy decisions grounded in the product; requested static or animated assets and real consumers | Inspect the delivered files, small-size use, fallback and production packaging when applicable |
| Verification record | Source state, commands, observed results, rendered evidence, limits and exact prerequisites for unavailable checks | Distinguish tests, builds, previews, native/device observation and release acceptance |
| Next-development plan | Recommended next slice, current versus proposed behavior, files/contracts, state and error paths, dependencies, acceptance and rollout/rollback where relevant | A developer can implement the first proposed slice without inventing its contract |

Update the project's existing architecture, design, verification and plan documents. Create a document only when no canonical home exists. For substantial visual changes, include an inspected preview of representative states; Tabshelf used a gallery, while Eave's unavailable native capture remained an explicit limit. A plan never stands in for an authorized implementation, and a passing test never stands in for a visible UI check.

## Fill the handoff with actual results

```markdown
# Product polish result: <product and scope>

## Delivered
<User-visible changes and the specific task they improve. Link changed code and design assets.>

## Evidence
<Current source/branch, reproduced findings, commands, observed outcomes, and preview or device states inspected.>

## Design and architecture
<Canonical documents updated, token/state/ownership decisions, and why they fit this product.>

## Limits
<Failed, skipped or unavailable checks and what each remaining gap prevents us from claiming.>

## Next slice
<One recommended feature with files/contracts, user journey, acceptance and dependencies. Mark it proposed.>

## Git state
<Actual branch and commit status.>
```

Scale the result to the request. An audit-only task delivers grounded findings and a plan without product edits. A narrow fix needs its changed behavior and focused proof, not every row above. Skip brand assets, themes, migrations and API contracts when the product or scope does not need them. Never carry historical Eave or Tabshelf pass counts into a new result.
