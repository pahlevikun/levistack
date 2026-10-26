# Formats and export

Set the destination before designing. Save the editable source, data and generator outside the installed skill. Export only the formats the user needs.

| Surface | Production approach |
|---|---|
| Documentation or a research page | Responsive HTML or SVG with a text equivalent, source ledger and nearby methods |
| Static poster | SVG or a layout source, then PNG or PDF at the intended size |
| Slide | Use the deck's actual aspect ratio and theme. Check labels at presentation distance |
| Social feed | Recompose for the requested landscape, square or portrait frame. Check mobile reading size |
| Carousel | One bounded takeaway per page, consistent sequence and sources that survive a shared single page |
| Print | Physical dimensions, margins, fonts and color handling agreed with the destination |
| Animation | Editable source, explicit step plan, finite preview and complete still |

Ratios such as 16:9, 1:1, 4:5 and 9:16 are useful working frames. They are not a promise of current platform requirements. Before publication, check the destination's primary documentation for dimensions, crop, file size and safe zones. Do not require a network service to produce a local asset.

## Readability

Measure text in its rendered context. A 24-unit label in a 1200-unit SVG becomes 8 pixels if shown 400 pixels wide. Increase type, reduce density, split the figure or provide a close-reading view. Do not shrink a source or caveat until it disappears.

For web, preserve readable body text at the smallest viewport and browser zoom. For a dense comparison, consider an accessible scroll region or small multiples. Keep direct labels, units and caveats together after reflow. Hover-only detail needs a keyboard and touch path. The resting view must still communicate the claim.

For print, check the actual page size and expected distance. Preserve live text in the editable source and disclose font substitutions. An outlined export can help printing when needed, but it needs a separate accessible text equivalent.

## Exact exports

For SVG, include a `viewBox`, accessible title/description and real vector marks. For PNG, verify actual pixel dimensions, background and alpha. For PDF, check physical size and font output. Render the exact file that will be delivered.

Use a local renderer or the project's export command. This skill has `png_from_svg.py` and `export_figure.py` (see [figure exports](figure-exports.md)). Reuse technical receipt commands for GIF or batch PNG when those tools are installed. Otherwise state the missing renderer and preserve the source.

Keep originals when compressing. Measure actual bytes saved and inspect small text, line edges, alpha and chart colors. An export optimized for one host may need a different format on another.

## Motion

Animate an actual sequence, relation or change. Declare step order from the evidence. Keep layout and semantic labels stable, and provide a complete still. In HTML/SVG, respect reduced motion and keep the meaning available with scripts disabled. A GIF needs a still alternative and a preview of its encoded palette.

**CSS-animated SVG** (keyframes and classes inside the file) may embed directly in a poster or page. Preserve the full `<defs><style>` block and the `prefers-reduced-motion` reset. Offer a static SVG or PNG alongside the animated file for feeds that auto-play or block animation. Page-level motion (carousel transitions) is separate from in-file SVG loops; both need a still that carries every factual claim.

For **sequenced infographic** motion (staggered icons, key numbers, connectors), use [animated SVG sequenced](animated-svg-sequenced.md) and `scripts/build_animated_svg.py`. That path does not export MP4. Rasterize a hold frame with `png_from_svg.py` when a feed needs PNG.

Keep autoplay finite and give controls when playback is long or interactive. The user should not need to wait for a caveat or pause on a moving number to understand the evidence.

## Publication handoff

A finished local asset is the default output. Do not schedule or post it without authorization. If publication is requested, preview the exact file, copy, alt text, account and destination. Verify stored payloads when that flow permits reading them back. Preserve real paragraph breaks and check duplicate submissions before retrying a write.

Run [publishing gate](publishing-gate.md) on scheduler payloads. Confirm [publication boundaries](publication-boundaries.md) for rights and attribution before open or client release.
