# Honest data graphics

Pick the chart for the comparison. Keep the data and transformation script with the editable artifact.

## Encode values

Bars compare magnitude with a common zero baseline. Use position or length when precise comparison matters. Lines show ordered change across a real continuous or temporal axis. Dots and distributions help show spread. Use small multiples for several comparable series.

Area and volume are harder to compare. If area encodes value, compute the area, not a radius or diameter proportional to the value. Do not use a decorative bubble, funnel, Sankey band or map region as a measured mark without a real quantity and scale.

For a timeline, space dates proportionally or label a categorical sequence explicitly. Mark uncertain ranges. For a network, define edge meaning and avoid implying causal or geographic distance through arbitrary placement.

State units, population, denominator and period near the graphic. Directly label where possible. Use one source-supported annotation for the main finding rather than adding visual effects to every mark.

## Check comparisons

- Use the same unit, period, population and axis treatment across comparable panels.
- Show a zero baseline for bars. If a different chart needs a truncated axis, mark it clearly and explain why it fits the question.
- Do not connect unrelated categories with a trend line.
- Distinguish zero from missing, suppressed or not applicable.
- Preserve uncertainty intervals and sample sizes where available. Never invent them.
- Recompute totals and percentage changes. Check filtering, ranking, ties and rounding.
- Explain indexes and normalized values. A chart of relative signal cannot silently become a chart of absolute prevalence.
- Use hue for category, ordered lightness for magnitude and a meaningful midpoint for divergence. Use measured palette decisions from project tokens. Keep direct labels or patterns as another cue.

## Narrow runnable example

`scripts/render_bars.py` accepts comparable nonnegative values and writes an editable accessible SVG. It rejects empty data, nonfinite values, negative values, a scale that clips the data and missing provenance. It includes a text data table in `<desc>`.

```json
{
  "title": "Fictional requests by stage",
  "unit": "requests",
  "period": "Synthetic example",
  "source": "Synthetic fixture, not observed data",
  "synthetic": true,
  "scale_max": 100,
  "data": [
    {"label": "Submitted", "value": 100},
    {"label": "Accepted", "value": 75},
    {"label": "Rejected", "value": 25}
  ]
}
```

```sh
python3 <infographic-skill>/scripts/render_bars.py chart.json chart.svg
```

The helper is a starting point for one chart family. Numeric labels are limited to six characters so they fit without silently rounding values. Convert to explicit display units or use a custom layout when values need more room. It cannot verify that a supplied citation is true or that categories are comparable. Inspect the source before running it. Use a custom chart or the project's plotting library for signed values, time series, uncertainty, maps and interactive analysis.

Render and inspect the SVG at its expected display size. Local raster tools can export PNG when installed. The existence of a valid file is not proof that the figure communicates the right claim.
