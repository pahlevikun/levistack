#!/usr/bin/env python3
"""Focused checks for broken native bindings and unsafe or ambiguous exports."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from export_svg import load_plan, load_svg
from inspect_native import inspect, inspect_excalidraw, inspect_svg

FIXTURES = Path(__file__).resolve().parents[1] / "evals"


class NativeChecks(unittest.TestCase):
    @unittest.skipUnless(shutil.which("rsvg-convert") and shutil.which("ffmpeg"), "rsvg-convert and ffmpeg required")
    def test_source_rect_styles_cannot_hide_labels_in_gif(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "styled.svg"
            source.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150"><style>rect{fill:white!important;stroke:black}</style><rect width="300" height="150"/><g id="node"><rect x="40" y="50" width="220" height="60"/><text x="60" y="85" font-size="20">ESSENTIAL LABEL</text></g></svg>')
            plan = directory / "plan.json"
            plan.write_text(json.dumps({"steps": [{"id": "node", "label": "Read label", "box": [40, 50, 220, 60]}]}))
            helper = Path(__file__).with_name("export_svg.py")
            for mode, suffix in (("png", "png"), ("gif", "gif")):
                subprocess.run([sys.executable, str(helper), mode, str(source), str(directory / f"result.{suffix}"), "--width", "300", "--plan", str(plan)], check=True, capture_output=True)

            def dark_label_pixels(path):
                result = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"], check=True, capture_output=True)
                pixels = result.stdout
                return sum(max(pixels[(y * 300 + x) * 3:(y * 300 + x) * 3 + 3]) < 100
                           for y in range(60, 90) for x in range(60, 240))

            original = dark_label_pixels(directory / "result.png")
            animated = dark_label_pixels(directory / "result.gif")
            self.assertGreater(original, 100)
            self.assertGreaterEqual(animated, original * .95, "highlight erased label pixels")

    def test_original_formats_keep_four_nodes_and_three_edges(self):
        svg = inspect(FIXTURES / "validation.svg")
        self.assertTrue({"client", "gate", "store", "reject"}.issubset(svg["ids"]))
        page = inspect(FIXTURES / "validation.drawio")["pages"][0]
        self.assertEqual({n["id"] for n in page["nodes"]}, {"client", "gate", "store", "reject"})
        self.assertEqual([(e["source"], e["target"]) for e in page["edges"]],
                         [("client", "gate"), ("gate", "store"), ("gate", "reject")])
        scene = inspect(FIXTURES / "validation.excalidraw")
        self.assertEqual([(e["start"]["elementId"], e["end"]["elementId"]) for e in scene["edges"]],
                         [("client", "gate"), ("gate", "store"), ("gate", "reject")])

    def test_dangling_and_nonreciprocal_text_bindings_fail(self):
        scene = json.loads((FIXTURES / "validation.excalidraw").read_text())
        bad = copy.deepcopy(scene)
        arrow = next(e for e in bad["elements"] if e["type"] == "arrow")
        arrow["endBinding"]["elementId"] = "missing"
        with self.assertRaisesRegex(ValueError, "missing active binding"):
            inspect_excalidraw(bad)
        owner = next(e for e in scene["elements"] if e["id"] == "client")
        owner["boundElements"] = []
        with self.assertRaisesRegex(ValueError, "reciprocal text binding"):
            inspect_excalidraw(scene)

    def test_duplicate_svg_ids_and_broken_marker_fail(self):
        root = ET.parse(FIXTURES / "validation.svg").getroot()
        ET.SubElement(root, "rect", {"id": "client"})
        with self.assertRaisesRegex(ValueError, "duplicate IDs"):
            inspect_svg(root)
        root = ET.parse(FIXTURES / "validation.svg").getroot()
        root.set("clip-path", "url(#missing)")
        with self.assertRaisesRegex(ValueError, "missing SVG references"):
            inspect_svg(root)

    def test_export_rejects_external_resource(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "remote.svg"
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><style>@import "https://example.invalid/font.css"</style></svg>')
            with self.assertRaisesRegex(ValueError, "external CSS"):
                load_svg(path)

    def test_explicit_steps_validate_ids_and_bounds(self):
        _, report = load_svg(FIXTURES / "validation.svg")
        steps, duration = load_plan(FIXTURES / "walk.json", report)
        self.assertEqual([s["id"] for s in steps], ["client", "gate", "store"])
        self.assertEqual(duration, 800)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.json"
            path.write_text(json.dumps({"steps": [{"id": "imaginary", "label": "bad", "box": [0, 0, 10, 10]}]}))
            with self.assertRaisesRegex(ValueError, "existing SVG ID"):
                load_plan(path, report)
            path.write_text(json.dumps({"steps": [{"id": "gate", "label": "bad", "box": [790, 0, 20, 20]}]}))
            with self.assertRaisesRegex(ValueError, "inside the viewBox"):
                load_plan(path, report)


if __name__ == "__main__":
    unittest.main()
