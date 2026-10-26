# Mermaid to animated GIF (browser capture)

Use this when the deliverable is a looping or one-shot GIF built straight from Mermaid source, with motion that fits the diagram.

You need network at render time (Mermaid.js from a CDN), Playwright with Chromium, and FFmpeg.

If you already have a trusted static SVG, want offline export, or need explicit step IDs, use the SVG walk in `references/svg-motion.md` and `scripts/export_svg.py gif` instead.

## Prerequisites

```sh
python3 --version
pip install playwright && playwright install chromium
ffmpeg -version
```

Pass `--allow-network` on the helper. Note CDN use in the receipt.

## Motion styles

| Style | What it does | Good for |
|---|---|---|
| `progressive` | Whole diagram stays visible. Parts brighten in order. Edges draw in. | Layers, sequences in order |
| `highlight-walk` | A spotlight moves. Visited parts stay bright. | Tutorials, step lists |
| `pulse-flow` | Dashed lines move along edges | Pipelines, data flow |
| `wave` | A brightness ripple moves across parts | Simple overviews, light motion |

Read the text around each block before you batch. A pipeline paragraph fits `pulse-flow`. A layered stack fits `progressive`. Re-run one block with another style when one file mixes different intents.

## Commands

Style drivers live in `scripts/mermaid_playwright_styles.py`. Block parsing lives in `scripts/mermaid_blocks.py`.

```sh
python3 <diagram-skill>/scripts/mermaid_playwright_gif.py figure.mmd -o ./gifs/ \
  --style progressive --allow-network

python3 <diagram-skill>/scripts/mermaid_playwright_gif.py article.md -o ./gifs/ \
  --style highlight-walk --fps 12 --duration 5 --no-loop --allow-network
```

If the GIF file grows too large, lower `--scale`, `--fps`, or `--duration`. Open the GIF and check thin strokes. Palette reduction can erase detail.

## Limits

- Untrusted Mermaid stays untrusted. Review labels and links before browser render.
- The bundled page uses strict Mermaid security. Odd click handlers may not run.
- This path does not honor `prefers-reduced-motion`. Ship a still PNG or SVG for accessibility.
- When the source is already SVG with known IDs, compare with `export_svg.py gif`.
