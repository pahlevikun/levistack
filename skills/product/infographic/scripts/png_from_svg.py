#!/usr/bin/env python3
"""Rasterize a self-contained SVG for poster or social export."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def refuse_overwrite(path: Path) -> None:
    if path.exists():
        raise ValueError(f"output already exists: {path}")


def rasterize(input_svg: Path, output_png: Path, width: int) -> None:
    if not shutil.which("rsvg-convert"):
        raise ValueError("missing rsvg-convert. Install it or use export_figure.py png-strict when export scripts exist")
    if not 100 <= width <= 6000:
        raise ValueError("width must be from 100 through 6000")
    refuse_overwrite(output_png)
    result = subprocess.run(
        ["rsvg-convert", "--width", str(width), "--output", str(output_png), str(input_svg)],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "rsvg-convert failed")


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1200)
    args = parser.parse_args(argv)
    try:
        rasterize(args.input, args.output, args.width)
    except ValueError as exc:
        print(f"png_from_svg: {exc}", file=sys.stderr)
        return 2
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
