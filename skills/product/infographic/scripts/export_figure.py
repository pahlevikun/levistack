#!/usr/bin/env python3
"""Export helpers for infographic layouts: PNG from SVG and themed Mermaid when export scripts exist."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from png_from_svg import rasterize
from sibling_diagram import diagram_scripts_dir, run_diagram_script


def cmd_png(args: argparse.Namespace) -> int:
    rasterize(args.input, args.output, args.width)
    print(args.output)
    return 0


def cmd_mermaid_render(args: argparse.Namespace) -> int:
    argv = [str(args.input), str(args.output)]
    if args.theme:
        argv.extend(["--theme", args.theme])
    result = run_diagram_script("mermaid_render.py", argv)
    if result.returncode:
        print(result.stderr.strip() or result.stdout, file=sys.stderr)
        return result.returncode or 2
    print(result.stdout.strip() or args.output)
    return 0


def cmd_mermaid_theme(args: argparse.Namespace) -> int:
    argv = ["--theme", args.theme, "--input", str(args.input), "--output", str(args.output)]
    result = run_diagram_script("mermaid_themes.py", argv)
    if result.returncode:
        print(result.stderr.strip() or result.stdout, file=sys.stderr)
        return result.returncode or 2
    print(result.stdout.strip() or args.output)
    return 0


def cmd_themes_list(_args: argparse.Namespace) -> int:
    result = run_diagram_script("mermaid_themes.py", ["--list"])
    if result.returncode:
        print(result.stderr.strip() or result.stdout, file=sys.stderr)
        return result.returncode or 2
    print(result.stdout, end="")
    return 0


def cmd_diagram_png(args: argparse.Namespace) -> int:
    scripts = diagram_scripts_dir()
    if scripts is None:
        return cmd_png(args)
    argv = ["png", str(args.input), str(args.output), "--width", str(args.width)]
    result = run_diagram_script("export_svg.py", argv)
    if result.returncode:
        print(result.stderr.strip() or result.stdout, file=sys.stderr)
        return result.returncode or 2
    print(result.stdout.strip() or args.output)
    return 0


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    png = sub.add_parser("png", help="SVG to PNG (local rsvg-convert)")
    png.add_argument("input", type=Path)
    png.add_argument("output", type=Path)
    png.add_argument("--width", type=int, default=1200)
    png.set_defaults(func=cmd_png)

    strict = sub.add_parser("png-strict", help="SVG to PNG via export_svg.py (static SVG checks)")
    strict.add_argument("input", type=Path)
    strict.add_argument("output", type=Path)
    strict.add_argument("--width", type=int, default=1200)
    strict.set_defaults(func=cmd_diagram_png)

    themed = sub.add_parser("mermaid-svg", help="render .mmd to SVG with optional levistack theme")
    themed.add_argument("input", type=Path)
    themed.add_argument("output", type=Path)
    themed.add_argument("--theme", help="theme id from export_figure.py themes list")
    themed.set_defaults(func=cmd_mermaid_render)

    inject = sub.add_parser("mermaid-theme", help="inject init block into .mmd")
    inject.add_argument("input", type=Path)
    inject.add_argument("output", type=Path)
    inject.add_argument("--theme", required=True)
    inject.set_defaults(func=cmd_mermaid_theme)

    lst = sub.add_parser("themes", help="list Mermaid presentation themes")
    lst.set_defaults(func=cmd_themes_list)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"export_figure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
