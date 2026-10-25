#!/usr/bin/env python3
"""Check truthful scales, provenance and text preservation in generated charts."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

from render_bars import build


class BarChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).resolve().parents[1] / "evals/sample-bars.json").read_text())

    def test_geometry_and_accessible_values_match_input(self):
        root = ET.fromstring(build(self.data))
        widths = [float(e.get("width")) for e in root.iter() if e.get("id", "").startswith("bar-")]
        self.assertEqual(widths, [630, 472.5, 157.5])
        text = " ".join(root.itertext())
        self.assertIn("SYNTHETIC EXAMPLE, NOT OBSERVED DATA", text)
        self.assertIn("Accepted: 75", text)
        self.assertIn(self.data["source"], text)

    def test_clipped_scale_and_nonfinite_values_fail(self):
        self.data["scale_max"] = 50
        with self.assertRaisesRegex(ValueError, "cover every value"):
            build(self.data)
        self.data["scale_max"] = 100
        for value in [-1, float("nan"), float("inf"), True]:
            self.data["data"][0]["value"] = value
            with self.assertRaisesRegex(ValueError, "finite and nonnegative"):
                build(self.data)

    def test_missing_provenance_fails_and_labels_stay_text(self):
        self.data["source"] = ""
        with self.assertRaisesRegex(ValueError, "source"):
            build(self.data)
        self.data["source"] = "Local <sample> & notes"
        self.data["data"][0]["label"] = "A < B & C"
        root = ET.fromstring(build(self.data))
        self.assertIn("A < B & C", " ".join(root.itertext()))
        self.assertFalse(any(e.tag.endswith("script") for e in root.iter()))

    def test_long_numbers_fail_instead_of_silent_rounding(self):
        self.data["data"][0]["value"] = 1234567
        self.data["scale_max"] = 2000000
        with self.assertRaisesRegex(ValueError, "explicit display units"):
            build(self.data)

    @unittest.skipUnless(shutil.which("rsvg-convert") and shutil.which("ffmpeg"), "rsvg-convert and ffmpeg required")
    def test_wide_labels_stay_inside_their_reserved_columns(self):
        self.data.update(title="Short title", source="W" * 92, synthetic=False)
        self.data["data"] = [{"label": "W" * 24, "value": 100}]
        source = build(self.data)
        root = ET.fromstring(source)
        height = int(root.get("viewBox").split()[3])
        row_y = int(next(e for e in root.iter() if e.get("id") == "bar-0").get("y"))
        footer_y = max(int(e.get("y")) for e in root.iter() if e.tag.endswith("text")) - 72
        self.assertIn("W" * 24, " ".join(root.itertext()))
        self.assertIn("W" * 92, " ".join(root.itertext()))
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "wide.svg"
            image = path.with_suffix(".png")
            path.write_bytes(source)
            subprocess.run(["rsvg-convert", "-w", "1200", "-o", str(image), str(path)], check=True, capture_output=True)
            pixels = subprocess.run(["ffmpeg", "-v", "error", "-i", str(image), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"], check=True, capture_output=True).stdout
            for x_start, x_end, y_start, y_end in ((365, 415, row_y, row_y + 60), (1120, 1200, footer_y, height)):
                dark = sum(min(pixels[(y * 1200 + x) * 3:(y * 1200 + x) * 3 + 3]) < 200
                           for y in range(y_start, y_end) for x in range(x_start, x_end))
                self.assertEqual(dark, 0, "text extends outside its reserved area")


if __name__ == "__main__":
    unittest.main()
