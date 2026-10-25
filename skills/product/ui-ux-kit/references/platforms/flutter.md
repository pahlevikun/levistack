# Flutter

One codebase for mobile, desktop and web. Decide the posture, read the existing theme first and drive layout from constraints.

## Theme first

Check for an existing `ThemeData`, color class, text style class or `ThemeExtension` before you create styles. Order of use: the project theme, then `Theme.of(context)`, then a hard-coded value only as a last resort.

- Define the app theme once with `ThemeData(useMaterial3: true, colorScheme: ...)` for light and dark.
- `ColorScheme.fromSeed` is good for exploring. For a fixed brand, build the scheme explicitly so the proven colors are the shipped colors. The generated `app_theme.dart` from the color binding does this and adds an `AppColors` extension for extra roles.
- All colors come from the scheme or the extension. No hex in a widget. No legacy accent properties.
- Configure component themes with their `...ThemeData` classes (for example `CardThemeData`, `AppBarTheme` uses `backgroundColor`).
- Text comes from `Theme.of(context).textTheme`. Spacing comes from a 4 dp scale kept in one place.

## Layout

- Read constraints. Use `LayoutBuilder` and `MediaQuery.sizeOf`. Never check device type or switch layouts on orientation near the top of the tree.
- Use `Expanded` and `Flexible` inside `Row` and `Column`. Handle unbounded constraints on purpose. Keep nesting shallow.
- Constrain maximum widths for readability on large screens.
- Never lock orientation.
- Use `PageStorageKey` on scrollables so scroll state survives a rotation.
- `ListView.builder` for long lists and keys for stateful items.

## Adaptive and platform behavior

- Phone to tablet: restructure with width breakpoints (navigation bar to rail, list to list and detail).
- Desktop and web: visible scrollbars, selectable text for read-only content, hover and focus states, keyboard shortcuts, focus traversal. Windows places the confirm button on the left, macOS, Linux, Android and iOS on the right.
- Use platform checks for idioms, not for layout.

## Navigation

Use a router such as GoRouter and `PopScope` for back handling. Pass typed arguments. Use named routes.

## Motion

Choose by need:

| Need | Use |
|---|---|
| One property on one widget | An implicit animation |
| A sequence or fine control | An explicit animation with a controller and a tween |
| A route change | A page route transition |
| Momentum and springs | A physics-based animation |
| A shared element between routes | Hero, with a unique tag per route pair |
| Several staggered movements | A staggered animation |

Dispose every controller. Treat tweens and curves as immutable. Use `AnimatedBuilder` or an animated widget, not `setState` in a listener, for complex trees.

## Accessibility

Add `Semantics` to custom interactive widgets and to meaningful images. Support large fonts. Keep tap targets at the platform minimum. On web, enable the accessibility tree. Test with a screen reader and with widget tests.

## Verify

Run on each target. Check large text, dark mode and a small window. Capture from the real target, not a screenshot of a different one.
