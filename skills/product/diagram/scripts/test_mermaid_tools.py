#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from mermaid_blocks import extract_mermaid_blocks, read_diagrams, slugify


class MermaidBlockTests(unittest.TestCase):
    def test_single_fence(self):
        text = "# Doc\n\n```mermaid\nflowchart LR\n  A-->B\n```\n"
        blocks = extract_mermaid_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertIn("A-->B", blocks[0][1])

    def test_multiple_fences(self):
        text = "```mermaid\nflowchart LR\n  X-->Y\n```\n\n```mermaid\nflowchart LR\n  P-->Q\n```\n"
        blocks = extract_mermaid_blocks(text)
        self.assertEqual(len(blocks), 2)

    def test_read_diagrams_names_multiple(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "readme.md"
            path.write_text(
                "```mermaid\na\n```\n\n```mermaid\nb\n```\n",
                encoding="utf-8",
            )
            blocks = read_diagrams(path)
            self.assertEqual([b.name for b in blocks], ["readme-1", "readme-2"])

    def test_slugify(self):
        self.assertEqual(slugify("Data Flow!"), "data-flow")

    def test_remote_requires_flag(self):
        from mermaid_remote_png import main

        with tempfile.TemporaryDirectory() as tmp:
            mmd = Path(tmp) / "x.mmd"
            mmd.write_text("flowchart LR\n  A-->B\n", encoding="utf-8")
            out = Path(tmp) / "out"
            out.mkdir()
            code = main([str(mmd), "-o", str(out), "--backend", "ink"])
            self.assertEqual(code, 2)

    def test_remote_ink_writes_png(self):
        from mermaid_remote_png import main

        payload = b"\x89PNG\r\n\x1a\n"
        with tempfile.TemporaryDirectory() as tmp:
            mmd = Path(tmp) / "x.mmd"
            mmd.write_text("flowchart LR\n  A-->B\n", encoding="utf-8")
            out = Path(tmp) / "out"
            with mock.patch("mermaid_remote_png.urllib.request.urlopen") as urlopen:
                urlopen.return_value.__enter__.return_value.read.return_value = payload
                code = main([str(mmd), "-o", str(out), "--backend", "ink", "--allow-remote"])
            self.assertEqual(code, 0)
            self.assertTrue(any(out.glob("*.png")))


if __name__ == "__main__":
    unittest.main()
