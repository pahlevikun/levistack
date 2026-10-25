#!/usr/bin/env python3
"""Extract the design language of a live website (or a saved HTML file) into JSON and a faithful DESIGN.md.

Standard library only. It reads the HTML, follows linked and inline CSS, and counts colors, fonts,
sizes, radii, shadows, spacing and motion. It does NOT run JavaScript, so a page whose styles are
built in the browser (CSS-in-JS, some SPAs) will look thin. For those, run extract-in-browser.js in
the page and pass its JSON with --browser-json.

  extract_site.py https://example.com --out extracted.json --design-md extracted-DESIGN.md
  extract_site.py --html saved.html --base https://example.com --out extracted.json
  extract_site.py --browser-json browser.json --out extracted.json
"""

import argparse
import colorsys
import json
import math
import os
import re
import statistics
import sys
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from oklch import contrast, delta_ok, hex_to_oklch, oklch_to_hex, rgb_to_hex  # noqa: E402

UA = "Mozilla/5.0 (compatible; design-system-kit/1.0)"
MAX_BYTES = 2_000_000
NAMED = {"white": "#FFFFFF", "black": "#000000"}
GENERIC_FONTS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace", "ui-rounded",
                 "inherit", "initial", "unset", "-apple-system", "blinkmacsystemfont", "segoe ui", "roboto", "helvetica neue", "helvetica", "arial", "emoji", "math"}


def fetch(url, timeout=15):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("only http and https URLs are allowed: %s" % url)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/css,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 - scheme checked above
        data = r.read(MAX_BYTES)
        charset = r.headers.get_content_charset() or "utf-8"
    return data.decode(charset, errors="replace")


# ---------- color parsing ----------

HEX = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b")
RGB = re.compile(r"rgba?\(\s*([\d.]+%?)[\s,]+([\d.]+%?)[\s,]+([\d.]+%?)(?:[\s,/]+([\d.]+%?))?\s*\)", re.I)
HSL = re.compile(r"hsla?\(\s*([\d.]+)(?:deg)?[\s,]+([\d.]+)%[\s,]+([\d.]+)%(?:[\s,/]+([\d.]+%?))?\s*\)", re.I)
OKL = re.compile(r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)(?:deg)?(?:\s*/\s*([\d.]+%?))?\s*\)", re.I)


def _num(v):
    return float(v[:-1]) / 100 if v.endswith("%") else float(v)


def parse_colors(value):
    """Return a list of (hex, alpha) found in a CSS value."""
    out = []
    for m in HEX.finditer(value):
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        out.append(("#" + h[:6].upper(), a))
    for m in RGB.finditer(value):
        r, g, b = (_num(m.group(i)) for i in (1, 2, 3))
        if "%" not in m.group(1):
            r, g, b = r / 255, g / 255, b / 255
        a = _num(m.group(4)) if m.group(4) else 1.0
        out.append((rgb_to_hex((r, g, b)), a))
    for m in HSL.finditer(value):
        h, s, l = float(m.group(1)) / 360, float(m.group(2)) / 100, float(m.group(3)) / 100
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        a = _num(m.group(4)) if m.group(4) else 1.0
        out.append((rgb_to_hex((r, g, b)), a))
    for m in OKL.finditer(value):
        L = _num(m.group(1))
        out.append((oklch_to_hex(L, float(m.group(2)), float(m.group(3))), _num(m.group(4)) if m.group(4) else 1.0))
    for name, hx in NAMED.items():
        if re.search(r"(?<![\w-])%s(?![\w-])" % name, value, re.I):
            out.append((hx, 1.0))
    return out


# ---------- css scanning ----------

COMMENT = re.compile(r"/\*.*?\*/", re.S)
DECL = re.compile(r"([a-zA-Z\-]+)\s*:\s*([^;{}]+)")
LENGTH = re.compile(r"(-?[\d.]+)(px|rem|em)\b")
TIME = re.compile(r"(-?[\d.]+)(ms|s)\b")
CUBIC = re.compile(r"cubic-bezier\(([^)]*)\)")


