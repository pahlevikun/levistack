# Project artifacts

Keep working files next to the deliverable, not inside the installed skill package.

## Suggested tree

```
{project}/{topic-slug}/
├── source/                 # inputs, exports from research
├── analysis.md             # optional: messy source triage
├── structured-content.md   # see structured-content guide
├── design-specification.md # office-style spec when needed
├── visual-brief.md         # from template when used
├── prompts/                # raster draft track only
│   └── {surface}-{slug}.md
└── exports/
    ├── figure.svg
    ├── figure.png
    └── receipt.md
```

**Slug:** two to four words, kebab-case from the topic. If the folder exists, append `-YYYYMMDD-HHMMSS`.

## Backup rule

Before overwriting `analysis.md`, a prompt file, or a raster export, rename the prior file with a `-backup-YYYYMMDD-HHMMSS` suffix.

## Receipt

List layout id, mood id, aspect ratio, tools run, dimensions, and checks not run. Pair with the evidence ledger from [evidence](evidence.md).
