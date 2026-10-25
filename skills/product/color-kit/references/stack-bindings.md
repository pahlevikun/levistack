# Bind the theme to a stack

Bind only the stack you were asked for. A binding maps roles, not palette steps. A theme change then repoints roles and no component changes.

## Contents
- The command
- Plain CSS and Tailwind
- SwiftUI and AppKit
- Jetpack Compose
- Flutter
- React Native
- Vue and Nuxt
- Desktop shells
- Car and TV
- Rules that hold for every stack

## The command

```bash
python3 scripts/theme/theme.py bind --tokens design/tokens.json --stack <flutter|compose|swiftui|react-native|vue> --out <folder>
```

The script lives in `design-system-kit`. Open a shell in its `specialities/design-system/` folder and pass absolute paths for `--tokens` and `--out`. It reads the roles in `tokens.json` for light and dark and writes one generated source file. Never edit it by hand. Rebuild instead. Plain CSS and Tailwind come from `theme.py build` as `theme.css` and `tailwind-theme.css`.

If the kit is not installed, write the same mapping by hand from `data/roles.csv`.

## Plain CSS and Tailwind

- Write the roles as CSS variables on `:root`. Put the alternate mode under one switching mechanism (see the modes guide).
- Keep `:root` and the dark block at the top level, not inside a layer that gets reordered.
- **Tailwind v4:** map variables with `@theme inline`, so utilities read the variable at render time. Do not nest `@theme` inside a mode block, because v4 does not support it. Do not wrap a variable twice (for example `hsl(var(--x))` when the variable already holds a full color).
- Do not add `dark:` variants per color. A role variable already changes with the mode. Per-color `dark:` classes are a sign that roles are missing.
- Delete a stale v3 color config when you move to `@theme`, or utilities come from two places.
- Chart colors get their own variables (`--chart-1`) mapped the same way.
- Test light, dark, system and the toggle transition.

## SwiftUI and AppKit

- Generated `AppColors.swift` gives `AppColor.primary` and the rest, each a dynamic color that follows the system appearance. It works on UIKit and on AppKit.
- You may also keep the colors in an asset catalog with light, dark and high contrast slots. Then the system picks the variant for Increased Contrast too. Prefer this when the product must honor Increased Contrast.
- Set one tint for interactive elements: `.tint(AppColor.primary)`. Decoration is not the tint's job.
- Use system semantic colors where the platform expects them (label, separator, system background). Use the brand roles for brand moments.
- Use system materials for blur behind bars and sheets. Do not hand-roll glass.
- Do not put hex in a view. Test Dark Mode, Increased Contrast and Dynamic Type together.
- AppKit keeps native control colors. Do not transplant iPhone rules.

## Jetpack Compose

- Generated `AppColors.kt` gives `LightColors` and `DarkColors` as Material 3 color schemes, plus `ExtraColors` for roles a scheme has no slot for (success, warning, info, link, focus ring).
- Wrap content with `MaterialTheme(colorScheme = ...)` and provide `LocalExtraColors`.
- On Android 12 and later you may start from the wallpaper-derived scheme. Keep the generated scheme as the static fallback and for the brand's own screens.
- Read colors from `MaterialTheme.colorScheme` or `LocalExtraColors.current`. No hex in a composable.
- Elevation in dark comes from surface tones, not shadows.

## Flutter

- Generated `app_theme.dart` gives `lightTheme()` and `darkTheme()` built from an explicit `ColorScheme`, plus an `AppColors` theme extension.
- `ColorScheme.fromSeed` is good for exploring. For a fixed brand use the explicit scheme so the colors you proved are the colors you ship.
- All colors come from `Theme.of(context).colorScheme` or `context.appColors`. No hex in a widget. No legacy accent properties.
- Configure component themes with their `...ThemeData` classes.
- Desktop and web targets add idioms: visible scrollbars on desktop, selectable text for read-only content, confirm button placement per OS. Keep them in the theme or a platform layer, not in screens.
- Use `MediaQuery.sizeOf` or `LayoutBuilder` for layout. Never lock orientation.

## React Native

- Generated `colors.ts` gives `lightColors`, `darkColors` and `useColors()`, which follows the system appearance.
- Keep platform forks in tokens and components, not scattered in screens. Pair every iOS shadow with an Android `elevation`, or the shadow is invisible on Android.
- If you use a component library with a theme file (for example HeroUI Native on Uniwind), put the role values in its single theme file. Its color format may differ from the web version of the same library. Check its docs. Use `onPress`, not `onClick`.
- Use semantic variants (primary, secondary, danger) in components, not raw colors.

## Vue and Nuxt

- Use the CSS variables from `theme.css`. The generated `useTheme.ts` only switches the mode through one attribute.
- In Nuxt a color-mode module is fine. Keep only one switching mechanism.
- Do not set colors in scoped styles with literals. Use the variables.

## Desktop shells

- Electron and Tauri: plain CSS variables plus `prefers-color-scheme`. Honor the OS accent color only if the brand allows it.
- macOS native: named colors in an asset catalog. Windows: theme resources and system accent. Linux: follow the toolkit.
- Keep keyboard focus rings at 2 px with a role color.

## Car and TV

- Car (Android Auto, CarPlay, in-car): the host owns most of the theme. Theme what it allows (accent, icons, artwork). Provide day and night values. See the modes guide.
- TV: the build gives you the same two sets. Make the app start in the dark set on purpose (tvOS: `.preferredColorScheme(.dark)` on the root view. Compose for TV: pass the dark scheme to `MaterialTheme`. Web on TV: set the dark attribute at start). Keep focus color and ring as roles with a 3:1 check. `bind` has no car or TV stack, use the stack the app is written in.

## Rules that hold for every stack

- Zero raw hex outside the palette and theme files.
- Roles in, components out. Themes override roles, not primitives.
- Both modes ship together and are tested together.
- One switching mechanism.
- Provide the hex fallback first and the vivid wide-gamut value after it, where wide gamut is used.
- Regenerate bindings from `tokens.json`. Do not hand-edit generated files.
