# Render, export and compress

Keep editable source and derived output separate. Choose the format for the consumer. Use SVG for scalable vector delivery, PNG for exact raster labels, GIF for an explicitly requested animation, and native draw.io or Excalidraw for continued editing. HTML is useful when the reader needs controls or responsive context.

## Prerequisites

Check only the tools the selected job needs. Do not install globally, change the project toolchain or upload source as a fallback.

```sh
python3 --version
command -v mmdc
command -v rsvg-convert
command -v ffmpeg
command -v ffprobe
command -v drawio
```

Use existing project dependencies first. A temporary local dependency folder is suitable for verification when permitted. Report the exact missing tool and which output it blocks. Preserve native source and provide a text equivalent when a renderer is unavailable. Do not call an unrendered source visually verified.

## Mermaid

The [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) renders locally with a browser dependency. Check its installed version and `mmdc --help`. Typical commands are:

```sh
mmdc -i figure.mmd -o figure.svg -b white
mmdc -i figure.mmd -o figure.png -b white -s 2
```

Use the renderer's Markdown input mode when appropriate, or extract true fenced blocks with a fence-aware parser. Inspect the output filenames before changing links. Keep `.mmd` source when replacing a Markdown fence with an image. Use descriptive alt text and a path relative to the document.

Resolve syntax errors in a small failing example, then restore the full diagram. Recheck semantics after a fallback or grammar change. A remote rendering API is optional only when the user authorizes sending that content there.

## SVG to PNG

```sh
python3 <diagram-skill>/scripts/export_svg.py png figure.svg figure.png --width 1200
```

The helper requires local `rsvg-convert` and accepts a complete static source. It does not capture arbitrary CSS animation or HTML wrappers. For HTML, capture the figure in a local browser after fonts and layout finish. Use an explicit static state for motion.

Check actual dimensions and background. Transparent output can make dark text unreadable on a dark host. Compare at the intended display width rather than only zooming into the full raster.

## GIF and animation

For the bundled semantic highlight pattern, use the explicit plan shown in the motion guide:

```sh
python3 <diagram-skill>/scripts/export_svg.py gif figure.svg figure.gif --plan walk.json --width 1000
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames,duration -of json figure.gif
```

It renders deterministic PNG frames, then uses FFmpeg palette generation and palette application. Check `ffmpeg -h filter=palettegen` and `ffmpeg -h filter=paletteuse` for the installed build. Keep a final still and the step plan. The helper makes a finite, non-looping file. Other animation patterns need their own frame generator and declared timing.

For a large GIF, reduce dimensions, redundant hold frames or frame rate after checking readability. Do not drop meaningful steps. Preview the actual encoded GIF, because palette reduction may erase a distinction that the SVG showed clearly.

## Compression

Work on a copy. Keep the original source and the uncompressed export. Lossless PNG optimization is a good first step if a local optimizer exists. If palette quantization is acceptable:

```sh
pngquant --quality 90-100 --output figure-small.png -- figure.png
```

Check the installed tool's options first. Read its result and compare dimensions, alpha, text edges, gradients and semantic colors. Keep the smaller file only when it is both smaller and still readable. A quality score is not visual evidence.

FFmpeg can also re-encode a PNG losslessly with `ffmpeg -i figure.png -c:v png -compression_level 9 -pred mixed figure-small.png`. Compare decoded pixels and actual file size. This may save little or increase size, so keep it only when the measurement supports it.

JPEG is useful for photographs, but it can damage small diagram text. If optimizing JPEG screenshots, preserve required color profiles and inspect before/after crops. Do not strip all metadata or overwrite every original by default. Measure actual bytes saved. Do not promise a fixed compression percentage or assume all consumers support the same image formats.

## Delivery receipt

Record input revision or hash, source and export paths, command and tool versions, dimensions, background, inspected sizes and remaining limits. For multiple figures, include per-file success and failure. A native editor check, structural check and visual inspection are separate evidence.
