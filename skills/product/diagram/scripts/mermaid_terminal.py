#!/usr/bin/env python3
"""Render Mermaid to terminal text via npx beautiful-mermaid when allowed."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from mermaid_blocks import read_diagrams, refuse_overwrite, temp_mmd
from mermaid_themes import apply_theme, terminal_theme_name


def render_terminal(
    mmd_path: Path, output: Path, use_ascii: bool, use_npx: bool, bm_theme: str | None
) -> None:
    refuse_overwrite(output)
    cmd = (["npx", "--yes", "beautiful-mermaid", str(mmd_path)] if use_npx else ["beautiful-mermaid", str(mmd_path)])
    if bm_theme:
        cmd.extend(["--theme", bm_theme])
    if use_ascii:
        cmd.append("--ascii")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "terminal render failed")
    output.write_text(result.stdout, encoding="utf-8")


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mermaid to terminal-friendly text.")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument(
        "--theme",
        help="levistack catalog id (injects init block; uses terminal_pairing for beautiful-mermaid when set)",
    )
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--allow-network", action="store_true")
    args = parser.parse_args(argv)

    blocks = read_diagrams(args.input)
    if not blocks:
        print("No mermaid content found.", file=sys.stderr)
        return 1
    code = blocks[0].code
    bm_theme = None
    if args.theme:
        code = apply_theme(code, args.theme)
        bm_theme = terminal_theme_name(args.theme)
    use_npx = args.allow_network or not shutil.which("beautiful-mermaid")
    if use_npx and not args.allow_network:
        print("Error: pass --allow-network for npx beautiful-mermaid.", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        mmd = Path(tmp) / "figure.mmd"
        mmd.write_text(code, encoding="utf-8")
        try:
            render_terminal(mmd, args.output, args.ascii, use_npx and args.allow_network, bm_theme)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
