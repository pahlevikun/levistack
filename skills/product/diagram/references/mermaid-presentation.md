# Mermaid presentation

Make Mermaid readable on docs, wikis, slides, and terminals. This is not `color-kit`. Use `color-kit` to build product tokens, then map roles into a theme when the user wants brand colors.

## Theme catalog

This skill ships **48** presentation themes in `data/mermaid-themes.json`. Ids and hex are levistack-owned. Some rows share mood with familiar editor palettes but are renamed and retuned. See [mermaid theme lineage](mermaid-theme-lineage.md).

```sh
python3 <diagram-skill>/scripts/mermaid_themes.py --list
python3 <diagram-skill>/scripts/mermaid_themes.py --list --json
python3 <diagram-skill>/scripts/mermaid_themes.py --theme harbor-slate --input fig.mmd --output fig-themed.mmd
python3 <diagram-skill>/scripts/mermaid_render.py fig-themed.mmd fig.svg --theme harbor-slate
```

Each theme has `mode` (light or dark), optional `family` and `tags`, and `high_contrast` when set. Optional `terminal_pairing` selects a beautiful-mermaid CLI theme for terminal output only.

### Pick a theme

| Surface | Starting themes |
|---|---|
| Light README | `paper-archive`, `inkwell`, `porcelain`, `patchwork-light` |
| Dark README or slides | `harbor-slate`, `afterhours-code`, `deep-stack`, `night-shift` |
| IDE-adjacent dark | `storm-dock`, `mocha-workbench`, `atom-bench`, `vault-dracula` |
| Ice / calm light | `nordic-frost`, `arctic-sheet`, `harbor-mist` |
| Warm editorial | `desert-shelf`, `golden-platform`, `sunset-minutes` |
| Nature / brand accent | `canopy-trail`, `conservatory`, `dusty-rosebud` |
| Print or PDF | `press-ready`, `print-room`, `sepia-stack` |
| Wiki with strict contrast | `wiki-contrast`, `audit-highvis`, `ballot-ink` |
| Terminal-style preview | `terminal-phosphor` (pairs with `zinc-dark` in terminal CLI) |
| Blueprint tone | `blueprint-draft` |
| Cosmic slides | `galaxy-well`, `orbit-lab` |

When the project has `color-kit` output, map roles with `mermaid_themes.merge_project_tokens` in code, or hand-map `surface`, `on-surface`, `accent`, `muted`, and `background` into the init block. Re-run `color-kit` contrast proof on the rendered PNG.

### Add or tune themes

Add a row to `data/mermaid-themes.json` with a new `id` and `themeVariables`. Run `python3 -m unittest discover -s scripts -p 'test_mermaid*.py'`. When you tune fills, prefer OKLCH-style lightness steps (see `color-expert`). Do not put raw hex in app UI code outside theme files.

## High contrast

Themes with `high_contrast: true` use strong text and edge separation. They help, but they do not replace measured contrast from `color-kit`. After render, inspect the PNG at final width.

## XY charts and interactive Mermaid

When the user needs `xychart-beta` or chart tooltips:

1. Confirm the installed Mermaid version supports the grammar.
2. Author in a standalone `.mmd`. Render to SVG first.
3. Enable hover tooltips only when the host supports interactive SVG and the user asked for them. Export static PNG for wikis.

## Terminal output

```sh
python3 <diagram-skill>/scripts/mermaid_terminal.py diagram.mmd -o diagram.txt --allow-network
python3 <diagram-skill>/scripts/mermaid_terminal.py diagram.mmd -o diagram.txt --ascii --allow-network
```

Needs `npx beautiful-mermaid` unless a local `beautiful-mermaid` binary exists. Optional `--theme` injects a levistack init block before render.

## Motion

Themed static export is separate from Playwright Mermaid GIF and from SVG walk GIF in the export guide (`SKILL.md`).