def to_px(num, unit):
    v = float(num)
    return v if unit == "px" else v * 16


def collect_css(html, base):
    css = [("inline-style-tag", m.group(1)) for m in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)]
    css += [("inline-attr", m.group(1)) for m in re.finditer(r'\sstyle="([^"]*)"', html, re.I)]
    links = []
    for m in re.finditer(r"<link\b[^>]*>", html, re.I):
        tag = m.group(0)
        if re.search(r'rel=["\']?(?:[^"\' >]*\s)?stylesheet', tag, re.I):
            h = re.search(r'href=["\']([^"\']+)["\']', tag, re.I)
            if h:
                links.append(urllib.parse.urljoin(base, h.group(1)))
    fonts = []
    for u in links:
        if "fonts.googleapis.com" in u:
            for fam in re.findall(r"family=([^:&]+)", u):
                fonts.append(urllib.parse.unquote_plus(fam))
    return css, [u for u in links if "fonts.googleapis.com" not in u], fonts


def read_stylesheets(urls, limit, notes):
    out, seen = [], set()
    queue = list(urls)
    while queue and len(out) < limit:
        u = queue.pop(0)
        if u in seen:
            continue
        seen.add(u)
        try:
            text = fetch(u)
        except Exception as e:  # noqa: BLE001 - report and continue
            notes.append("could not fetch %s (%s)" % (u, type(e).__name__))
            continue
        out.append(("sheet", text))
        for m in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", text):
            queue.append(urllib.parse.urljoin(u, m.group(1)))
    return out


def analyze(css_blobs, html):
    colors = defaultdict(Counter)  # hex -> bucket -> weight
    fonts, sizes, weights, radii, shadows, gaps = Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    durations, easings, linehs = [], Counter(), []
    custom = {}
    face_families = set()
    dark_media = False

    text = "\n".join(COMMENT.sub("", b) for _, b in css_blobs)
    if re.search(r"prefers-color-scheme\s*:\s*dark", text):
        dark_media = True
    for m in re.finditer(r"@font-face\s*{[^}]*font-family\s*:\s*['\"]?([^;'\"}]+)", text):
        face_families.add(m.group(1).strip())
    for prop, value in DECL.findall(text):
        prop = prop.lower()
        value = value.strip()
        if prop.startswith("--"):
            custom[prop] = value
    for prop, value in DECL.findall(text):
        prop = prop.lower()
        value = value.strip()
        if prop.startswith("--"):
            bucket = "token"
        elif prop == "color":
            bucket = "text"
        elif prop.startswith("background"):
            bucket = "bg"
        elif prop.startswith("border") or prop.startswith("outline"):
            bucket = "border"
        elif prop in ("fill", "stroke"):
            bucket = "icon"
        else:
            bucket = None
        if "var(" in value:
            for vm in re.finditer(r"var\((--[\w-]+)", value):
                if vm.group(1) in custom:
                    value = value.replace(vm.group(0), custom[vm.group(1)], 1)
        if bucket:
            for hx, a in parse_colors(value):
                if a >= 0.5:
                    colors[hx][bucket] += 1
        if prop == "font-family":
            first = value.split(",")[0].strip().strip("'\"")
            if first and first.lower() not in GENERIC_FONTS and not first.startswith("var("):
                fonts[first] += 1
        elif prop == "font-size":
            m = LENGTH.search(value)
            if m:
                sizes[round(to_px(m.group(1), m.group(2)), 1)] += 1
        elif prop == "font-weight":
            if value.isdigit():
                weights[int(value)] += 1
            elif value in ("bold", "bolder"):
                weights[700] += 1
        elif prop == "line-height":
            if re.fullmatch(r"[\d.]+", value):
                linehs.append(float(value))
        elif prop.startswith("border") and "radius" in prop:
            for m in LENGTH.finditer(value):
                radii[round(to_px(m.group(1), m.group(2)))] += 1
            if "%" in value and "50%" in value:
                radii[9999] += 1
        elif prop == "box-shadow" and value.lower() != "none":
            shadows[re.sub(r"\s+", " ", value)[:120]] += 1
        elif prop in ("padding", "margin", "gap", "row-gap", "column-gap") or prop.startswith(("padding-", "margin-")):
            for m in LENGTH.finditer(value):
                px = to_px(m.group(1), m.group(2))
                if 0 < px <= 160:
                    gaps[round(px)] += 1
        elif prop.startswith(("transition", "animation")):
            for m in TIME.finditer(value):
                ms = float(m.group(1)) * (1000 if m.group(2) == "s" else 1)
                if 0 < ms <= 3000:
                    durations.append(ms)
            for m in CUBIC.finditer(value):
                easings["cubic-bezier(%s)" % re.sub(r"\s+", "", m.group(1))] += 1
            for kw in ("ease-in-out", "ease-out", "ease-in", "linear"):
                if re.search(r"(?<![\w-])%s(?![\w-])" % kw, value):
                    easings[kw] += 1

    for m in re.finditer(r'<meta[^>]+name=["\']theme-color["\'][^>]+content=["\']([^"\']+)', html, re.I):
        for hx, _ in parse_colors(m.group(1)):
            colors[hx]["token"] += 3
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', html, re.I)
    return {
        "colors": colors, "fonts": fonts, "face_families": sorted(face_families), "sizes": sizes, "weights": weights, "radii": radii,
        "shadows": shadows, "gaps": gaps, "durations": durations, "easings": easings, "line_heights": linehs,
        "custom_props": {k: v for k, v in list(custom.items())[:80]}, "dark_media": dark_media,
        "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else "", "description": desc.group(1).strip() if desc else "",
    }


