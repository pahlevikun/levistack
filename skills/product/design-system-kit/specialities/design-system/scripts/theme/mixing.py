"""Mix two colors in different spaces and read the result. Standard library only."""

import math

from oklch import (contrast, hex_to_oklch, hex_to_rgb, linear_to_oklab, linear_to_srgb, oklab_to_linear,
                   oklab_to_oklch, oklch_to_hex, oklch_to_oklab, rgb_to_hex, srgb_to_linear)

SPACES = ("srgb", "linear", "oklab", "oklch")


def _lerp(a, b, t):
    return a + (b - a) * t


def mix(a, b, t=0.5, space="oklab"):
    """Blend a toward b. t=0 gives a, t=1 gives b."""
    if space not in SPACES:
        raise ValueError("space must be one of %s" % ", ".join(SPACES))
    ra, rb = hex_to_rgb(a), hex_to_rgb(b)
    if space == "srgb":
        return rgb_to_hex([_lerp(x, y, t) for x, y in zip(ra, rb)])
    la, lb = [srgb_to_linear(c) for c in ra], [srgb_to_linear(c) for c in rb]
    if space == "linear":
        return rgb_to_hex([linear_to_srgb(_lerp(x, y, t)) for x, y in zip(la, lb)])
    oa, ob = linear_to_oklab(*la), linear_to_oklab(*lb)
    if space == "oklab":
        lab = [_lerp(x, y, t) for x, y in zip(oa, ob)]
        return rgb_to_hex([linear_to_srgb(v) for v in oklab_to_linear(*lab)])
    (L1, C1, H1), (L2, C2, H2) = hex_to_oklch(a), hex_to_oklch(b)
    if C1 < 0.01:
        H1 = H2
    if C2 < 0.01:
        H2 = H1
    dh = ((H2 - H1 + 180) % 360) - 180
    return oklch_to_hex(_lerp(L1, L2, t), _lerp(C1, C2, t), (H1 + dh * t) % 360)


def compare(a, b, t=0.5, on=None):
    """The same blend in every space, with the contrast against `on` when given."""
    rows = []
    for space in SPACES:
        m = mix(a, b, t, space)
        row = {"space": space, "hex": m, "L": round(hex_to_oklch(m)[0], 3)}
        if on:
            row["contrast"] = round(contrast(m, on), 2)
        rows.append(row)
    return rows


def ramp(a, b, steps, space="oklab"):
    return [mix(a, b, i / (steps - 1), space) for i in range(steps)]


def to_markdown(a, b, t, rows, on=None):
    out = ["# Mix %s and %s at %g\n\n" % (a, b, t)]
    out.append("| Space | Result | OKLab lightness |%s\n|---|---|---:|%s\n" % (" Contrast on %s |" % on if on else "", "---:|" if on else ""))
    for r in rows:
        out.append("| %s | %s | %.3f |%s\n" % (r["space"], r["hex"], r["L"], (" %.2f |" % r["contrast"]) if on else ""))
    out.append("\nUse `oklab` for tints, hover and pressed colors. It keeps lightness steady and avoids the muddy middle that `srgb` makes. Use `oklch` for a gradient that should pass through hues.\n")
    return "".join(out)
