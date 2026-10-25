# Original identity and SVG motion

Apply this procedure when logo, branding or identity assets are in scope. Theme refinement alone preserves the existing mark.

## Ground the brief

Read the product's real name, purpose, audience, existing mark, theme tokens, README and asset consumers. Record sources for name, copy and color; mark absent facts as unknown. Establish required deliverables, background/embedding contexts, small-size use and animation expectations. Use existing answers and authorization. Ask only for an unresolved brand decision that would materially change the work.

For an established identity, refine its real constraints. For a new or explicitly replaced mark, sketch several ideas from the product's actual behavior or metaphor, narrow to two or three distinct silhouettes and compare them in monochrome and at small size. A direction should fit this subject, not merely its category. Study other marks for composition; do not paste their artwork or invent a trademark-clearance claim.

## Deliver the requested asset set

Create an original reusable mark with a coherent visual grammar and optical alignment. Establish static artwork before animation. Use concrete paths/geometry, a correct viewBox and useful transparent/background variants. Keep brand colors in reference values and document their role mapping; native application controls need not inherit the brand's decorative colors.

When a full SVG icon/banner system with motion is requested, deliver:

- Static application/repository icon.
- Animated icon with a complete static fallback.
- Static wordmark/banner for the actual consumer's dimensions.
- Animated wordmark/banner with the same complete fallback.

Follow existing project asset names when possible; otherwise use explicit names such as `icon.svg`, `icon-animated.svg`, `logo.svg` and `logo-animated.svg`. Preserve a separate transparent template mark when native status/menu rendering needs it. A 512-square icon and 904×256 README banner are possible export contracts, not universal UI requirements. Add PNG, social, monochrome or platform exports only when requested or required by the actual project. Exported iOS/Android artwork does not establish mobile-app support.

Include a compact preview with light/dark grounds, small icon sizes, mark/wordmark usage, clear space, color values, font assumptions and motion policy. Keep product claims grounded. Do not force a three-column banner, terminal transcript, orbital motif or unrelated social kit onto every product.

## Author motion and fallback together

Choose choreography that reveals the mark's structure: draw/reveal, assemble, settle and hold where that suits the shape. Keep motion finite or give the complete mark a readable settled hold in a loop. Do not add a perpetual breathing effect as a substitute for a concept.

The base SVG is fully legible without animation. Apply initial hidden states only inside the motion-enabled CSS or equivalent mechanism; static renderers should not inherit invisible artwork. Reduced Motion shows the complete final mark and disables nonessential animation. Define duration, sequence, easing, interruption and expected looping behavior. Verify the real embedding mode, because inline SVG, image elements and documentation renderers can behave differently.

## Validate the actual assets

1. Parse each SVG as XML; check namespace, dimensions/viewBox, unique IDs, references and escaping of XML metacharacters. Resolve all fonts, filters, masks, clips and imported assets. Prefer self-contained assets when the consumer cannot fetch dependencies. Confirm no accidental active scripts or remote asset dependency was introduced.
2. Render the static icon/banner at delivery resolution and realistic small sizes. Open the images; inspect legibility, silhouette, alignment, clipping, clear space, light/dark contrast and fidelity across exports.
3. Play the animated variants in an actual compatible renderer. Observe time advancing, the intended reveal, final hold and loop boundary. A static raster comparison cannot prove playback.
4. Activate Reduced Motion and inspect the complete settled mark plus computed animation state. After CSS pruning/optimization, repeat this check; visually identical static images can hide deleted accessibility rules.
5. Load the assets through the actual application/package/README import path. Build the production artifact and inspect its output; a mocked import and typecheck do not establish bundler resolution. Check SVG support and dimensions in the real documentation embedding mode.
6. Verify each requested PNG/platform export's dimensions, transparency/background policy, content bounds and consistency with the source mark. Record unsupported formats or unavailable renderers explicitly.

Use the project's existing validators/renderers when available. If they are missing, perform these checks directly with available XML, raster and browser tools; no external skill installation is required. Never claim a validator or renderer ran without saved output. Preserve source/license attribution and report the actual delivered files, inspected states and remaining limitations.