def cluster_colors(colors):
    """Merge near-identical colors. Returns a list of dicts sorted by total weight."""
    items = sorted(((hx, sum(b.values()), b) for hx, b in colors.items()), key=lambda x: -x[1])
    clusters = []
    for hx, w, b in items:
        for c in clusters:
            if delta_ok(hx, c["hex"]) < 0.025:
                c["weight"] += w
                for k, v in b.items():
                    c["buckets"][k] += v
                break
        else:
            clusters.append({"hex": hx, "weight": w, "buckets": Counter(b)})
    for c in clusters:
        L, C, H = hex_to_oklch(c["hex"])
        c.update({"L": round(L, 3), "C": round(C, 3), "H": round(H, 1), "neutral": C < 0.035})
    return sorted(clusters, key=lambda c: -c["weight"])


def guess(a, clusters):
    chroma = [c for c in clusters if not c["neutral"] and 0.12 < c["L"] < 0.97]
    neutrals = [c for c in clusters if c["neutral"]]
    # brand = used a lot AND colorful. Weight chroma so a loud button color beats a common pale tint.
    chroma.sort(key=lambda c: -(c["weight"] * (0.4 + c["C"] * 4)))
    s = {}
    primary = chroma[0] if chroma else None
    if primary:
        s["hue"], s["chroma"] = primary["H"], round(max(0.05, min(0.21, primary["C"])), 3)
        second = next((c for c in chroma[1:] if min((c["H"] - primary["H"]) % 360, (primary["H"] - c["H"]) % 360) > 25), None)
        if second:
            s["secondary_hue"] = second["H"]
    mid_neutrals = [c for c in neutrals if 0.3 < c["L"] < 0.97] or neutrals
    if mid_neutrals:
        n = max(mid_neutrals, key=lambda c: c["weight"])
        s["neutral_hue"], s["neutral_chroma"] = n["H"], round(max(0.003, n["C"]), 3)
    bg = [c for c in clusters if "bg" in c["buckets"]]
    if bg:
        top = max(bg, key=lambda c: c["buckets"]["bg"])
        s["ground"] = "dark" if top["L"] < 0.4 else ("soft" if top["L"] < 0.97 else "light")
    if a["radii"]:
        total = sum(a["radii"].values())
        pill = a["radii"].get(9999, 0) + sum(v for k, v in a["radii"].items() if k >= 100)
        med = statistics.median([k for k, v in a["radii"].items() if k < 100 for _ in range(v)] or [0])
        s["shape"] = "pill" if pill / total > 0.35 else "sharp" if med == 0 else "crisp" if med <= 6 else "soft" if med <= 16 else "pebble"
    else:
        s["shape"] = "crisp"
    if a["gaps"]:
        pads = [k for k, v in a["gaps"].items() for _ in range(min(v, 50))]
        med = statistics.median(pads)
        s["density"] = "dense" if med <= 10 else "airy" if med >= 20 else "balanced"
    if a["fonts"]:
        top = a["fonts"].most_common(1)[0][0]
        s["font_display"] = top
        key = top.lower()
        s["voice"] = ("friendly-humanist" if any(x in key for x in ("nunito", "quicksand", "rounded")) else
                      "classic-serif" if any(x in key for x in ("serif", "georgia", "garamond", "times", "newsreader", "lora", "merriweather")) and "sans" not in key else
                      "editorial-warm" if any(x in key for x in ("fraunces", "recoleta", "canela", "tiempos")) else
                      "data-dense" if any(x in key for x in ("plex", "mono", "courier", "code")) else
                      "geometric-modern" if any(x in key for x in ("jakarta", "poppins", "montserrat", "dm sans", "manrope", "circular", "gotham", "sf pro", "avenir", "futura")) else
                      "neutral-grotesk")
    if a["durations"]:
        med = statistics.median(a["durations"])
        bounce = any(any(float(x) > 1.0 or float(x) < 0 for x in re.findall(r"-?[\d.]+", k)[1:4:2]) for k in a["easings"] if k.startswith("cubic"))
        s["motion"] = "springy" if bounce else "snappy-tech" if med < 120 else "crisp" if med <= 320 else "calm-drift" if med <= 500 else "theatrical"
    else:
        s["motion"] = "still"
    s["source_note"] = "Guesses from static CSS. Confirm with the screenshots."
    return s


