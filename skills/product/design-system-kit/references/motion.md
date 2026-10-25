# Motion in the design system

Motion craft is owned by the `ui-ux-kit` skill: the frequency gate, easing, duration, springs, gestures, sheets and reduced motion. This guide only records what the system stores and how the builder picks it.

## Required call

At Step 4, load `ui-ux-kit` for every screen or component that moves. Use its motion spec. Record the result here as tokens. Do not invent times or curves in this skill.

## What the system stores

Every profile defines the same tokens, so components never hard-code a time.

| Token | Meaning |
|---|---|
| `--dur-fast` | Small state changes such as hover, press and toggle |
| `--dur-base` | Most transitions such as menus, tabs and fades |
| `--dur-slow` | Large or entering things such as sheets and page changes |
| `--ease-out` | Things that enter or respond |
| `--ease-in-out` | Things that move on screen |
| `--ease-in` | Kept for completeness. The craft guide bans it in UI |
| `--motion-distance` | How far an entrance travels |
| `--press-scale` | The scale of a pressed control |
| `--stagger` | Delay between siblings that enter in a list |

## The six profiles

The mixer picks one. The values are in `data/theme/motion.json`.

| Profile | Durations (ms) | Feel | Fits |
|---|---|---|---|
| still | 90 / 140 / 200 | Almost none. Opacity and color only | Legal, clinical, dense data |
| calm-drift | 160 / 320 / 560 | Slow and soft with no bounce | Wellness, reading, night modes |
| crisp | 100 / 160 / 240 | Short and decisive | Tools, fintech, trust |
| springy | 140 / 260 / 420 | Light overshoot and a squishy press | Consumer, food, kids, social |
| snappy-tech | 80 / 130 / 200 | Tiny and fast | Developer tools, data |
| theatrical | 140 / 480 / 900 | Slow reveals and staggers | Premium, editorial, hero moments only |

## Platform scale

The builder scales durations and travel by platform: desktop about 0.8, web 1.0, mobile 1.0, TV about 1.35, car about 0.6. The reduced-motion block in `theme.css` sets durations to 1 ms and travel to 0.

## Rules for this kit

- The motion data file stays here because the mixer reads it. Craft rules live in `ui-ux-kit`.
- If the craft guide and a profile disagree, the craft guide wins and the profile is changed. The `fast` value always stays in the press band (100 to 160 ms or less). `base` is for ordinary transitions. `slow` is for entrances and sheets, so it may pass 300 ms, and it grows on TV.
- Every token is used by a component. An unused motion token is deleted.
