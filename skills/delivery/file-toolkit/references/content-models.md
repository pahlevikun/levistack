# Normalized content models

The JSON templates are valid `create` inputs. Use them directly, changing only
content and task-specific values. Extracted models can be passed back to `create`
when the chosen output supports that model. Metadata warnings do not become body
text. Unknown model features are not silently reconstructed.

- **Document:** `kind: document`, optional `title`, and `paragraphs` as strings.
  Native output supports plain content, not arbitrary rich runs or page layouts.
- **Spreadsheet:** `kind: spreadsheet`, `sheets` with a `name` and either `rows`
  (arrays of scalar values) or `cells` (`cell` in A1 notation and `value`). A string
  starting with `=` is a formula in spreadsheet output. CSV/TSV stores that string
  literally: opening it in another spreadsheet can execute a formula, so review
  untrusted values before distributing. Dense conversion is bounded to 100,000
  cells, 10,000 rows and 1,024 columns.
- **Presentation:** `kind: presentation`, `slides` each with `title` and string
  `paragraphs`. Native PPTX uses simple title/body text boxes. Long text may need
  a smaller font or additional slides; render and inspect it.
- **Image:** `kind: image`, integer `width`/`height` (1–8192), `background`, and
  `shapes`. The closed shape set is `rect` (`x,y,width,height,rx`), `circle`
  (`cx,cy,r`), `line` (`x1,y1,x2,y2`), and `text` (`x,y,font-size,text`). Shapes
  accept `fill` and `stroke`. Colors are three/six-digit hex, `none` or
  `transparent`. Coordinates are finite numbers. No embedded resources or scripts.
- **Audio:** `kind: audio`, `duration_seconds` (greater than zero, at most 60),
  `sample_rate` (8000–96000), `frequency_hz` (zero for silence, below Nyquist), and
  `amplitude` (0–1). It creates mono, signed 16-bit PCM before optional transcoding.
  This is a test tone, not voice or music generation.

Preserve a copy of the original file and inspect which features it contains before
recreating it. For example, a parsed workbook with external links and cached values
cannot safely become an equivalent workbook through this simple model. Report
those features and use a suitable native editor instead.
