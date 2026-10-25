# Step 3: Critique against the system

Now that the system exists, judge the real screens against it. A critique with no system is taste. A critique with a system is a check, and every fix is concrete: "this padding should be `space-md`, this color should be `text-muted`."

The short guide in `specialities/ui-critique/GUIDE.md` is the core method. For the detail of one screen (states, motion, gestures, forms, platform behavior) the checks come from `ui-ux-kit`, and for color pairs they come from `color-kit`. Cite their rule ids in findings. This file adds the system-aware checklist, the platform lens and the report shape.

## Contents
- What to critique
- The order of checks
- Platform lens
- Severity
- Fix format
- Report shape
- Do not

## What to critique

- Screens or components the user shows (screenshots, a URL, code).
- The product's current UI, if it exists, compared to the new system. This shows the gap between where it is and where the system says it should be.
- The new system's own preview, if there is nothing else yet.

For code, read the real components. For a URL or screenshots, say what you could and could not see.

## The order of checks

Go top-down. Fix hierarchy before polish.

1. **Purpose and hierarchy.** What is the one thing this screen is for? Can you tell in 3 seconds? Is the primary action the most visible thing, and only one per screen?
2. **Layout and spacing.** Do the gaps come from the scale (`space-*`)? Are related things close and unrelated things apart? Is alignment consistent? Is there dead space or crowding?
3. **Typography.** Are sizes from the type scale? Is there a clear level for title, body and label? Line length 60 to 75 characters? Line height right? Too many weights or families?
4. **Color.** Does color follow the roles? Is the primary used once? Is the 60-30-10 split roughly right? Does any text or edge fail contrast? Is color the only signal anywhere?
5. **Shape and depth.** Are radii and shadows from the kit? Are cards, inputs and buttons consistent with each other? Is the signature move present and used the same way?
6. **Components and states.** Do all interactive parts have default, hover or focus, pressed, disabled, loading and error states? Are the same things built the same way?
7. **Content.** Are labels short and clear? Are empty, long and error texts handled?
8. **Motion.** Does motion use the tokens, explain change, and stop for reduced motion?
9. **Accessibility.** Contrast, target size, focus visible, labels and names, order, zoom, screen reader names. See the platform lens for the numbers.
10. **Consistency with the system.** Count hard-coded values. List every place that bypasses a token.

## Platform lens

Apply the profile for each platform the screen runs on (see `platforms.md`).

| Platform | Look for |
|---|---|
| Mobile | Targets under 44 pt or 48 dp, actions out of thumb reach, text that breaks at 200%, clashes with the notch or home indicator, hover-only UI |
| Desktop | No keyboard path, no focus ring, controls too large for the density, no shortcuts, missing resize behavior |
| Web | Breaks at 320 px or 400% zoom, fixed pixel widths, low contrast links, no reduced-motion handling, focus lost on route change |
| TV | Anything not reachable by D-pad, weak focus state, text under 28 px at 1080p, content outside the safe area, pure-white blocks, thin fonts |
| Car | Tasks that need more than a few glances, targets under 76 px, long lists, typing, looping animation, a weak night mode |

## Severity

| Level | Meaning |
|---|---|
| **Blocker** | The user cannot finish the task, or it fails accessibility or safety (car) |
| **Major** | The task is harder or slower, or the system is clearly broken |
| **Minor** | Polish and consistency |
| **Note** | An idea or a question |

## Fix format

For each finding, name the element and the exact change:

```
[Major] Checkout, "Pay now" button
Problem: 36 px tall, text #7A7A7A on #F2F2F2 (3.1:1). It is the main action but looks disabled.
Fix:     use button-primary: height 48 (control-height), background primary, text on-primary (7.2:1).
Why:     hierarchy and contrast. The system defines this button.
```

Order by impact, not by where it appears on the screen.

## Report shape

1. A short verdict: what works, and the three changes that matter most.
2. The findings list, grouped by severity, each in the fix format.
3. A count: how many hard-coded values, how many contrast failures, how many missing states.
4. What you could not check, and what you assumed.
5. What to change in the **system** itself (a missing token, a missing component, a wrong default), as distinct from what to change on the screens.

## Do not

- Critique before the system exists. Step 2 comes first.
- Say "looks off" without a number or a token.
- Rewrite the product. Stay with fixes that map to the system.
- Hide a finding because the fix is large. Mark it and move on.
