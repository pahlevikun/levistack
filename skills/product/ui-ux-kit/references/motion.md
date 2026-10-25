# Motion

Motion tells people what changed and what to do next. First decide whether to animate at all. Then decide how long and how.

## Contents
- Should this animate?
- Write the purpose
- Easing
- Duration
- Springs
- Following the finger
- Sheets
- Transitions
- Loading and live data
- Forbidden forms
- Reduced motion
- Platform notes
- Verify

## Should this animate?

The first question is how often a person sees it. Frequency decides before taste does.

| How often | Decision |
|---|---|
| 100 or more times a day (palette, shortcut, tab switch) | No animation |
| Tens of times a day (hover, list move, inline toggle) | Remove it or cut it to the minimum |
| Occasional (modal, drawer, toast, page change) | Standard animation |
| Rare or first time (onboarding, first fill, celebration) | Delight is allowed |

Never animate an action started from the keyboard. A high motion dial does not overrule this table. The dial says how motion feels where it exists. The table says where it exists.

## Write the purpose

Every motion answers "why does this move?" in one sentence. Valid answers: spatial consistency (it leaves the way it came), state indication, feedback, explanation of how a feature works, avoiding a jarring cut. "It looked cool" is not an answer. If you cannot write the sentence, delete the motion.

Write a short thesis before you build:
- **Focal moment:** the one sequence that earns authorship, if any.
- **Continuity:** the changes that need explaining.
- **Feedback:** the controls that need acknowledging.
- **Budget:** what may be expensive and how often it runs.

The focal moment must come from this product. A generic fade-and-rise, a hover lift or a scroll reveal is not a thesis.

## Easing

```
Entering or leaving?       ease-out
Moving or morphing on screen?  ease-in-out
Color or hover change?     ease
Constant (progress, scrub)? linear
Otherwise                  ease-out
```

- **Do not use ease-in in UI.** It starts slow, and the delay lands in the moment the user watches hardest. Exits use ease-out too.
- Built-in easings are weak. Use stronger curves: ease-out `cubic-bezier(0.23, 1, 0.32, 1)`, ease-in-out `cubic-bezier(0.77, 0, 0.175, 1)`, sheets `cubic-bezier(0.32, 0.72, 0, 1)`.
- Do not use bounce or elastic by reflex.
- Take the curves from the theme tokens when the theme has them.

## Duration

| Purpose | Duration |
|---|---|
| Press feedback, toggle | 100 to 160 ms |
| Tooltip, small popover | 125 to 200 ms |
| Dropdown, select | 150 to 250 ms |
| Modal, drawer on desktop | 200 to 300 ms |
| Full-height sheet on mobile | 200 to 500 ms |
| Page or route change | 250 to 350 ms |
| Authored entrance (marketing, onboarding) | longer, never gates content |

UI motion stays at or under 300 ms. Exits run faster than entrances (about 70 percent). Long feedback feels like latency. A faster spinner makes the same wait feel shorter. See `data/motion-bands.csv` for the full table with platforms.

Use the theme's duration tokens: fast, base, slow. Platform scales: desktop about 0.8 times, TV about 1.35 times, car about 0.6 times.

## Springs

Springs have no fixed duration. They settle. Use them for drag with momentum, gestures the user may reverse mid-flight, and anything that should feel physical.

- Default: critically damped, no bounce.
- Add bounce (0.1 to 0.3) only after a flick or drag release that carried momentum.
- A spring keeps its velocity when interrupted. A keyframe animation restarts. That is the real reason to use one.
- Do not tie a value straight to pointer position for a functional readout. For decoration, run it through a spring.

## Following the finger

When something can be dragged, handle the uncertainty of the input. The order matters.

1. **Track one to one.** While the finger is down, the element moves exactly as far as the finger. No multiplier, no easing. Remove any transition on the property while tracking, or every frame queues behind the easing.
2. **Damp past the edge.** Beyond a boundary the element still moves, but less. A hard stop reads as a bug. For pull to refresh, use an exponential damp so it feels like rubber and never leaves the screen.
3. **Measure speed over a window of about 100 ms.** Instant speed is noise (events a millisecond apart). Whole-gesture average hides the flick. Use the last 100 ms.
4. **Commit on distance or speed.** Close if the drag passed about one third of the travel, or the release speed is high (about 0.55 px per ms in a typical window). Distance alone ignores a flick. Speed alone locks out slow, deliberate users. Below the threshold, animate back to rest and never park between states.
5. **Lock the axis before claiming the gesture.** Claim it only after it proves horizontal or vertical (more than about 8 px and a clear lead). Claim it earlier and the page stops scrolling inside your component.
6. **Recover dropped frames.** Read coalesced pointer events when the platform has them.
7. **Handle cancel.** A pointer cancel must reset state. Without it, a swipe interrupted by the system leaves a stuck element.