def build(url, html, css_blobs, notes, extra_fonts):
    a = analyze(css_blobs, html)
    clusters = cluster_colors(a["colors"])
    for f in extra_fonts:
        a["fonts"][f] += 5
    suggest = guess(a, clusters)
    if len(clusters) < 4:
        notes.append("Very few colors were found. The styles are probably built in the browser. Run extract-in-browser.js on the page and pass the result with --browser-json.")
    return {
        "source": url, "title": a["title"], "description": a["description"], "notes": notes,
        "colors": [{"hex": c["hex"], "weight": c["weight"], "L": c["L"], "C": c["C"], "H": c["H"], "neutral": c["neutral"],
                    "used_as": dict(c["buckets"].most_common())} for c in clusters[:24]],
        "fonts": a["fonts"].most_common(8), "font_faces": a["face_families"],
        "font_sizes": sorted(a["sizes"].items()), "font_weights": sorted(a["weights"].items()),
        "radii": sorted(a["radii"].items()), "shadows": a["shadows"].most_common(6),
        "spacing_px": sorted(a["gaps"].items()), "durations_ms": sorted(set(round(d) for d in a["durations"]))[:20],
        "easings": a["easings"].most_common(6), "dark_mode_in_css": a["dark_media"], "custom_properties": a["custom_props"],
        "suggest": suggest,
    }


