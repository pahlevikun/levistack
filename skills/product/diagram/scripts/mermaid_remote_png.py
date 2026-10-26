#!/usr/bin/env python3
"""Render Mermaid to PNG with local mmdc or optional mermaid.ink (user must opt in)."""

from __future__ import annotations

import argparse
import base64
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from mermaid_blocks import read_diagrams, refuse_overwrite, slugify, temp_mmd, write_manifest

INK_URL = "https://mermaid.ink/img/"
USER_AGENT = "levistack-diagram/1.0 (+local batch export)"


def render_ink(code: str, output: Path, bg: str) -> None:
    refuse_overwrite(output)
    token = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
    url = f"{INK_URL}{token}?bgColor={bg.lstrip('#')}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            output.write_bytes(response.read())
    except urllib.error.HTTPError as exc:
        raise ValueError(f"remote render failed: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"remote render failed: {exc.reason}") from exc


def render_mmdc(code: str, output: Path, scale: int) -> None:
    if not shutil.which("mmdc"):
        raise ValueError("mmdc is not installed")
    refuse_overwrite(output)
    with temp_mmd(code, output.parent) as source:
        cmd = ["mmdc", "-i", str(source), "-o", str(output), "-b", "white", "-s", str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode:
            raise ValueError(result.stderr.strip() or "mmdc failed")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Mermaid sources to PNG.")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("-o", "--output-dir", type=Path, required=True)
    parser.add_argument("--backend", choices=("mmdc", "ink"), default="mmdc")
    parser.add_argument("--allow-remote", action="store_true")
    parser.add_argument("--bg", default="white")
    parser.add_argument("--scale", type=int, default=2)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args(argv)

    if args.backend == "ink" and not args.allow_remote:
        print("Error: ink sends source to mermaid.ink. Pass --allow-remote.", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    for input_path in args.inputs:
        blocks = read_diagrams(input_path)
        if args.manifest:
            write_manifest(blocks, args.manifest, input_path)
        for block in blocks:
            output = args.output_dir / f"{slugify(block.name)}.png"
            if args.backend == "mmdc":
                render_mmdc(block.code, output, args.scale)
            else:
                render_ink(block.code, output, args.bg)
            count += 1
            print(output)

    if not count:
        print("No diagrams rendered.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
