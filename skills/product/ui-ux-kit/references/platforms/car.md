# Car displays

For Android Auto, Apple CarPlay, Android Automotive and OEM in-car systems. The driver's job is to drive. The interface must never compete with it. These rules are ours, built from the glance model that automotive guidelines use. Always check the host platform's current guide and the car maker's own rules before you freeze a value.

## The glance model

- One glance should take about 2 seconds.
- A whole task should fit in about 12 seconds of looking away from the road, in two or three short glances.
- If a task needs more, it is not a driving task. Move it to a parked state, a phone, or voice.

Write the task as a list of glances. Count them. Cut steps until it fits.

## What belongs in a car

Only short, glanceable tasks that the host platform allows for your app category (for example navigation, media, messaging, point of interest, charging). **Payments, checkout, sign-up, long forms and browsing do not belong in a car.** Hand them to the phone or to a parked state. An app that must show a checkout on a car screen has the wrong plan.

- Android Auto and CarPlay only accept apps in permitted categories and render them through the host's templates. A React Native or Flutter app cannot draw those templates by itself. You need the host's template library and native code (Car App Library on Android, CarPlay templates on iOS).
- Android Automotive OS and some OEM systems allow more, but each has its own review rules.

## Use the host

- Most car platforms give template screens (list, grid, pane, message, map, now playing) and own the theme, the typography and the item limits. Use the templates and the host's components. They are tested and certified.
- Theme only what the host allows: accent, icons, artwork.
- Content limits change while the car is moving. Design for the smallest limit.

## Targets, type and layout

- Targets at least 76 dp (about 76 px at 1x) with generous gaps. The host enforces its own minimum on template apps. Keep controls off hard-to-reach or bezel-covered edges.
- Body at least 24 px and labels of three words or fewer. Large type, high contrast.
- Few choices per screen. No long lists. Page or cap them.
- No free text. Offer voice, presets or a short list.
- Keep the primary action in the place the driver expects. Do not move things between visits.

## Color

- A dark ground and a lifted text color for night. A bright high-contrast set for day. Switch by ambient light or headlights, never by hand.
- Both modes pass the high contrast floor. Glare lowers contrast, so keep a margin above the phone floor.
- Use red only for real danger. Never rely on color alone for state.

## Motion and media

- No looping animation, parallax or auto-advancing content.
- Keep motion that carries meaning, such as a turn cue or a route change. Keep it short.
- Android Auto and CarPlay apps cannot show video at all. Some Android Automotive OS builds allow it when parked, with the maker's approval. Treat video as off by default. Keep notifications short and rare.

## Interaction

- Voice is a first-class input. Anything that needs typing offers voice.
- Physical controls (rotary, steering wheel keys) must reach every item. Keep focus order simple and visible.
- Confirm only what must be confirmed. A confirmation that needs reading is too long for driving.
- Keep session state. A driver who looks away must find the screen as they left it.

## Verify

- Time each task with a stopwatch or a recorded run and count the glances.
- Use the host simulator or desktop head unit for templates. Use a real car or an OEM rig for glare, night and distance.
- Check the smallest item limit, the day and night modes, and voice flows.
- Say which checks came from a simulator and which from a car. Do not claim a driving-safety result you did not measure.
