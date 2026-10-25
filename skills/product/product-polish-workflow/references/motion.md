# Motion in a shipped product

The craft of motion (the frequency gate, purpose, easing, duration, springs, gestures, reduced motion) is owned by `ui-ux-kit`. Load it and read its motion guide for any new or changed animation. This note covers only what is different when the product already ships.

## Audit what ships

Inspect current motion first, then change only defects or additions that are in scope. For each existing motion record:

- The user purpose and how often it is seen.
- Trigger, property, duration, easing or spring, and final state.
- What happens on interruption, rapid repeat and cancel.
- The Reduced Motion result, in every layer that moves (CSS, SVG animation, script, canvas).
- Whether the product already has motion tokens or a motion library. Use them before adding another system.

Audit actual playback on the matching surface. A screenshot, a source read, a build or a typecheck cannot establish perceived timing. Use saved captures or bounded recordings when helpful. Report observed behavior separately from inferred source behavior. Do not invent a motion score and do not force a branded report.

## Change what is in scope

- Remove motion that delays a frequent task, hides content or adds constant idle movement.
- Never make business state, content visibility, focus restoration or cleanup depend only on an animation callback.
- Keep the incumbent platform's transitions. Do not re-implement native navigation motion.
- Content must be available when animation is disabled or fails to start.

## Evidence limits

State which checks came from a device, a simulator or the source. Check input during animation, rapid repetition, cancellation, resize, and switching appearance or motion preference.
