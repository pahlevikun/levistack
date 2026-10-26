# Mermaid theme lineage

Two related systems. Do not mix their ids.

## Levistack catalog (`data/mermaid-themes.json`)

- **Renderer:** `mmdc` (and anything that honors Mermaid `init` blocks).
- **Shape:** `base` theme + `themeVariables` (fills, text, lines).
- **Count:** run `python3 scripts/mermaid_themes.py --list`.
- **Ownership:** levistack ids (`harbor-slate`, `afterhours-code`, …) and hex sets. Not upstream pack names.

We may take **ideas** from public palette families (ice blue, warm solar paper, vivid dark slides, link-blue product docs). We **do not** ship third-party theme ids or verbatim hex tables from pretty-mermaid-skills or other repos.

## beautiful-mermaid (terminal and optional SVG CLI)

- **Renderer:** `npx beautiful-mermaid` (`mermaid_terminal.py`).
- **Shape:** 15 named themes (`tokyo-night`, `nord`, `zinc-light`, …) defined inside that npm package.
- **Link:** when a catalog row has `terminal_pairing`, `--theme <levistack-id>` passes that name to beautiful-mermaid **and** injects the levistack init block for any other tool that reads the `.mmd` file.

## color-kit and theme-factory

- **color-kit:** source of truth for product roles and measured contrast. Map into `themeVariables` or regenerate a catalog row from a brief.
- **theme-factory:** mood words for slides (ocean, desert, galaxy, …). Use them in a `color-kit` brief or pick a catalog `family` / `tags` match. Do not copy slide hex tables into the repo.

## Add a theme

1. Pick a new `id` and `label` (levistack voice, not upstream id).
2. Set `mode`, `family`, optional `tags`, optional `terminal_pairing` from the allowed 15 CLI names.
3. Tune `themeVariables`. Prefer OKLCH-minded lightness steps (`color-expert`).
4. Run `python3 -m unittest discover -s scripts -p 'test_mermaid*.py'`.
5. Add a row to the pick table in [mermaid presentation](mermaid-presentation.md) when the theme is a common default.
