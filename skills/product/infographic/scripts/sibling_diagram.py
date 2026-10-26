#!/usr/bin/env python3
"""Locate optional Mermaid export scripts next to this skill in the catalog tree."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def diagram_scripts_dir() -> Path | None:
    env = os.environ.get("LEVISTACK_DIAGRAM_SCRIPTS")
    if env:
        path = Path(env).resolve()
        if (path / "mermaid_themes.py").is_file():
            return path
    here = Path(__file__).resolve().parent
    candidate = here.parent.parent / "diagram" / "scripts"
    if (candidate / "mermaid_themes.py").is_file():
        return candidate
    return None


def run_diagram_script(script_name: str, argv: list[str]) -> subprocess.CompletedProcess[str]:
    scripts = diagram_scripts_dir()
    if scripts is None:
        raise ValueError(
            "Mermaid export scripts not found. Set LEVISTACK_DIAGRAM_SCRIPTS to the scripts directory "
            "that contains mermaid_themes.py and export_svg.py"
        )
    cmd = [sys.executable, str(scripts / script_name), *argv]
    return subprocess.run(cmd, capture_output=True, text=True)
