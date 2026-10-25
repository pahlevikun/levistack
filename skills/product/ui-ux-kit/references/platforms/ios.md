# iOS and iPadOS

For native iOS and iPadOS in SwiftUI or UIKit, and for React Native or Flutter apps shipped to Apple devices. The platform guide governs structure, navigation and interaction in every posture. Brand shows in the layer the platform leaves open: tint, type, motion and content.

## The slop test

Would a fluent iPhone user trust this app, or pause at an off-spec control? The tell is "ported from a website": a reinvented navigation bar, a custom back gesture, a web-shaped button, a hover affordance. Use system components. Depart only for a reason the user would see.

## Structure

- **Safe area.** Lay out inside the safe-area insets. Nothing under the notch, Dynamic Island, home indicator or rounded corners.
- **Navigation.** Tab bar for three to five sections (sections, never actions). Two destinations need no tab bar. Navigation stack for hierarchy. Sheet for a self-contained task. No custom global nav and no mixed metaphors.
- **Edge swipe back stays alive.** Never disable it or cover it.
- **Large titles** on top-level screens that collapse to inline on scroll. Deep screens stay inline.
- **Grouped or inset lists** for settings-shaped content. No bespoke card stacks.
- **Modality is deliberate.** A sheet for a focused dismissible task, a full-screen cover for immersion. Clear Cancel and Done. Honor swipe to dismiss unless data loss needs a guard.

## Targets and type

- 44 by 44 pt minimum for every tappable control, with room between neighbours.
- System text styles from Large Title to Caption so type follows Dynamic Type. No fixed point sizes. Body is 17 pt. The floor is 11 pt.
- San Francisco carries the UI. A brand face may appear in display moments only.

## Color and materials

- Semantic system colors adapt to Dark Mode and Increased Contrast. Raw hex breaks there.
- Dark Mode is a first-class appearance. Design and test both.
- One tint color drives interactive elements. Decoration is not its job.
- System materials for blur behind bars and sheets. No hand-rolled glass.

## Components

- Native controls: switch, segmented control, stepper, system pickers, action sheets, alerts, context menus, swipe actions. Reinventing these is the most common native slop.
- System symbols for icons. Do not mix a web icon set in.
- A destructive confirmation is an action sheet with the destructive option marked.
- Pull to refresh uses the system control.

## Motion

- System transitions: push slides, sheets rise, dismiss reverses the entrance.
- Springs for gestures, critically damped by default.
- Reduce Motion: crossfade instead of parallax and large slides.

## iPad

Restructure with size classes. A tab bar may become a sidebar. Use split views and popovers where the phone used sheets. Multitasking can give a phone-width window on an iPad, so layout follows size classes, never the device model.

## Verify

- Capture from the Simulator with the command line screenshot tool, not from a browser.
- Flip to dark and to a large Dynamic Type size, then capture again.
- Simulators give breadth. Gestures, haptics and speed need a device. Say which one produced each check.

## Stack notes

SwiftUI: small struct views, `@State` and `@Observable`, `NavigationStack`, `.tint`. See `data/stack-notes.csv`. UIKit: system controls and trait collections. For React Native and Flutter on iOS, keep the platform rules above and use the platform guides in this folder for the stack.
