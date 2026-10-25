# CSS keyframe animation inside SVG

Use this for **self-contained animated SVG**: motion lives in a `<style>` block in `<defs>`, classes on groups and shapes, and `@keyframes`. No JavaScript required. Browsers and many design tools play it when the file opens.

This is separate from the bundled **semantic highlight** helper (`export_svg.py animate` / `gif`), which overlays rectangular focus steps on a static diagram. Use CSS motion for ambient loops, staggered sequences, stroke reveals, and brand-style marks. Use the highlight helper for a short, finite walkthrough on dense technical graphs when you do not want to hand-author keyframes.

In the levistack repo, full references are `docs/assets/logo-animated.svg` (logo plus stepped UI spine) and `docs/assets/icon-animated.svg` (icon loop). Study them before inventing a new pattern.

## When to choose CSS motion

| Goal | Approach |
|---|---|
| Looping icon, mascot, or subtle ambient motion | CSS keyframes in SVG |
| Ordered steps on a process diagram with stable layout | CSS stagger (`animation-delay`) or highlight helper |
| One-shot social GIF without SVG playback | Render CSS SVG to GIF via browser capture or `export_svg.py gif` only when a static SVG plus plan exists |
| Facts that must not depend on motion | Complete still frame; motion is decorative or sequential emphasis only |

## Authoring rules

1. **Static meaning first.** Every label, node, and edge must read correctly with animations disabled. The first painted frame should be usable as a still.
2. **Named structure.** Stable `id` on clips, filters, and semantic groups. Classes only for motion (`float`, `steam`, `step`, `s1`…), not for one-off geometry.
3. **Transform origin.** Set `transform-origin` on groups that rotate or float so motion pivots predictably.
4. **Stroke motion.** `stroke-dasharray` and `stroke-dashoffset` keyframes suit path reveals (steam, spine, connectors). Reset dashoffset in reduced-motion.
5. **Staggered sequence.** Share one `@keyframes` block; use per-element `animation-delay` classes (for example `s1`…`s7`) for ordered emphasis. Delays must match a declared step list in the receipt.
6. **Opacity and glint.** Prefer `stroke-opacity` or `fill` keyframes for emphasis, not sole encoding of state.
7. **Timing.** Use one master duration per loop (for example 4.6s or 6s) and `ease-in-out` unless a step needs `steps()` (for example a blink cursor).
8. **Accessibility.** Root `role="img"`, `aria-label` or `aria-labelledby` with `<title>` / `<desc>`. Decorative fog or glint must not replace text equivalents in the deliverable package.
9. **`prefers-reduced-motion`.** End the stylesheet with a block that disables animations and restores visible static geometry:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    stroke-dashoffset: 0 !important;
    opacity: 1 !important;
    transform: none !important;
  }
}
```

10. **No script in the SVG** for factual diagrams unless the user explicitly wants interactive controls; then follow the SVG and motion guide for Play/Pause and reduced motion in HTML wrappers.

## Mermaid and other sources

Render Mermaid to SVG first. Add CSS animation in a **copy** or a dedicated `*-animated.svg` so the static export stays available. Do not assume Mermaid CLI will preserve hand-added `<style>`; verify after any re-render.

## Verify

Open the file in a browser or SVG viewer at target size. Check:

- first frame (still export mentally or duplicate file without animation);
- one full loop at 1x;
- reduced-motion media query (animations off, dash offsets cleared);
- text legibility and contrast at export width;
- clip paths and filters still apply while animating.

Record loop duration, class-to-meaning map, and checks run in the delivery receipt.

## Hand off to infographic

Deliver:

- `figure.svg` (static) and `figure-animated.svg` when both are needed;
- which elements map to which semantic steps;
- confirmation that reduced-motion leaves a complete figure.

Infographic embeds the animated SVG inline or by reference without stripping `<style>` or `@media` blocks.
