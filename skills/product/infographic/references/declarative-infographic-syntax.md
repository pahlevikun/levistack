# Declarative infographic syntax (optional)

Some renderers accept a small text DSL: a template line, a `data` block, and an optional `theme` block. This skill does not bundle a renderer. Use this path only when the user already installed one locally.

## When to use

- User supplies a template name and asks for DSL output.
- Structured lists, sequences, comparisons, hierarchies, or simple charts already live in [structured content](structured-content.md).
- Facts are locked in the evidence ledger before export.

Prefer SVG or HTML from the evidence track when no renderer is installed.

## Shape of a file

1. First line: `infographic <template-name>` from the renderer's template list.
2. `data` block with two-space indent: title, description, and one primary collection (`lists`, `sequences`, `compares`, `root`, `values`, etc.).
3. Optional `theme` block: palette colors, fonts, stylize flags.

Do not mix conflicting data shapes. Binary compare templates need two roots. Hierarchy templates use a single `root` tree.

## Mapping from structured content

| Structured content | Typical data field |
|---|---|
| Section list with icons | `lists` on a list-style template |
| Ordered steps | `sequences` with optional `order asc` |
| Side-by-side options | `compares` on a compare-style template |
| Org or taxonomy | `root` / `children` on a hierarchy template |
| Numeric series | `values` on a chart-style template |

Translate labels from the ledger verbatim. Run contrast checks on public theme colors at delivery size.

## Output hygiene

- Emit DSL only in a file the user asked for.
- Keep a copy in `exports/` with the receipt.
- If rendering fails, fix data shape before restyling.
