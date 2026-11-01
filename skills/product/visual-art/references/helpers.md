# Reusable art helpers

Run with Python 3.9 or newer. No package installation or network access is required
for scene JSON or interactive HTML. Resolve file-toolkit's scripts/files.py from
its actual installed skill directory when rendering or encoding.

```sh
python3 scripts/art.py scene --seed 42 --count 80 --width 640 --height 480 --palette '#17324d,#f6ae2d,#f3f0e8' --output scene.json
python3 scripts/art.py render scene.json --toolkit /path/to/file-toolkit/scripts/files.py --output artwork.svg
python3 scripts/art.py explore --seed 42 --output explore.html
python3 scripts/art.py gif frame01.png frame02.png --toolkit /path/to/file-toolkit/scripts/files.py --fps 8 --output loop.gif
```

The scene generator emits file-toolkit's kind=image schema with a closed palette,
size bounds and deterministic circle geometry. Static compositions can use that
owner's rect, circle, line and text primitives. The interactive HTML has no external
scripts: seed/count controls redraw a canvas, and Download PNG exports the current
frame. No browser is launched by the helper.

Outputs are new files by default; --overwrite is explicit. Render and GIF commands
forward to file-toolkit without a shell, with its validation and capability checks.
Use file-toolkit capabilities to learn whether actual image/GIF encoding is available.
Tests: scripts/test_art.py. This helper does not synthesize speech or operate a live
image-generation service; those require their own available tools and task authority.
