#!/usr/bin/env python3
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from build_animated_svg import build, validate, write_svg


class BuildAnimatedSvgTests(unittest.TestCase):
    def test_validate_rejects_empty_steps(self):
        with self.assertRaises(ValueError):
            validate({"title": "T", "source": "S", "steps": []})

    def test_build_has_reduced_motion(self):
        data = {
            "title": "Test",
            "source": "unit test",
            "synthetic": True,
            "steps": [{"glyph": "1", "value_display": "9", "label": "Nine"}],
        }
        tree = build(data)
        style = tree.find(".//{http://www.w3.org/2000/svg}style")
        self.assertIsNotNone(style)
        self.assertIn("prefers-reduced-motion", style.text or "")

    def test_build_has_tabular_nums(self):
        data = {
            "title": "Test",
            "source": "unit test",
            "synthetic": True,
            "steps": [{"glyph": "1", "value_display": "9", "label": "Nine"}],
        }
        tree = build(data)
        style = tree.find(".//{http://www.w3.org/2000/svg}style")
        self.assertIn("tabular-nums", style.text or "")

    def test_build_metadata_duration(self):
        data = {
            "title": "Test",
            "source": "unit test",
            "synthetic": True,
            "steps": [{"glyph": "1", "value_display": "9", "label": "Nine"}],
        }
        tree = build(data)
        meta = tree.find(".//{http://www.w3.org/2000/svg}metadata")
        self.assertIsNotNone(meta)
        self.assertIn("svg-only", meta.text or "")

    def test_write_refuses_overwrite(self):
        data = {
            "title": "Test",
            "source": "unit test",
            "synthetic": True,
            "steps": [{"glyph": "1", "value_display": "9", "label": "Nine"}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.svg"
            write_svg(data, out)
            self.assertTrue(out.is_file())
            with self.assertRaises(ValueError):
                write_svg(data, out)

    def test_example_file_roundtrip(self):
        example = Path(__file__).resolve().parent.parent / "examples" / "animated-steps" / "steps.json"
        data = json.loads(example.read_text(encoding="utf-8"))
        tree = build(data)
        title = tree.find(".//{http://www.w3.org/2000/svg}title")
        self.assertEqual(title.text, data["title"])


if __name__ == "__main__":
    unittest.main()
