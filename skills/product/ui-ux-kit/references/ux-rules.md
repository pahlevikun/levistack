# UX rules

The rules that decide whether a screen is easy to use. The full table is `data/ux-rules.csv` (108 rows with id, platform, check, severity and the evidence that proves it). This guide explains the groups and the order to apply them.

## Contents
- Priority order
- Accessibility
- Touch and gestures
- Navigation
- Forms
- Feedback and states
- Permissions and haptics
- Copy
- Layout and type
- Performance
- AI surfaces
- Pre-delivery pass

## Priority order

Apply in this order. A failure higher up outweighs polish lower down.

1. The main task works.
2. States are decided (loading, empty, error, offline, stale).
3. The screen can be used at all: accessibility, targets, focus, text scaling.
4. The system holds: tokens, roles, one component per job.
5. Platform fit: navigation, gestures, safe areas, adaptive layout.
6. Polish: hierarchy, spacing, type.
7. Motion and delight, never at the cost of 1 to 6.
8. Consistency across screens.

## Accessibility

- Every control has a name and a role. Icon-only buttons need a label. Decorative icons beside visible text are hidden from the accessibility tree.
- Text scales to 200 percent with no clipping. Bound custom chrome text (a multiplier of about 1.3 to 1.5) and leave body text unbounded.
- Color is never the only signal.
- Focus is always visible and follows reading order. Overlays and sticky bars never hide the focused control. Modal dialogs trap focus and return it on close.
- Reduced motion is honored.
- Every gesture has an alternative: swipe to delete has a tap to reveal, pinch has plus and minus, drag to reorder has move up and down.
- Dynamic changes are announced (loading, error, success, content updates).
- Sign-in allows password managers and paste. Do not make the user solve a puzzle.
- Time limits can be extended. Auto-advancing content can be paused.
- Never lock orientation.

## Touch and gestures

- Targets: 44 by 44 pt on iOS, 48 by 48 dp on Android, 24 px minimum and about 44 for touch on the web, 64 px on TV, 76 dp in a car. Keep 8 px between targets.
- Small icons get an expanded hit area.
- One primary gesture per region. Do not nest tap and drag. Do not fight system gestures (edge swipe back, predictive back, home indicator).
- Press feedback within 100 ms.
- Frequent actions inside the content live in the lower half of a phone screen. Rare or destructive ones can sit at the top. Where the platform puts a primary action in a bar (the iOS Done button, the Android top app bar action), follow the platform.
- Hover is never required. Hover cards wait about 150 ms so they do not flicker.

## Navigation

See the container tree in the screen anatomy guide. Platform rules:

- iOS: tab bar for sections, stack for hierarchy, sheet for a bounded task, large titles on top-level screens, edge swipe back alive.
- Android: navigation bar on compact width and rail or drawer on wide windows, system and predictive back always working, one FAB for one primary action.
- Web and desktop: the URL is the state. Keyboard path for every command. Show shortcuts.
- Preserve drafts and selection across back, dismissal, failure and refresh.
- An empty state teaches one next step. A failure is not an empty result.

## Forms

- A visible label above each field. A placeholder is not a label.
- The right keyboard type and autofill hint on every input.
- Validate after blur or a short pause, not on every key. Show the error next to the field with cause and fix. Move focus to the first error. For several errors, add a linked summary.
- The submit control stays visible with the keyboard open. Scroll to the last field.
- Reserve space for helper and error text.
- Do not ask for something already given in the same flow.
- Show password visibility. Keep a wrong form's input.
- A control that needs a sentence of instructions should be redesigned. A limit that remains (password rules, file type and size) stays visible beside the field and is linked with an accessible description.

## Feedback and states

- Loading: a skeleton of the final layout for content, a spinner only for button-level work. Never a full-screen spinner over the tab bar.
- Empty: composed, with the action that fills it.
- Error: inside the block, with retry. Use an alert dialog only for decisions that must interrupt.
- Success: a state change and optionally a light haptic. Silent when the result is visible.
- A destructive action names its outcome and has a visible Cancel. It is quieter before it is armed. Prevent duplicate submission. Reset confirmation with its selected record.
- Stale data carries a freshness stamp.

## Checkout and payments

- Offer the platform's native pay sheet (Apple Pay, Google Pay) before a card form.
- Card, address and one-time code fields carry the right autofill hints and keyboard types.
- Show the total, what it includes and what happens next before the final action.
- Block a second submit while paying, and make the request safe to repeat (an idempotency key), so a double tap never charges twice.
- A failed payment keeps the cart and the typed fields, says the cause and offers a retry or another method.
- Never ask again for something already given in the flow.
- None of this runs in a car. See the car guide.

## Permissions and haptics

Never ask for a system permission on cold start or in a mount effect. Ask at the moment of intent, with context, then request.

| Permission | Ask when |
|---|---|
| Notifications | After the first value moment (first task made, first order placed) |
| Location | When the user taps a location feature |
| Camera or photos | When the user starts capture or upload |
| Contacts | When the user opens an invite or share flow |

Haptics: a selection tick for pickers and toggles, a light impact for meaningful confirmation, a notification pattern for async outcomes. Never on plain taps or navigation.

## Copy

- Controls name their action. Errors name the problem and the way out.
- Real, believable content. No lorem, no fake names, no totals that do not add up.
- No filler verbs ("seamless", "supercharge"). No exclamation-heavy onboarding. No greeting header unless personalization is the product.
- Do not use an em dash in visible strings.
- Self-audit every visible string before shipping.
- In a car, labels are three words or fewer.

## Layout and type

- Spacing from the scale (4 or 8 grid). One pair of gutters per screen.
- Safe areas and insets come from the platform API. No magic numbers.
- Scroll content is not hidden behind fixed bars.
- Body text 16 or more on mobile. Smallest text 11. Inputs 16 or more on the web so iOS does not zoom.
- Type scale from tokens, at most five sizes on a screen. Tabular figures for numbers that align or change.
- Reading text 45 to 75 characters per line.
- Group by space, alignment and type hierarchy before borders. Prefer removing an element to restyling it.

## Performance

- Virtualize long lists. Stable keys.
- Animate on the UI thread. Keep continuous input out of state.
- Reserve space for images so layout does not jump. Use proper image sizes and caching.
- First paint shows the right background and fonts.
- Debounce high-frequency events.

## AI surfaces

A product with a model in it needs more than a chat box:

- Show streaming honestly. Let the user stop it.
- Say when output may be wrong, and show sources when you have them.
- Let the user correct and retry. Keep their input after an error.
- Mark generated content as generated.
- Confirm before an agent takes a consequential action, and show what it did.
- The refusal and error states are real states with copy.

## Pre-delivery pass

Use `templates/preflight.md`. Run it on the smallest supported phone, in landscape, at the largest text size, with reduced motion on, in both light and dark, and with the screen reader on the main task. Say which checks came from a device and which from a simulator or the source.
