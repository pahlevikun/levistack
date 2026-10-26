#!/usr/bin/env python3
import unittest

from mermaid_themes import apply_theme, get_theme, load_catalog, merge_project_tokens, terminal_theme_name


class ThemeCatalogTests(unittest.TestCase):
    def test_catalog_loads(self):
        themes = load_catalog()["themes"]
        self.assertGreaterEqual(len(themes), 40)

    def test_apply_prepends_init(self):
        out = apply_theme("flowchart LR\n  A-->B\n", "inkwell")
        self.assertTrue(out.startswith("%%{init:"))
        self.assertIn("A-->B", out)

    def test_high_contrast_flag(self):
        theme = get_theme("audit-highvis")
        self.assertTrue(theme.get("high_contrast"))

    def test_merge_project_tokens(self):
        merged = merge_project_tokens("porcelain", {"surface": "#111111", "accent": "#ff00ff"})
        self.assertEqual(merged["themeVariables"]["mainBkg"], "#111111")

    def test_terminal_pairing(self):
        self.assertEqual(terminal_theme_name("harbor-slate"), "tokyo-night-storm")


if __name__ == "__main__":
    unittest.main()
