# Design, theme and interaction procedure

## Establish the real journey

Identify audience, entry point, primary task, important content, next destination, exit and recovery. Walk the current interface with representative data. Inspect first use, populated content, loading, pending, success, empty, failure, partial results and permission-limited states where they occur. Keep optional permissions and onboarding tied to the task.

Distinguish a missing reusable token, a one-off implementation of an existing component, a conceptual flow mismatch and a local defect. Fix the narrowest correct owner. For a formal critique or a refine/redesign decision, use the [design audit](design-audit.md). For a broad feature inventory, use [journey QA](journey-qa.md). Put the primary task before secondary editing; make action labels explicit. Preserve drafts and selection across Back, dismissal, failures and refresh. A healthy empty state teaches one next step. A failure is not an empty result; provide a concrete retry/recovery path and access to complete diagnostic text.

Group related information through spacing, alignment and type hierarchy. Working app screens need useful density, quiet chrome and readable records; they do not inherit marketing-page hero sizes, image quotas or artificial metrics. Use real content, honest fixture labels and meaningful status. Remove ornament that obscures the task without thinning useful content. Reserve prominent filled actions for the current primary task or an explicit destructive confirmation.

## Choose and inspect a constrained target

Use a supplied approved image first. For substantial visual changes, capture a valid incumbent baseline and state what may change. When useful and available, generate a realistic target with actual copy, controls, assets and platform constraints, then inspect it before UI edits. Compare two or three bounded directions only when a novel layout, identity or palette choice needs exploration.

Record target dimensions, screen/state and intended departures. Reject impossible native chrome, misleading capability, illegible copy or unsupported controls. Generated targets guide hierarchy; exact token definitions and real platform constraints take precedence. Build real controls rather than a flattened image background. For a novel interaction with no product precedent, make two or three small competing prototypes and compare the task path, comprehension, accessibility, implementation cost and actual feel on the same device. Select one and discard the others before production work. Small technical fixes and audits do not require new concept images. If rendering/generation is unavailable, continue source-grounded work with that limit explicit.

## Extract and maintain the design system

Inspect supplied images and neighboring screens before inferring values. Record concrete color roles, typography, spacing, radii, borders/elevation, icon sizing, component anatomy/states, navigation and motion. Separate measured values from estimates. Reuse the incumbent system unless the user authorized a replacement. Use a compact spacing/type scale appropriate to the platform; optical alignment and long-content readability matter more than forcing every size onto a fashionable grid.

Document the selected direction, exact semantic values, component variants, responsive behavior, motion policy, accessibility and evidence in the project's existing design-system document. New tokens need consumed roles; do not add unused ramps, framework dependencies or speculative components. Preserve existing brand assets during theme work unless identity changes are requested.

## Build calming Light, Dark and System themes

1. Establish mood, medium, audience, existing brand constraints and supported modes from available context. Calming is a design goal to inspect, not a numeric score.
2. Compare suitable methods. Anchor-derived perceptual ramps provide controlled roles; extraction/desaturation preserves an existing identity; harmony or cyclic schemes suit more expressive work. Explain the choice briefly rather than prescribing a hue for every product.
3. Use OKLCH for perceptual palette/ramp work. Define lightness progression and restrained chroma; map out-of-gamut colors by reducing chroma while preserving lightness/hue as far as possible. Use a verified conversion tool or library rather than naive RGB channel clipping. A tooling dependency need not become a runtime dependency.
4. Keep reference colors → semantic roles → component consumption. Define canvas/panel/surface, text/secondary/muted, accent/on-accent, selection/on-selection, focus, control boundary, placeholder and required status roles. Keep decorative dividers distinct from boundaries needed to identify controls. Domain colors, such as a user-selected group color, keep their meaning.
5. Map roles separately for both modes. Dark is not an inversion: tune neutral surfaces, chroma and readable foregrounds. System follows the actual platform preference; an explicit choice overrides it. Preserve native control color scheme and accessibility preferences. Keep fallbacks compatible with the deployment target; avoid raising the browser/OS floor incidentally.
6. Verify every consumed text/surface and control-state pair. For WCAG contrast-ratio checks use at least 4.5:1 for normal text, 3:1 for large text and required non-text control/focus indicators against adjacent colors. Large means at least 24 CSS px, or about 18.67 CSS px when bold. Decorative elements and disabled states are not normal-text claims. If using another contrast model, label its metric and thresholds separately.
7. Check actual computed/painted combinations, including opacity, hover, pressed, selected, placeholder and focus. Contrast ratio uses linearized sRGB luminance: (lighter + 0.05) / (darker + 0.05). Account for the actual composited background. Treat images, complex opacity and native rendering as separately inspected cases when the sampler cannot model them.
8. Test forced/high contrast and reduced transparency when supported. On the web, a probe with forced-color-adjust disabled can verify authored semantic aliases; browser-forced body text alone can hide a broken alias. On native platforms, observe actual preference APIs and refresh existing views when preferences change.

Sample settled states after finite transitions. Do not count a slider's internal value as painted text or imply all animation frames were measured. Keep static calculations, rendered samples and qualitative appearance review as distinct evidence.

## Interaction and responsive layout

- Use real headings, links, buttons and associated labels. Give icon-only controls accessible names and visible focus. Keyboard order follows the visual task. Native apps use their framework's accessibility semantics.
- Preserve familiar navigation. Tabs are peer destinations, drill-down uses the established stack, bounded tasks use an existing sheet/dialog pattern. A local polish pass does not rebuild navigation.
- Named destructive confirmation has explicit Cancel and outcome copy. Make it quieter before arming, prevent duplicate pending submission and preserve failure context. Give one owner to success announcements. Reset confirmation with its selected record and handle async identity as described in the architecture guide.
- Match actual target units. iOS commonly uses 44 pt and Android 48 dp touch regions; desktop density follows native conventions. For web touch/coarse input, target about 44 CSS px where applicable. Enlarge hit regions without inflating small native glyphs. Check gaps and overlapping hit areas instead of treating a number as full certification.
- Reflow navigation and detail actions at narrow widths. Keep the active destination visible. If horizontal navigation scroll is intentional, confine it to that region; body overflow remains a defect. Inline shorthand styles must not override responsive CSS sizing.
- Read complete selected-item titles and critical identifiers; wrapping or expandable details can retain dense lists. Check long/missing/localized copy, zoom and large text. Preserve diagnostic selection/scroll across refresh and clamp it when content shrinks.
- Native mobile layouts use actual safe-area, keyboard and scalable-type APIs. Check the shortest supported viewport, keyboard-open actions and scrolling to the last field. macOS retains native menus/tabs/control behavior; iPhone navigation and typography rules are not transplanted into AppKit.

## Motion with a purpose

Use the [motion procedure](motion.md) to audit or create transitions. Native custom colors resolve from the supplied appearance and are refreshed rather than frozen into cached platform colors.

## Inspect and finish

Capture after assets/fonts load at the target viewport and relevant states. Compare hierarchy/proportion first, then typography, spacing, colors and assets. Use same-size images for parity claims; concept images with different dimensions cannot establish pixel equality. Check controls and resulting state as well as screenshots.

Batch material fixes, rerender affected states and inspect again. Stop when the authorized slice and its acceptance conditions are satisfied. Report remaining mismatches and unavailable surfaces instead of aesthetic scores or unsupported accessibility/release claims.
