#!/usr/bin/env python3
"""Discover raster image backends for labeled synthetic infographic drafts."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
@dataclass(frozen=True)
class Backend:
    id: str
    label: str
    kind: str  # api | agent | local
    available: bool
    detail: str


def _has(key: str) -> bool:
    return bool(os.environ.get(key, "").strip())


def probe_backends() -> list[Backend]:
    openai = _has("OPENAI_API_KEY")
    openrouter = _has("OPENROUTER_API_KEY")
    codex = shutil.which("codex") is not None
    rsvg = shutil.which("rsvg-convert") is not None

    return [
        Backend(
            id="agent-native",
            label="Host image tool (Cursor GenerateImage, Codex imagegen, etc.)",
            kind="agent",
            available=True,
            detail="Agent invokes the runtime native tool. Prompt file must exist first.",
        ),
        Backend(
            id="openai",
            label="OpenAI Images API",
            kind="api",
            available=openai,
            detail="Set OPENAI_API_KEY. Uses images/generations.",
        ),
        Backend(
            id="openrouter",
            label="OpenRouter Images API",
            kind="api",
            available=openrouter,
            detail="Set OPENROUTER_API_KEY. OpenAI-compatible images endpoint.",
        ),
        Backend(
            id="codex-cli",
            label="Codex CLI (login required)",
            kind="agent",
            available=codex,
            detail="codex on PATH. Agent usually drives this, not batch HTTP.",
        ),
        Backend(
            id="local-vector",
            label="Local SVG raster (evidence track)",
            kind="local",
            available=rsvg,
            detail="png_from_svg.py via rsvg-convert. Not model-generated art.",
        ),
    ]


def available_backend_ids() -> list[str]:
    return [b.id for b in probe_backends() if b.available]


def resolve_backend(
    preferred: str,
    override: str | None = None,
    *,
    allow_agent_native: bool = True,
) -> tuple[str, str]:
    """Return (backend_id, rationale). Raises ValueError when resolution fails."""
    if override and override.strip():
        chosen = override.strip()
        ids = {b.id for b in probe_backends()}
        if chosen not in ids:
            raise ValueError(f"unknown backend: {chosen}")
        backend = next(b for b in probe_backends() if b.id == chosen)
        if not backend.available and backend.id != "agent-native":
            raise ValueError(f"backend not available: {chosen} ({backend.detail})")
        return chosen, "user override"

    if preferred == "ask":
        raise ValueError("preferred_raster_backend is ask: confirm with the user")

    if preferred not in ("auto",) and preferred:
        backend = next((b for b in probe_backends() if b.id == preferred), None)
        if backend is None:
            raise ValueError(f"unknown preferred backend: {preferred}")
        if not backend.available and backend.id != "agent-native":
            raise ValueError(f"pinned backend unavailable: {preferred}")
        return preferred, "pinned in preferences"

    api_ready = [b for b in probe_backends() if b.kind == "api" and b.available]
    if len(api_ready) == 1:
        return api_ready[0].id, "only one API key present"
    if len(api_ready) > 1:
        raise ValueError(
            "multiple API backends detected: set preferred_raster_backend in infographic.prefs.json or pass --backend"
        )

    if allow_agent_native:
        return "agent-native", "default when no API key is configured"

    if not api_ready:
        raise ValueError("no API backend available and agent-native disabled")
    raise ValueError("could not resolve raster backend")
