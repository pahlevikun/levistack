"""Color math for the theme builder. Standard library only.

OKLab and OKLCH follow Bjorn Ottosson's published matrices. Contrast follows WCAG 2.x
(relative luminance) and APCA 0.0.98G (advisory). CVD simulation uses Machado 2009
matrices at full severity, applied in linear RGB.
"""

import math

# ---------- sRGB <-> linear ----------


def srgb_to_linear(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def linear_to_srgb(v):
    v = max(0.0, min(1.0, v))
    return 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join("%02X" % round(max(0, min(1, c)) * 255) for c in rgb)


# ---------- OKLab / OKLCH ----------


def linear_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def oklab_to_linear(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_oklab(L, C, H):
    h = math.radians(H)
    return L, C * math.cos(h), C * math.sin(h)


def oklab_to_oklch(L, a, b):
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360 if C > 1e-7 else 0.0
    return L, C, H


def hex_to_oklch(h):
    r, g, b = (srgb_to_linear(c) for c in hex_to_rgb(h))
    return oklab_to_oklch(*linear_to_oklab(r, g, b))


def _linear_rgb_of(L, C, H):
    return oklab_to_linear(*oklch_to_oklab(L, C, H))


def in_gamut(L, C, H, eps=1e-4):
    return all(-eps <= v <= 1 + eps for v in _linear_rgb_of(L, C, H))


def clamp_chroma(L, C, H):
    """Pull chroma down (never lightness or hue) until the color fits sRGB."""
    if in_gamut(L, C, H):
        return C
    lo, hi = 0.0, C
    for _ in range(28):
        mid = (lo + hi) / 2
        if in_gamut(L, mid, H):
            lo = mid
        else:
            hi = mid
    return lo


def max_chroma(L, H):
    return clamp_chroma(L, 0.5, H)


def oklch_to_hex(L, C, H):
    L = max(0.0, min(1.0, L))
    C = clamp_chroma(L, max(0.0, C), H)
    rgb = [linear_to_srgb(v) for v in _linear_rgb_of(L, C, H)]
    return rgb_to_hex(rgb)


def css_oklch(L, C, H):
    return "oklch(%.1f%% %.3f %.1f)" % (L * 100, C, H)


# ---------- contrast ----------


def luminance(h):
    r, g, b = (srgb_to_linear(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def _apca_y(h):
    r, g, b = hex_to_rgb(h)
    y = 0.2126729 * r ** 2.4 + 0.7151522 * g ** 2.4 + 0.0721750 * b ** 2.4
    return y if y >= 0.022 else y + (0.022 - y) ** 1.414


def apca(text, bg):
    """APCA Lc, signed (negative = light text on dark ground). Advisory only."""
    yt, yb = _apca_y(text), _apca_y(bg)
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        s = (yb ** 0.56 - yt ** 0.57) * 1.14
        return 0.0 if s < 0.1 else (s - 0.027) * 100
    s = (yb ** 0.65 - yt ** 0.62) * 1.14
    return 0.0 if s > -0.1 else (s + 0.027) * 100


def lightness_gap(a, b):
    return abs(hex_to_oklch(a)[0] - hex_to_oklch(b)[0])


# ---------- color-vision deficiency ----------

_CVD = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def cvd(h, kind):
    lin = [srgb_to_linear(c) for c in hex_to_rgb(h)]
    m = _CVD[kind]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return rgb_to_hex([linear_to_srgb(v) for v in out])


def delta_ok(a, b):
    la = linear_to_oklab(*(srgb_to_linear(c) for c in hex_to_rgb(a)))
    lb = linear_to_oklab(*(srgb_to_linear(c) for c in hex_to_rgb(b)))
    return math.dist(la, lb)


# ---------- fixing contrast by moving lightness ----------


def push_for_contrast(h, against, target, direction=None):
    """Return h moved in lightness (hue and chroma kept) until contrast(h, against) >= target.

    direction: +1 lighter, -1 darker. Default: away from the ground.
    """
    if contrast(h, against) >= target:
        return h
    L, C, H = hex_to_oklch(h)
    if direction is None:
        direction = -1 if luminance(against) > 0.18 else 1
    cur = L
    for _ in range(300):
        cur += direction * 0.005
        if cur <= 0 or cur >= 1:
            break
        cand = oklch_to_hex(cur, C, H)
        if contrast(cand, against) >= target:
            return cand
    return oklch_to_hex(0.0 if direction < 0 else 1.0, 0, H)


def hue_name(h):
    h %= 360
    names = [
        (8, "Rose"), (22, "Coral"), (40, "Terracotta"), (58, "Amber"), (80, "Honey"), (100, "Saffron"),
        (120, "Lime"), (138, "Fern"), (156, "Sage"), (172, "Jade"), (192, "Teal"), (212, "Lagoon"),
        (234, "Sky"), (254, "Cobalt"), (272, "Indigo"), (292, "Iris"), (312, "Orchid"), (335, "Berry"),
        (352, "Blush"), (361, "Rose"),
    ]
    for top, name in names:
        if h < top:
            return name
    return "Rose"
