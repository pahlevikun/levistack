# Role inventory: <product>

Fill this for an existing product before you change a color. One row per color that survives the audit.

| Color found | Uses | Role it plays today | Role it should play | Token to use | Action |
|---|---:|---|---|---|---|
| `#3366FF` | 41 | button fill, link, selected tab | primary, link | `primary`, `link` | keep. Split link into its own step |
| `#3467FF` | 6 | button fill | primary | `primary` | merge into `#3366FF` |
| `#F4F4F5` | 29 | card ground | surface | `surface` | keep |
| `#D1D5DB` | 18 | input edge and divider | border and border-strong | both | split. The edge fails 3:1 |

## Notes

- A color that plays no role is a missing token or a mistake. Say which.
- Count the ramps. More ramps than neutral, one accent and the status colors in use means the palette outgrew its structure.
- Do not average duplicates. Keep the most used one.
- This table is a proposal. Do not rewrite colors in the product until the user accepts it.
