# Mixing and gradients

Use this when you need a color between two colors: a tint, a hover state, a disabled state, a surface wash or a gradient.

```bash
python3 scripts/theme/theme.py mix "#1F6FEB" "#FFFFFF" --ratio 0.15 --on "#FFFFFF"
python3 scripts/theme/theme.py mix "#1F6FEB" "#FFFFFF" --steps 7 --space oklab
```

The first form shows the same blend in four spaces, with the contrast on the ground you name. The second prints a ramp.

## Which space

| Space | Use | Watch for |
|---|---|---|
| `oklab` | Tints, shades, hover, pressed, calm gradients | The default choice |
| `oklch` | A gradient that should sweep through hues | The path can pass through a color you did not choose |
| `linear` | Light that adds up (glows, blurs) | Midpoints look bright and thin |
| `srgb` | Matching what a browser does by default | Dark, muddy midpoints |

## Decisions as rules

State the rule, not a hex. The rule survives a rebuild and a theme change.

- Hover: mix the fill 8 to 12 percent toward the text color of its ground.
- Pressed: mix 14 to 18 percent.
- Disabled: mix the fill 60 percent toward the ground, and do not let it pass for a normal control.
- Subtle fill: mix the brand 8 to 14 percent into the ground.

Then measure each result with `theme.py contrast`. A mix that fails is moved by lightness, not by hue.

## Gradients

- Use one purpose per gradient: depth, focus, or a brand moment. A gradient with no purpose is decoration.
- Choose the space by intent and preview it.
- Measure text on the lightest and the darkest stop, not on the middle.
- Avoid the default blue-to-purple. It reads as a template.
- Keep a flat fallback color for each gradient.

## Screens add light, paint takes it away

On a screen, red light plus green light makes yellow. With paint, blue plus yellow makes green. Do not carry paint rules into RGB. If a request says "mix like paint", pick the colors by eye and measure the result, because no screen blend gives a paint result.
