#!/usr/bin/env python3
"""Export a local static SVG or a finite, explicitly ordered focus walkthrough."""

import argparse
import copy
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from inspect_native import inspect_svg

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def load_svg(path):
    raw = Path(path).read_bytes()
    if len(raw) > 10_000_000 or b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("SVG is too large or uses unsupported XML declarations")
    root = ET.fromstring(raw)
    report = inspect_svg(root)
    if report["external_hrefs"]:
        raise ValueError("external hrefs are unsupported. Use a self-contained source")
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] in {"script", "foreignObject", "image", "animate", "animateMotion", "animateTransform", "set"}:
            raise ValueError("use a static vector SVG without scripts, foreignObject, images or SMIL")
        if any(key.lower().startswith("on") for key in element.attrib):
            raise ValueError("event handlers are unsupported")
        text = " ".join(element.attrib.values()) + (element.text or "")
        resources = re.findall(r"url\((.*?)\)", text, flags=re.IGNORECASE)
        if "@import" in text.lower() or any(not value.strip().strip("'\"").startswith("#") for value in resources):
            raise ValueError("external CSS resources are unsupported")
        if re.search(r"(?:animation\s*:|animation-name\s*:|@keyframes)", text):
            raise ValueError("input must be static. Keep animation in a separate derived file")
    return root, report


def load_plan(path, report):
    plan = json.loads(Path(path).read_text())
    steps = plan.get("steps", [])
    duration = plan.get("step_ms", 900)
    if isinstance(duration, bool) or not isinstance(duration, int) or not 300 <= duration <= 2000:
        raise ValueError("step_ms must be an integer from 300 through 2000")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 8 or duration * (len(steps) + 1) > 5000:
        raise ValueError("use 1 through 8 steps with total duration at most 5 seconds")
    x, y, width, height = report["viewBox"]
    for step in steps:
        box = step.get("box", [])
        if step.get("id") not in report["ids"] or not isinstance(step.get("label"), str) or not step["label"].strip():
            raise ValueError("each step needs an existing SVG ID and a nonempty label")
        if len(box) != 4 or not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in box):
            raise ValueError("each focus box needs four finite numbers")
        bx, by, bw, bh = box
        if min(bw, bh) <= 0 or bx < x or by < y or bx + bw > x + width or by + bh > y + height:
            raise ValueError("focus box must fit inside the viewBox")
    return steps, duration


def focus(root, box):
    return ET.SubElement(root, f"{{{NS}}}rect", {
        "x": str(box[0]), "y": str(box[1]), "width": str(box[2]), "height": str(box[3]),
        "fill": "none", "stroke": "#a33a16", "stroke-width": "4", "rx": "8",
        "aria-hidden": "true", "pointer-events": "none",
        "style": "fill:none!important;stroke:#a33a16!important;stroke-width:4!important"})


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"{command[0]} failed: {result.stderr.strip()}")


def require(name):
    if not shutil.which(name):
        raise ValueError(f"missing {name}. Install or use the project's renderer, then retry")


def rasterize(root, output, width, directory):
    source = directory / "frame.svg"
    source.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
    run(["rsvg-convert", "--width", str(width), "--output", str(output), str(source)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["png", "gif", "animate"])
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--plan")
    parser.add_argument("--width", type=int, default=1200)
    args = parser.parse_args()
    output = Path(args.output)
    try:
        if output.exists():
            raise ValueError("output already exists. Choose a new path")
        if not 100 <= args.width <= 6000:
            raise ValueError("width must be from 100 through 6000")
        root, report = load_svg(args.input)
        if args.mode != "png" and not args.plan:
            raise ValueError("gif and animate require --plan")
        steps, duration = load_plan(args.plan, report) if args.plan else ([], 0)
        if args.mode == "animate":
            overlay = ET.SubElement(root, f"{{{NS}}}g", {"class": "diagram-walk", "aria-hidden": "true"})
            rules = []
            count = len(steps) + 1
            for index, step in enumerate(steps):
                rect = focus(overlay, step["box"])
                rect.set("style", rect.get("style", "") + f";opacity:0;animation:diagram-walk-{index} {duration * count}ms linear 1")
                start = index / count * 100
                end = (index + 1) / count * 100 - .01
                if index == 0:
                    frames = f"0%,{end:.4f}%{{opacity:1}} {end+.005:.4f}%,100%{{opacity:0}}"
                else:
                    frames = f"0%,{start-.005:.4f}%{{opacity:0}} {start:.4f}%,{end:.4f}%{{opacity:1}} {end+.005:.4f}%,100%{{opacity:0}}"
                rules.append(f"@keyframes diagram-walk-{index}{{{frames}}}")
            rules.append("@media (prefers-reduced-motion:reduce){.diagram-walk{display:none}} @media print{.diagram-walk{display:none}}")
            ET.SubElement(root, f"{{{NS}}}style").text = "\n".join(rules)
            with output.open("xb") as stream:
                stream.write(ET.tostring(root, encoding="utf-8", xml_declaration=True))
        else:
            require("rsvg-convert")
            if args.mode == "gif":
                require("ffmpeg")
            with tempfile.TemporaryDirectory(prefix="diagram-export-") as temporary:
                directory = Path(temporary)
                if args.mode == "png":
                    rasterize(root, directory / "result.png", args.width, directory)
                    final = directory / "result.png"
                else:
                    for index, step in enumerate(steps):
                        frame = copy.deepcopy(root)
                        focus(frame, step["box"])
                        rasterize(frame, directory / f"{index:03d}.png", args.width, directory)
                    rasterize(root, directory / f"{len(steps):03d}.png", args.width, directory)
                    final = directory / "result.gif"
                    run(["ffmpeg", "-v", "error", "-framerate", f"1000/{duration}", "-i", str(directory / "%03d.png"),
                         "-filter_complex", "[0:v]split[a][b];[a]palettegen[p];[b][p]paletteuse", "-loop", "-1", str(final)])
                with output.open("xb") as stream:
                    stream.write(final.read_bytes())
        print(json.dumps({"output": str(output), "bytes": output.stat().st_size, "mode": args.mode,
                          "steps": [s["label"] for s in steps], "note": "inspect the actual output and provide a static alternative"}))
    except (ValueError, OSError, KeyError, TypeError, ET.ParseError) as error:
        print(f"export_svg: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
