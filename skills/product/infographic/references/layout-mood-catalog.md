# Layout and mood catalog

Use this catalog when the user wants a mood board, keyword-driven layout, or raster draft track. For office-style statistical posters, still start from [layout types](layout-types.md).

Load keyword hints from [../data/layout-keywords.json](../data/layout-keywords.json). When a keyword matches, lead with that layout and mood list. Otherwise infer from data shape and audience.

## Layouts

| Id | Best for |
|---|---|
| `tile-board` | Several topics on one canvas, overview |
| `lane-timeline` | Dates, history, ordered change |
| `split-binary` | A vs B, before and after, pros and cons |
| `matrix-compare` | Many factors across options |
| `layer-stack` | Priority tiers, pyramid, iceberg |
| `branch-tree` | Categories, taxonomy |
| `hub-rays` | One idea with related spokes |
| `cutaway` | Parts inside a whole, exploded view |
| `metric-panel` | KPIs, dashboard feel |
| `funnel-path` | Stages that narrow |
| `cycle-ring` | Repeating process |
| `overlap-sets` | Shared and distinct concepts |
| `road-milestones` | Journey with turns |
| `comic-beats` | Short story beats |
| `module-dense` | High density how-to or product map |

Default layout when nothing fits: `tile-board`.

## Moods (visual tone)

| Id | Reader feel |
|---|---|
| `editorial-clean` | Calm grid, generous space |
| `paper-sketch` | Hand note, craft paper |
| `chalk-classroom` | Dark board, teaching tone |
| `schematic-blue` | Engineering print, precise lines |
| `flat-brand` | Flat color, marketing clarity |
| `watercolor-story` | Soft paint, narrative |
| `neon-night` | High contrast glow |
| `vintage-print` | Aged paper, serif accents |
| `wireframe-draft` | Grayscale structure only |
| `knoll-flatlay` | Organized objects from above |

Default mood for drafts: `editorial-clean`. Use project palette tokens for measured contrast.

## Suggested pairs

| Content shape | Layout + mood |
|---|---|
| Timeline | `lane-timeline` + `paper-sketch` |
| Steps | `lane-timeline` + `schematic-blue` |
| Two-sided debate | `split-binary` + `flat-brand` |
| Tier list | `layer-stack` + `paper-sketch` |
| Overlap | `overlap-sets` + `editorial-clean` |
| Funnel metrics | `funnel-path` + `flat-brand` |
| Cycle | `cycle-ring` + `paper-sketch` |
| Technical parts | `cutaway` + `schematic-blue` |
| KPI story | `metric-panel` + `flat-brand` |
| Classroom explainer | `tile-board` + `chalk-classroom` |
| Journey | `road-milestones` + `watercolor-story` |
| Dense guide | `module-dense` + `editorial-clean` or `vintage-print` |

## Aspect presets

| Name | Ratio | Typical use |
|---|---|---|
| `landscape-wide` | 16:9 | Decks, YouTube thumb |
| `portrait-tall` | 9:16 | Stories, mobile scroll |
| `square` | 1:1 | Feed tile |
| `print-poster` | 3:4 or 2:3 | Print shop |
| `cinema` | 2.35:1 | Wide hero |

Custom ratios are allowed when the user names width and height. Record the choice in the receipt.

## Map to composition patterns

| Catalog layout | See also in [composition](composition.md) |
|---|---|
| `split-binary`, `matrix-compare` | Comparison lanes |
| `lane-timeline`, `road-milestones` | Timeline |
| `hub-rays`, `branch-tree` | Network or hierarchy |
| `metric-panel` | Statistical panels |
