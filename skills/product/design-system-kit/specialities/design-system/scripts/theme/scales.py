"""Chart color scales built from rules: sequential, diverging and categorical. Standard library only."""

import itertools

from oklch import contrast, cvd, delta_ok, hex_to_oklch, oklch_to_hex, push_for_contrast
import names

KINDS = ("sequential", "diverging", "categorical")
GOLDEN = 137.508


def _bell(t):
    """Chroma follows a soft hill, so the ends stay calm and the middle carries the hue."""
    return 0.45 + 0.55 * (1 - abs(2 * t - 1) ** 1.6)


def sequential(hue, n=7, chroma=0.13, dark=False):
    """One hue from near the ground to the strongest end. Lightness moves one way and in even steps."""
    lo, hi = (0.30, 0.90) if dark else (0.96, 0.32)
    out = []
    for i in range(n):
        t = i / (n - 1)
        L = lo + (hi - lo) * t
        out.append(oklch_to_hex(L, chroma * _bell(t), (hue + 14 * t) % 360))
    return out


def diverging(hue_a, hue_b, n=9, chroma=0.13, dark=False):
    """Two hues meeting at a neutral middle. Both sides use the same lightness at the same distance,
    so the scale also reads in grayscale and for people who confuse the two hues."""
    n = n if n % 2 else n + 1
    mid = n // 2
    end_L, mid_L = (0.78, 0.28) if dark else (0.38, 0.95)
    out = []
    for i in range(n):
        d = abs(i - mid) / mid
        L = mid_L + (end_L - mid_L) * d
        hue = hue_a if i < mid else hue_b
        c = 0.01 if i == mid else chroma * (0.35 + 0.65 * d)
        out.append(oklch_to_hex(L, c, hue))
    return out


def categorical(hue, n=6, ground="#FFFFFF", chroma=0.13, dark=False, min_cvd=0.06, min_ratio=3.0):
    """Distinct marks. Build a pool of candidates (every 15 degrees of hue, four lightness bands), keep the
    ones that are visible on the ground, then pick one at a time the candidate farthest from those already
    chosen. Distance is the smallest of the normal view and the three color-blind views."""
    if n > 10:
        raise ValueError("more than 10 categories do not stay distinct. Group them, or label the marks directly")
    bands = [0.58, 0.68, 0.78, 0.88] if dark else [0.46, 0.56, 0.66, 0.76]
    pool = []
    for k in range(24):
        for L in bands:
            c = oklch_to_hex(L, chroma, (hue + 15 * k) % 360)
            if contrast(c, ground) >= min_ratio:
                pool.append(c)
    if len(pool) < n:
        pool = [push_for_contrast(oklch_to_hex(L, chroma, (hue + 15 * k) % 360), ground, min_ratio) for k in range(24) for L in bands]
    views = {c: [c] + [cvd(c, kind) for kind in ("protan", "deutan", "tritan")] for c in pool}

    def apart(a, b):
        return min(delta_ok(x, y) for x, y in zip(views[a], views[b]))

    chosen = [min(pool, key=lambda c: abs(((hex_to_oklch(c)[2] - hue + 180) % 360) - 180))]
    while len(chosen) < n:
        chosen.append(max((c for c in pool if c not in chosen), key=lambda c: min(apart(c, o) for o in chosen)))
    return chosen


def _worst_pair(cols):
    best = None
    for (i, a), (j, b) in itertools.combinations(enumerate(cols), 2):
        d = min([delta_ok(a, b)] + [delta_ok(cvd(a, k), cvd(b, k)) for k in ("protan", "deutan", "tritan")])
        if best is None or d < best[0]:
            best = (d, i, j)
    return best


def check(kind, cols, ground):
    """Plain facts about a scale, as (label, value, need, pass)."""
    rows = []
    lights = [hex_to_oklch(c)[0] for c in cols]
    if kind == "sequential":
        steps = [abs(b - a) for a, b in zip(lights, lights[1:])]
        rows.append(("smallest lightness step", round(min(steps), 3), 0.03, min(steps) >= 0.03))
        rows.append(("lightness moves one way", "yes" if all(b < a for a, b in zip(lights, lights[1:])) or all(b > a for a, b in zip(lights, lights[1:])) else "no", "yes", all(b < a for a, b in zip(lights, lights[1:])) or all(b > a for a, b in zip(lights, lights[1:]))))
    if kind == "diverging":
        mid = len(cols) // 2
        gap = max(abs(lights[mid - k] - lights[mid + k]) for k in range(1, mid + 1))
        rows.append(("largest lightness gap between mirrored steps", round(gap, 3), 0.02, gap <= 0.02))
    if kind == "categorical":
        worst = _worst_pair(cols)
        rows.append(("closest pair, normal and color-blind views (OKLab)", round(worst[0], 3), 0.06, worst[0] >= 0.06))
        low = min(contrast(c, ground) for c in cols)
        rows.append(("weakest mark on the ground", round(low, 2), 3.0, low >= 3.0))
    return rows


def to_markdown(kind, cols, ground, rows, hue, dark):
    out = ["# %s scale (%s ground %s, start hue %.0f)\n\n" % (kind.capitalize(), "dark" if dark else "light", ground, hue)]
    out.append("| # | Color | Name | Contrast on ground |\n|---:|---|---|---:|\n")
    for i, c in enumerate(cols, 1):
        out.append("| %d | %s | %s | %.2f |\n" % (i, c, names.describe(c), contrast(c, ground)))
    out.append("\n| Check | Value | Need | Result |\n|---|---:|---:|---|\n")
    for label, val, need, ok in rows:
        out.append("| %s | %s | %s | %s |\n" % (label, val, need, "pass" if ok else "**FAIL**"))
    out.append("\nSeparate touching marks with a 1 to 2 px stroke in the ground color. Label marks directly when you can, and add a pattern or a shape when two series must stay apart for everyone.\n")
    return "".join(out)
