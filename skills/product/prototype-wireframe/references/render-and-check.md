# Render and check

## Contents
- Render with headless chromium
- Batch render
- Fonts offline
- Check before you show it
- No vision? Check by measuring
- Common traps
- Delivery

## Render with headless chromium

One fresh process per shot. It is deterministic, and it does not keep state like a browser daemon.

```bash
CHROME=${CHROME:-"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}   # or chromium / google-chrome on Linux
"$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=390,844 \
  --screenshot=out.png "file://$PWD/screen.html"
```

`file://` URLs work, so no server is needed. Window size equals the fixed-size screen container, so the capture has no margin.

## Batch render

Write a `render.sh` and keep it with the prototype. Read each file's size from a generated `sizes.txt`, then run `bash render.sh`. Do not type a loop with nested command substitution inline, because it waits on approval and the batch never starts. The same script re-renders the one screen you fixed.

Assert the line count of `sizes.txt` equals the HTML count before the loop. A pattern that requires a closing brace after `height:844px` matches nothing, and zero screens render.

## Fonts offline

Do not link web fonts. If the network is down, the browser silently falls back and the mockup looks wrong. Self-host the woff2 files in `fonts/` next to the HTML, declare each weight with `@font-face` and a relative path, and commit them.

## Check before you show it

1. **Files:** `file out.png` says PNG, the PNG count equals the screen count, and no file is suspiciously small (a blank render is tiny).
2. **DOM tests, after `document.fonts.ready` and a short wait:**
   - pairwise overlap between positioned elements,
   - horizontal overflow (`scrollWidth - clientWidth`),
   - each rect measured against the design frame (the phone), not the browser window.
   Fix and re-run until they print nothing. Move a collided label to a free band, not 4 px sideways.
3. **Vision, one targeted question per screen:** "anything overlapping, clipped or cut off at the edge? does the selection box line up with its target? any element drawn twice?" Never ask "does this look good".
4. **Counts:** `<svg` count equals `</svg>` count, and the expected number of cards, tiles and badges is present. A replace that matches nothing leaves a section empty and the board still renders.
5. **Contrast:** compute it from the two hex tokens, and fix the token, not each screen.
6. **Thumbnails:** shrink every variant to about 240 px wide and look at them side by side (see `variant-gate.md`).

## No vision? Check by measuring

Never say a layout "looks right" when you cannot see it.

- Confirm PNG type, pixel size and a non-trivial byte size.
- Scan the PNG for the brand colors and count the pixels. A slot that lost an element drops by a large factor. Assert against about half the healthy value, never against "greater than zero".
- Measure the bounding box of the drawn mark. A mark that fills 28% of the canvas reads as a tiny logo.
- Print a 56×56 downscale as characters (accent `R`, ink `#`, mid `+`, background `.`) to read the shapes.

## Common traps

- A helper that returns bare `<rect>` or `<text>` and gets placed in a `<div>` does not error. The browser draws a text fallback. Build one `<svg viewBox>` string per section.
- Hoist token values into locals before an f-string, or the inner quotes close the string.
- One literal `%` (such as `border-radius:50%`) inside a `%`-formatted string raises `unsupported format character`. Use `999px`, or `.format()`.
- A fixed-size wrapper with `border-radius` on a capture page bleeds page chrome into the shot. Use `html,body{margin:0;overflow:hidden}` and size the page to the square.
- Heavy CSS such as `feTurbulence` noise stalls software rendering. Drop it before the shot.
- For icon sets, capture one 1024 master (retry up to three shots, since a single shot can be half painted) and downscale every size from it with `ffmpeg`. Never capture each size on its own.
- A non-tabular number face shakes when the value changes. Put the number in a fixed-width, left-aligned box.

## Delivery

Keep the HTML, the render script and the receipt (`templates/receipt.md`) next to the PNG so a change is one re-render. Mermaid diagrams and infographics are a different job: render them with the tool the repo already uses.
