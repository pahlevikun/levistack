# Design and interaction procedure for a shipped product

This guide covers the part of design work that belongs to polishing a product that already ships: the real journey, the constrained target, who owns what, and how to finish. Palettes, systems, components and motion each have an owner skill. Call the owner. Do not repeat its rules here.

## Who owns what

| The work is about | Call | You keep |
|---|---|---|
| A palette, a brand color, Light or Dark or contrast modes, color tokens, a contrast fix, a color audit | `color-kit` | Scope, the shipped surface and the evidence that the result renders correctly |
| One screen or one component: hierarchy, states, motion, UX, gestures, forms, platform behavior (iOS, Android, React Native, Flutter, desktop, web, car, TV) | `ui-ux-kit` | The journey, the acceptance rows in the tracker and the code change |
| The token file, type and space scales, `DESIGN.md`, library governance, a critique against a system | `design-system-kit` | Which parts of the product adopt it first |
| A throwaway answer to one open question | `prototype-wireframe` | The decision and what goes into the plan |

The call is a gate, not a suggestion. When a task touches one of the first three rows, load that skill and use its steps and its files.

## Establish the real journey

Identify audience, entry point, primary task, important content, next destination, exit and recovery. Walk the current interface with representative data. Inspect first use, populated content, loading, pending, success, empty, failure, partial results and permission-limited states where they occur. Keep optional permissions and onboarding tied to the task.

Distinguish a missing reusable token, a one-off implementation of an existing component, a conceptual flow mismatch and a local defect. Fix the narrowest correct owner. For a formal critique or a refine/redesign decision, use the [design audit](design-audit.md). For a broad feature inventory, use [journey QA](journey-qa.md). Put the primary task before secondary editing and make action labels explicit. Preserve drafts and selection across Back, dismissal, failures and refresh. A healthy empty state teaches one next step. A failure is not an empty result: provide a concrete retry or recovery path and access to complete diagnostic text.

Group related information through spacing, alignment and type hierarchy. Working app screens need useful density, quiet chrome and readable records. They do not inherit marketing-page hero sizes, image quotas or artificial metrics. Use real content, honest fixture labels and meaningful status. Remove ornament that obscures the task without thinning useful content. Reserve prominent filled actions for the current primary task or an explicit destructive confirmation.

## Choose and inspect a constrained target

Use a supplied approved image first. For substantial visual changes, capture a valid incumbent baseline and state what may change. When useful and available, generate a realistic target with actual copy, controls, assets and platform constraints, then inspect it before UI edits. Compare two or three bounded directions only when a novel layout, identity or palette choice needs exploration.

Record target dimensions, screen and state, and the intended departures. Reject impossible native chrome, misleading capability, illegible copy or unsupported controls. Generated targets guide hierarchy. Exact token definitions and real platform constraints take precedence. Build real controls rather than a flattened image background. For a novel interaction with no product precedent, ask `prototype-wireframe` for two or three small competing prototypes and compare the task path, comprehension, accessibility, implementation cost and actual feel on the same device. Select one and discard the others before production work. Small technical fixes and audits do not need new concept images. If rendering or generation is unavailable, continue source-grounded work with that limit explicit.

## Work with the design system that exists

Inspect supplied images and neighboring screens before inferring values. Reuse the incumbent system unless the user authorized a replacement. Separate measured values from estimates. If the product has no token system, or the work needs one, hand that part to `design-system-kit` and take its tokens back. New tokens need consumed roles. Do not add unused ramps, framework dependencies or speculative components. Preserve existing brand assets unless identity changes were requested.

## Color and theme work

Load `color-kit`. It chooses the strategy, builds the roles for every mode, proves the contrast and binds the stack. In a shipped product you add three duties it does not have:

- **Preserve identity.** Tell `color-kit` which colors are confirmed and which are domain colors (for example a user-selected group color). They keep their meaning.
- **Check the shipped surface.** Sample painted pairs after finite transitions. Do not count a slider's internal value as painted text. Keep static calculations, rendered samples and appearance review as separate evidence.
- **Respect the deployment target.** Keep fallbacks compatible with the browser or OS floor. Native custom colors resolve from the supplied appearance and refresh when preferences change.

## Screen, component and interaction work

Load `ui-ux-kit`. It owns states, components, motion, gestures, forms, navigation and platform behavior. In a shipped product you add these duties:

- A local polish pass does not rebuild navigation. Preserve familiar navigation, tab and stack structure.
- Destructive flows: name the outcome, keep an explicit Cancel, prevent duplicate submission, keep failure context and give one owner to success announcements. Reset confirmation with its selected record and handle async identity as described in the architecture guide.
- Read complete selected-item titles and critical identifiers. Check long, missing and localized copy, zoom and large text. Preserve diagnostic selection and scroll across refresh and clamp them when content shrinks.
- Write the behavior you verified as acceptance rows. They join the journey tracker (see [journey QA](journey-qa.md)).

## Motion

Load `ui-ux-kit` and read its motion guide. Use the [motion note](motion.md) here only for how to audit motion that already ships.

## Inspect and finish

Capture after assets and fonts load at the target viewport and relevant states. Compare hierarchy and proportion first, then typography, spacing, colors and assets. Use same-size images for parity claims. Concept images with different dimensions cannot establish pixel equality. Check controls and resulting state as well as screenshots.

Batch material fixes, rerender affected states and inspect again. Stop when the authorized slice and its acceptance conditions are satisfied. Report remaining mismatches and unavailable surfaces instead of aesthetic scores or unsupported accessibility and release claims.
