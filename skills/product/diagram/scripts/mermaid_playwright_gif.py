#!/usr/bin/env python3
"""Mermaid to GIF via Playwright frame capture and FFmpeg."""

from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from mermaid_blocks import read_diagrams, refuse_overwrite
from mermaid_playwright_styles import ELEMENT_COLLECTION, STYLE_BODY, STYLES

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"


def require_tools() -> None:
    missing: list[str] = []
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg")
    try:
        import playwright  # noqa: F401
    except ImportError:
        missing.append("playwright (pip install playwright && playwright install chromium)")
    if missing:
        raise ValueError("missing tools: " + ", ".join(missing))


def flow_direction(code: str) -> str:
    head = code.strip().split("\n", 1)[0].lower()
    return "horizontal" if any(x in head for x in (" lr", " rl", "graph lr", "graph rl")) else "vertical"


def build_html(code: str, style: str, theme: str, bg: str, padding: int, extra_css: str) -> str:
    driver = STYLE_BODY.get(style)
    if not driver:
        raise ValueError(f"unknown style: {style}")
    collection = ELEMENT_COLLECTION.replace("{direction}", flow_direction(code))
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="{MERMAID_CDN}"></script>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: {bg}; display: inline-block; padding: {padding}px; }}
  .mermaid svg {{ display: block; }}
  {extra_css}
</style></head><body>
<pre class="mermaid">{html.escape(code)}</pre>
<script>
(async function() {{
  mermaid.initialize({{ startOnLoad: false, theme: '{theme}', securityLevel: 'strict' }});
  try {{ await mermaid.run(); }} catch (e) {{ console.error(e); }}
  var svg = document.querySelector('svg');
  if (!svg) {{ window.setProgress = function() {{}}; window.animationReady = true; return; }}
  var rect = svg.getBoundingClientRect();
  if (rect.width > 0 && rect.width < 700) {{
    var ratio = 700 / rect.width;
    var w = Math.ceil(rect.width * ratio), h = Math.ceil(rect.height * ratio);
    svg.setAttribute('width', w); svg.setAttribute('height', h);
    svg.style.width = w + 'px'; svg.style.height = h + 'px';
  }}
  {collection}
  {driver}
  window.setProgress(0);
  window.animationReady = true;
}})();
</script></body></html>"""


def _ffmpeg(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or cmd[0])


def capture_frames(html_path: Path, frames_dir: Path, fps: int, duration: float, hold: float, scale: int) -> None:
    from playwright.sync_api import sync_playwright

    anim = max(1, int(fps * duration))
    hold_frames = int(fps * hold)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(device_scale_factor=scale)
        page = context.new_page()
        page.set_viewport_size({"width": 1400, "height": 900})
        page.goto(html_path.as_uri())
        page.wait_for_function("window.animationReady === true", timeout=30000)
        size = page.evaluate(
            """() => {
            const svg = document.querySelector('svg');
            if (!svg) return { width: 800, height: 400 };
            const rect = svg.getBoundingClientRect();
            const pad = parseFloat(getComputedStyle(document.body).padding) || 0;
            return { width: Math.ceil(rect.width + pad * 2), height: Math.ceil(rect.height + pad * 2) };
        }"""
        )
        page.set_viewport_size({
            "width": max(400, min(size["width"], 2400)),
            "height": max(200, min(size["height"], 1600)),
        })
        for i in range(anim + 1):
            page.evaluate(f"window.setProgress({i / anim})")
            page.screenshot(path=str(frames_dir / f"frame_{i:04d}.png"))
        last = anim
        for _ in range(hold_frames):
            last += 1
            page.screenshot(path=str(frames_dir / f"frame_{last:04d}.png"))
        context.close()
        browser.close()


def assemble_gif(frames_dir: Path, output: Path, fps: int, loop: int) -> None:
    palette = frames_dir / "palette.png"
    pattern = str(frames_dir / "frame_%04d.png")
    _ffmpeg(["ffmpeg", "-y", "-framerate", str(fps), "-i", pattern, "-vf", "palettegen=stats_mode=diff", str(palette)])
    _ffmpeg([
        "ffmpeg", "-y", "-framerate", str(fps), "-i", pattern, "-i", str(palette),
        "-lavfi", "paletteuse=dither=floyd_steinberg", "-loop", str(loop), str(output),
    ])


def render_gif(
    name: str,
    code: str,
    output_dir: Path,
    *,
    style: str,
    theme: str,
    bg: str,
    padding: int,
    fps: int,
    duration: float,
    hold: float,
    loop: int,
    scale: int,
    extra_css: str,
) -> Path:
    output = output_dir / f"{name}.gif"
    refuse_overwrite(output)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        html_path = root / "page.html"
        html_path.write_text(
            build_html(code, style, theme, bg, padding, extra_css), encoding="utf-8",
        )
        frames_dir = root / "frames"
        frames_dir.mkdir()
        capture_frames(html_path, frames_dir, fps, duration, hold, scale)
        assemble_gif(frames_dir, output, fps, loop)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Animated GIF from Mermaid via Playwright.")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("-o", "--output-dir", type=Path)
    parser.add_argument("-s", "--style", choices=STYLES, default="progressive")
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--duration", type=float, default=4.0)
    parser.add_argument("--hold", type=float, default=1.0)
    parser.add_argument("--theme", default="default")
    parser.add_argument("--bg", default="#ffffff")
    parser.add_argument("--padding", type=int, default=40)
    parser.add_argument("--scale", type=int, default=2)
    parser.add_argument("--custom-css", type=Path)
    parser.add_argument("--no-loop", action="store_true")
    parser.add_argument("--allow-network", action="store_true")
    args = parser.parse_args(argv)

    if not args.allow_network:
        print("Error: pass --allow-network to load Mermaid.js from the CDN.", file=sys.stderr)
        return 2
    try:
        require_tools()
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    extra_css = args.custom_css.read_text(encoding="utf-8") if args.custom_css else ""
    loop = 1 if args.no_loop else 0
    count = 0

    for input_path in args.inputs:
        out_dir = args.output_dir or input_path.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        for block in read_diagrams(input_path):
            path = render_gif(
                block.name,
                block.code,
                out_dir,
                style=args.style,
                theme=args.theme,
                bg=args.bg,
                padding=args.padding,
                fps=args.fps,
                duration=args.duration,
                hold=args.hold,
                loop=loop,
                scale=args.scale,
                extra_css=extra_css,
            )
            count += 1
            print(path)

    return 0 if count else 1


if __name__ == "__main__":
    raise SystemExit(main())
