# Visual theming for infographics

Posters and carousels need two color layers: **editorial** (headline, panels, background) and **embedded figures** (Mermaid, technical SVG, charts).

## Editorial layer

1. When the repo has no tokens yet, define surface, on-surface, accent, muted, danger, and chart colors in the visual brief.
2. Map roles to CSS variables or inline SVG fills in the layout source. Do not scatter raw hex outside the token file or theme block.
3. Match shipped design system files when the project provides them.
4. Slide mood words can seed a palette brief. Do not copy unrelated hex tables into the poster.

## Embedded Mermaid or technical figures

1. Complete the technical pass when the figure is topology, not a simple bar chart.
2. For presentation color on Mermaid, use the theme catalog exposed by `export_figure.py themes` when export scripts are installed.
3. Apply themes from this skill:

```sh
python3 <infographic-skill>/scripts/export_figure.py themes
python3 <infographic-skill>/scripts/export_figure.py mermaid-theme IN.mmd OUT.mmd --theme harbor-slate
python3 <infographic-skill>/scripts/export_figure.py mermaid-svg OUT-themed.mmd fig.svg --theme harbor-slate
```

Set `LEVISTACK_DIAGRAM_SCRIPTS` when export scripts live outside the default sibling path.

## Contrast on the composed page

Measure text and panels on the **final** background at export width. Figure theme contrast does not cover headline copy on a tinted poster field. Re-run pair checks on composed roles when both layers use product tokens.

## One accent rule

Keep one dominant accent per view. Technical figure accents should not fight the poster headline color. Prefer muted figure themes inside busy layouts.
