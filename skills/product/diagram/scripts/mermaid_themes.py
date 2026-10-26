#!/usr/bin/env python3
"""Load levistack Mermaid presentation themes and inject init blocks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "mermaid-themes.json"
_INIT_RE = re.compile(r"^%%\{init:.*?\}%%\s*\n?", re.DOTALL | re.MULTILINE)
# beautiful-mermaid CLI theme ids (terminal/SVG), not levistack catalog ids
TERMINAL_PAIRINGS = frozenset(
    {
        "zinc-light",
        "zinc-dark",
        "tokyo-night-light",
        "tokyo-night",
        "tokyo-night-storm",
        "catppuccin-latte",
        "catppuccin-mocha",
        "nord-light",
        "nord",
        "dracula",
        "github-light",
        "github-dark",
        "solarized-light",
        "solarized-dark",
        "one-dark",
    }
)


def load_catalog() -> dict:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    themes = payload.get("themes", [])
    if not isinstance(themes, list) or not themes:
        raise ValueError("mermaid-themes.json must list themes")
    ids = [t.get("id") for t in themes]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate theme id in catalog")
    for theme in themes:
        _validate_theme(theme)
    return payload


def _validate_theme(theme: dict) -> None:
    for key in ("id", "label", "mode", "themeVariables"):
        if key not in theme:
            raise ValueError(f"theme missing {key}: {theme.get('id')}")
    if theme["mode"] not in {"light", "dark"}:
        raise ValueError(f"invalid mode for {theme['id']}")
    vars_ = theme["themeVariables"]
    if not isinstance(vars_, dict) or not vars_:
        raise ValueError(f"themeVariables empty for {theme['id']}")
    pairing = theme.get("terminal_pairing")
    if pairing is not None and pairing not in TERMINAL_PAIRINGS:
        raise ValueError(f"unknown terminal_pairing for {theme['id']}: {pairing}")


def get_theme(theme_id: str) -> dict:
    for theme in load_catalog()["themes"]:
        if theme["id"] == theme_id:
            return theme
    raise ValueError(f"unknown theme: {theme_id}")


def init_block(theme: dict) -> str:
    variables = json.dumps(theme["themeVariables"], separators=(",", ":"))
    return f"%%{{init: {{'theme': 'base', 'themeVariables': {variables}}} }}%%\n"


def apply_theme(source: str, theme_id: str) -> str:
    theme = get_theme(theme_id)
    body = _INIT_RE.sub("", source.lstrip())
    return init_block(theme) + body


def terminal_theme_name(theme_id: str) -> str | None:
    """beautiful-mermaid theme for terminal render, if catalog defines a pairing."""
    return get_theme(theme_id).get("terminal_pairing")


def merge_project_tokens(theme_id: str, roles: dict[str, str]) -> dict:
    """Map color-kit style roles onto themeVariables when keys are present."""
    theme = get_theme(theme_id)
    merged = dict(theme["themeVariables"])
    mapping = {
        "surface": "mainBkg",
        "on-surface": "textColor",
        "accent": "primaryBorderColor",
        "muted": "lineColor",
        "background": "background",
    }
    for role, var_name in mapping.items():
        if role in roles and roles[role]:
            merged[var_name] = roles[role]
    out = dict(theme)
    out["themeVariables"] = merged
    return out


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List or apply levistack Mermaid themes.")
    parser.add_argument("--list", action="store_true", help="print theme ids")
    parser.add_argument("--json", action="store_true", help="with --list, emit JSON")
    parser.add_argument("--theme", help="theme id for --apply")
    parser.add_argument("--input", type=Path, help=".mmd source")
    parser.add_argument("--output", type=Path, help="themed .mmd output")
    args = parser.parse_args(argv)

    if args.list:
        themes = load_catalog()["themes"]
        if args.json:
            print(
                json.dumps(
                    [
                        {
                            "id": t["id"],
                            "label": t["label"],
                            "mode": t["mode"],
                            "high_contrast": t.get("high_contrast", False),
                            "family": t.get("family"),
                            "terminal_pairing": t.get("terminal_pairing"),
                            "tags": t.get("tags"),
                        }
                        for t in themes
                    ],
                    indent=2,
                )
            )
        else:
            for t in themes:
                flag = " hc" if t.get("high_contrast") else ""
                print(f"{t['id']}: {t['label']} ({t['mode']}{flag})")
        return 0

    if not (args.theme and args.input and args.output):
        if not args.list:
            parser.error("use --list or pass --theme, --input, and --output")
        return 0
    text = args.input.read_text(encoding="utf-8")
    args.output.write_text(apply_theme(text, args.theme), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
