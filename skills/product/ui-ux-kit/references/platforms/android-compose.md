# Android, Jetpack Compose and Views

For native Android in Jetpack Compose or Views, and for React Native or Flutter apps shipped to Android. Material 3 governs structure, navigation and interaction in every posture. Brand shows through Material theming: color roles, type scale, shape and motion.

## The slop test

Would a fluent Android user trust this app, or trip on off-spec parts? The usual tell is an iOS app wearing Android skin: a bottom-only nav copied from the iPhone, a back arrow that ignores system back, Cupertino switches and dialogs.

## Structure

- **Navigation fits the width.** A navigation bar (three to five destinations) on compact widths. A navigation rail or drawer on expanded widths. Never ship a phone bottom bar untouched on a tablet.
- **System back always works.** Honor the predictive back gesture. Never trap the user.
- **Edge to edge with window insets.** Apply status bar, navigation bar, cutout and keyboard insets so content never hides.
- **Top app bar** for screen context. Pair it with one FAB when a screen has a single primary action. Never stack FABs.
- Drive layout from window size classes. Foldables change posture, so test folded, unfolded and tabletop.

## Targets and type

- 48 by 48 dp minimum with at least 8 dp between targets.
- The Material type scale (Display, Headline, Title, Body, Label) by role. Never hand-pick sizes per screen. Use sp so type follows the font scale. Roboto is the system face. Theme a brand face through the type scale.

## Color and theming

- Material color roles (primary, on-primary, surface, surface variant, secondary container, outline, error). Role tokens resolve light, dark and contrast variants. Raw hex breaks there.
- Dynamic Color from the wallpaper on Android 12 and later where it fits, with a static fallback.
- Dark theme is a first-class scheme. Never a quick invert.
- Tonal elevation: depth from surface tones, not arbitrary shadows.

## Components and motion

- Material components: filled, tonal, outlined and text buttons, FAB, switches, chips, snackbars, bottom sheets, dialogs, navigation bar, rail and drawer. Do not port iOS controls.
- Snackbars for transient feedback. Dialogs only for decisions that must interrupt.
- Material motion patterns: container transform, shared axis, fade through. Honor the Remove animations setting with a crossfade or an instant cut.

## Compose rules

- Keep composables small and pure. State flows down and events flow up. Hoist state. Expose immutable UI state from the view model.
- `LazyColumn` with stable keys for lists. No nested scroll containers.
- Use `Modifier` before extra layouts. `Row` and `Column` for linear layout. `Box` only for overlap. Avoid `fillMaxSize` by default and deep nesting.
- Use `MaterialTheme` roles and typography. No hard-coded text styles or colors.
- Add semantics and content descriptions. Use `testTag` for tests.
- Use the Compose animation APIs. Keep animation logic out of the view model.
- Wrap content with the generated `LightColors` and `DarkColors` and `LocalExtraColors` from the color binding.

## Verify

- Capture from an emulator or a device with `adb`, not from a browser. Capture each device class.
- Flip the night mode and the font scale (for example 1.3) and capture again. Restore the settings after.
- Emulators give breadth. Gestures, refresh rates and speed need hardware.
