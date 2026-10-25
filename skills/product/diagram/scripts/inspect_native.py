#!/usr/bin/env python3
"""Print a compact structural inventory without rendering or fetching resources."""

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


def unique_ids(elements):
    ids = [e.get("id") for e in elements if e.get("id")]
    duplicates = [value for value, count in Counter(ids).items() if count > 1]
    if duplicates:
        raise ValueError("duplicate IDs: " + ", ".join(duplicates))
    return set(ids)


def inspect_svg(root):
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError("expected a namespaced SVG root")
    values = [float(x) for x in root.get("viewBox", "").replace(",", " ").split()]
    if len(values) != 4 or not all(map(math.isfinite, values)) or min(values[2:]) <= 0:
        raise ValueError("viewBox must have four finite numbers and positive dimensions")
    elements = list(root.iter())
    ids = unique_ids(elements)
    missing = set()
    external = []
    for element in elements:
        for key, value in element.attrib.items():
            if key.rsplit("}", 1)[-1] == "href":
                if value.startswith("#"):
                    if value[1:] not in ids:
                        missing.add(value[1:])
                else:
                    external.append(value)
        for target in re.findall(r"url\(\s*['\"]?#([^)'\"\s]+)", " ".join(element.attrib.values()) + (element.text or "")):
            if target not in ids:
                missing.add(target)
    for target in root.get("aria-labelledby", "").split():
        if target not in ids:
            missing.add(target)
    if missing:
        raise ValueError("missing SVG references: " + ", ".join(sorted(missing)))
    return {"format": "svg", "viewBox": values, "ids": sorted(ids), "external_hrefs": external,
            "labels": ["".join(e.itertext()) for e in elements if e.tag.endswith("}text")]}


def inspect_drawio(root):
    if root.tag not in {"mxfile", "mxGraphModel"}:
        raise ValueError("expected mxfile or mxGraphModel")
    pages = list(root.findall("diagram")) if root.tag == "mxfile" else [root]
    if not pages:
        raise ValueError("no draw.io pages")
    output = []
    for page in pages:
        model = page if page.tag == "mxGraphModel" else page.find("mxGraphModel")
        if model is None:
            raise ValueError("compressed draw.io is unsupported. Export uncompressed XML in the editor")
        cells = list(model.iter("mxCell"))
        ids = unique_ids(cells)
        for cell in cells:
            for key in ("parent", "source", "target"):
                if cell.get(key) and cell.get(key) not in ids:
                    raise ValueError(f"cell {cell.get('id')}: missing {key} {cell.get(key)}")
        output.append({"name": page.get("name", "page"),
                       "nodes": [{"id": c.get("id"), "label": c.get("value", ""),
                                  "parent": c.get("parent"), "visible": c.get("visible", "1")}
                                 for c in cells if c.get("vertex") == "1"],
                       "edges": [{"id": c.get("id"), "source": c.get("source"),
                                  "target": c.get("target"), "label": c.get("value", ""),
                                  "style": c.get("style", "")}
                                 for c in cells if c.get("edge") == "1"]})
    return {"format": "drawio", "pages": output, "limit": "uncompressed XML reference check only"}


def inspect_excalidraw(scene):
    if scene.get("type") != "excalidraw" or not isinstance(scene.get("elements"), list):
        raise ValueError("expected an Excalidraw scene with elements")
    elements = scene["elements"]
    if not all(isinstance(e, dict) and isinstance(e.get("id"), str) and e["id"] for e in elements):
        raise ValueError("every element needs a nonempty string ID")
    unique_ids(elements)
    active = {e["id"]: e for e in elements if not e.get("isDeleted")}
    warnings = []
    for element in active.values():
        for key in ("x", "y", "width", "height"):
            value = element.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{element['id']}: {key} must be finite")
        references = []
        if element.get("containerId"):
            references.append(element["containerId"])
        for key in ("startBinding", "endBinding"):
            if element.get(key):
                references.append(element[key]["elementId"])
            elif element.get("type") == "arrow":
                warnings.append(f"{element['id']}: {key} is unbound, endpoints not inferred")
        references.extend(x["id"] for x in element.get("boundElements") or [])
        references.extend([element["frameId"]] if element.get("frameId") else [])
        for target in references:
            if target not in active:
                raise ValueError(f"{element['id']}: missing active binding {target}")
        if element.get("type") == "text" and element.get("containerId"):
            owner = active[element["containerId"]]
            if element["id"] not in {b["id"] for b in owner.get("boundElements") or []}:
                raise ValueError(f"{element['id']}: container lacks reciprocal text binding")
    return {"format": "excalidraw", "active": len(active), "deleted": len(elements) - len(active),
            "labels": [{"id": e["id"], "text": e.get("text", ""), "container": e.get("containerId")}
                       for e in active.values() if e.get("type") == "text"],
            "edges": [{"id": e["id"], "start": e.get("startBinding"), "end": e.get("endBinding")}
                      for e in active.values() if e.get("type") in {"arrow", "line"}],
            "types": dict(Counter(e.get("type") for e in active.values())), "warnings": warnings,
            "limit": "reference check only. Native editor open and drag checks remain required"}


def inspect(path):
    raw = Path(path).read_bytes()
    if len(raw) > 10_000_000:
        raise ValueError("input exceeds 10 MB. Split it before inspection")
    if raw.lstrip().startswith(b"{"):
        return inspect_excalidraw(json.loads(raw))
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("XML declarations with DTD or entities are unsupported")
    root = ET.fromstring(raw)
    return inspect_svg(root) if root.tag.endswith("}svg") else inspect_drawio(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.input), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError, ET.ParseError) as error:
        print(f"inspect_native: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
