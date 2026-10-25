#!/usr/bin/env python3
"""Write a sourced, zero-baseline bar figure. Preserve the JSON as editable data."""

import argparse
import json
import math
from pathlib import Path
import sys
import textwrap
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def build(data):
    for key in ("title", "unit", "period", "source"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    rows = data.get("data", [])
    if not isinstance(rows, list) or not 1 <= len(rows) <= 12:
        raise ValueError("data must contain 1 through 12 comparable rows")
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("label"), str) or not row["label"].strip():
            raise ValueError("each row needs a label")
        value = row.get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError("values must be finite and nonnegative. Use another chart for signed data")
    maximum = data.get("scale_max", max(row["value"] for row in rows) or 1)
    if isinstance(maximum, bool) or not isinstance(maximum, (int, float)) or not math.isfinite(maximum) or maximum <= 0 or maximum < max(r["value"] for r in rows):
        raise ValueError("scale_max must be positive, finite and cover every value")
    if "synthetic" in data and not isinstance(data["synthetic"], bool):
        raise ValueError("synthetic must be a boolean")
    if any(len(str(row["value"])) > 6 for row in rows) or len(str(maximum)) > 6:
        raise ValueError("numeric labels exceed six characters. Convert to explicit display units or use a custom layout")
    title_lines = textwrap.wrap(data["title"], 24)
    if len(title_lines) > 3 or any(len(r["label"]) > 24 for r in rows):
        raise ValueError("shorten the title to three lines and row labels to 24 characters")
    source_lines = textwrap.wrap("Source: " + data["source"], 48)
    if len(source_lines) > 10 or len(data["unit"]) > 30 or len(data["period"]) > 60:
        raise ValueError("shorten the source line, unit or period. Keep full detail in the ledger")
    detail_lines = textwrap.wrap(f"{data['unit']} | {data['period']}", 42)
    detail_top = 140 + (len(title_lines) - 1) * 48
    chart_top = detail_top + len(detail_lines) * 30 + 20
    footer_top = chart_top + len(rows) * 72 + 54
    height = footer_top + len(source_lines) * 24 + 75
    root = ET.Element(f"{{{NS}}}svg", {"viewBox": f"0 0 1200 {height}", "role": "img", "aria-labelledby": "bars-title bars-desc"})
    ET.SubElement(root, f"{{{NS}}}title", {"id": "bars-title"}).text = data["title"]
    description = f"{data['period']}. Unit: {data['unit']}. Zero baseline, maximum {maximum}. "
    description += " ".join(f"{r['label']}: {r['value']}." for r in rows)
    description += " Source: " + data["source"]
    if data.get("synthetic"):
        description = "Synthetic example, not observed data. " + description
    ET.SubElement(root, f"{{{NS}}}desc", {"id": "bars-desc"}).text = description
    ET.SubElement(root, f"{{{NS}}}rect", {"width": "1200", "height": str(height), "fill": "#ffffff"})

    def text(x, y, value, size=24, weight="400", anchor="start"):
        ET.SubElement(root, f"{{{NS}}}text", {"x": str(x), "y": str(y), "font-family": "Arial, sans-serif", "font-size": str(size), "font-weight": weight, "fill": "#17212b", "text-anchor": anchor}).text = value

    if data.get("synthetic"):
        text(60, 45, "SYNTHETIC EXAMPLE, NOT OBSERVED DATA", 20, "700")
    for index, line in enumerate(title_lines):
        text(60, 100 + index * 48, line, 42, "700")
    for index, line in enumerate(detail_lines):
        text(60, detail_top + index * 30, line)
    for index, row in enumerate(rows):
        y = chart_top + index * 72
        for line_index, line in enumerate(textwrap.wrap(row["label"], 12)):
            text(60, y + 22 + line_index * 27, line, 25)
        width = row["value"] / maximum * 630
        ET.SubElement(root, f"{{{NS}}}rect", {"id": f"bar-{index}", "x": "420", "y": str(y), "width": f"{width:.6f}", "height": "40", "fill": "#214f78"})
        text(1140, y + 30, str(row["value"]), 25, "700", "end")
    ET.SubElement(root, f"{{{NS}}}line", {"x1": "420", "x2": "1050", "y1": str(footer_top - 35), "y2": str(footer_top - 35), "stroke": "#17212b"})
    text(420, footer_top - 5, "0", 20)
    text(1000, footer_top - 5, str(maximum), 20)
    for index, line in enumerate(source_lines):
        text(60, footer_top + 45 + index * 24, line, 21)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        result = build(json.loads(Path(args.input).read_text()))
        with Path(args.output).open("xb") as stream:
            stream.write(result)
        print(f"wrote {args.output}. Render and inspect at the delivery size")
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"render_bars: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
