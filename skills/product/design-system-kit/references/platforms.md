# Platforms: mobile, desktop, web, TV and car

One design system can serve many screens. The colors, the voice and the shapes stay the same. The **sizes, spacing, focus and motion** change with the screen, the input and the viewing distance. This file says how.

Numbers here are safe starting points. Always check the target platform's own guide (Apple Human Interface Guidelines, Material, Android TV and Auto guides, the OEM kit) before you freeze them.

## Contents
- How a platform changes the system
- The five profiles
- Choosing the lead platform
- Several platforms at once
- Checks per platform
- Running it

## How a platform changes the system

| Part of the system | What the platform changes |
|---|---|
| Type | Base size, smallest text, weight (no thin weights on TV or in a car) |
| Spacing | The whole scale grows or shrinks by a multiplier |
| Controls | Height, padding, the smallest tap or focus target |
| Focus | Ring width, scale-up on focus (TV), keyboard order (desktop, web) |
| Motion | Durations and travel (slower on TV, almost none in a car) |
| Color | Contrast floor, default ground (dark on TV and in a car), no pure white blocks on TV |
| Layout | Safe areas, columns, how many choices fit on one screen |

Tokens do not fork per platform. There is one `theme.css`, and each other platform is a small override block (`platforms.css`) that changes only the values above.

## The five profiles

| | Mobile | Desktop | Web | TV | Car |
|---|---|---|---|---|---|
| Input | Touch | Pointer and keyboard | Touch, pointer, keyboard | Remote, D-pad focus | Touch, rotary, wheel keys, voice |
| Viewing | Hand, 30 cm | Arm's length | Varies | About 3 m | Quick glances |
| Body text | 16 px or more | 13 to 14 px | 16 px | 28 px or more | 24 px or more |
| Control height | 48 | 36 | 44 | 72 | 76 |
| Smallest target | 44 pt (iOS), 48 dp (Android) | 24 px | 24 px (WCAG 2.2), 44 for touch | 64 px | 76 dp |
| Focus ring | 2 px | 2 px | 2 px | 4 px plus scale about 1.08 | 4 px |
| Motion | Normal | Quicker (x0.8) | Normal | Slower (x1.35) | Minimal (x0.6) |
| Default ground | Either | Either | Either | Dark | Dark, with an automatic day mode |
| Contrast floor | Standard | Standard | Standard | High | High |

### Mobile (iOS, Android)
- Respect the notch, status bar, home indicator and system gesture edges. Put main actions in thumb reach.
- Text must scale to 200% without clipping (dynamic type, font scale).
- Use the platform's back and gesture rules. Prefer sheets and bottom bars to dropdowns and hover menus.
- Test outdoors: raise contrast for text over photos.

### Desktop (macOS, Windows, Linux)
- Every action has a keyboard path and a visible focus state. Show shortcuts next to commands.
- Hover, right-click and drag are fine, but never the only way.
- Density can be higher: 32 to 36 px controls are normal. Windows resize, so set a minimum width and let panes grow.
- Follow the OS for window controls, menus, dialogs and notifications.

### Web (responsive)
- Mobile first at 360 px, then 480, 768, 1024, 1280, 1536. Use fluid type and spacing (`clamp`).
- Support zoom to 400%, text spacing changes, `prefers-color-scheme`, `prefers-reduced-motion` and forced colors.
- Keep reading lines at 60 to 75 characters. Respect `env(safe-area-inset-*)` on notched phones.

### TV (tvOS, Android TV, web on TV)
- Everything is reached by focus. The focused item must be obvious from the couch: a ring of 4 px or more and a scale-up.
- Stay inside the safe area: about 5% inset (on a 1920 x 1080 canvas, roughly 80 px at the sides and 60 px top and bottom).
- Body text at 28 px or more at 1080p. No hairline weights. Dark ground. Avoid large pure-white areas and fully saturated red, which bloom on some panels.
- No hover, no tiny targets. Keep focus order simple, remember the last position, and use few choices per screen with clear rails.
- Video and art lead. The chrome stays quiet.

### Car (Android Auto, CarPlay, in-car OS)
- Design for glances. One glance is about 2 seconds, and a whole task should fit in about 12 seconds of looking away from the road.
- Targets of 76 dp or more, generous gaps, short labels, large type. No long lists, no free text. Offer voice for typing.
- Day and night themes switch by ambient light or headlights, not by hand. Keep contrast high in both.
- No looping animation, no parallax, no auto-advancing content.
- Use the host's templates and components where they exist. They are certified and tested.

## Choosing the lead platform

The **lead** is the platform whose values go into `theme.css` and `DESIGN.md`. Pick the one with the strictest needs among the ones you serve, so that nothing breaks when the others are derived: car, then TV, then mobile, then web, then desktop. For example, a product on web and TV leads with TV for contrast and focus, and the web block overrides sizes down.

If the user names one platform, lead with it and say what you assumed for the others.

## Several platforms at once

- Build one `theme.css` and one `platforms.css`. Set `data-platform="tv"` (or `car`, `mobile`, and so on) on the root element, and the override block applies.
- Do not copy the layout. A TV home screen is rails of art, a phone home screen is a list. Share tokens and components, and design each layout on its own.
- Write platform differences in `DESIGN.md` under Layout, one short paragraph each.

## Checks per platform

The builder checks these for every platform you list:

| Check | Pass rule |
|---|---|
| Body text size | At least the profile's minimum |
| Control height | At least the profile's smallest target |
| Smallest text | At least 70% of the minimum body size, and never below 10 px |

And by hand, per platform:

- Mobile: 200% text, one-handed reach, offline and slow-network states.
- Desktop: full keyboard run-through, resize to the minimum width, high-DPI and standard-DPI screens.
- Web: 320 px width, 400% zoom, keyboard only, reduced motion, forced colors.
- TV: every screen reachable with the D-pad only, focus never lost, text readable at 3 m.
- Car: each task can be done in two or three glances, works at night and in glare.

## Running it

```bash
python3 scripts/theme/theme.py build --brief "your brief" --platform tv,web --out out/
```

The first platform leads. `out/platforms.css` holds the override blocks. `out/report.md` lists the platform checks.
