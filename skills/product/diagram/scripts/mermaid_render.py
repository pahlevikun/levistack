#!/usr/bin/env python3
"""Render Mermaid with a levistack theme via mmdc."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from mermaid_blocks import refuse_overwrite
from mermaid_themes import apply_theme, get_theme, load_catalog


def write_mmdc_config(theme_id: str, path: Path) -> None:
    theme = get_theme(theme_id)
    path.write_text(
        json.dumps({"theme": "base", "themeVariables": theme["themeVariables"]}, indent=2) + "\n",
        encoding="utf-8",
    )


def render(
    input_path: Path,
    output_path: Path,
    theme_id: str | None,
    background: str,
    scale: int,
) -> None:
    if not shutil.which("mmdc"):
        raise ValueError("mmdc is not installed")
    refuse_overwrite(output_path)
    source = input_path.read_text(encoding="utf-8")
    if theme_id:
        source = apply_theme(source, theme_id)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config = root / "mermaid.config.json"
        if theme_id:
            write_mmdc_config(theme_id, config)
        mmd = root / "figure.mmd"
        mmd.write_text(source, encoding="utf-8")
        cmd = ["mmdc", "-i", str(mmd), "-o", str(output_path), "-b", background, "-s", str(scale)]
        if theme_id:
            cmd.extend(["-c", str(config)])
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            raise ValueError(result.stderr.strip() or "mmdc failed")


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render .mmd to SVG or PNG with optional levistack theme.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--theme", help="theme id from mermaid_themes.py --list")
    parser.add_argument("-b", "--background", default="white")
    parser.add_argument("-s", "--scale", type=int, default=2)
    parser.add_argument("--list-themes", action="store_true")
    args = parser.parse_args(argv)

    if args.list_themes:
        for theme in load_catalog()["themes"]:
            print(theme["id"])
        return 0

    try:
        render(args.input, args.output, args.theme, args.background, args.scale)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