def from_browser(path):
    with open(path, encoding="utf-8") as f:
        b = json.load(f)
    colors = defaultdict(Counter)
    for k, bucket in (("text", "text"), ("bg", "bg"), ("border", "border")):
        for hx, n in b.get(k, {}).items():
            colors[hx.upper()][bucket] += n
    fonts = Counter(b.get("fonts", {}))
    a = {"colors": colors, "fonts": fonts, "face_families": b.get("faces", []),
         "sizes": Counter({float(k): v for k, v in b.get("sizes", {}).items()}),
         "weights": Counter({int(k): v for k, v in b.get("weights", {}).items()}),
         "radii": Counter({int(float(k)): v for k, v in b.get("radii", {}).items()}),
         "shadows": Counter(b.get("shadows", {})), "gaps": Counter({int(float(k)): v for k, v in b.get("gaps", {}).items()}),
         "durations": [float(d) for d in b.get("durations", [])], "easings": Counter(b.get("easings", {})), "line_heights": [],
         "custom_props": b.get("custom_props", {}), "dark_media": bool(b.get("dark_media")), "title": b.get("title", ""), "description": ""}
    clusters = cluster_colors(a["colors"])
    return {
        "source": b.get("url", "browser"), "title": a["title"], "description": "", "notes": ["From the in-browser extractor (computed styles)."],
        "colors": [{"hex": c["hex"], "weight": c["weight"], "L": c["L"], "C": c["C"], "H": c["H"], "neutral": c["neutral"], "used_as": dict(c["buckets"].most_common())} for c in clusters[:24]],
        "fonts": a["fonts"].most_common(8), "font_faces": a["face_families"], "font_sizes": sorted(a["sizes"].items()), "font_weights": sorted(a["weights"].items()),
        "radii": sorted(a["radii"].items()), "shadows": a["shadows"].most_common(6), "spacing_px": sorted(a["gaps"].items()),
        "durations_ms": sorted(set(round(d) for d in a["durations"]))[:20], "easings": a["easings"].most_common(6), "dark_mode_in_css": a["dark_media"],
        "custom_properties": a["custom_props"], "suggest": guess(a, clusters),
    }


