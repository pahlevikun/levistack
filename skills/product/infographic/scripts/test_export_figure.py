#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

from sibling_diagram import diagram_scripts_dir


class SiblingDiagramTests(unittest.TestCase):
    def test_diagram_sibling_present_in_repo(self):
        scripts = diagram_scripts_dir()
        self.assertIsNotNone(scripts)
        self.assertTrue((scripts / "mermaid_themes.py").is_file())

    def test_png_from_svg_refuses_existing(self):
        from png_from_svg import refuse_overwrite

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.png"
            path.write_bytes(b"x")
            with self.assertRaises(ValueError):
                refuse_overwrite(path)


if __name__ == "__main__":
    unittest.main()
