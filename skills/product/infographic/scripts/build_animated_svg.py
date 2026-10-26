#!/usr/bin/env python3
"""Build a sequenced infographic as one self-contained CSS-animated SVG."""

from __future__ import annotations

import argparse
import json
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

TITLE_HOLD = 1.0
STEP_STRIDE = 1.55
ICON_LEAD = 0.0
VALUE_LEAD = 0.22
LABEL_LEAD = 0.45
CONNECTOR_LEAD = 0.85


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def validate(data: dict) -> None:
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError("title must be a nonempty string")
    if not isinstance(data.get("source"), str) or not data["source"].strip():
        raise ValueError("source must be a nonempty string")
    steps = data.get("steps")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 5:
        raise ValueError("steps must contain 1 through 5 items")
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            raise ValueError(f"step {index} must be an object")
        for key in ("glyph", "value_display", "label"):
            if not isinstance(step.get(key), str) or not step[key].strip():
                raise ValueError(f"step {index} needs {key}")
        if len(step["label"]) > 48:
            raise ValueError(f"step {index} label too long (48 max)")
        if len(step["value_display"]) > 16:
            raise ValueError(f"step {index} value_display too long (16 max)")
    if "synthetic" in data and not isinstance(data["synthetic"], bool):
        raise ValueError("synthetic must be a boolean when present")


def theme_defaults(data: dict) -> dict[str, str]:
    raw = data.get("theme") if isinstance(data.get("theme"), dict) else {}
    return {
        "background": str(raw.get("background", "#0f1419")),
        "ink": str(raw.get("ink", "#f4f7fb")),
        "muted": str(raw.get("muted", "#9aa4b2")),
        "accent": str(raw.get("accent", "#5b8def")),
        "line": str(raw.get("line", "#3a4250")),
    }


def total_duration(data: dict, n: int) -> float:
    hold = float(data.get("hold_seconds", 2.5))
    custom = data.get("duration_seconds")
    if custom is not None:
        return float(custom)
    return TITLE_HOLD + n * STEP_STRIDE + hold


