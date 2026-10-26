# Visual type atlas

Map a chart or map type to notation, density rules, and handoffs. This skill owns technical truth and editable source. Multi-panel editorial layout usually moves to `infographic`.

## How to use

1. Find the type in the table.
2. Follow the primary notation column.
3. When the handoff column names another skill, pass source, evidence ledger, and exports.

Aim for **4–10 nodes** per figure when you can. Split when the table says "split view".

## Types (selected)

| Type | Primary notation | Handoff or note |
|---|---|---|
| Flowchart, process | Mermaid flowchart | none |
| Sequence, API | Mermaid sequence | none |
| State machine | Mermaid state | none |
| ER, data model | Mermaid ER or schema guide | none |
| Deployment, C4-like | Mermaid flowchart subgraphs | Label the abstraction level |
| Architecture delta | Two figures or titled proposed view | Evidence per version |
| Swimlane | Mermaid flowchart with subgraph lanes | none |
| Timeline, Gantt | Mermaid gantt | Check host support |
| Quadrant, matrix | SVG or HTML figure | `infographic` for poster |
| Wardley map | SVG or HTML | `infographic`, strategic labels only |
| User journey, service blueprint | SVG lanes plus HTML | `infographic` |
| Sankey, waterfall, treemap | SVG or `infographic` data JSON | `infographic` |
| Org chart, tree | Mermaid flowchart TB or SVG | none |
| Layer stack, governance | SVG stack | `design-system-kit` for tokens |
| Fishbone, Ishikawa | Mermaid or SVG | Causal labels must be sourced |
| Kanban | Table or simple SVG columns | Not a full board product |
| Heatmap, scatter, bubble | Mermaid xychart when supported, else SVG | Sourced data only |
| Story map | HTML grid | `infographic` |
| Medallion, data flow | Mermaid or SVG | Pipeline evidence |
| Branded poster, carousel | Layout composition | `infographic` |

For types not listed, use Mermaid when the grammar fits. Otherwise use SVG with semantic groups from the SVG motion guide in `SKILL.md`.

## Wardley, journey, blueprint

These need narrative spacing and brand roles. Start with a brief list of stages or capabilities. Build a low-density SVG or HTML scaffold. Run `color-kit` when colors are not tokenized yet. Hand to `infographic` when the deliverable is a multi-panel story.

## Density rule

When the user wants more than nine labeled nodes in one view, propose an overview plus a detail figure. Record the split in the receipt.
