# Frame the work and choose a posture

Read the room before you design. Most weak interface work jumps to a default look (indigo gradient, five tabs, a stack of white cards) because nobody read the brief.

## Contents
- Read the signals
- Say the frame in a few lines
- Choose the posture
- Set the dials as observable targets
- Category bias
- The signature move
- Ask one question or none
- Work from the product

## Read the signals

1. **Kind of thing.** A page that is read (landing, marketing, portfolio), a screen that is worked in (dashboard, inbox, settings, wallet, editor), or a single component.
2. **Kind of product.** Social, utility, fitness and health, fintech, commerce, content and media, productivity, kids, field and ops tool, car, TV.
3. **Vibe words.** Clean, playful, premium, native-feeling, dense, calm.
4. **Reference apps** the user names. On mobile, real apps are the design language.
5. **Context of use.** One-handed on a train, two-handed on a couch, gloves in the field, eyes on the road, across a living room. Context sets density and target size. Taste does not.
6. **Platforms** and which one is first-class.
7. **Quiet constraints.** Accessibility needs, kids (bigger targets, no dark patterns), regulated fields, offline use, driving.

Read the repo before the brief: tokens, theme files, existing components, `DESIGN.md`, `package.json`, `pubspec.yaml`, the Gradle and Xcode project. The stack and the system you find outrank every default here.

## Say the frame in a few lines

```
FRAME: <kind of product> for <audience>, <vibe> language, leaning <stack and design language>.
platforms: <iOS first-class | Android first-class | web | desktop | TV | car>, lead <one>
posture:   <unified-brand | iOS-first | Android-first | per-platform-native>
kind:      <page | working screen | component>
context:   <where, with what hands, how long a look>
```

Show it to the user and let them correct it before you go on.

## Choose the posture

| Posture | Meaning |
|---|---|
| unified-brand | One look on every platform. Native navigation chrome underneath |
| iOS-first | iOS idioms lead. Android adapts |
| Android-first | Material idioms lead. iOS adapts |
| per-platform-native | Components diverge on purpose (system icons, switches, pickers, sheets) |

Rules:
- Name the posture. A posture is a commitment, not a mood.
- **Chrome lags content.** Keep navigation chrome native (bars, back, transitions) until the brand needs to own it. A custom tab bar with broken safe areas and no press states is the most common failure of "expressive" apps. Brand the content first. Earn the chrome.
- Never mix platform chrome. No Android FAB on iOS. No iOS bottom sheet pattern copied unchanged onto Android. No hover-dependent affordance on touch.
- Translate idioms between platforms. Do not transplant them (see the platform guides).

## Set the dials as observable targets

Three dials help as shorthand: **expression** (native to fully branded), **motion** (native transitions to gesture-driven), **density** (airy to cockpit). Baseline them low on mobile, because convention is a feature on a phone.

A number alone is not evidence. Pair each dial with something a second reader can check on the render:

| Dial | Observable anchor |
|---|---|
| Expression | How many components are custom versus platform |
| Motion | How many things move besides press feedback and navigation |
| Density | Rows per screen, tap target size, text size |

Hard floors that no dial overrides: targets stay at least 44 pt or 48 dp, reduced motion is honored, animation stays off the main thread, text scales with the system.

| The brief reads as | Expression | Motion | Density |
|---|---|---|---|
| Native-feeling, clean | 1 to 3 | 2 to 3 | 3 to 4 |
| Utility tool | 3 to 4 | 3 to 4 | 4 to 5 |
| Consumer social or feed | 5 to 7 | 5 to 7 | 4 to 5 |
| Brandy, playful, kids | 7 to 9 | 6 to 8 | 2 to 4 |
| Premium or fashion | 7 to 9 | 5 to 7 | 2 to 3 |
| Pro tool, trading, ops | 3 to 5 | 2 to 3 | 7 to 9 |
| Car | 2 to 4 | 1 to 2 | 2 to 3 |
| TV | 4 to 6 | 3 to 5 | 2 to 3 |

When two rows fire and disagree, the surface wins over the mood.

## Category bias

| Kind | Prefer | Avoid |
|---|---|---|
| Fintech | Tabular figures, trust neutrals, explicit states for money-moving actions | Mascots, gradient balance cards, digits that jiggle in animation |
| Health and fitness | One hero metric per screen, plain encouraging copy | Triple stat dashboards, red as progress, streak guilt |
| Consumer social | Content first, fast feeds, quiet chrome | Heavy cards around every post, engagement-bait badges |
| Commerce | Photo room, sticky clear price and buy, honest urgency | Badge confetti, fake countdowns |
| Productivity | Density, keyboard flows, instant response | Onboarding tours, illustrated empty states everywhere |
| Kids | Targets of 56 or more, high contrast, zero dark patterns | Tiny icon buttons, ad-like layouts, infinite scroll |
| Car | Few big controls, short labels, voice, host templates | Free text, long lists, motion, small targets |
| TV | Focus rings, rails, big type, dark ground | Hover, tiny text, dense screens |

## The signature move

Each screen gets at most one bold move: a distinctive header, one signature interaction, one expressive component. Everything else stays quiet. A screen where everything is expressive reads as noise, and an app where every screen shouts has no voice.

## Ask one question or none

If the read genuinely forks ("native like Things or branded like Duolingo?"), ask exactly one question with your recommended answer. If you can infer, say your assumption and go on. When the user cannot judge your assertion at all, build two or three low-fidelity options instead of describing them. Nobody can choose a design from adjectives.

## Work from the product

- Reuse what exists. Extend an established system. Replace it only for an approved redesign.
- Identify the audience, the primary task and the important states before you draw.
- Do not turn a small fix into a discovery workshop.
- Never change silently: tab order, route and deep-link paths, token names, form field meaning, learned gestures.
