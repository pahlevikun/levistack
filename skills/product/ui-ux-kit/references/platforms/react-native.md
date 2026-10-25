# React Native and Expo

One codebase for iOS and Android. Decide the posture first: unified-brand, iOS-first, Android-first or per-platform-native. Then follow the platform guide for each target.

## Read the stack first

Read `package.json`, `app.json` and the theme config before any code. Detect the Expo SDK, the router (Expo Router or React Navigation), the styling system (StyleSheet, a utility system, Tamagui, Paper), the icon family and any existing tokens. The detected stack wins over every default here. First-generation code that imports the wrong styling system is a total loss, and thirty seconds of sniffing prevents it.

## Navigation

- Design the route tree before screens. Tabs, push, modal, sheet and full-screen groups follow the container tree in the screen anatomy guide.
- Sign-in and onboarding are route groups swapped on session, not conditional renders inside screens.
- Every detail screen is a route with params, so it is deep-linkable.
- Do not override the Android back button except to confirm a discard.
- Keep native navigation chrome until the brand needs to own it.

## Layout

- Safe areas: the navigator header owns the top inset. Otherwise use the safe-area hook. Bottom of a scroll: inset plus spacing. No `paddingTop: 50` style numbers.
- The header owns the title. Do not repeat it under the header.
- Content is top-aligned. Center only empty states, sign-in and interstitials.
- Keyboard: the submit control stays visible with the keyboard open. Use the right keyboard type and autofill on every input.
- Lists: `FlatList` or a faster list with stable keys and measured rows. Never `ScrollView` with `map` for unbounded data. Add pull to refresh to every feed.

## Type, color and surfaces

- System fonts are a respectable default on mobile. A custom face has to earn its place: one or two families, loaded before the splash hides, proven under large text. Bound custom chrome text with a max font multiplier.
- One accent, one gray family, both modes from the start through the system appearance hook. Pure black is allowed as an OLED choice when stated.
- Do not default to the indigo gradient look.
- Cards are not the only grouping tool. Use space, hairlines and grouped lists.
- Define two or three elevation levels once, each with iOS shadow props and Android elevation together. A shadow color without an elevation is invisible on Android.
- Blur only over media and overlays.

## Interaction

- Use `Pressable` with press feedback and `hitSlop` for small targets.
- Press feedback: ripple on Android, opacity or a scale of 0.97 on iOS, or one branded press style used on both.
- `Alert` is for destructive confirmations only. Success is a state change. Errors are inline.
- Haptics: selection ticks and outcomes, never plain taps.
- Ask permissions at the moment of intent.
- Pickers, switches and share sheets are system components by default.

## Motion and speed

- Reanimated on the UI thread. Never `useNativeDriver: false` on transform or opacity. Scroll position lives in a shared value, not in state.
- Order of work: native navigation transitions (free), press feedback, layout animations, scroll-linked chrome, gestures.
- Do not replay entering animation in recycled cells. Stagger only the first few rows.
- Honor reduced motion. Gestures still work. Decoration collapses.
- Do not try shared-element transitions or a custom pull to refresh by default. Approximate and say so, or use the system control.
- Use an optimized image component with sizes and a recycling key. Hold the splash until fonts and first data are ready.

## Web target (react-native-web)

Hover exists only as an enhancement. Add a max content width of about 640 to 760 so a phone layout is not stretched to 1440.

## Verify

Run on a simulator and an emulator, and on a device for gestures. Test large text and dark. Say which evidence came from where.
