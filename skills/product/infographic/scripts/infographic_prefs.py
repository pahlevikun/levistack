#!/usr/bin/env python3
"""Load levistack infographic preferences (EXTEND-style, JSON or YAML frontmatter)."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PREFS_JSON_NAMES = (
    "infographic.prefs.json",
    ".levistack/infographic.prefs.json",
)
PREFS_EXTEND_NAMES = (
    "infographic.extend.md",
    ".levistack/infographic.extend.md",
)

DEFAULTS: dict[str, Any] = {
    "version": 1,
    "preferred_raster_backend": "auto",
    "quick_mode": False,
    "skip_confirm": False,
    "default_aspect": "landscape-wide",
    "default_layout": "tile-board",
    "default_mood": "editorial-clean",
    "default_language": "en",
    "generation_batch_size": 4,
    "openrouter_model": "google/gemini-2.5-flash-image-preview",
    "openai_model": "gpt-image-1",
    "style_prefix": "",
}


@dataclass
class LoadedPreferences:
    values: dict[str, Any]
    source: Path | None
    searched: list[Path] = field(default_factory=list)


def _xdg_config() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    if base:
        return Path(base) / "levistack"
    return Path.home() / ".config" / "levistack"


def preference_search_paths(project_dir: Path | None = None) -> list[Path]:
    paths: list[Path] = []
    if project_dir is not None:
        root = project_dir.resolve()
        for name in PREFS_JSON_NAMES:
            paths.append(root / name)
        for name in PREFS_EXTEND_NAMES:
            paths.append(root / name)
    xdg = _xdg_config()
    paths.append(xdg / "infographic.prefs.json")
    paths.append(xdg / "infographic.extend.md")
    paths.append(Path.home() / ".levistack" / "infographic.prefs.json")
    return paths


def _parse_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    block = match.group(1)
    data: dict[str, Any] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        raw = raw.strip().strip('"').strip("'")
        if raw.lower() in ("true", "false"):
            data[key] = raw.lower() == "true"
        elif raw.isdigit():
            data[key] = int(raw)
        else:
            try:
                data[key] = json.loads(raw)
            except json.JSONDecodeError:
                data[key] = raw
    return data


def _parse_extend_md(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = _parse_frontmatter(text)
    fence = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if fence:
        try:
            blob = json.loads(fence.group(1))
            if isinstance(blob, dict):
                data.update(blob)
        except json.JSONDecodeError:
            pass
    return data


def _load_file(path: Path) -> dict[str, Any]:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.name.endswith(".extend.md") or path.suffix == ".md":
        return _parse_extend_md(path)
    raise ValueError(f"unsupported preferences file: {path}")


def load_preferences(project_dir: Path | None = None) -> LoadedPreferences:
    searched = preference_search_paths(project_dir)
    for path in searched:
        if path.is_file():
            raw = _load_file(path)
            if not isinstance(raw, dict):
                raise ValueError(f"preferences root must be an object: {path}")
            merged = {**DEFAULTS, **raw}
            return LoadedPreferences(values=merged, source=path, searched=searched)
    return LoadedPreferences(values=dict(DEFAULTS), source=None, searched=searched)


def write_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    template = Path(__file__).resolve().parent.parent / "templates" / "infographic.prefs.json"
    path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