A control that only toggles a class on tap is finished with a press scale. Anything the user can drag needs the list above.

Tap versus drag: about 8 px of movement starts a drag. A long press adds a timer of about 260 ms that any movement cancels.

## Sheets

A sheet is five decisions:

- **Origin.** It comes from where the finger came from.
- **Layer.** The page behind retreats a little. It does not only dim.
- **Controller.** Can it be dragged back? If it can be dragged open, it can be dragged closed.
- **Detents.** Snap to the nearest rest position. Never stop between.
- **Destination.** Including how it ends: dismiss reverses the entrance.

## Transitions

- A card that becomes a page uses a shared element or a FLIP transform. Measure the first and last frames, then animate the difference with a transform. A frame of white in the middle is the counter-example.
- Back must be draggable where the platform expects it.
- Keep a direction cue so people know where they are.
- Do not re-implement native navigation transitions. They are free and expected.
- Custom transitions that fight the navigation model disorient.

## Loading and live data

- Show a skeleton for a known layout and a spinner for a short unknown wait. Use real progress for a long wait. Never loop forever without a way out.
- Animate only the digits that changed. Use tabular figures so numbers do not shake.
- Success feedback arrives when the result is known. Never make business state, focus restoration or cleanup depend on an animation-complete callback.

## Forbidden forms

- Animating layout properties (width, height, top, left, margin) when a transform can do it. Use transform and opacity. Treat filter and clip-path as conditional: fine on a small area, a measured cost on a full-screen blur.
- Scroll position copied into state every frame. Keep continuous input (pointer, scroll, drag) in motion values or shared values, not in component state.
- A heavy scroll handler. A cheap passive read is fine. The work inside is what fails.
- Entrance animation in recycled list cells that replays mid-scroll. Stagger only the first few rows and guard by index.
- Looping decoration near text, in reading views and in a car.
- Content that stays hidden if the script fails. The default state must be visible.

## Reduced motion

Reduced motion is a contract that every layer must keep, because it is a signal, not a mechanism:

- **CSS:** gate movement behind the reduced-motion media query. A blanket rule that zeroes durations is better than nothing but misses the layers below.
- **SVG animation (SMIL):** does not read CSS durations. Pause it with its own call.
- **Script:** anything that writes opacity and transform per frame must read the preference itself and show the final state. Zeroed durations only make the hidden state arrive faster.
- **Canvas and WebGL:** degrade to a still.
- **Loops:** write perpetual loops so the first and last frames match.

What may stay: an opacity or color change that carries a state change, at the short duration. Remove movement, not meaning. Reduced motion does not mean slower. Mobile is not reduced motion, and reduced motion is not mobile. They are different signals.

## Platform notes

| Platform | Notes |
|---|---|
| iOS | System push, sheet rise and reverse dismiss. Springs for gestures. Crossfade for Reduce Motion |
| Android | Container transform, shared axis, fade through. Honor the Remove animations setting |
| React Native | Reanimated on the UI thread. Never `useNativeDriver: false` on transform or opacity. Press feedback first, then state transitions, scroll-linked chrome, then gestures |
| Flutter | Implicit for one property, explicit for sequences, physics for momentum, hero for route sharing. Dispose controllers |
| Web | CSS first. View Transitions for shared state change. Respect the media query |
| Desktop | Quicker. Hover and keyboard feedback matter more than flourishes |
| TV | Slower and larger travel. Focus move shows a ring and a scale together |
| Car | Minimal. Only motion that carries meaning |

## Verify

- Every motion has a written purpose and a duration token.
- Frequent actions are not animated.
- Interruption, rapid repeat and cancel all work.
- Reduced motion keeps meaning and removes movement.
- It is smooth on the slowest target device. A screenshot cannot prove timing. Check actual playback.
- Removing the animation would lose meaning, not just decoration.