def build(data: dict) -> ET.ElementTree:
    validate(data)
    width = int(data.get("width", 1200))
    height = int(data.get("height", 675))
    if not 400 <= width <= 2400 or not 300 <= height <= 2400:
        raise ValueError("width and height out of supported range")
    steps = data["steps"]
    theme = theme_defaults(data)
    duration = total_duration(data, len(steps))
    title_lines = textwrap.wrap(data["title"], 42)
    if len(title_lines) > 2:
        raise ValueError("shorten title to two lines at this width")

    root = ET.Element(
        f"{{{NS}}}svg",
        {
            "viewBox": f"0 0 {width} {height}",
            "width": str(width),
            "height": str(height),
            "role": "img",
            "aria-labelledby": "seq-title seq-desc",
        },
    )
    defs = ET.SubElement(root, f"{{{NS}}}defs")
    style = ET.SubElement(defs, f"{{{NS}}}style")
    style.text = _css(duration, len(steps))

    ET.SubElement(root, f"{{{NS}}}title", {"id": "seq-title"}).text = data["title"]
    desc = ET.SubElement(root, f"{{{NS}}}desc", {"id": "seq-desc"})
    desc.text = f"{data['title']}. Source: {data['source']}"

    ET.SubElement(
        root,
        f"{{{NS}}}rect",
        {"width": str(width), "height": str(height), "fill": theme["background"]},
    )

    title_y = 72 + (len(title_lines) - 1) * 8
    title_g = ET.SubElement(root, f"{{{NS}}}g", {"class": "seq-title"})
    for i, line in enumerate(title_lines):
        ET.SubElement(
            title_g,
            f"{{{NS}}}text",
            {
                "x": str(width // 2),
                "y": str(title_y + i * 52),
                "text-anchor": "middle",
                "fill": theme["ink"],
                "font-size": "44",
                "font-weight": "700",
                "font-family": "system-ui, sans-serif",
            },
        ).text = line

    n = len(steps)
    margin = 80
    gap = 40
    usable = width - 2 * margin - gap * (n - 1)
    col_w = usable / n
    row_top = height * 0.42

    for i, step in enumerate(steps):
        cx = margin + col_w * (i + 0.5)
        base = TITLE_HOLD + i * STEP_STRIDE
        group = ET.SubElement(root, f"{{{NS}}}g", {"class": f"seq-step seq-step-{i + 1}"})

        icon = ET.SubElement(
            group,
            f"{{{NS}}}g",
            {
                "class": "seq-icon",
                "style": f"animation-delay:{base + ICON_LEAD:.3f}s",
            },
        )
        ET.SubElement(
            icon,
            f"{{{NS}}}rect",
            {
                "x": str(cx - 48),
                "y": str(row_top - 48),
                "width": "96",
                "height": "96",
                "rx": "22",
                "fill": theme["accent"],
                "fill-opacity": "0.18",
                "stroke": theme["accent"],
                "stroke-width": "2",
            },
        )
        ET.SubElement(
            icon,
            f"{{{NS}}}text",
            {
                "x": str(cx),
                "y": str(row_top + 10),
                "text-anchor": "middle",
                "fill": theme["accent"],
                "font-size": "36",
                "font-weight": "700",
                "font-family": "system-ui, sans-serif",
            },
        ).text = step["glyph"][:1]

        val = ET.SubElement(
            group,
            f"{{{NS}}}text",
            {
                "class": "seq-value",
                "style": f"animation-delay:{base + VALUE_LEAD:.3f}s",
                "x": str(cx),
                "y": str(row_top + 88),
                "text-anchor": "middle",
                "fill": theme["ink"],
                "font-size": "48",
                "font-weight": "800",
                "font-family": "ui-monospace, monospace",
            },
        )
        val.text = step["value_display"]

        lbl = ET.SubElement(
            group,
            f"{{{NS}}}text",
            {
                "class": "seq-label",
                "style": f"animation-delay:{base + LABEL_LEAD:.3f}s",
                "x": str(cx),
                "y": str(row_top + 132),
                "text-anchor": "middle",
                "fill": theme["muted"],
                "font-size": "20",
                "font-family": "system-ui, sans-serif",
            },
        )
        lbl.text = step["label"]

        if i < n - 1:
            x1 = cx + col_w * 0.35
            x2 = cx + col_w * 0.35 + gap + col_w * 0.3
            mid_y = row_top
            conn = ET.SubElement(
                root,
                f"{{{NS}}}g",
                {
                    "class": "seq-connector",
                    "style": f"animation-delay:{base + CONNECTOR_LEAD:.3f}s",
                },
            )
            ET.SubElement(
                conn,
                f"{{{NS}}}path",
                {
                    "d": f"M{x1:.1f},{mid_y:.1f} H{x2:.1f}",
                    "fill": "none",
                    "stroke": theme["line"],
                    "stroke-width": "3",
                    "stroke-linecap": "round",
                    "pathLength": "100",
                },
            )
            ET.SubElement(
                conn,
                f"{{{NS}}}path",
                {
                    "d": f"M{x2 - 10:.1f},{mid_y - 8:.1f} L{x2:.1f},{mid_y:.1f} L{x2 - 10:.1f},{mid_y + 8:.1f}",
                    "fill": "none",
                    "stroke": theme["line"],
                    "stroke-width": "3",
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "class": "seq-arrow",
                    "style": f"animation-delay:{base + CONNECTOR_LEAD + 0.18:.3f}s",
                },
            )

    foot = data["source"]
    if data.get("synthetic"):
        foot = f"Synthetic demo. {foot}"
    ET.SubElement(
        root,
        f"{{{NS}}}text",
        {
            "x": str(margin),
            "y": str(height - 36),
            "fill": theme["muted"],
            "font-size": "14",
            "font-family": "system-ui, sans-serif",
        },
    ).text = foot[:120]

    return ET.ElementTree(root)


def _css(duration: float, step_count: int) -> str:
    pop = 0.55
    fade = 0.4
    draw = 0.45
    d = max(duration, 3.0)
    return f"""
.seq-title {{ opacity: 0; transform: translateY(14px); animation: seq-fade-rise {fade:.2f}s ease-out {TITLE_HOLD * 0.2:.2f}s forwards; }}
.seq-icon {{ opacity: 0; transform: scale(0.6); transform-box: fill-box; transform-origin: center; animation: seq-pop {pop:.2f}s cubic-bezier(0.34, 1.4, 0.64, 1) forwards; }}
.seq-value, .seq-label {{ opacity: 0; transform: translateY(10px); animation: seq-fade-rise {fade:.2f}s ease-out forwards; }}
.seq-connector path:first-child {{
  stroke-dasharray: 100; stroke-dashoffset: 100;
  animation: seq-draw {draw:.2f}s ease-out forwards;
}}
.seq-arrow {{ opacity: 0; animation: seq-fade-in 0.2s ease-out forwards; }}
@keyframes seq-fade-rise {{
  from {{ opacity: 0; transform: translateY(14px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes seq-pop {{
  0% {{ opacity: 0; transform: scale(0.5); }}
  70% {{ opacity: 1; transform: scale(1.08); }}
  100% {{ opacity: 1; transform: scale(1); }}
}}
@keyframes seq-draw {{
  to {{ stroke-dashoffset: 0; }}
}}
@keyframes seq-fade-in {{
  to {{ opacity: 1; }}
}}
@media (prefers-reduced-motion: reduce) {{
  .seq-title, .seq-icon, .seq-value, .seq-label, .seq-connector path, .seq-arrow {{
    animation: none !important; opacity: 1 !important; transform: none !important; stroke-dashoffset: 0 !important;
  }}
}}
/* total timeline ~{d:.1f}s, {step_count} steps */
"""


def write_svg(data: dict, output: Path) -> None:
    if output.exists():
        raise ValueError(f"output already exists: {output}")
    tree = build(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON spec (see templates/animated-infographic.json)")
    parser.add_argument("output", type=Path, help="Output .svg path")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        write_svg(data, args.output)
        print(args.output)
        return 0
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
