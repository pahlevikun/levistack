"""Turn a recipe into a full, contrast-checked theme. Standard library only."""

import itertools

from oklch import (apca, contrast, cvd, delta_ok, hex_to_oklch, lightness_gap, oklch_to_hex,
                   push_for_contrast, hex_to_rgb)

STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
L_BRAND = [0.975, 0.945, 0.895, 0.825, 0.735, 0.645, 0.555, 0.47, 0.39, 0.31, 0.235]
CF_BRAND = [0.10, 0.22, 0.42, 0.66, 0.88, 1.0, 1.0, 0.92, 0.78, 0.62, 0.48]
L_NEUTRAL = [0.985, 0.965, 0.93, 0.88, 0.76, 0.62, 0.50, 0.40, 0.30, 0.22, 0.16]
CF_NEUTRAL = [0.6, 0.7, 0.85, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.8, 0.7]

STATUS_HUES = {"success": 150, "warning": 82, "danger": 27, "info": 245}

SPACE = {
    "airy":     [4, 8, 12, 16, 24, 32, 48, 64, 96, 128],
    "balanced": [4, 8, 12, 16, 20, 24, 32, 48, 64, 80],
    "dense":    [2, 4, 8, 12, 16, 20, 24, 32, 40, 48],
}
SPACE_NAMES = ["3xs", "2xs", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl"]


def ramp(h, c, L=L_BRAND, cf=CF_BRAND):
    return {s: oklch_to_hex(L[i], c * cf[i], h) for i, s in enumerate(STEPS)}


def pull_neutral(n, which):
    """Live knob: move the neutral hue 60 percent of the way toward cool (250) or warm (75)."""
    if which not in ("cool", "warm"):
        return n
    target = 250 if which == "cool" else 75
    d = ((target - n["hue"] + 180) % 360) - 180
    return dict(n, hue=(n["hue"] + d * 0.6) % 360)


def apply_amount(r):
    """Live knob: how much of the color strategy shows. 1 is the full recipe, 0 is a gray product.
    Brand chroma scales fully. The neutral tint scales less, so surfaces keep some character.
    Status colors do not scale, because they must stay readable."""
    amount = max(0.0, min(1.0, float(r.get("color_amount", 1.0))))
    n = pull_neutral(r["neutral"], r.get("neutral_temp"))
    n = dict(n, chroma=n["chroma"] * (0.35 + 0.65 * amount))
    return amount, n


def ink_and_paper(neutral):
    h, c = neutral["hue"], neutral["chroma"]
    return oklch_to_hex(0.995, c * 0.3, h), oklch_to_hex(0.13, c * 0.7, h)


def pick_solid(rmp, grounds, order, on_options, ui_ratio=3.0, avoid=None):
    """First step whose color is visible on every ground (>= ui_ratio) and carries readable text.

    avoid=(hex, min_gap): skip steps that are too close in lightness to another color, so
    pairs such as success and danger stay apart for people with red-green color blindness.
    """
    for step in order:
        solid = rmp[step]
        if any(contrast(solid, g) < ui_ratio for g in grounds):
            continue
        if avoid and lightness_gap(solid, avoid[0]) < avoid[1]:
            continue
        best = max(on_options, key=lambda o: contrast(o, solid))
        if contrast(best, solid) >= 4.5:
            return step, solid, best
    step = order[0]
    solid = push_for_contrast(rmp[step], grounds[0], ui_ratio)
    best = max(on_options, key=lambda o: contrast(o, solid))
    return step, solid, push_for_contrast(best, solid, 4.5, direction=1 if contrast("#FFFFFF", solid) >= contrast("#000000", solid) else -1)


def stateful(rmp, step, direction, on, base_solid):
    """Hover and pressed colors: one and two ramp steps toward more contrast with the ground."""
    i = STEPS.index(step)
    out = []
    for k in (1, 2):
        j = max(0, min(len(STEPS) - 1, i + direction * k))
        col = rmp[STEPS[j]]
        if contrast(on, col) < 4.5:
            col = push_for_contrast(col, on, 4.5)
        out.append(col)
    return out


def build_mode(mode, r, pal, paper, ink, soft):
    """Semantic colors for one mode. Returns (tokens, checks)."""
    n = pal["neutral"]
    dark = mode == "dark"
    if not dark:
        bg, surface, raised, sunken = (n[100], n[50], paper, n[200]) if soft else (n[50], paper, paper, n[100])
        text = {"soft": n[800], "standard": n[900], "high": n[950]}[r["contrast"]]
        muted, subtle = n[600], n[500]
        border = n[300] if soft else n[200]
        strong_pool = [n[s] for s in (400, 500, 600, 700)]
        order = [600, 500, 700, 400, 800, 300, 900]
        direction = 1
        on_options = [paper, ink]
        sub_bg, sub_fg = 100, 800
        link_step = 700
        ring_step = 500
    else:
        bg, surface, raised, sunken = (n[900], n[800], n[700], n[950]) if soft else (n[950], n[900], n[800], ink)
        text = {"soft": n[100], "standard": n[50], "high": paper}[r["contrast"]]
        muted, subtle = n[400], n[500]
        border = n[700] if soft else n[800]
        strong_pool = [n[s] for s in (600, 500, 400, 300)]
        order = [400, 300, 500, 200, 600, 700]
        direction = -1
        on_options = [ink, paper]
        sub_bg, sub_fg = 900, 200
        link_step = 300
        ring_step = 400

    border_strong = next((c for c in strong_pool if contrast(c, bg) >= 3.0 and contrast(c, surface) >= 3.0), strong_pool[-1])
    tokens = {
        "background": bg, "surface": surface, "surface-raised": raised, "surface-sunken": sunken,
        "border": border, "border-strong": border_strong,
        "text": text, "text-muted": push_for_contrast(muted, bg, 4.5), "text-subtle": subtle,
    }
    for ground in (surface, raised, sunken):
        if contrast(tokens["text-muted"], ground) < 4.5:
            tokens["text-muted"] = push_for_contrast(tokens["text-muted"], ground, 4.5)
    checks = [
        ("text on background", tokens["text"], bg, 4.5), ("text on surface", tokens["text"], surface, 4.5),
        ("text on surface-raised", tokens["text"], raised, 4.5), ("text on surface-sunken", tokens["text"], sunken, 4.5),
        ("text-muted on background", tokens["text-muted"], bg, 4.5), ("text-muted on surface", tokens["text-muted"], surface, 4.5),
        ("text-muted on surface-raised", tokens["text-muted"], raised, 4.5), ("text-muted on surface-sunken", tokens["text-muted"], sunken, 4.5),
        ("border-strong on background", border_strong, bg, 3.0), ("border-strong on surface", border_strong, surface, 3.0),
    ]

    for role in ("primary", "secondary", "tertiary"):
        step, solid, on = pick_solid(pal[role], [bg, surface], order, on_options)
        hov, prs = stateful(pal[role], step, direction, on, solid)
        sub = pal[role][sub_bg]
        sub_text = push_for_contrast(pal[role][sub_fg], sub, 4.5)
        tokens.update({
            role: solid, "on-" + role: on, role + "-hover": hov, role + "-pressed": prs,
            role + "-subtle": sub, "on-" + role + "-subtle": sub_text,
        })
        checks += [
            ("%s on background" % role, solid, bg, 3.0), ("on-%s on %s" % (role, role), on, solid, 4.5),
            ("on-%s on %s-hover" % (role, role), on, hov, 4.5), ("on-%s on %s-pressed" % (role, role), on, prs, 4.5),
            ("on-%s-subtle on %s-subtle" % (role, role), sub_text, sub, 4.5),
        ]
        if role == "primary":
            link = push_for_contrast(pal[role][link_step], bg, 4.5)
            for ground in (surface, raised):
                if contrast(link, ground) < 4.5:
                    link = push_for_contrast(link, ground, 4.5)
            ring = push_for_contrast(pal[role][ring_step], bg, 3.0)
            if contrast(ring, surface) < 3.0:
                ring = push_for_contrast(ring, surface, 3.0)
            tokens.update({"link": link, "focus-ring": ring})
            checks += [("link on background", link, bg, 4.5), ("link on surface", link, surface, 4.5), ("link on surface-raised", link, raised, 4.5),
                       ("focus-ring on background", ring, bg, 3.0), ("focus-ring on surface", ring, surface, 3.0)]

    for role in ("danger", "success", "warning", "info"):
        avoid = (tokens["danger"], 0.12) if role == "success" else None
        step, solid, on = pick_solid(pal[role], [bg, surface], order, on_options, avoid=avoid)
        sub = pal[role][sub_bg]
        sub_text = push_for_contrast(pal[role][sub_fg], sub, 4.5)
        tokens.update({role: solid, "on-" + role: on, role + "-subtle": sub, "on-" + role + "-subtle": sub_text})
        checks += [("%s on background" % role, solid, bg, 3.0), ("on-%s on %s" % (role, role), on, solid, 4.5),
                   ("on-%s-subtle on %s-subtle" % (role, role), sub_text, sub, 4.5)]
    return tokens, checks


def type_scale(v, xs_floor=0):
    base, ratio = v["base"], v["scale"]
    sizes = {
        "xs": base * ratio ** -1.5, "sm": base * ratio ** -0.75, "base": base,
        "lg": base * ratio, "xl": base * ratio ** 2, "2xl": base * ratio ** 3,
        "3xl": base * ratio ** 4, "4xl": base * ratio ** 5, "5xl": base * ratio ** 6,
    }
    out = {k: round(val * 2) / 2 for k, val in sizes.items()}
    out["xs"] = max(out["xs"], xs_floor)
    out["sm"] = max(out["sm"], out["xs"] + 1)
    return out


def chart_colors(r, mode):
    L = [0.60, 0.74, 0.50, 0.82, 0.66, 0.44] if mode == "light" else [0.74, 0.62, 0.82, 0.54, 0.68, 0.88]
    out = []
    for i in range(6):
        h = (r["hue"] + 60 * i + (20 if i % 2 else 0)) % 360
        out.append(oklch_to_hex(L[i], 0.13, h))
    return out


def shadow_color(pal, dark):
    h = hex_to_oklch(pal["primary"][900])
    c = oklch_to_hex(0.28 if not dark else 0.05, h[1] * 0.7, h[2])
    rgb = [round(x * 255) for x in hex_to_rgb(c)]
    return "%d %d %d" % tuple(rgb)


def build(recipe, lib):
    r = recipe
    amount, n = apply_amount(r)
    pal = {
        "primary": ramp(r["hue"], r["chroma"] * amount),
        "secondary": ramp(r["secondary_hue"], r["chroma"] * amount * r["secondary_chroma_mul"]),
        "tertiary": ramp(r["tertiary_hue"], r["chroma"] * amount * r["tertiary_chroma_mul"]),
        "neutral": ramp(n["hue"], n["chroma"], L_NEUTRAL, CF_NEUTRAL),
    }
    sc = max(0.10, min(0.15, r["chroma"] * 0.9))
    for role, hue in STATUS_HUES.items():
        if role == "danger" and r.get("danger_hue") is not None:
            hue = r["danger_hue"]
        pal[role] = ramp(hue, sc)
    paper, ink = ink_and_paper(n)
    soft = r["ground"] == "soft"

    modes, checks = {}, []
    for mode in ("light", "dark"):
        tokens, ch = build_mode(mode, r, pal, paper, ink, soft)
        modes[mode] = tokens
        checks += [(mode,) + c for c in ch]

    rows = []
    for mode, name, fg, bg, need in checks:
        ratio = contrast(fg, bg)
        rows.append({"mode": mode, "pair": name, "fg": fg, "bg": bg, "ratio": round(ratio, 2),
                     "need": need, "apca": round(apca(fg, bg), 1), "pass": ratio >= need})

    notes = []
    for mode in ("light", "dark"):
        t = modes[mode]
        for k in ("hue",):
            pass
        s, d = t["success"], t["danger"]
        worst = min(delta_ok(cvd(s, kind), cvd(d, kind)) for kind in ("protan", "deutan"))
        gap = lightness_gap(s, d)
        if worst < 0.07 and gap < 0.10:
            notes.append("%s: success and danger look alike under red-green color blindness (OKLab distance %.2f, lightness gap %.2f). Always add an icon or a label." % (mode, worst, gap))

    chart = {m: chart_colors(r, m) for m in ("light", "dark")}
    for m, cols in chart.items():
        worst = min(delta_ok(cvd(a, "deutan"), cvd(b, "deutan")) for a, b in itertools.combinations(cols, 2))
        if worst < 0.05:
            notes.append("%s chart colors: two series are close under deuteranopia (distance %.2f). Add direct labels or patterns." % (m, worst))

    voice = lib["voices"][r["voice"]]
    shape = lib["shapes"][r["shape"]]
    elev = lib["elevations"][shape["elevation"]]
    motion = dict(lib["motion"][r["motion"]])

    plat_ids = r.get("platforms") or ["web"]
    scaled = {pid: scale_for(lib["platforms"][pid], voice, shape, r["density"], motion) for pid in plat_ids}
    lead = scaled[plat_ids[0]]
    pchecks = platform_checks(lib["platforms"], scaled, plat_ids)

    return {
        "recipe": r, "palettes": pal, "modes": modes, "chart": chart, "checks": rows, "notes": notes,
        "paper": paper, "ink": ink,
        "type": {"sizes": lead["sizes"], "voice": voice, "id": r["voice"]},
        "space": lead["space"], "radius": shape["radius"], "border": shape["border"], "pad": lead["pad"],
        "control_height": lead["control_height"], "focus_ring": lead["focus_ring"],
        "elevation": {"id": shape["elevation"], "describe": elev["describe"], "levels": elev["levels"],
                      "shadow_light": shadow_color(pal, False), "shadow_dark": shadow_color(pal, True)},
        "motion": lead["motion"],
        "platforms": {"ids": plat_ids, "scaled": scaled, "profiles": {p: lib["platforms"][p] for p in plat_ids}, "checks": pchecks},
    }


AMOUNTS = [0, 0.25, 0.5, 0.75, 1]
TEMPS = ["cool", "as-built", "warm"]


def live_grid(recipe, lib):
    """Build the recipe at every knob position for the live tuning page. Each cell is a full build
    that has passed through the same contrast gate, so the page can show the verdict per position."""
    grid = {}
    for amount in AMOUNTS:
        for temp in TEMPS:
            t = build(dict(recipe, color_amount=amount, neutral_temp=temp), lib)
            bad = [c for c in t["checks"] if not c["pass"]]
            grid["%g|%s" % (amount, temp)] = {
                "light": t["modes"]["light"], "dark": t["modes"]["dark"], "pal": t["palettes"],
                "total": len(t["checks"]), "fails": len(bad),
                "failing": ["%s %s %.2f<%.1f" % (c["mode"], c["pair"], c["ratio"], c["need"]) for c in bad[:4]],
            }
    return grid


def xs_floor_for(pl):
    return max(11, round(pl["min_body"] * 0.75))


def snap(n):
    """Keep spacing on a tidy grid: even numbers below 8, multiples of 4 from 8 up."""
    return max(2, even(n)) if n < 8 else max(8, int(round(n / 4.0)) * 4)


def even(n):
    return int(round(n / 2.0)) * 2


def scale_for(pl, voice, shape, density, motion):
    """Type, space, control and motion values for one platform profile."""
    base = max(pl["min_body"], round(voice["base"] * pl["type_mul"]))
    v = dict(voice)
    v["base"] = base
    m = dict(motion)
    m["dur"] = [max(1, int(round(d * pl["motion_mul"]))) for d in motion["dur"]]
    m["distance"] = int(round(motion["distance"] * pl["motion_mul"]))
    return {
        "sizes": type_scale(v, xs_floor_for(pl)),
        "space": {k: snap(s * pl["space_mul"]) for k, s in zip(SPACE_NAMES, SPACE[density])},
        "pad": [int(round(shape["pad"][0] * pl["space_mul"])), int(round(shape["pad"][1] * pl["space_mul"]))],
        "control_height": pl["control_height"], "min_target": pl["min_target"], "focus_ring": pl["focus_ring"], "motion": m,
    }


def platform_checks(profiles, scaled, ids):
    rows = []
    for pid in ids:
        pl, sc = profiles[pid], scaled[pid]
        rows.append({"platform": pid, "check": "body text size", "value": sc["sizes"]["base"], "need": pl["min_body"], "pass": sc["sizes"]["base"] >= pl["min_body"]})
        rows.append({"platform": pid, "check": "control height", "value": sc["control_height"], "need": pl["min_target"], "pass": sc["control_height"] >= pl["min_target"]})
        rows.append({"platform": pid, "check": "smallest text (xs)", "value": sc["sizes"]["xs"], "need": xs_floor_for(pl), "pass": sc["sizes"]["xs"] >= xs_floor_for(pl)})
    return rows
