---
name: ui-ux-kit
description: "Design and build one screen or one component with good UI, UX and motion: pick the posture, name the screen's one question, choose the navigation container, specify components with all their states, plan motion by how often it is seen, apply the UX rules, then verify on the real surface and write acceptance rows. Covers iOS, Android (Kotlin and Compose), React Native, Flutter, desktop, web (React, Next, Vue, Nuxt, Svelte, Tailwind), car displays (glance rules for driving) and TV (focus and distance). Use when asked to build, redesign or review a screen, a component, an interaction, a transition or a gesture. Not for palettes and modes (color-kit), the whole token file (design-system-kit), a journey tracker for a shipped product (product-polish-workflow) or a throwaway answer (prototype-wireframe)."
metadata:
  version: 1.0.0
  author: levistack
  license: MIT
  group: product
  category: product-design
  department: product
  related_skills:
    - design-system-kit
    - color-kit
    - prototype-wireframe
  invokes:
    - skill: color-kit
      when: Color roles or contrast on a screen
  tags:
    - ui
    - ux
    - components
    - motion
    - accessibility
  capabilities:
    - screen_and_component_design
  languages:
    - en

---

# UI and UX kit

Build one screen or one component well. This skill owns hierarchy, states, components, motion and UX for every platform, including the car and the TV. It does not choose palettes (that is `color-kit`) and it does not own the token file (that is `design-system-kit`).

Work through every step in order. Keep a step short for a small request. Never skip silently: write `Step N: skipped, because ...`.

## Step 0: Frame

Read the signals and write the frame in a few lines: product, audience, platforms and the lead, posture (unified-brand, iOS-first, Android-first or per-platform-native), kind (page, working screen or component), context of use (hands, distance, how long a look). Show it and let the user correct it. If the read forks, ask one question with your recommendation. Guide: `references/frame-and-posture.md`.

## Step 1: Read the system

Read the repo first: tokens, theme files, existing components, `DESIGN.md`, the stack files. Use what exists, by name.

- Tokens exist: use them. Invent no values.
- A palette or a mode is needed and none exists: load `color-kit`, then use its roles.
- A whole app or a whole token file is needed: load `design-system-kit`, and come back for the screens.
- Nothing exists and the scope is one screen: propose a small set of roles and say they are assumptions.

Never write a raw hex or a raw size in a component. Use roles and tokens.

## Step 2: Plan the screen

Name the one question, the one finding and the list of blocks. Choose the navigation container with the tree. Decide the states owed. Pick at most one signature move. Fill `templates/screen-brief.md`. Guide: `references/screen-anatomy.md`. For one component only, skip to Step 3.

## Step 3: Components

Scope the component, keep the register and the existing tokens, then specify and build it with all eight states, the geometry rules, variants and sizes, and the native equivalents for each platform. Fill `templates/component-spec.md`. Guide: `references/components.md`.

## Step 4: Motion

Run the gate for every candidate: how often is it seen, and what is its purpose in one sentence? Write the thesis and the contract. Use duration and easing tokens, springs for drag, one-to-one tracking for gestures, and a reduced-motion path for every layer. Fill `templates/motion-spec.md`. Guide: `references/motion.md`. Timing table: `data/motion-bands.csv`.

## Step 5: UX rules

Apply the rules in priority order: the task, states, accessibility, system, platform, polish, motion. Filter `data/ux-rules.csv` by your platforms and walk the critical and high rows. Handle forms, feedback, permissions, haptics and copy. Guide: `references/ux-rules.md`.

## Step 6: Platform pass

Open the guide for each platform you serve and apply it. Use `data/stack-notes.csv` for the stack's do and don't rules and `data/targets-and-sizes.csv` for targets and text sizes.

| Platform | Guide |
|---|---|
| iOS and iPadOS | `references/platforms/ios.md` |
| Android, Compose and Views | `references/platforms/android-compose.md` |
| React Native and Expo | `references/platforms/react-native.md` |
| Flutter | `references/platforms/flutter.md` |
| Desktop (macOS, Windows, Linux, Electron, Tauri) | `references/platforms/desktop.md` |
| Web (React, Next, Vue, Nuxt, Svelte, Tailwind) | `references/platforms/web.md` |
| Car (Android Auto, CarPlay, in-car) | `references/platforms/car.md` |
| TV (tvOS, Android TV, web on TV) | `references/platforms/tv.md` |

