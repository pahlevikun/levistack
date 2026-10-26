# Wiki and Confluence

Publish diagrams when the host does not run Mermaid in the reader's browser.

## GitHub wiki or GitHub-flavored Markdown

1. Write Mermaid in a `.mmd` file or a fence in the wiki page.
2. Render PNG or SVG with `scripts/mermaid_render.py` or the batch export guide in `SKILL.md`.
3. On a white wiki background, use a high-contrast theme (`audit-highvis`, `wiki-contrast`).
4. Embed `![alt](path.png)` in the wiki page. Keep the `.mmd` in the repo for edits.

Animated GIF on a wiki is rarely worth the size. Use static PNG unless the user asks for motion.

## Confluence

Many spaces block live Mermaid. Default path:

1. Export PNG and SVG.
2. Attach both. Use SVG when Confluence allows vector attach.
3. Put the Mermaid source in a collapsible code block or a linked repo file for maintainers.

Note in the receipt that Confluence may recompress images.

## Batch pages

For many blocks in one Markdown file, use `mermaid_blocks_cli.py` and `mermaid_remote_png.py` or themed `mermaid_render.py` per block. One failure must not block the rest.