def faithful_design_md(ex):
    """Write what the site actually uses, with its exact values. No re-derivation."""
    cl = ex["colors"]
    chroma = [c for c in cl if not c["neutral"]]
    chroma.sort(key=lambda c: -(c["weight"] * (0.4 + c["C"] * 4)))
    neutrals = sorted([c for c in cl if c["neutral"]], key=lambda c: c["L"])
    text = next((c for c in sorted(cl, key=lambda c: -c["used_as"].get("text", 0)) if c["used_as"].get("text")), None)
    bg = next((c for c in sorted(cl, key=lambda c: -c["used_as"].get("bg", 0)) if c["used_as"].get("bg")), None)
    border = next((c for c in sorted(cl, key=lambda c: -c["used_as"].get("border", 0)) if c["used_as"].get("border")), None)
    bg_hex = bg["hex"] if bg else (neutrals[-1]["hex"] if neutrals else "#FFFFFF")
    text_hex = text["hex"] if text else (neutrals[0]["hex"] if neutrals else "#111111")
    primary = chroma[0]["hex"] if chroma else text_hex
    secondary = chroma[1]["hex"] if len(chroma) > 1 else primary
    on_primary = "#FFFFFF" if contrast("#FFFFFF", primary) >= contrast("#000000", primary) else "#000000"
    fonts = [f for f, _ in ex["fonts"]]
    display = fonts[0] if fonts else "system-ui"
    body = fonts[1] if len(fonts) > 1 else display
    sizes = [s for s, _ in ex["font_sizes"]]
    base = min(sizes, key=lambda s: abs(s - 16)) if sizes else 16
    big = max(sizes) if sizes else 40
    radii = [r for r, _ in ex["radii"] if r < 100]
    rmax = max(radii) if radii else 8
    name = (ex["title"] or ex["source"]).split("|")[0].split("-")[0].strip()[:40] or "Extracted site"

    def px(v):
        return "%gpx" % v
    fm = ['---', 'version: alpha', 'name: "%s (as found)"' % name.replace('"', ""), 'description: "Design language read from %s. Values are exactly as found; nothing was corrected."' % ex["source"].replace('"', ""),
          "colors:", '  neutral: "%s"' % bg_hex, '  on-surface: "%s"' % text_hex, '  primary: "%s"' % primary, '  on-primary: "%s"' % on_primary, '  secondary: "%s"' % secondary]
    if border:
        fm.append('  outline: "%s"' % border["hex"])
    fm += ["typography:", "  headline-lg:", '    fontFamily: "%s"' % display, "    fontSize: %s" % px(big), "    fontWeight: 700", "    lineHeight: 1.15",
           "  body-md:", '    fontFamily: "%s"' % body, "    fontSize: %s" % px(base), "    fontWeight: 400", "    lineHeight: 1.5",
           "rounded:", "  md: %s" % px(min(rmax, 12) if rmax else 8), "  lg: %s" % px(rmax if rmax else 8), "  full: 9999px", "---", ""]
    ratio = contrast(text_hex, bg_hex)
    body_md = ["# %s (as found)" % name, "", "## Overview", "", "This file records what %s uses today. %s" % (ex["source"], ex["description"] or ""), "",
               "## Colors", ""]
    for c in cl[:10]:
        body_md.append("- `%s` used %d times (%s)%s" % (c["hex"], c["weight"], ", ".join("%s %d" % kv for kv in list(c["used_as"].items())[:3]) or "token", " - neutral" if c["neutral"] else ""))
    body_md += ["", "Text on page ground: `%s` on `%s` = %.2f:1%s." % (text_hex, bg_hex, ratio, "" if ratio >= 4.5 else " (below the 4.5:1 AA target)"), "",
                "## Typography", "", "Fonts by use: %s." % (", ".join("%s (%d)" % f for f in ex["fonts"][:5]) or "none found"),
                "Sizes seen: %s px. Weights: %s." % (", ".join("%g" % s for s in sizes[:14]), ", ".join(str(w) for w, _ in ex["font_weights"]) or "n/a"), "",
                "## Layout", "", "Spacing values seen (px): %s." % ", ".join(str(k) for k, _ in ex["spacing_px"][:16]), "",
                "## Elevation & Depth", "", ("Shadows: " + "; ".join("`%s`" % s for s, _ in ex["shadows"][:3])) if ex["shadows"] else "No box shadows found. Depth comes from color and borders.", "",
                "## Shapes", "", "Radii seen (px): %s." % (", ".join(str(r) for r, _ in ex["radii"]) or "none"), "",
                "## Motion", "", "Durations seen (ms): %s. Easings: %s." % (", ".join(str(d) for d in ex["durations_ms"]) or "none", ", ".join(e for e, _ in ex["easings"][:3]) or "none"), "",
                "## Do's and Don'ts", "", "- Do treat this file as a record of the current state, not as a target.", "- Don't copy another company's brand. Use it to learn mechanics, then remix.", ""]
    return "\n".join(fm + body_md)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url", nargs="?")
    p.add_argument("--html", help="a saved HTML file instead of a URL")
    p.add_argument("--base", default="", help="base URL used to resolve links in --html")
    p.add_argument("--browser-json", help="JSON produced by extract-in-browser.js")
    p.add_argument("--out", default="extracted.json")
    p.add_argument("--design-md", help="also write a faithful DESIGN.md of the site as found")
    p.add_argument("--max-css", type=int, default=12)
    a = p.parse_args(argv)

    if a.browser_json:
        ex = from_browser(a.browser_json)
    else:
        notes = []
        if a.html:
            with open(a.html, encoding="utf-8", errors="replace") as f:
                html = f.read()
            base = a.base or "file://" + os.path.abspath(a.html)
        elif a.url:
            html, base = fetch(a.url), a.url
        else:
            p.error("give a URL, --html or --browser-json")
        blobs, links, gfonts = collect_css(html, base)
        blobs += read_stylesheets(links, a.max_css, notes)
        ex = build(base, html, blobs, notes, gfonts)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(ex, f, indent=2)
    print("wrote %s: %d colors, %d fonts, suggest %s" % (a.out, len(ex["colors"]), len(ex["fonts"]), {k: v for k, v in ex["suggest"].items() if k in ("hue", "chroma", "shape", "voice", "motion", "density", "ground")}))
    for n in ex["notes"]:
        print("note: " + n)
    if a.design_md:
        with open(a.design_md, "w", encoding="utf-8") as f:
            f.write(faithful_design_md(ex))
        print("wrote %s" % a.design_md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
