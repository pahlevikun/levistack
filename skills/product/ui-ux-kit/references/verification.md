# Verify the interface

A screen is not done when the code compiles. It is done when you have looked at it on the right surface and you can say what you checked.

## Contents
- Evidence by platform
- The render loop
- Ask precise questions
- Native screens
- Accessibility checks
- Write the acceptance rows
- Report honestly

## Evidence by platform

| Platform | Where the evidence comes from |
|---|---|
| iOS | The Simulator for breadth. A real device for gestures, haptics, refresh rate and speed |
| Android | An emulator or a device. A real device for gestures, haptics, refresh rate and speed |
| React Native, Flutter | The Simulator or emulator of each target. Not a browser |
| Web | A real browser at several widths, with keyboard only, zoom and reduced motion |
| Desktop | The built app on each OS, with keyboard only and a resized window |
| TV | The emulator for layout. A real panel and remote for focus, distance and color |
| Car | The host's simulator or desktop head unit for templates. A real car or an OEM rig for glances, glare and night |

A web mockup is a demonstration and not native proof. If you show one, list for each control the native control it stands in for and mark the native behavior as unverified. A browser screenshot proves nothing about Dynamic Type, a screen reader or system gestures.

## The render loop

1. Build and run the real screen. Wait for fonts and images.
2. Capture at representative sizes: the smallest phone, a large phone, a tablet or wide window, and the size where the user saw the problem.
3. Capture both modes, the largest text size, and reduced motion.
4. Compare with the intended direction or a supplied reference. Hierarchy and proportion first, then type, spacing, color and assets.
5. Fix every material problem in one batch.
6. Render again. Look again. Stop when the acceptance rows pass or when a bounded pass cannot fix something (then report it).

A visible failure in the render outranks the code. If a problem shows in a screenshot, it is real.

## Ask precise questions

Do not ask "does this look good?" Ask:

- Where does the eye land first, second and third? Is that the order that matters?
- Is anything clipped, overlapping or cut at an edge?
- Is the primary action the clearest thing on screen, and is there only one?
- Is the focus state obvious? Can you tell which item is selected?
- Does the finding sit next to its action?
- Are two things the same color that mean different things?
- In grayscale, is the order still readable?

For a cold-drop check on mobile, drop onto a screen without context and answer: what app is this, what screen am I on, where am I in the structure, how do I get back? A screen where the user cannot answer is a high-impact problem whatever the polish.

## Native screens

- Capture from the Simulator or emulator, not from a browser.
- Flip the appearance (dark) and the text size from the command line or the settings, then capture again. Restore the settings after.
- Say which evidence came from a simulator and which from hardware.
- Audit from the source on five dimensions: accessibility (labels, order, scaling, targets, reduced motion, contrast), performance (startup, virtualized lists, jank, wasted rendering, image handling), appearance and theming (hard-coded colors, dark, dynamic color, materials), platform conformance (gestures, insets, navigation, controls, icons), and adaptivity (tablet, orientation, keyboard, multitasking, foldables).
- Rate platform conformance first: does it read as native or as a ported website? List the violations.

## Accessibility checks

- Run the platform's automated checker if there is one (accessibility lint, Xcode inspector, Accessibility Scanner, axe).
- Then do the manual pass: keyboard or remote only, screen reader on the main task, largest text, reduced motion, high contrast.
- Check every contrast pair with the gate in the color skill. Do not estimate.
- Test tap target size by measuring, not by looking.

## Write the acceptance rows

Write one row per observable behavior into `ux-acceptance.csv` (template in `templates/`). Use the same columns as the journey tracker in `product-polish-workflow`:

`Feature ID, Surface, Feature / capability, User story, Expected behavior based on code, Code anchors, Initial test approach, Initial test command or route, Status, Test result, Errors, Fix status, Retest result, Notes`

- Give each row a stable ID such as `UX001`.
- Every row needs at least one code anchor.
- Write the expected behavior from the current code and the rule it proves (cite a rule id such as `TOUCH-02`).
- Use the status values: Not Tested, Passed, Failed - Product, Failed - UX, Failed - Logistical, Failed - Test Infra, Blocked - Env, Fixed, Passed after fix.
- Validate the file: `node scripts/check-acceptance.mjs ux-acceptance.csv`.

Do not invent a separate source of truth. There is one tracker per product.

## Report honestly

State what changed, what you tested and on what surface, and what remains. List each check you could not run as Not verified. Never mark a row Passed from old output. Fresh evidence from this session is required.
