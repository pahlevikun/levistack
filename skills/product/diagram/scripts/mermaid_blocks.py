#!/usr/bin/env python3
"""Extract ```mermaid fences from Markdown and name blocks for batch export."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

_OPEN = re.compile(r"^(`{3,})mermaid\s*$", re.IGNORECASE)
_CLOSE = re.compile(r"^(`{3,})\s*$")


@dataclass(frozen=True)
class Block:
    index: int
    name: str
    code: str
    line_start: int


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "diagram"


def refuse_overwrite(path: Path) -> None:
    if path.exists():
        raise ValueError(f"refusing to overwrite existing file: {path}")


@contextmanager
def temp_mmd(code: str, directory: Path):
    handle = tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", dir=directory, delete=False, encoding="utf-8",
    )
    try:
        handle.write(code)
        handle.flush()
        handle.close()
        yield Path(handle.name)
    finally:
        Path(handle.name).unlink(missing_ok=True)


def extract_mermaid_blocks(text: str) -> list[tuple[int, str, int]]:
    """Return (index, code, line_start) for each top-level mermaid fence."""
    lines = text.splitlines()
    found: list[tuple[int, str, int]] = []
    index = 0
    i = 0
    while i < len(lines):
        open_match = _OPEN.match(lines[i].strip())
        if not open_match:
            i += 1
            continue
        tick = open_match.group(1)
        start = i
        i += 1
        body: list[str] = []
        while i < len(lines):
            line = lines[i].strip()
            if _CLOSE.match(line) and line.startswith(tick):
                code = "\n".join(body).strip()
                if code:
                    index += 1
                    found.append((index, code, start + 1))
                i += 1
                break
            body.append(lines[i])
            i += 1
        else:
            raise ValueError(f"unclosed mermaid fence starting at line {start + 1}")
    return found


def read_diagrams(path: Path) -> list[Block]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".mmd":
        code = text.strip()
        return [Block(1, path.stem, code, 1)] if code else []

    raw = extract_mermaid_blocks(text)
    if not raw:
        return []
    if len(raw) == 1:
        _, code, line = raw[0]
        return [Block(1, path.stem, code, line)]
    return [Block(idx, f"{path.stem}-{idx}", code, line) for idx, code, line in raw]


def write_manifest(blocks: list[Block], manifest_path: Path, source: Path) -> None:
    payload = {
        "source": str(source),
        "blocks": [
            {"index": b.index, "name": b.name, "line_start": b.line_start, "code": b.code}
            for b in blocks
        ],
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List Mermaid blocks in .md or .mmd files.")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--manifest", type=Path, help="write JSON manifest")
    parser.add_argument("--json", action="store_true", help="print block summary as JSON")
    args = parser.parse_args(argv)

    rows: list[dict[str, object]] = []
    for path in args.inputs:
        blocks = read_diagrams(path)
        if args.manifest:
            write_manifest(blocks, args.manifest, path)
        for block in blocks:
            rows.append({
                "file": str(path),
                "name": block.name,
                "line_start": block.line_start,
                "chars": len(block.code),
            })

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            print(f"{row['file']}:{row['line_start']} {row['name']} ({row['chars']} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
