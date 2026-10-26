# Render, export and compress

Keep editable source separate from exports. Pick the format for the reader.

- SVG for scalable vectors
- PNG for exact raster labels
- GIF when the user asked for motion
- draw.io or Excalidraw when they will keep editing in the native tool
- HTML when they need controls or responsive layout

## Prerequisites

Check only the tools this job needs. Do not install global tools, change the project toolchain, or upload source as a silent fallback.

```sh
python3 --version
command -v mmdc
command -v rsvg-convert
command -v ffmpeg
command -v ffprobe
command -v drawio
```

Prefer project dependencies. A temp local folder is fine for a one-off check when allowed. Name the missing tool and which output it blocks. Keep native source and a text equivalent when render is unavailable. Do not call an export visually verified if you never rendered it.

## Mermaid

The [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) renders on your machine. It needs a browser stack. Check the version and `mmdc --help`. Typical commands:

```sh
mmdc -i figure.mmd -o figure.svg -b white
mmdc -i figure.mmd -o figure.png -b white -s 2
```

Use Markdown input mode when it fits, or extract real fenced blocks with a fence-aware parser. Check output file names before you change links. Keep `.mmd` source when you replace a fence with an image. Use clear alt text and paths relative to the document. Batch publish steps are in the batch-export guide from `SKILL.md`.

Fix syntax in a small failing snippet first, then restore the full diagram. Re-check meaning after any fallback or grammar change. A remote render API is allowed only when the user OKs sending content (`mermaid_remote_png.py --backend ink --allow-remote`).

## SVG to PNG

```sh
python3 <diagram-skill>/scripts/export_svg.py png figure.svg figure.png --width 1200
```

You need local `rsvg-convert` and a complete static SVG. This helper does not capture arbitrary CSS animation or HTML wrappers. For HTML, capture in a browser after fonts and layout settle. Use one explicit static frame for motion work.

Check real width, height, and background. Transparent PNG can hide dark text on a dark page. Judge at the size readers will see, not only at full zoom.

## GIF and animation

For the bundled highlight walk, use the plan from the motion guide:

```sh
python3 <diagram-skill>/scripts/export_svg.py gif figure.svg figure.gif --plan walk.json --width 1000
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames,duration -of json figure.gif
```

The helper renders PNG frames, then runs FFmpeg palette generation and palette use. See `ffmpeg -h filter=palettegen` and `ffmpeg -h filter=paletteuse` for your build. Keep a final still and the step plan. Output is finite and non-looping by default. Other motion needs its own frame plan and timing. Mermaid-source GIFs with browser motion styles use the Playwright GIF guide from `SKILL.md`.

For a large GIF, shrink size, drop extra hold frames, or lower frame rate after you check readability. Do not drop meaningful steps. Preview the real GIF file. Palette reduction can remove a color the SVG still showed.

## Compression

Work on a copy. Keep source and the uncompressed export. Try lossless PNG optimization first when a local tool exists. When palette quantization is acceptable:

```sh
pngquant --quality 90-100 --output figure-small.png -- figure.png
```

Read the tool help. Open the result. Compare size, alpha, text edges, gradients, and semantic colors. Keep the smaller file only when it is smaller and still readable. A quality score is not proof.

FFmpeg can re-encode PNG losslessly: `ffmpeg -i figure.png -c:v png -compression_level 9 -pred mixed figure-small.png`. Compare pixels and bytes. Keep it only when size actually drops.

JPEG suits photos. It can harm small diagram text. For JPEG screenshots, keep needed color profiles and inspect crops. Do not strip all metadata or overwrite every original by default. Measure bytes saved. Do not promise a fixed percent smaller. Do not assume every reader accepts every format.

## Delivery receipt

Record input revision or hash, source and export paths, commands, tool versions, dimensions, background, sizes you checked, and limits left open. For many files, list per-file pass or fail. Native editor check, structural check, and visual check are separate evidence.
