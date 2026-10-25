"""Find every color literal in a project and group the near duplicates. Standard library only.

Reads CSS, SCSS, JS, TS, JSX, TSX, Vue, Svelte, HTML, XML, Swift, Kotlin, Dart and JSON-like theme
files. It reports facts (counts, files, clusters). It never edits a file, and it never decides which
duplicate to keep. That is a proposal for a person to accept.
"""

import os
import re
from collections import Counter, defaultdict

from oklch import delta_ok, hex_to_oklch, oklch_to_hex, rgb_to_hex

EXTS = {".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".html", ".htm", ".xml",
        ".swift", ".kt", ".kts", ".dart", ".json", ".astro"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", "Pods", ".gradle", ".dart_tool", "DerivedData",
             "coverage", "scratch", ".venv", "venv", "__pycache__", "vendor", ".idea", "out"}
TOKEN_FILE_HINT = re.compile(r"(theme|token|color|colour|palette|variables|design-system|styles?\.css|colors\.xml|colors\.kt|colors\.dart)", re.I)

HEX = re.compile(r"(?<![\w&/#-])#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![\w-])")
FUNC = re.compile(r"\b(rgba?|hsla?|oklch)\(\s*([^)]*)\)", re.I)
ANDROID = re.compile(r"\bColor\(\s*0x([0-9a-fA-F]{2})([0-9a-fA-F]{6})\s*\)")


def _norm_hex(h, android_order=False):
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 8 and android_order:  # Android resources write #AARRGGBB
        return "#" + h[2:8].upper()
    return "#" + h[:6].upper()


def _func_to_hex(name, body):
    import colorsys
    nums = re.findall(r"[-\d.]+%?", body)
    try:
        if name.lower().startswith("rgb") and len(nums) >= 3:
            vals = []
            for n in nums[:3]:
                vals.append(float(n[:-1]) / 100 if n.endswith("%") else float(n) / 255)
            return rgb_to_hex(vals)
        if name.lower().startswith("hsl") and len(nums) >= 3:
            h, s, l = float(nums[0]) / 360, float(nums[1].rstrip("%")) / 100, float(nums[2].rstrip("%")) / 100
            return rgb_to_hex(colorsys.hls_to_rgb(h, l, s))
        if name.lower() == "oklch" and len(nums) >= 3:
            L = float(nums[0][:-1]) / 100 if nums[0].endswith("%") else float(nums[0])
            return oklch_to_hex(L, float(nums[1]), float(nums[2]))
    except ValueError:
        return None
    return None


def scan_text(text, android_order=False):
    found = [_norm_hex(m.group(1), android_order) for m in HEX.finditer(text)]
    for m in FUNC.finditer(text):
        h = _func_to_hex(m.group(1), m.group(2))
        if h:
            found.append(h)
    for m in ANDROID.finditer(text):
        found.append("#" + m.group(2).upper())
    return found


def walk(root, max_files=5000):
    n = 0
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            if os.path.splitext(name)[1].lower() in EXTS:
                n += 1
                if n > max_files:
                    return
                yield os.path.join(base, name)


def audit(root, near=0.02):
    by_color = defaultdict(Counter)
    token_hits, other_hits = Counter(), Counter()
    scanned = 0
    for path in walk(root):
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                text = f.read(400000)
        except OSError:
            continue
        scanned += 1
        rel = os.path.relpath(path, root)
        colors = scan_text(text, android_order=path.lower().endswith(".xml"))
        is_token_file = bool(TOKEN_FILE_HINT.search(rel))
        for c in colors:
            by_color[c][rel] += 1
            (token_hits if is_token_file else other_hits)[c] += 1
    total = sum(sum(files.values()) for files in by_color.values())
    ranked = sorted(by_color, key=lambda c: -sum(by_color[c].values()))
    clusters = []
    for c in ranked:
        for cl in clusters:
            if delta_ok(c, cl["lead"]) < near:
                cl["members"].append(c)
                break
        else:
            clusters.append({"lead": c, "members": [c]})
    out = []
    for cl in clusters:
        files = Counter()
        count = 0
        for m in cl["members"]:
            files.update(by_color[m])
            count += sum(by_color[m].values())
        L, C, H = hex_to_oklch(cl["lead"])
        out.append({"lead": cl["lead"], "members": cl["members"], "count": count, "files": files.most_common(3),
                    "L": round(L, 3), "C": round(C, 3), "H": round(H, 1), "neutral": C < 0.035,
                    "outside_token_files": sum(other_hits[m] for m in cl["members"])})
    out.sort(key=lambda x: -x["count"])
    return {"root": root, "files_scanned": scanned, "literals": total, "unique": len(by_color), "clusters": out}


def to_markdown(rep, limit=40):
    chroma = [c for c in rep["clusters"] if not c["neutral"]]
    neutral = [c for c in rep["clusters"] if c["neutral"]]
    dup = [c for c in rep["clusters"] if len(c["members"]) > 1]
    lines = ["# Color audit", "", "Scanned %d files. Found %d literals, %d unique colors, %d groups after merging near duplicates (OKLab distance under 0.02)." % (
        rep["files_scanned"], rep["literals"], rep["unique"], len(rep["clusters"])), "",
        "- Chromatic groups: %d. Neutral groups: %d." % (len(chroma), len(neutral)),
        "- Groups that hide near duplicates: %d. Each is one color that drifted." % len(dup),
        "- Literals outside token and theme files: %d. These bypass the system." % sum(c["outside_token_files"] for c in rep["clusters"]), "",
        "| Color | Uses | Outside token files | Merged from | OKLCH (L C H) | Top files |", "|---|---:|---:|---|---|---|"]
    for c in rep["clusters"][:limit]:
        merged = ", ".join(c["members"][1:4]) + (" ..." if len(c["members"]) > 4 else "") if len(c["members"]) > 1 else "-"
        top = "; ".join("%s (%d)" % f for f in c["files"])
        lines.append("| %s | %d | %d | %s | %.2f %.3f %.0f | %s |" % (c["lead"], c["count"], c["outside_token_files"], merged, c["L"], c["C"], c["H"], top))
    if len(rep["clusters"]) > limit:
        lines.append("| ... | | | %d more groups | | |" % (len(rep["clusters"]) - limit))
    lines += ["", "Next: give every surviving group a role (see the role inventory), keep the most used color of each duplicate group, and retire the rest.",
              "Do not average duplicates. Report this table before changing anything."]
    return "\n".join(lines) + "\n"
