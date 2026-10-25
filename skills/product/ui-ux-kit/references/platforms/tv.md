# TV and big screens

For tvOS, Android TV, Google TV and web apps on TV. The user sits about 3 meters away with a remote. Nothing is reached by pointing. Everything is reached by focus. These rules are ours, from the 10-foot model. Check the platform guide and test on a real panel.

## Focus is the interface

- Every item must be reachable with the D-pad. Focus is never lost, never trapped and never invisible.
- The focused item is obvious from across the room: a ring of 4 px or more, a scale-up of about 1.08, and a tone change, together. The ring color passes 3:1 against both the item and the ground.
- Remember the last focus when the user comes back. Keep focus order simple and predictable.
- Back always works and returns to where the user came from.
- No hover. No small targets. No gesture that only a touch screen can do.

## Layout

- Stay inside the safe area of about 5 percent. On a 1920 by 1080 canvas that is roughly 80 px at the sides and 60 px at top and bottom.
- Build with rails: rows of cards that scroll sideways, stacked vertically. Keep the number of choices on one screen small.
- Use large artwork. Video and art lead. The chrome stays quiet.
- Place the side menu and the content so focus moves between them with one key.
- Long lists need paging or rails with clear edges.

## Type and targets

- Body text at least 28 px at 1080p. Avoid thin weights. Keep line lengths short.
- Targets at least 64 px. Spacing generous so focus moves cleanly.
- Titles short. Do not ask for typing. Offer voice or a keyboard overlay with large keys.

## Color

- A dark ground by default. A TV is watched in a dim room.
- Avoid large pure-white areas and fully saturated red. They bloom on some panels.
- Keep contrast high. Check on a real panel, because panels differ.

## Motion

- Slower and larger than a phone (about 1.35 times). A focus move shows the ring and the scale together so the eye can follow.
- Keep motion calm. Auto-play previews start after focus rests and stop when focus leaves.
- Do not auto-advance content without a way to pause.

## Verify

- Walk every screen with the remote only. Never touch a pointer.
- Sit at 3 meters and read the smallest text and the focus state.
- Check on at least one real panel, and with the system's reduced motion and large text settings where they exist.
- Check the safe-area overlay.
- Say which checks came from an emulator and which from a TV.
