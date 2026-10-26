# Mermaid batches for publishing

Use this when the site does not draw Mermaid, or when readers need PNG files next to the text.

## Pick a renderer

| Situation | What to use |
|---|---|
| Normal case, keep work on your machine | Local [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) (`mmdc`). See the export guide from `SKILL.md`. |
| No `mmdc`, and the user OKs sending source off the machine | `scripts/mermaid_remote_png.py --backend ink --allow-remote` |
| Many diagrams in one Markdown file | `scripts/mermaid_blocks_cli.py`, then render each manifest row |

Keep a `.mmd` copy when you swap a fence for an image. Use clear file names and alt text. Match how the repo already links images (relative or absolute).

## List blocks and write a manifest

```sh
python3 <diagram-skill>/scripts/mermaid_blocks_cli.py path/to/doc.md --manifest /tmp/doc-mermaid.json
```

The manifest holds the block index, name, line number, and source text. One bad block does not stop the rest.

## Local PNG batch

```sh
python3 <diagram-skill>/scripts/mermaid_remote_png.py README.md -o ./images/ --backend mmdc --scale 2
```

You need `mmdc` on PATH. The script will not overwrite an existing PNG.

## Remote PNG (opt in only)

Run this only after the user agrees to send diagram text to a public render service:

```sh
python3 <diagram-skill>/scripts/mermaid_remote_png.py docs/flow.md -o ./images/ \
  --backend ink --allow-remote --bg white
```

Say in the receipt that content left the machine. If the service times out, split the diagram or try `mmdc`.

## Replace fences in Markdown

1. Write PNGs into the project image folder (`images/` or whatever the repo uses).
2. Replace each ` ```mermaid ` fence with `![short title](relative/path.png)` only when the user asked for static publish assets.
3. Report how many blocks you rendered, which paths you wrote, which files you edited, and which blocks you skipped.

A mermaid fence inside a literal code example is not a live diagram. Use the block helper or a fence-aware pass. Do not treat inner fences as runnable.
