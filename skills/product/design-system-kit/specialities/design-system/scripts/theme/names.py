"""Name a color with the nearest plain word from our own list. Standard library only."""

import json
import math
import os

from oklch import hex_to_oklch, oklch_to_hex, oklch_to_oklab

_HERE = os.path.dirname(os.path.abspath(__file__))
_CACHE = []


def _load():
    if not _CACHE:
        path = os.path.join(_HERE, "..", "..", "data", "theme", "names.json")
        with open(path, encoding="utf-8") as f:
            for name, L, C, H in json.load(f)["names"]:
                _CACHE.append((name, oklch_to_hex(L, C, H), oklch_to_oklab(L, C, H)))
    return _CACHE


def nearest(hex_color, k=1):
    """The k closest names, each as (name, hex, distance)."""
    L, C, H = hex_to_oklch(hex_color)
    point = oklch_to_oklab(L, C, H)
    ranked = sorted(((math.dist(point, lab), name, hx) for name, hx, lab in _load()))
    return [(name, hx, round(d, 3)) for d, name, hx in ranked[:k]]


def describe(hex_color):
    """One short phrase: 'Harbor' for a match, 'close to Harbor' or 'near Harbor' otherwise."""
    name, _, d = nearest(hex_color)[0]
    return name if d < 0.03 else ("close to " + name if d < 0.06 else "near " + name)
