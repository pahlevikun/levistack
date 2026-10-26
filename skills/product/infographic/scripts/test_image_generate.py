#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from infographic_prefs import load_preferences, _parse_frontmatter
from raster_backends import resolve_backend


class InfographicPrefsTests(unittest.TestCase):
    def test_frontmatter_parse(self):
        text = "---\npreferred_raster_backend: openai\nquick_mode: true\n---\n"
        data = _parse_frontmatter(text)
        self.assertEqual(data["preferred_raster_backend"], "openai")
        self.assertTrue(data["quick_mode"])

    def test_load_defaults_without_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            loaded = load_preferences(Path(tmp))
            self.assertIsNone(loaded.source)
            self.assertEqual(loaded.values["default_layout"], "tile-board")

    def test_load_json_prefs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "infographic.prefs.json"
            path.write_text(
                json.dumps({"preferred_raster_backend": "agent-native", "generation_batch_size": 2}),
                encoding="utf-8",
            )
            loaded = load_preferences(root)
            self.assertEqual(loaded.source.resolve(), path.resolve())
            self.assertEqual(loaded.values["preferred_raster_backend"], "agent-native")
            self.assertEqual(loaded.values["generation_batch_size"], 2)


class RasterBackendTests(unittest.TestCase):
    def test_resolve_override(self):
        backend, reason = resolve_backend("auto", "agent-native")
        self.assertEqual(backend, "agent-native")
        self.assertEqual(reason, "user override")

    def test_resolve_ask_raises(self):
        with self.assertRaises(ValueError):
            resolve_backend("ask", None)


if __name__ == "__main__":
    unittest.main()
