#!/usr/bin/env python3
"""Preferences, backend discovery, and optional raster generation (stdlib HTTP)."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from infographic_prefs import load_preferences, preference_search_paths, write_template
from png_from_svg import refuse_overwrite
from raster_backends import probe_backends, resolve_backend

ASPECT_TO_SIZE: dict[str, str] = {
    "16:9": "1792x1024",
    "9:16": "1024x1792",
    "1:1": "1024x1024",
    "4:3": "1024x768",
    "3:4": "768x1024",
}


def _read_prompt(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("prompt file is empty")
    return text


def _http_post_json(url: str, payload: dict, headers: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail[:500]}") from exc


def _save_b64_image(b64_data: str, output: Path) -> None:
    refuse_overwrite(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = base64.b64decode(b64_data)
    output.write_bytes(raw)


def _openai_images(prompt: str, model: str, size: str) -> bytes:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": 1,
    }
    data = _http_post_json(url, payload, headers)
    item = data.get("data", [{}])[0]
    if "b64_json" in item:
        return base64.b64decode(item["b64_json"])
    if "url" in item:
        with urllib.request.urlopen(item["url"], timeout=120) as resp:
            return resp.read()
    raise RuntimeError("OpenAI response had no image data")


def _openrouter_images(prompt: str, model: str, size: str) -> bytes:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    url = "https://openrouter.ai/api/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/pahlevikun/levistack",
        "X-Title": "levistack-infographic",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": 1,
    }
    data = _http_post_json(url, payload, headers)
    item = data.get("data", [{}])[0]
    if "b64_json" in item:
        return base64.b64decode(item["b64_json"])
    if "url" in item:
        with urllib.request.urlopen(item["url"], timeout=120) as resp:
            return resp.read()
    raise RuntimeError("OpenRouter response had no image data")


def cmd_prefs_path(args: argparse.Namespace) -> int:
    loaded = load_preferences(args.project)
    if loaded.source:
        print(loaded.source)
        return 0
    for path in loaded.searched:
        print(f"# missing: {path}", file=sys.stderr)
    return 1


def cmd_prefs_show(args: argparse.Namespace) -> int:
    loaded = load_preferences(args.project)
    out = {"source": str(loaded.source) if loaded.source else None, "values": loaded.values}
    print(json.dumps(out, indent=2))
    return 0


def cmd_prefs_init(args: argparse.Namespace) -> int:
    target = args.output or (args.project or Path.cwd()) / "infographic.prefs.json"
    write_template(target)
    print(target)
    return 0


def cmd_backends(args: argparse.Namespace) -> int:
    rows = [
        {
            "id": b.id,
            "label": b.label,
            "kind": b.kind,
            "available": b.available,
            "detail": b.detail,
        }
        for b in probe_backends()
    ]
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            flag = "yes" if row["available"] else "no"
            print(f"{row['id']}\t{flag}\t{row['detail']}")
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    loaded = load_preferences(args.project)
    pref = loaded.values.get("preferred_raster_backend", "auto")
    try:
        backend_id, reason = resolve_backend(pref, args.backend)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps({"backend": backend_id, "reason": reason, "preferences": str(loaded.source)}))
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    loaded = load_preferences(args.project)
    pref = loaded.values.get("preferred_raster_backend", "auto")
    backend_id, reason = resolve_backend(pref, args.backend)

    prompt_path = args.prompt_file
    prompt = _read_prompt(prompt_path)
    prefix = loaded.values.get("style_prefix") or ""
    if prefix:
        prompt = f"{prefix}\n\n{prompt}"

    aspect = args.aspect or "16:9"
    size = ASPECT_TO_SIZE.get(aspect, ASPECT_TO_SIZE["16:9"])

    receipt = {
        "backend": backend_id,
        "reason": reason,
        "prompt_file": str(prompt_path),
        "output": str(args.output),
        "aspect": aspect,
        "size": size,
        "dry_run": args.dry_run,
    }

    if backend_id == "agent-native":
        receipt["action"] = "Agent must call the host image tool with the prompt file. No HTTP call from this script."
        print(json.dumps(receipt, indent=2))
        return 0

    if backend_id in ("codex-cli", "local-vector"):
        receipt["action"] = f"Backend {backend_id} is not driven by this script. See references/raster-python.md."
        print(json.dumps(receipt, indent=2))
        return 0

    if args.dry_run:
        print(json.dumps(receipt, indent=2))
        return 0

    refuse_overwrite(args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    if backend_id == "openai":
        model = args.model or loaded.values.get("openai_model", "gpt-image-1")
        raw = _openai_images(prompt, model, size)
    elif backend_id == "openrouter":
        model = args.model or loaded.values.get("openrouter_model", "google/gemini-2.5-flash-image-preview")
        raw = _openrouter_images(prompt, model, size)
    else:
        print(f"unsupported backend for generate: {backend_id}", file=sys.stderr)
        return 2

    args.output.write_bytes(raw)
    receipt["bytes"] = len(raw)
    receipt["model"] = model
    print(json.dumps(receipt, indent=2))
    return 0


def cmd_batch(args: argparse.Namespace) -> int:
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, list):
        raise ValueError("batch manifest must be a JSON array")
    loaded = load_preferences(args.project)
    batch_size = int(loaded.values.get("generation_batch_size", 4))
    if args.batch_size:
        batch_size = args.batch_size

    results = []
    for index, item in enumerate(manifest):
        if not isinstance(item, dict):
            raise ValueError(f"batch item {index} must be an object")
        prompt_file = Path(item["prompt_file"])
        output = Path(item["output"])
        aspect = item.get("aspect", "16:9")
        backend = item.get("backend")
        ns = argparse.Namespace(
            project=args.project,
            prompt_file=prompt_file,
            output=output,
            aspect=aspect,
            backend=backend,
            model=item.get("model"),
            dry_run=args.dry_run,
        )
        code = cmd_generate(ns)
        results.append({"prompt_file": str(prompt_file), "output": str(output), "exit": code})
        if code and not args.continue_on_error:
            break
        if (index + 1) % batch_size == 0 and not args.dry_run:
            pass  # sequential batches; parallel is agent responsibility
    print(json.dumps({"results": results}, indent=2))
    return 0 if all(r["exit"] == 0 for r in results) else 2


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=None, help="Project root for preference search")
    sub = parser.add_subparsers(dest="command", required=True)

    prefs = sub.add_parser("prefs", help="preference helpers")
    prefs_sub = prefs.add_subparsers(dest="prefs_cmd", required=True)
    p_path = prefs_sub.add_parser("path", help="print path to loaded prefs or exit 1")
    p_path.set_defaults(func=cmd_prefs_path)
    p_show = prefs_sub.add_parser("show", help="print merged preferences JSON")
    p_show.set_defaults(func=cmd_prefs_show)
    p_init = prefs_sub.add_parser("init", help="write template infographic.prefs.json")
    p_init.add_argument("--output", type=Path, default=None)
    p_init.set_defaults(func=cmd_prefs_init)

    backends = sub.add_parser("backends", help="list raster backends")
    backends.add_argument("--json", action="store_true")
    backends.set_defaults(func=cmd_backends)

    resolve_p = sub.add_parser("resolve", help="resolve backend from prefs and env")
    resolve_p.add_argument("--backend", default=None)
    resolve_p.set_defaults(func=cmd_resolve)

    gen = sub.add_parser("generate", help="generate PNG via API backend or print agent receipt")
    gen.add_argument("--prompt-file", type=Path, required=True)
    gen.add_argument("--output", type=Path, required=True)
    gen.add_argument("--aspect", default="16:9")
    gen.add_argument("--backend", default=None)
    gen.add_argument("--model", default=None)
    gen.add_argument("--dry-run", action="store_true")
    gen.set_defaults(func=cmd_generate)

    batch = sub.add_parser("batch", help="run generate for each manifest entry (sequential)")
    batch.add_argument("manifest", type=Path)
    batch.add_argument("--dry-run", action="store_true")
    batch.add_argument("--batch-size", type=int, default=None)
    batch.add_argument("--continue-on-error", action="store_true")
    batch.set_defaults(func=cmd_batch)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, RuntimeError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
