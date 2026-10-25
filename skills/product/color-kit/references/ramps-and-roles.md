# Ramps and roles

A color system is ramps that feed roles. A ramp is a set of steps in one hue. A role is a job such as page ground, border or primary fill. Components use roles. They never use ramp steps.

## Contents
- Work in OKLCH
- What a system needs
- What a good ramp looks like
- Several hues at once
- Fit the gamut
- Every step has a job
- Names
- Rules of use
- When the kit is not installed

## Work in OKLCH

OKLCH has three numbers: lightness L (0 to 1), chroma C (colorfulness, 0 to about 0.3) and hue H (0 to 360). Even steps in L look even to the eye, and the hue stays itself as L changes. HSL does neither, so a ramp built by varying HSL lightness drifts and bunches at one end.

Keep the terms apart:
- **Chroma** is colorfulness against a gray of the same lightness.
- **Saturation** is colorfulness against the color's own brightness.
- **Lightness** is how light the color looks against white.

Use a color library (culori, colorjs.io, chroma.js) or the kit script for the math. Do not compute a ramp by hand or by eye.

## What a system needs

| Ramp | How many | Notes |
|---|---|---|
| Neutral | 1 | Ground, borders and text. Needs the most steps |
| Accent (brand) | 1 | Interactive and selected states. A second hue only when two things must be told apart at a glance |
| Status | 0 to 4 | Danger, warning, success, info. Add one only when the product shows that state |

A ramp for a status the product never shows is maintenance for zero pixels.

## What a good ramp looks like

Check these properties on any ramp, in any notation:

- **Lightness steps steadily** in OKLCH L.
- **Hue is constant** from end to end. A drifting hue reads as two blended colors.
- **Chroma peaks in the middle** and falls toward both ends. The lightest and darkest steps are nearly neutral.
- **Steps are finer at the light end.** Keep steps 50 to 200 about 0.04 to 0.05 apart in L and mid steps about 0.07 to 0.10. Even spacing leaves too few pale steps.
- **No two neighbours look the same.** If adjacent steps are under 0.03 apart in L, the ramp has more steps than decisions.
- **Both ends stop short of pure black and white.**

The kit builds an 11-step ramp (50 to 950) with these lightness values: .975, .945, .895, .825, .735, .645, .555, .47, .39, .31, .235 for the brand, and .985 down to .16 for the neutral.

## Several hues at once

When the accent and the status ramps sit together, they must agree step for step.

- **Match lightness exactly.** Red 500 and blue 500 should read equally bright, or one button looks heavier.
- **Match vividness as a proportion.** Hues do not share a maximum chroma. A saturated yellow and a saturated blue are not equally far from gray. Set each ramp to the same share of what its own hue can reach.
- Yellows and cyans peak much lower than reds and blues. Copying the same chroma number across hues makes warning look weak beside danger.
- **Keep every status hue at least 15 degrees of hue away from the accent.** If the brand is red, danger cannot also be red. Give the destructive action a different treatment, such as an outlined button with an icon.
- **Keep success and danger far apart in lightness** (at least 0.12 in L) so people with red-green color blindness can tell them apart.

## Fit the gamut

Asking for more chroma than a screen can show clips a channel and shifts the hue. Fix it by **lowering chroma at the same lightness and hue** until the color fits. Never change lightness or hue to fix clipping. Browsers map `oklch()` for you, but scripts that convert to hex do not.

For wide-gamut screens, write the sRGB value first and the vivid P3 value after it, inside `@media (color-gamut: p3)`. An sRGB screen then shows a color you chose, not one the browser clipped.

## Every step has a job

Generate the steps the roles call for and skip the rest.

| Role | Tailwind-style step | 12-step role scale |
|---|---|---|
| Page ground | 50 | 1 |
| Subtle ground | 50 or 100 | 2 |
| Component ground | 100 | 3 |
| Hovered component | 200 | 4 |
| Pressed or selected | 200 | 5 |
| Quiet border or divider | 200 | 6 |
| Border, focus ring | 300 | 7 |
| Hovered border | 400 | 8 |
| Solid fill | 600 | 9 |
| Solid fill hover | 700 | 10 |
| Low-contrast text | 700 | 11 |
| High-contrast text | 900 | 12 |

The two numbering styles differ in kind. A role-defined scale (12 steps) keeps step 9 as "the solid" in every ramp and in dark mode, so component code never changes. A lightness-defined scale (50 to 950) inverts in dark mode, so the mapping lives in the semantic tier. For a new system prefer the role-defined idea. On Tailwind keep 50 to 950 and put the role map in the semantic layer.

A solid on step 600 is usual because white text on most 500 fills fails 4.5:1. Where the table repeats a step, those roles look the same. A design that needs component hover and quiet border to differ needs the 12-step version.

## Names

Two tiers, three only by exception:

- **Primitives** name a value by hue and step (`blue-600`, `neutral-200`). They are never used in a component.
- **Semantics** name a job (`text-muted`, `border-strong`, `primary`). They point at a primitive. Components use only this tier. Themes override only this tier.
- A **component** tier (`button-danger-bg`) only where a component truly departs from the system. One is an exception. Twenty means roles are missing.

Naming grammar (pick one and keep it):

| Concept | Use | Never mix in |
|---|---|---|
| Foreground | `text` | fg, foreground, ink, content |
| Ground | `background`, `surface` | fill, bg used as a synonym for surface |
| Edge | `border` | stroke, outline, line |
| Brand | `primary` (kit) or `accent` | brand, theme, used loosely |

Use one word per concept so `text-disabled` can be guessed from `text-muted`. Keep **border** and **separator** as separate roles even if they share a value today. A border encloses a control. A separator divides content. Reserve `primary` for one meaning. Never name a role by its look (`blue-button`, `sidebar-gray`) or number it (`text-2`).

See `data/roles.csv` for the full role inventory and its light and dark rules.

## Rules of use

- **One color, one meaning.** Treat hues within 15 degrees as the same color. If the accent means interactive, every interactive element uses it and nothing else does.
- **One filled action per view.** The primary gets the fill. Peers stay neutral. Put color on the ground of the control, not only on its label.
- **Use a token only in its own role.** Do not borrow a border token for text because it looks right today.
- **Never carry meaning by color alone.** Add an icon or a word.
- **Measure the rendered pair.** See the contrast proof guide.
- **Write the decision, not the value** where you can: "label is the better of paper and ink against the fill", "hover is one step toward more contrast". Rules survive a palette change. Frozen hex values do not.

## When the kit is not installed

If `design-system-kit` is not available, do the same work with a color library:

1. Read the brand color in whatever format it comes. Convert to OKLCH.
2. Build the neutral, accent and needed status ramps with the properties above. Check each property on the output.
3. Map ramps to the roles in `data/roles.csv` for light and for dark.
4. Measure every pair in `data/essential-pairs.csv` with the same library. Report only numbers you measured.
5. Write the roles as CSS variables, or in the stack's own theme file.
