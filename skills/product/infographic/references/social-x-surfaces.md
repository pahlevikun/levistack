# Social X surfaces

Package infographics for X (Twitter): single image posts, multi-image threads, quote posts, and long articles.

## Surface types

| Type | Assets | Copy |
|---|---|---|
| Single image post | One PNG or JPG at checked dimensions | Short hook plus caveat line if needed |
| Multi-image | Ordered frames from carousel export | Number thread intent in draft |
| Quote post | New image or reuse plus comment | Comment must stand alone |
| X Article | Markdown body, cover image, inline figures | Run publishing gate on HTML or MD pipeline |

Always verify current image count and size limits via [formats](formats.md) or platform docs before delivery.

## Workflow

1. Recompose each frame for X width. Do not stretch a tall poster without reflow ([formats](formats.md)).
2. Write alt text from the bounded claim, not from decorative detail alone.
3. Prepare copy in a local draft file. Keep numbers and citations exact when editing prose.
4. Run [publishing gate](publishing-gate.md) on the exact scheduler payload.
5. **Do not click Post or Publish** without explicit user confirmation in the current thread.

## Browser automation

If the user asks to post through a browser, prefer their stated tool (extension, computer use, or script). Never mix accounts. Never publish on their behalf silently.

For articles with local images, upload through the editor flow the user chooses. Map placeholders to files in the receipt.

## Relation to other guides

- Rights and attribution: [publication boundaries](publication-boundaries.md).
- Raster hero for the article: [cover hero surfaces](cover-hero-surfaces.md).
- Keyword layout hints: [layout mood catalog](layout-mood-catalog.md) plus [../data/layout-keywords.json](../data/layout-keywords.json).
