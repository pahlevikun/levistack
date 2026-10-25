#!/usr/bin/env python3
"""Mix a design direction, build contrast-checked tokens, and write DESIGN.md.

Standard library only (Python 3.9+).

  theme.py list [domains|moods|harmonies|shapes|voices|motion|signatures|neutrals]
  theme.py explore --brief "calming meditation app" [--count 3] [--seed 1]
  theme.py build   --brief "..." --out DIR [--seed 1] [--recipe recipe.json] [--from-extract extracted.json]
  theme.py check   DESIGN.md
  theme.py contrast --pairs pairs.csv [--tokens tokens.json] [--mode light|dark] [--out report.md]
  theme.py audit   DIR [--out audit.md]
  theme.py bind    --tokens tokens.json --stack flutter|compose|swiftui|react-native|vue --out DIR

build and explore also accept --from-brief color-brief.json (the same keys as the flags, e.g. {"brief": "...", "mood": "calm", "platform": "mobile"}).

Overrides for explore and build:
  --domain a,b  --mood a,b  --hue 0-360  --accent-hue 0-360  --chroma low|mid|high|0.12
  --temp -1..1  --ground light|soft|dark  --harmony ID  --shape ID  --voice ID  --motion ID
  --signature a,b  --neutral ID  --density airy|balanced|dense  --danger-hue 0-360
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import audit_colors  # noqa: E402
import bind as binder  # noqa: E402
import build as builder  # noqa: E402
import check_pairs  # noqa: E402
import emit  # noqa: E402
import mixer  # noqa: E402
import mixing  # noqa: E402
import names  # noqa: E402
import scales  # noqa: E402
from oklch import contrast, hex_to_oklch, hue_name  # noqa: E402


def add_mix_args(p):
    p.add_argument("--brief", default="")
    p.add_argument("--seed", default="1")
    p.add_argument("--domain")
    p.add_argument("--mood")
    p.add_argument("--hue", type=float)
    p.add_argument("--accent-hue", type=float)
    p.add_argument("--chroma")
    p.add_argument("--temp", type=float)
    p.add_argument("--ground", choices=["light", "soft", "dark"])
    p.add_argument("--harmony")
    p.add_argument("--shape")
    p.add_argument("--voice")
    p.add_argument("--motion")
    p.add_argument("--signature")
    p.add_argument("--neutral")
    p.add_argument("--density", choices=["airy", "balanced", "dense"])
    p.add_argument("--danger-hue", type=float)
    p.add_argument("--color-amount", type=float, help="0 to 1. How much of the color strategy shows. 1 is the full recipe")
    p.add_argument("--neutral-temp", choices=["cool", "warm", "as-built"], help="move the neutral hue toward cool or warm")
    p.add_argument("--region")
    p.add_argument("--platform", help="comma list of mobile,desktop,web,tv,car. The first one leads the tokens, the rest get overrides.")


def overrides_from(a):
    o = {}
    if getattr(a, "platform", None):
        o["platforms"] = [x.strip() for x in a.platform.split(",") if x.strip()]
    for k in ("hue", "accent_hue", "temp", "ground", "harmony", "shape", "voice", "motion", "neutral", "density", "danger_hue", "region", "color_amount", "neutral_temp"):
        v = getattr(a, k, None)
        if v is not None:
            o[k] = v
    if a.chroma:
        try:
            o["chroma"] = float(a.chroma)
        except ValueError:
            o["chroma"] = a.chroma
    if a.signature:
        o["signature"] = a.signature.split(",")
    return o


def split(v):
    return [x.strip() for x in v.split(",") if x.strip()] if v else None


def validate_ids(lib, a):
    problems = []
    amount = getattr(a, "color_amount", None)
    if amount is not None and not 0 <= amount <= 1:
        problems.append("--color-amount must be between 0 and 1, got %s" % amount)
    for key, table in (("domain", "domains"), ("mood", "moods")):
        for i in split(getattr(a, key)) or []:
            if i not in lib[table]:
                problems.append("unknown %s '%s'. Try: theme.py list %s" % (key, i, table))
    for key, table in (("harmony", "harmonies"), ("shape", "shapes"), ("voice", "voices"), ("motion", "motion"), ("neutral", "neutrals")):
        i = getattr(a, key, None)
        if i and i not in lib[table]:
            problems.append("unknown %s '%s'. Try: theme.py list %s" % (key, i, table))
    for i in split(a.signature) or []:
        if i not in lib["signatures"]:
            problems.append("unknown signature '%s'. Try: theme.py list signatures" % i)
    for i in split(getattr(a, "platform", None)) or []:
        if i not in lib["platforms"]:
            problems.append("unknown platform '%s'. Try: theme.py list platforms" % i)
    return problems


def apply_extract(recipe, ex, lib):
    """Pull hue, chroma, neutral, shape, voice and motion from an extraction (extract_site.py)."""
    s = ex.get("suggest", {})
    old_hue = recipe["hue"]
    for k in ("hue", "chroma", "density", "ground"):
        if s.get(k) is not None:
            recipe[k] = s[k]
    delta = recipe["hue"] - old_hue
    if s.get("secondary_hue") is not None:
        recipe["secondary_hue"] = s["secondary_hue"]
    else:
        recipe["secondary_hue"] = round((recipe["secondary_hue"] + delta) % 360, 1)
    recipe["tertiary_hue"] = round((recipe["tertiary_hue"] + delta) % 360, 1)
    recipe["name"] = "%s %s" % (recipe["name"].split()[0], hue_name(recipe["hue"]))
    n = recipe["neutral"]
    if s.get("neutral_hue") is not None:
        n["hue"], n["chroma"], n["id"], n["describe"] = s["neutral_hue"], s.get("neutral_chroma", n["chroma"]), "extracted", "the neutral found on the source site"
    for k in ("shape", "voice", "motion"):
        if s.get(k) in lib[{"shape": "shapes", "voice": "voices", "motion": "motion"}[k]]:
            recipe[k] = s[k]
    recipe["why"]["hue"] = "Taken from the extracted site (%s)." % ex.get("source", "unknown")
    recipe["brief"] = (recipe["brief"] + " | remix of " + ex.get("source", "")).strip(" |")
    return recipe


def cmd_list(a):
    lib = mixer.library()
    table = lib[a.what] if a.what in lib else None
    if not table:
        print("choose one of: domains moods harmonies shapes voices motion signatures neutrals")
        return 2
    for k, v in table.items():
        desc = v.get("describe") or v.get("label") or ", ".join(v.get("words", []))
        print("%-22s %s" % (k, desc))
    return 0


def summarize(r, t=None):
    prim = t["modes"]["light"]["primary"] if t else ""
    return "%-16s %s | seed %s | hue %3.0f c %.3f %s | %s | %s | %s | %s | %s | %s" % (
        r["name"], prim, r["seed"], r["hue"], r["chroma"], r["harmony"], r["shape"], r["voice"], r["motion"], "+".join(r["signatures"]), r["neutral"]["id"], "+".join(r.get("platforms", ["web"])))


def cmd_explore(a):
    lib = mixer.library()
    bad = validate_ids(lib, a)
    if bad:
        print("\n".join(bad), file=sys.stderr)
        return 2
    recipes = mixer.explore(a.brief, a.count, a.seed, split(a.domain), split(a.mood), overrides_from(a), lib)
    if not recipes:
        print("No recipes. Add --domain or a clearer brief.", file=sys.stderr)
        return 2
    out = []
    for i, r in enumerate(recipes, 1):
        t = builder.build(r, lib)
        print("%d. %s" % (i, summarize(r, t)))
        print("   swatches: %s" % "  ".join("%s %s" % (k, t["modes"]["light"][k]) for k in ("primary", "secondary", "tertiary", "background")))
        out.append(r)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print("wrote %s" % a.out)
    print("Pick one, then: theme.py build --brief \"%s\" --seed <its seed> --out DIR   (repeat the same flags you gave explore)" % a.brief)
    print("Or save with --out recipes.json and build with: --recipe recipes.json --pick N")
    return 0


def cmd_build(a):
    lib = mixer.library()
    bad = validate_ids(lib, a)
    if bad:
        print("\n".join(bad), file=sys.stderr)
        return 2
    if a.recipe:
        with open(a.recipe, encoding="utf-8") as f:
            recipe = json.load(f)
        if isinstance(recipe, list):
            recipe = recipe[a.pick - 1]
    else:
        recipe = mixer.mix(a.brief, a.seed, split(a.domain), split(a.mood), overrides_from(a), lib)
    if a.from_extract:
        with open(a.from_extract, encoding="utf-8") as f:
            recipe = apply_extract(recipe, json.load(f), lib)
    t = builder.build(recipe, lib)
    os.makedirs(a.out, exist_ok=True)
    files = {
        "recipe.json": json.dumps(recipe, indent=2), "tokens.json": emit.tokens_json(t), "theme.css": emit.theme_css(t),
        "tailwind-theme.css": emit.tailwind_css(t), "DESIGN.md": emit.design_md(t, lib), "report.md": emit.report_md(t, lib),
        "preview.html": emit.preview_html(t, lib), "platforms.css": emit.platforms_css(t),
    }
    if a.live:
        files["live.html"] = emit.preview_html(t, lib, builder.live_grid(recipe, lib))
    for name, text in files.items():
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as f:
            f.write(text)
    fails = [c for c in t["checks"] if not c["pass"]]
    pfails = [c for c in t["platforms"]["checks"] if not c["pass"]]
    print("%s" % summarize(recipe, t))
    print("wrote %s to %s" % (", ".join(files), a.out))
    print("contrast: %d checks, %d failing. platform: %d checks, %d failing" % (len(t["checks"]), len(fails), len(t["platforms"]["checks"]), len(pfails)))
    for n in t["notes"]:
        print("note: " + n)
    return 1 if (fails or pfails) else 0


# ---------- check: a small DESIGN.md linter ----------

SECTIONS = ["Overview", "Brand & Style", "Colors", "Typography", "Layout", "Layout & Spacing", "Elevation & Depth", "Elevation", "Shapes", "Components", "Do's and Don'ts"]
ORDER = {"overview": 0, "brand & style": 0, "colors": 1, "typography": 2, "layout": 3, "layout & spacing": 3, "elevation & depth": 4, "elevation": 4, "shapes": 5, "components": 6, "do's and don'ts": 7}


def parse_yaml_lite(text):
    """Parse the small YAML subset this tool writes (nested maps, scalars). Not a general parser."""
    root, stack = {}, [(-1, {})]
    stack[0] = (-1, root)
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = (len(raw) - len(raw.lstrip(" "))) // 2
        key, _, val = raw.strip().partition(":")
        key = key.strip().strip('"')
        val = val.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if val == "":
            node = {}
            parent[key] = node
            stack.append((indent, node))
        else:
            parent[key] = val.strip('"')
    return root


def resolve(path, tree):
    cur = tree
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def cmd_check(a):
    with open(a.file, encoding="utf-8") as f:
        text = f.read()
    errors, warnings = [], []
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        print("error: no YAML front matter")
        return 1
    tree = parse_yaml_lite(m.group(1))
    body = text[m.end():]
    blocks = re.findall(r"```yaml\n(.*?)```", body, re.S)
    for b in blocks:
        extra = parse_yaml_lite(b)
        for k in extra:
            if k in tree:
                errors.append("duplicate top-level key '%s' (front matter and a yaml block)" % k)
        tree.update(extra)
    heads = re.findall(r"^## (.+)$", body, re.M)
    seen = set()
    last = -1
    for h in heads:
        if h in seen:
            errors.append("duplicate section '## %s'" % h)
        seen.add(h)
        o = ORDER.get(h.lower())
        if o is not None:
            if o < last:
                warnings.append("section '%s' is out of order" % h)
            last = max(last, o)
    for need in ("Colors", "Typography"):
        if need not in heads:
            warnings.append("missing section '%s'" % need)
    refs = re.findall(r'"\{([a-zA-Z0-9_.\-]+)\}"', text)
    for ref in refs:
        if resolve(ref, tree) is None:
            errors.append("broken reference {%s}" % ref)
    colors = tree.get("colors", {})
    for name, comp in tree.get("components", {}).items():
        bg, fg = comp.get("backgroundColor"), comp.get("textColor")
        if bg and fg:
            bgv = resolve(bg.strip("{}"), tree) if bg.startswith("{") else bg
            fgv = resolve(fg.strip("{}"), tree) if fg.startswith("{") else fg
            if isinstance(bgv, str) and isinstance(fgv, str) and bgv.startswith("#") and fgv.startswith("#"):
                ratio = contrast(fgv, bgv)
                if ratio < 4.5:
                    warnings.append("contrast %.2f < 4.5 in component '%s' (%s on %s)" % (ratio, name, fgv, bgv))
    for name, val in colors.items():
        if not re.match(r"^#[0-9a-fA-F]{6}$", str(val)):
            warnings.append("color '%s' is not #RRGGBB: %s" % (name, val))
    for e in errors:
        print("error: " + e)
    for w in warnings:
        print("warning: " + w)
    print("%d error(s), %d warning(s). For the full official linter run: npx @google/design.md lint %s" % (len(errors), len(warnings), a.file))
    return 1 if errors else 0


def cmd_contrast(a):
    try:
        rows = check_pairs.read_pairs(a.pairs)
    except (ValueError, OSError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    tokens = check_pairs.load_tokens(a.tokens) if a.tokens else None
    results = check_pairs.measure(rows, tokens, a.mode)
    text = check_pairs.to_markdown(results)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote %s" % a.out)
    if a.json:
        print(json.dumps(results, indent=2))
    else:
        fails = [r for r in results if not r["pass"]]
        for r in results:
            if r["error"]:
                print("ERROR %-34s %s" % (r["name"], r["error"]))
            else:
                print("%s %-34s %-5s %5.2f (need %.1f) APCA %.0f" % ("pass " if r["pass"] else "FAIL ", r["name"], r["mode"], r["ratio"], r["need"], r["apca"]))
        print("%d pairs, %d failing" % (len(results), len(fails)))
    return 1 if any(not r["pass"] for r in results) else 0


def cmd_audit(a):
    if not os.path.isdir(a.dir):
        print("not a folder: %s" % a.dir, file=sys.stderr)
        return 2
    rep = audit_colors.audit(a.dir)
    text = audit_colors.to_markdown(rep, a.limit)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote %s" % a.out)
    else:
        print(text)
    return 0


def cmd_bind(a):
    try:
        written = binder.bind(a.tokens, a.stack, a.out)
    except (ValueError, KeyError, OSError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    for w in written:
        print("wrote %s" % w)
    return 0


def cmd_name(a):
    for h in a.colors:
        try:
            near = names.nearest(h, a.k)
        except ValueError:
            print("error: '%s' is not a hex color" % h, file=sys.stderr)
            return 2
        print("%s  %s" % (h.upper(), "; ".join("%s %s (distance %.3f)" % (n, hx, d) for n, hx, d in near)))
    return 0


def cmd_scale(a):
    dark = a.mode == "dark"
    ground = a.ground or ("#101010" if dark else "#FFFFFF")
    if a.kind == "sequential":
        cols = scales.sequential(a.hue, a.n, a.chroma, dark)
    elif a.kind == "diverging":
        cols = scales.diverging(a.hue, a.hue2 if a.hue2 is not None else (a.hue + 180) % 360, a.n, a.chroma, dark)
    else:
        try:
            cols = scales.categorical(a.hue, a.n, ground, a.chroma, dark)
        except ValueError as e:
            print("error: %s" % e, file=sys.stderr)
            return 2
    rows = scales.check(a.kind, cols, ground)
    if a.json:
        text = json.dumps({"kind": a.kind, "ground": ground, "colors": cols,
                           "checks": [{"check": c, "value": v, "need": n, "pass": ok} for c, v, n, ok in rows]}, indent=2)
    else:
        text = scales.to_markdown(a.kind, cols, ground, rows, a.hue, dark)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote " + a.out)
    else:
        print(text)
    return 1 if any(not ok for *_, ok in rows) else 0


def cmd_mix(a):
    try:
        if a.steps:
            cols = mixing.ramp(a.a, a.b, a.steps, a.space or "oklab")
            print("\n".join("%d  %s" % (i + 1, c) for i, c in enumerate(cols)))
            return 0
        rows = mixing.compare(a.a, a.b, a.ratio, a.on)
    except (ValueError, KeyError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if a.space:
        rows = [r for r in rows if r["space"] == a.space]
    text = mixing.to_markdown(a.a, a.b, a.ratio, rows, a.on)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote " + a.out)
    else:
        print(text)
    return 0


def apply_brief(argv):
    """--from-brief file.json fills in flags that the command line did not set."""
    if "--from-brief" not in argv:
        return argv
    i = argv.index("--from-brief")
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        print("error: --from-brief needs a JSON file", file=sys.stderr)
        raise SystemExit(2)
    path = argv[i + 1]
    with open(path, encoding="utf-8") as f:
        brief = json.load(f)
    known = {"brief", "seed", "domain", "mood", "hue", "accent_hue", "chroma", "temp", "ground", "harmony", "shape", "voice", "motion",
             "signature", "neutral", "density", "danger_hue", "region", "platform", "color_amount", "neutral_temp"}
    given = {x for x in argv if x.startswith("--")}
    extra = []
    for key, val in brief.items():
        flag = "--" + key.replace("_", "-")
        if key not in known:
            print("note: brief key '%s' is not a build option and was ignored" % key, file=sys.stderr)
            continue
        if flag in given or val in (None, ""):
            continue
        extra += [flag, ",".join(val) if isinstance(val, list) else str(val)]
    return argv[:i] + argv[i + 2:] + extra


def main(argv=None):
    argv = apply_brief(list(sys.argv[1:] if argv is None else argv))
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list")
    s.add_argument("what", nargs="?", default="")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("explore")
    add_mix_args(s)
    s.add_argument("--count", type=int, default=3)
    s.add_argument("--out")
    s.set_defaults(fn=cmd_explore)
    s = sub.add_parser("build")
    add_mix_args(s)
    s.add_argument("--out", required=True)
    s.add_argument("--recipe")
    s.add_argument("--pick", type=int, default=1, help="when --recipe holds a list from explore, which one (1-based)")
    s.add_argument("--from-extract")
    s.add_argument("--live", action="store_true", help="also write live.html, a page with knobs for color amount, neutral temperature and mode. Every knob position passes the contrast gate or says why not")
    s.set_defaults(fn=cmd_build)
    s = sub.add_parser("check")
    s.add_argument("file")
    s.set_defaults(fn=cmd_check)
    s = sub.add_parser("contrast")
    s.add_argument("--pairs", required=True, help="CSV with the columns name,fg,bg,need and an optional mode")
    s.add_argument("--tokens", help="tokens.json from build, to resolve semantic names")
    s.add_argument("--mode", default="light", choices=["light", "dark"])
    s.add_argument("--out")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_contrast)
    s = sub.add_parser("audit")
    s.add_argument("dir")
    s.add_argument("--out")
    s.add_argument("--limit", type=int, default=40)
    s.set_defaults(fn=cmd_audit)
    s = sub.add_parser("bind")
    s.add_argument("--tokens", required=True)
    s.add_argument("--stack", required=True)
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_bind)
    s = sub.add_parser("name", help="name colors with the nearest plain word")
    s.add_argument("colors", nargs="+")
    s.add_argument("--k", type=int, default=1)
    s.set_defaults(fn=cmd_name)
    s = sub.add_parser("scale", help="a chart scale: sequential, diverging or categorical")
    s.add_argument("kind", choices=scales.KINDS)
    s.add_argument("--hue", type=float, default=250)
    s.add_argument("--hue2", type=float, help="the second hue of a diverging scale")
    s.add_argument("--n", type=int, default=6)
    s.add_argument("--chroma", type=float, default=0.13)
    s.add_argument("--mode", choices=["light", "dark"], default="light")
    s.add_argument("--ground", help="hex of the surface the marks sit on")
    s.add_argument("--out")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_scale)
    s = sub.add_parser("mix", help="blend two colors in several spaces")
    s.add_argument("a")
    s.add_argument("b")
    s.add_argument("--ratio", type=float, default=0.5, help="0 gives a, 1 gives b")
    s.add_argument("--space", choices=mixing.SPACES)
    s.add_argument("--on", help="a ground hex, to report contrast")
    s.add_argument("--steps", type=int, help="print a ramp of this many steps instead")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_mix)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