For a cross-platform product, translate idioms between platforms. Never transplant them. Do not stretch a phone layout onto a tablet or a window.

## Step 7: Verify

Build and run the real thing. Look at it on the right surface. Check light, dark, the largest text, reduced motion, the smallest screen and the screen reader on the main task. Ask precise questions about the render. Fix problems in one batch and look again. Run `templates/preflight.md`. Write `ux-acceptance.csv` rows and validate them with `node scripts/check-acceptance.mjs ux-acceptance.csv`. Guide: `references/verification.md`.

## Step 8: Hand off

Report what changed, what you tested and on which surface, which checks were not verified, and the acceptance rows you wrote. If the work is part of a shipped product, give the rows to `product-polish-workflow` so they join its journey tracker. If new roles or states were needed, hand them to `design-system-kit`.

## Rules

1. **Read the room first.** Frame before you draw. Name the posture.
2. **One question per screen.** The biggest block answers it. State the finding.
3. **Use the system that exists.** Tokens by name. No raw values.
4. **Chrome lags content.** Keep platform chrome native until the brand needs it.
5. **Every state, every time.** Eight for a control, and the view states for a screen.
6. **Motion needs a purpose and a frequency check.** Do not animate frequent actions.
7. **Targets and text meet the platform minimum.** Car 76 dp, TV 64 px, iOS 44 pt, Android 48 dp.
8. **A gesture always has an alternative.**
9. **Evidence from the right surface.** A browser screenshot is not native proof.
10. **Driving first in a car.** Two or three glances, host templates, voice, no decorative motion, and no checkout or typing.

## What is in this folder

| Path | Use |
|---|---|
| `references/frame-and-posture.md` | Signals, posture, dials as observable targets, category bias |
| `references/screen-anatomy.md` | One question, blocks, shell, lists, charts, states, phone widths, tells |
| `references/components.md` | Scope, eight states, geometry, inventory, native equivalents, packaging |
| `references/motion.md` | Frequency gate, easing, duration, springs, gestures, sheets, reduced motion |
| `references/ux-rules.md` | The rule groups and the order to apply them |
| `references/verification.md` | Evidence by platform, the render loop, acceptance rows |
| `references/platforms/` | iOS, Android, React Native, Flutter, desktop, web, car and TV guides |
| `data/ux-rules.csv` | 108 rules with id, platform, check, severity and evidence |
| `data/motion-bands.csv` | Duration and easing by purpose and platform |
| `data/stack-notes.csv` | Do and don't per stack |
| `data/targets-and-sizes.csv` | Targets, text sizes and safe areas by platform |
| `templates/` | Screen brief, component spec, motion spec, preflight, acceptance CSV |
| `scripts/check-acceptance.mjs` | Validates the acceptance CSV |

## Related skills

- `color-kit`: owns palettes, roles, modes and contrast proof. Call it when a screen needs a new palette or a mode.
- `design-system-kit`: owns the token file, type, space, `DESIGN.md` and governance. Call it for a whole system.
- `product-polish-workflow`: audits and changes a shipped product and keeps the journey tracker. It takes your acceptance rows.
- `prototype-wireframe`: answers one open question with a throwaway before you build for real.
- `tdd`: test behavior of the real component first.
- `verify`: prove the rendered result on the real surface.
- `challenge-me`: stress-test the direction before you build.

## Done when

- The frame and posture are written and the user agreed.
- The screen's question and finding are stated, or the component's spec is filled.
- Every state exists and uses tokens and roles.
- Every motion has a purpose, a token and a reduced-motion path.
- Platform minimums hold for every platform served.
- It was run on the right surface and the checks are listed, with Not verified items named.
- `ux-acceptance.csv` is valid and every row has a code anchor.
