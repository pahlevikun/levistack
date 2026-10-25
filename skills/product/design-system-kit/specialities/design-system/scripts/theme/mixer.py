"""Mix ingredients from data/theme/*.json into one recipe. Standard library only.

The mixer is seeded: the same brief and seed always give the same recipe. A different seed
gives a different, still compatible recipe. Nothing here picks a color value directly. It picks
hues, chroma and the other ingredients. theme.py turns the recipe into tokens.
"""

import hashlib
import json
import os
import random
import re

from oklch import hue_name

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "theme")

CHROMA = {"low": 0.075, "mid": 0.115, "high": 0.17}
MOOD_WORDS = {
    # common words a person says -> mood id
    "calming": "calm", "relaxing": "calm", "peaceful": "calm", "quiet": "calm", "soothing": "calm", "zen": "calm",
    "tasty": "appetizing", "delicious": "appetizing", "yummy": "appetizing", "hungry": "appetizing",
    "reliable": "trustworthy", "safe": "trustworthy", "secure": "trustworthy", "professional": "trustworthy",
    "fun": "playful", "cheerful": "playful", "cute": "playful", "quirky": "playful",
    "luxury": "premium", "luxurious": "premium", "elegant": "premium", "high-end": "premium", "upscale": "premium", "exclusive": "premium",
    "dynamic": "energetic", "vibrant": "energetic", "lively": "energetic", "loud": "energetic",
    "organic": "earthy", "natural": "earthy", "rustic": "earthy", "cozy": "earthy",
    "sterile": "clinical", "medical": "clinical", "precise": "clinical", "minimal": "focused",
    "retro": "nostalgic", "vintage": "nostalgic", "classic": "nostalgic",
    "sci-fi": "futuristic", "cyber": "futuristic", "neon": "futuristic", "modern": "fresh",
    "brutalist": "bold", "strong": "bold", "punk": "rebellious", "edgy": "rebellious",
    "soft": "gentle", "tender": "gentle", "kind": "gentle", "warm": "wholesome",
    "magazine": "editorial", "journal": "editorial", "technical": "technical", "geeky": "technical",
    "happy": "optimistic", "sunny": "optimistic", "night": "serene-night", "bedtime": "serene-night",
    "celebrate": "festive", "party": "festive", "athletic": "sporty", "sporty": "sporty",
    "dark": "mysterious", "moody": "mysterious", "mysterious": "mysterious", "clean": "fresh",
    "friendly": "social", "community": "social", "focused": "focused", "simple": "focused",
}


