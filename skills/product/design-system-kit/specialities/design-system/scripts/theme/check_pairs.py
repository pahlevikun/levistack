"""Measure foreground and background pairs. Standard library only.

This is the single contrast gate for the product skills. A pairs file is a CSV with the columns
name,fg,bg,need and an optional mode column. fg and bg are hex colors (#RGB, #RRGGBB or
#RRGGBBAA) or semantic token names that are looked up in a tokens.json made by theme.py build.
A color with alpha is composited over its background before it is measured, so the result is
the pair as it renders.
"""

import csv
import json

from oklch import apca, contrast


def _hex_parts(h):
    h = h.strip().lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    if len(h) not in (6, 8) or any(c not in "0123456789abcdefABCDEF" for c in h):
        raise ValueError("not a hex color: %r" % h)
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return rgb, alpha


def composite(fg, bg):
    """Return fg over bg as #RRGGBB. bg must be opaque (alpha is ignored)."""
    (fr, fg_, fb), a = _hex_parts(fg)
    (br, bg_, bb), _ = _hex_parts(bg)
    if a >= 0.999:
        return "#%02X%02X%02X" % (fr, fg_, fb)
    mix = lambda f, b: round(f * a + b * (1 - a))  # noqa: E731
    return "#%02X%02X%02X" % (mix(fr, br), mix(fg_, bg_), mix(fb, bb))


def load_tokens(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    light = {k: v["$value"] for k, v in data.get("semantic", {}).get("color", {}).items()}
    dark = {k: v["$value"] for k, v in data.get("dark", {}).get("semantic", {}).get("color", {}).items()}
    return {"light": light, "dark": dark}


def resolve(value, table):
    value = value.strip()
    if value.startswith("#"):
        return value
    if value in table:
        return table[value]
    raise KeyError("unknown token or color: %s" % value)


def measure(rows, tokens=None, default_mode="light"):
    out = []
    for row in rows:
        mode = (row.get("mode") or default_mode).strip() or default_mode
        table = (tokens or {}).get(mode, {})
        name = row["name"].strip()
        try:
            need = float(row.get("need") or 4.5)
        except ValueError:
            out.append({"name": name, "mode": mode, "fg": row.get("fg"), "bg": row.get("bg"), "shown_fg": None, "shown_bg": None,
                        "ratio": None, "need": 0.0, "apca": None, "pass": False, "error": "need must be a number, got %r" % row.get("need")})
            continue
        try:
            bg = resolve(row["bg"], table)
            fg = resolve(row["fg"], table)
            # A translucent ground is composited over the page ground of its own mode.
            base = table.get("background") or ("#000000" if mode == "dark" else "#FFFFFF")
            bg_solid = composite(bg, base) if len(bg.lstrip("#")) in (4, 8) else bg
            fg_solid = composite(fg, bg_solid)
            ratio = contrast(fg_solid, bg_solid)
            out.append({"name": name, "mode": mode, "fg": fg, "bg": bg, "shown_fg": fg_solid, "shown_bg": bg_solid,
                        "ratio": round(ratio, 2), "need": need, "apca": round(abs(apca(fg_solid, bg_solid)), 1),
                        "pass": ratio >= need, "error": None})
        except (KeyError, ValueError) as e:
            out.append({"name": name, "mode": mode, "fg": row.get("fg"), "bg": row.get("bg"), "shown_fg": None, "shown_bg": None,
                        "ratio": None, "need": need, "apca": None, "pass": False, "error": str(e)})
    return out


def read_pairs(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = [h.strip() for h in (reader.fieldnames or [])]
        for col in ("name", "fg", "bg"):
            if col not in header:
                raise ValueError("pairs file needs the header name,fg,bg,need (missing %s). Found: %s" % (col, ", ".join(header) or "nothing"))
        reader.fieldnames = header
        rows = [r for r in reader if r.get("name") and not r["name"].startswith("#")]
    if not rows:
        raise ValueError("pairs file has no rows")
    return rows


def to_markdown(results):
    fails = [r for r in results if not r["pass"]]
    lines = ["# Contrast report", "", "%d pairs, %d failing." % (len(results), len(fails)), "",
             "| Pair | Mode | Foreground | Background | Ratio | Need | APCA Lc | Result |", "|---|---|---|---|---:|---:|---:|---|"]
    for r in results:
        if r["error"]:
            lines.append("| %s | %s | %s | %s | - | %.1f | - | **ERROR** %s |" % (r["name"], r["mode"], r["fg"], r["bg"], r["need"], r["error"]))
            continue
        shown = r["shown_fg"] if r["shown_fg"] != r["fg"] else r["fg"]
        lines.append("| %s | %s | %s | %s | %.2f | %.1f | %.0f | %s |" % (
            r["name"], r["mode"], shown, r["shown_bg"], r["ratio"], r["need"], r["apca"], "pass" if r["pass"] else "**FAIL**"))
    lines += ["", "A color with alpha is shown as it renders over its background. APCA Lc is advice: body text wants 75 or more, large text 60 or more."]
    return "\n".join(lines) + "\n"
