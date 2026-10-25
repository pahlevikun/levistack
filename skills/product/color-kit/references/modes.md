# Modes: light, dark, high contrast, night and TV

A mode is a full set of role values, composed on purpose. It is never the light set with the numbers flipped.

## Contents
- The mode list
- Dark
- High contrast
- Car day and night
- TV and big screens
- Brand and density themes
- How the mode is switched
- Test every mode

## The mode list

| Mode | When | Notes |
|---|---|---|
| Light | Always | The default for most products |
| Dark | Always, unless the product is a single fixed look | A second composition, not an inversion |
| High contrast | When the platform has the setting, or for accessibility | Its own values, per appearance |
| Dimmed | Long reading or sleep products | A softer dark with lower contrast steps and a lifted ground |
| Car day and night | Car displays | The host or the light sensor switches it. Both modes are high contrast |
| TV | TV screens | Dark ground by default, no large pure-white areas |
| Brand or white-label | Several brands on one library | Override roles only, never the raw palette |

## Dark

- **Reverse the roles first, then tune the values.** Swap ground and text roles, then adjust.
- **Raise surfaces by making them lighter.** Shadows do not show on dark grounds, so depth comes from lightness: ground, surface, raised, menu, each a step lighter.
- **Lower chroma.** A color that looks confident on white looks neon on near-black. Move the accent one or two steps lighter and a little less vivid (about 10 to 20 percent).
- **Do not use pure white text.** Use an off-white. Do not use pure black ground. Use a deep tinted neutral. Large pure-black fields can smear when scrolling on OLED, and pure white blooms.
- **OLED exception.** Pure black is a legitimate choice on OLED phones when you choose it on purpose and keep elevation from borders or lighter surfaces. Say it in the brief.
- **The dark end needs more separation.** Steps that read as pale backgrounds collapse together as dark surfaces. Widen them.
- **Contrast does not survive the mirror.** A pair that passes in light says nothing about dark. Measure every pair again.
- **Brand solids move to lighter steps** (300 to 400) and their label flips to dark ink.
- **Images and logos.** Dim large bright images a little. Provide a light-on-dark logo. Avoid large bright areas.
- **Material You and system colors.** On Android 12 and later you may start from the wallpaper-derived scheme and keep your own as the static fallback.

## High contrast

- Give it its own values for each appearance. A block that darkens the accent in dark mode lowers contrast there.
- Use solid colors, not alpha. Give every control an explicit border.
- Drop decorative shadows and glows. Shadows are invisible or distracting beside strong borders.
- The increased-contrast value should widen the gap to its ground by at least 0.15 in OKLCH L over the default. Aim for APCA Lc 90 on body text. Measure it, do not assume.
- On the web, test `forced-colors` and `prefers-contrast: more`. A probe with `forced-color-adjust: none` helps check that your own role aliases are right. A browser-forced body text alone can hide a broken alias.
- On native, read the real accessibility settings (Increase Contrast, Bold Text, high contrast text) and refresh views when they change.

```css
:root { --color-primary: var(--blue-600); }
@media (prefers-contrast: more) { :root { --color-primary: var(--blue-900); } }
@media (prefers-color-scheme: dark) { :root { --color-primary: var(--blue-400); } }
@media (prefers-color-scheme: dark) and (prefers-contrast: more) { :root { --color-primary: var(--blue-200); } }
```

## Car day and night

- Switch by ambient light or headlights, not by hand. Keep the same roles and swap values.
- Both modes are high contrast. Glare lowers contrast, so use a higher floor than a phone.
- Night: a dark ground with lifted text, no pure white blocks, low blue light for long drives.
- Use the host's theme where the host owns the template (Android Auto, CarPlay, in-car OS templates). Your colors apply to the parts the host lets you theme: icons, accent, artwork.
- Do not use red for anything but real danger. Do not use color alone for state.

## TV and big screens

- Dark ground by default. A TV is seen in a dim room.
- Avoid large pure-white areas and fully saturated red. They bloom on some panels.
- Focus is the main state. Make it unmistakable with color, a ring and a scale-up together. The ring color must pass 3:1 against both the item and the ground.
- Keep text at high contrast. Thin weights wash out at 3 meters.
- Keep a safe margin. Do not put key colors or text in the outer 5 percent.

## Brand and density themes

- Themes repoint the **semantic tier**. The raw palette and the components stay untouched.
- A theme type is one of: color mode, brand, density. Keep them independent so a brand can have a dark mode.
- Document which roles a theme may change and which are fixed.
- Test every component in every theme.

## How the mode is switched

Use **one** switching mechanism everywhere.

| Mechanism | Use when |
|---|---|
| `prefers-color-scheme` only | There is no manual toggle. Nothing to store |
| A `data-theme` attribute or class | Users can override the system. The media query sets only the initial value |
| `light-dark()` | You want both values in one declaration. Needs `color-scheme: light dark`, and a class toggle must set `color-scheme` too |

A media query that sets some tokens plus a class that sets others gives a half-themed screen the moment a user overrides the system. On native, follow the system appearance by default, and let an explicit app choice override it.

## Test every mode

- Every pair, in every mode. Mirrored pairs score differently.
- Pressed, focused, disabled and selected states in each mode, not only the resting state.
- Borders and dividers stay visible in both light and dark.
- Scrims and overlays: measure the composed result over real content.
- Large text and increased contrast together.
- The mode switch itself: no flash of the wrong mode on load.