def load_raw(name):
    with open(os.path.join(DATA, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def load(name):
    return {k: v for k, v in load_raw(name).items() if not k.startswith("_")}


def library():
    shapes = load("shapes")
    elevations = shapes.pop("elevations")
    domains = load("domains")
    for did, extra in load_raw("rules").get("domain_forbid", {}).items():
        if did in domains:
            merged = domains[did].setdefault("forbid", {})
            for key, ids in extra.items():
                merged[key] = sorted(set(merged.get(key, [])) | set(ids))
    return {
        "domains": domains, "moods": load("moods"), "neutrals": load("neutrals"),
        "harmonies": load("harmonies"), "shapes": shapes, "elevations": elevations,
        "voices": load("voices"), "motion": load("motion"), "signatures": load("signatures"),
        "platforms": load("platforms"),
    }


def seed_int(brief, seed):
    h = hashlib.sha1(("%s|%s" % (brief.strip().lower(), seed)).encode("utf-8")).hexdigest()
    return int(h[:12], 16)


def words(text):
    return re.findall(r"[a-z][a-z\-]+", text.lower())


def match_domains(brief, lib, limit=2):
    text = " " + brief.lower() + " "
    scores = {}
    for did, d in lib["domains"].items():
        s = 0
        for term in d["aka"] + [did.replace("-", " ")]:
            if re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", text):
                s += 2 if " " in term else 1
        if s:
            scores[did] = s
    ranked = sorted(scores, key=lambda k: (-scores[k], k))
    return ranked[:limit]


def match_moods(brief, lib):
    found = []
    for w in words(brief):
        mid = w if w in lib["moods"] else MOOD_WORDS.get(w)
        if mid and mid in lib["moods"] and mid not in found:
            found.append(mid)
    return found[:3]


def in_zone(h, zones):
    h %= 360
    for lo, hi in zones:
        lo %= 360
        hi = hi % 360 if hi != 360 else 360
        if lo <= hi:
            if lo <= h <= hi:
                return True
        elif h >= lo or h <= hi:
            return True
    return False


def pick_hue(rng, zones):
    spans = []
    for lo, hi in zones:
        width = (hi - lo) % 360 if hi != lo else 360
        if hi == 360 and lo == 0:
            width = 360
        spans.append((lo, max(width, 1)))
    total = sum(w for _, w in spans)
    r = rng.uniform(0, total)
    for lo, w in spans:
        if r <= w:
            return (lo + r) % 360
        r -= w
    return spans[-1][0] % 360


def weighted(rng, options, want, want2, forbid, boost=4.0, boost2=3.0):
    pool, weights = [], []
    for oid in options:
        if oid in forbid:
            continue
        w = 1.0
        if oid in want:
            w += boost
        if oid in want2:
            w += boost2
        pool.append(oid)
        weights.append(w)
    if not pool:
        pool, weights = list(options), [1.0] * len(options)
    return rng.choices(pool, weights=weights, k=1)[0]


def collect(lib, domain_ids, mood_ids, key):
    want, want2, forbid = [], [], set()
    for did in domain_ids:
        want += lib["domains"][did].get("want", {}).get(key, [])
        forbid |= set(lib["domains"][did].get("forbid", {}).get(key, []))
    for mid in mood_ids:
        want2 += lib["moods"][mid].get("want", {}).get(key, [])
        forbid |= set(lib["moods"][mid].get("forbid", {}).get(key, []))
    return want, want2, forbid


def density_for(mood_ids, domain_ids):
    airy = {"calm", "premium", "editorial", "gentle", "serene-night", "mysterious"}
    dense = {"technical", "focused", "clinical"}
    if any(m in dense for m in mood_ids) and not any(m in airy for m in mood_ids):
        return "dense"
    if any(m in airy for m in mood_ids) and not any(m in dense for m in mood_ids):
        return "airy"
    return "balanced"


def mix(brief="", seed="1", domains=None, moods=None, overrides=None, lib=None):
    """Return a recipe dict. overrides may hold: hue, accent_hue, chroma (low|mid|high or float),
    temp, ground, harmony, shape, voice, motion, signature (list), neutral, density, region,
    color_amount (0 to 1), neutral_temp (cool, warm or as-built)."""
    lib = lib or library()
    overrides = overrides or {}
    rng = random.Random(seed_int(brief + "|" + ",".join(domains or []) + ",".join(moods or []), seed))
    why = {}

    domain_ids = [d for d in (domains or match_domains(brief, lib)) if d in lib["domains"]]
    mood_ids = [m for m in (moods or match_moods(brief, lib)) if m in lib["moods"]]
    if not mood_ids and domain_ids:
        defaults = list(lib["domains"][domain_ids[0]]["moods"])
        mood_ids = defaults[:2]
        extra = [m for m in lib["moods"] if m not in mood_ids and m not in defaults]
        if rng.random() < 0.5 and extra:
            mood_ids.append(rng.choice(extra))
            why["mood"] = "Default moods of the domain, plus one random neighbour for a less predictable result."
    if not mood_ids:
        mood_ids = rng.sample(sorted(lib["moods"]), 2)
        why["mood"] = "No mood in the brief, so two were drawn from the seed."
    why.setdefault("domain", "Matched from the brief." if domain_ids else "No domain matched, so the hue is free.")

    # ---- hue ----
    if overrides.get("hue") is not None:
        hue = float(overrides["hue"]) % 360
        why["hue"] = "Set by the caller."
    elif domain_ids:
        hue = pick_hue(rng, lib["domains"][domain_ids[0]]["hue_zones"]) + rng.uniform(-6, 6)
        why["hue"] = "Drawn from the hue zones of %s." % domain_ids[0]
    else:
        hue = rng.uniform(0, 360)
    hue %= 360

    # ---- chroma ----
    base_level = lib["domains"][domain_ids[0]]["chroma"] if domain_ids else "mid"
    c = overrides.get("chroma")
    if isinstance(c, (int, float)):
        chroma = float(c)
    else:
        chroma = CHROMA.get(c or base_level, CHROMA["mid"])
    mul = 1.0
    for m in mood_ids:
        mul *= lib["moods"][m]["chroma_mul"] ** (1.0 / len(mood_ids))
    chroma *= mul * rng.uniform(0.94, 1.06)

    # ---- temperature (moves hue and chroma together) ----
    temp = overrides.get("temp")
    if temp is None:
        temp = sum(lib["moods"][m]["temp"] for m in mood_ids) / len(mood_ids)
    warm_zone = in_zone(hue, [(0, 100), (330, 360)])
    cool_zone = in_zone(hue, [(180, 270)])
    if temp > 0:
        chroma *= 1 + 0.18 * temp * (1 if warm_zone else -1 if cool_zone else 0)
    elif temp < 0:
        chroma *= 1 + 0.18 * (-temp) * (1 if cool_zone else -1 if warm_zone else 0)
    chroma = max(0.05, min(0.21, chroma))

    # ---- ground and contrast ----
    ground = overrides.get("ground") or None
    if not ground:
        votes = [lib["moods"][m]["ground"] for m in mood_ids]
        pref = [v for v in votes if v != "any"]
        ground = max(set(pref), key=pref.count) if pref else "light"
    contrast_order = {"soft": 0, "standard": 1, "high": 2}
    contrast_level = sorted((lib["moods"][m]["contrast"] for m in mood_ids), key=lambda k: contrast_order[k])[len(mood_ids) // 2]

    # ---- platform: the first one leads, the rest get override files ----
    platforms = [p for p in (overrides.get("platforms") or ["web"]) if p in lib["platforms"]] or ["web"]
    lead = lib["platforms"][platforms[0]]
    if not overrides.get("ground") and lead.get("ground_hint"):
        ground = lead["ground_hint"]
        why["ground"] = "The %s platform profile prefers a %s ground." % (platforms[0], ground)
    if contrast_order[lead["contrast_floor"]] > contrast_order[contrast_level]:
        contrast_level = lead["contrast_floor"]
        why["contrast"] = "Raised to %s because of the %s platform profile." % (contrast_level, platforms[0])

    # ---- harmony and secondary hues ----
    wh, wh2, fh = collect(lib, domain_ids, mood_ids, "harmonies")
    harmony = overrides.get("harmony") or weighted(rng, sorted(lib["harmonies"]), wh, wh2, fh)
    hd = lib["harmonies"][harmony]
    sec_hue = overrides.get("accent_hue")
    if sec_hue is None:
        if len(domain_ids) > 1:
            sec_hue = pick_hue(rng, lib["domains"][domain_ids[1]].get("accent_zones") or lib["domains"][domain_ids[1]]["hue_zones"])
            why["accent"] = "Taken from the accent zones of %s, the second domain." % domain_ids[1]
        else:
            sec_hue = hue + rng.choice(hd["secondary"])
    ter_hue = hue + rng.choice(hd["tertiary"])
    sec_hue, ter_hue = float(sec_hue) % 360, ter_hue % 360
    why["harmony"] = "%s: %s." % (harmony, hd["describe"])

    # ---- neutral ----
    wn, wn2, fn = collect(lib, domain_ids, mood_ids, "neutrals")
    neutral_id = overrides.get("neutral") or weighted(rng, sorted(lib["neutrals"]), wn, wn2, fn)
    n = lib["neutrals"][neutral_id]
    n_hue = hue if n["hue"] == "brand" else float(n["hue"])
    # temperature pulls the neutral toward warm (75) or cool (250)
    target = 75 if temp > 0 else 250
    pull = min(1.0, abs(temp) * 0.6)
    d = ((target - n_hue + 180) % 360) - 180
    n_hue = (n_hue + d * pull) % 360
    neutral = {"id": neutral_id, "hue": n_hue, "chroma": n["chroma"], "describe": n["describe"]}

    # ---- shape, voice, motion, signature ----
    def pick(key, table, override_key):
        w, w2, f = collect(lib, domain_ids, mood_ids, key)
        if overrides.get(override_key):
            return overrides[override_key]
        return weighted(rng, sorted(table), w, w2, f)

    shape = pick("shapes", lib["shapes"], "shape")
    voice = pick("voices", lib["voices"], "voice")
    motion = pick("motion", lib["motion"], "motion")
    ws, ws2, fs = collect(lib, domain_ids, mood_ids, "signatures")
    sigs = list(overrides.get("signature") or [])
    if not sigs:
        first = weighted(rng, sorted(lib["signatures"]), ws, ws2, fs)
        sigs = [first]
        if rng.random() < 0.35:
            second = weighted(rng, [s for s in sorted(lib["signatures"]) if s != first], ws, ws2, fs | {first})
            sigs.append(second)

    density = overrides.get("density") or density_for(mood_ids, domain_ids)
    lead_word = lib["moods"][mood_ids[0]]["words"][0].split()[0].capitalize()
    name = "%s %s" % (lead_word, hue_name(hue))

    return {
        "name": name, "brief": brief, "seed": str(seed),
        "domains": domain_ids, "moods": mood_ids,
        "hue": round(hue, 1), "chroma": round(chroma, 4), "temp": round(temp, 2),
        "ground": ground, "contrast": contrast_level, "density": density,
        "harmony": harmony, "secondary_hue": round(sec_hue, 1), "tertiary_hue": round(ter_hue, 1),
        "secondary_chroma_mul": hd["chroma_mul"][0], "tertiary_chroma_mul": hd["chroma_mul"][1],
        "neutral": neutral, "shape": shape, "voice": voice, "motion": motion, "signatures": sigs,
        "region": overrides.get("region"), "danger_hue": overrides.get("danger_hue"),
        "color_amount": max(0.0, min(1.0, float(overrides.get("color_amount", 1.0)))),
        "neutral_temp": overrides.get("neutral_temp") if overrides.get("neutral_temp") in ("cool", "warm") else "as-built",
        "platforms": platforms,
        "why": why,
    }


def explore(brief, count=3, seed="1", domains=None, moods=None, overrides=None, lib=None):
    """Return `count` recipes that differ in harmony, shape, voice and hue family."""
    lib = lib or library()
    out, seen = [], set()
    n = 0
    while len(out) < count and n < 200:
        r = mix(brief, "%s-%d" % (seed, n), domains, moods, overrides, lib)
        key = (r["harmony"], r["shape"], r["voice"], int(r["hue"] // 40))
        coarse = (r["shape"], r["voice"])
        n += 1
        if key in seen or coarse in {(o["shape"], o["voice"]) for o in out}:
            continue
        seen.add(key)
        out.append(r)
    return out
