"""Tests for the theme builder: color math, the ingredient library, the mixer, the builder and the extractor.

Run: python3 -m unittest discover -s scripts/tests -p "test_theme*.py"   (from specialities/design-system)
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.join(HERE, "..", "theme")
sys.path.insert(0, THEME)

import audit_colors  # noqa: E402
import build  # noqa: E402
import check_pairs  # noqa: E402
import emit  # noqa: E402
import extract_site  # noqa: E402
import mixer  # noqa: E402
import mixing  # noqa: E402
import names  # noqa: E402
import oklch  # noqa: E402
import scales  # noqa: E402
import theme  # noqa: E402

LIB = mixer.library()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

BRIEFS = [
    "a calming meditation app", "food delivery app", "fintech banking app", "kids learning game", "luxury fashion store",
    "developer tools dashboard", "legal services portal", "music streaming", "car navigation", "streaming video for tv",
]
PLATFORMS = [["mobile"], ["desktop"], ["web"], ["tv"], ["car"], ["web", "tv", "mobile"]]


class ColorMath(unittest.TestCase):
    def test_hex_round_trip(self):
        for h in ("#336699", "#FF8800", "#0A0A0A", "#F4F6F8"):
            L, C, H = oklch.hex_to_oklch(h)
            back = oklch.oklch_to_hex(L, C, H)
            diff = max(abs(int(h[i:i + 2], 16) - int(back[i:i + 2], 16)) for i in (1, 3, 5))
            self.assertLessEqual(diff, 1, (h, back))

    def test_contrast_known_values(self):
        self.assertAlmostEqual(oklch.contrast("#000000", "#FFFFFF"), 21.0, places=1)
        self.assertAlmostEqual(oklch.contrast("#777777", "#FFFFFF"), 4.48, places=1)

    def test_gamut_clamp_keeps_lightness_and_hue(self):
        L, C, H = 0.7, 0.4, 150
        c = oklch.clamp_chroma(L, C, H)
        self.assertLess(c, C)
        self.assertTrue(oklch.in_gamut(L, c, H))

    def test_push_for_contrast(self):
        fixed = oklch.push_for_contrast("#9AA0A6", "#FFFFFF", 4.5)
        self.assertGreaterEqual(oklch.contrast(fixed, "#FFFFFF"), 4.5)

    def test_apca_polarity(self):
        dark_on_light = oklch.apca("#222222", "#FFFFFF")
        light_on_dark = oklch.apca("#FFFFFF", "#222222")
        self.assertGreater(dark_on_light, 60)
        self.assertLess(light_on_dark, -60)


class Library(unittest.TestCase):
    def test_counts(self):
        self.assertGreaterEqual(len(LIB["domains"]), 30)
        self.assertGreaterEqual(len(LIB["moods"]), 20)
        self.assertEqual(set(LIB["platforms"]), {"mobile", "desktop", "web", "tv", "car"})

    def test_references_resolve(self):
        tables = {"shapes": LIB["shapes"], "voices": LIB["voices"], "motion": LIB["motion"], "signatures": LIB["signatures"],
                  "neutrals": LIB["neutrals"], "harmonies": LIB["harmonies"]}
        for owner in ("domains", "moods"):
            for oid, o in LIB[owner].items():
                for key in ("want", "forbid"):
                    for table, ids in o.get(key, {}).items():
                        for i in ids:
                            self.assertIn(i, tables[table], "%s.%s.%s.%s" % (owner, oid, key, table))
        for did, d in LIB["domains"].items():
            for m in d["moods"]:
                self.assertIn(m, LIB["moods"], did)
            self.assertIn(d["chroma"], ("low", "mid", "high"), did)
            self.assertTrue(d["hue_zones"], did)

    def test_every_shape_has_a_known_elevation(self):
        for sid, s in LIB["shapes"].items():
            self.assertIn(s["elevation"], LIB["elevations"], sid)


class Mixer(unittest.TestCase):
    def test_same_input_same_recipe(self):
        a = mixer.mix("a calming meditation app", "7", lib=LIB)
        b = mixer.mix("a calming meditation app", "7", lib=LIB)
        self.assertEqual(a, b)

    def test_seed_changes_result(self):
        recipes = [mixer.mix("food delivery app", str(i), lib=LIB) for i in range(12)]
        self.assertGreater(len({(r["shape"], r["voice"], r["harmony"], r["neutral"]["id"]) for r in recipes}), 4)

    def test_domain_matching(self):
        self.assertIn("wellness-meditation", mixer.match_domains("a calming meditation app", LIB))
        self.assertIn("food-delivery", mixer.match_domains("food delivery app", LIB))

    def test_forbidden_ingredients_never_drawn(self):
        for i in range(40):
            r = mixer.mix("a calming meditation app", str(i), lib=LIB)
            self.assertNotIn(r["shape"], ("brut", "sharp", "rules", "crisp"))

    def test_platform_floor(self):
        r = mixer.mix("streaming video app", "1", overrides={"platforms": ["tv"]}, lib=LIB)
        self.assertEqual(r["ground"], "dark")
        self.assertEqual(r["contrast"], "high")

    def test_explore_gives_distinct_directions(self):
        rs = mixer.explore("fintech banking app", 3, "1", lib=LIB)
        self.assertEqual(len(rs), 3)
        self.assertEqual(len({(r["shape"], r["voice"]) for r in rs}), 3)


class Builder(unittest.TestCase):
    def test_all_checks_pass_for_every_brief_and_platform(self):
        failures = []
        for brief in BRIEFS:
            for plats in PLATFORMS:
                for seed in ("1", "2"):
                    r = mixer.mix(brief, seed, overrides={"platforms": plats}, lib=LIB)
                    t = build.build(r, LIB)
                    bad = [c for c in t["checks"] if not c["pass"]] + [c for c in t["platforms"]["checks"] if not c["pass"]]
                    if bad:
                        failures.append((brief, plats, seed, bad[:2]))
        self.assertEqual(failures, [], failures[:3])

    def test_tv_sizes_are_larger_than_mobile(self):
        r = mixer.mix("streaming app", "1", overrides={"platforms": ["tv", "mobile"]}, lib=LIB)
        t = build.build(r, LIB)
        sc = t["platforms"]["scaled"]
        self.assertGreaterEqual(sc["tv"]["sizes"]["base"], 28)
        self.assertGreater(sc["tv"]["sizes"]["base"], sc["mobile"]["sizes"]["base"])
        self.assertGreater(sc["tv"]["control_height"], sc["mobile"]["control_height"])

    def test_dark_and_light_modes_have_the_same_roles(self):
        t = build.build(mixer.mix("fintech app", "3", lib=LIB), LIB)
        self.assertEqual(set(t["modes"]["light"]), set(t["modes"]["dark"]))

    def test_dark_ground_is_not_pure_black(self):
        t = build.build(mixer.mix("music app", "3", lib=LIB), LIB)
        self.assertNotEqual(t["modes"]["dark"]["background"].upper(), "#000000")


class Outputs(unittest.TestCase):
    def test_build_writes_all_files_and_design_md_passes_check(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "design")
            with redirect_stdout(io.StringIO()):
                code = theme.main(["build", "--brief", "a calming meditation app", "--seed", "1", "--platform", "mobile,tv", "--out", out])
            self.assertEqual(code, 0)
            for name in ("recipe.json", "tokens.json", "theme.css", "platforms.css", "tailwind-theme.css", "DESIGN.md", "report.md", "preview.html"):
                self.assertTrue(os.path.getsize(os.path.join(out, name)) > 100, name)
            json.loads(read(os.path.join(out, "tokens.json")))
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = theme.main(["check", os.path.join(out, "DESIGN.md")])
            self.assertEqual(code, 0, buf.getvalue())
            css = read(os.path.join(out, "theme.css"))
            self.assertIn("prefers-reduced-motion", css)
            self.assertIn("--color-primary", css)
            self.assertIn('data-theme="dark"', css)

    def test_check_catches_a_broken_reference(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "DESIGN.md")
            write(p, '---\nversion: alpha\nname: x\ncolors:\n  primary: "#112233"\n  on-primary: "#FFFFFF"\n---\n\n## Colors\n\n```yaml\ncomponents:\n  button:\n    backgroundColor: "{colors.nope}"\n```\n')
            with redirect_stdout(io.StringIO()):
                self.assertEqual(theme.main(["check", p]), 1)

    def test_css_braces_balance(self):
        t = build.build(mixer.mix("food app", "2", overrides={"platforms": ["web", "tv"]}, lib=LIB), LIB)
        for css in (emit.theme_css(t), emit.platforms_css(t), emit.tailwind_css(t)):
            self.assertEqual(css.count("{"), css.count("}"))


class Gates(unittest.TestCase):
    def _build(self, d, brief="fintech app"):
        out = os.path.join(d, "design")
        with redirect_stdout(io.StringIO()):
            theme.main(["build", "--brief", brief, "--seed", "2", "--out", out])
        return out

    def test_contrast_pairs_resolve_tokens_and_fail_bad_pairs(self):
        with tempfile.TemporaryDirectory() as d:
            out = self._build(d)
            pairs = os.path.join(d, "pairs.csv")
            write(pairs, "name,fg,bg,need,mode\nbody,text,background,4.5,light\nbody dark,text,background,4.5,dark\nbad,#999999,#FFFFFF,4.5,light\n")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = theme.main(["contrast", "--pairs", pairs, "--tokens", os.path.join(out, "tokens.json")])
            self.assertEqual(code, 1)
            self.assertIn("FAIL  bad", buf.getvalue())
            self.assertIn("pass  body", buf.getvalue())
            self.assertIn("1 failing", buf.getvalue())

    def test_contrast_composites_alpha_over_the_background(self):
        with tempfile.TemporaryDirectory() as d:
            pairs = os.path.join(d, "pairs.csv")
            write(pairs, "name,fg,bg,need\nhalf black on white,#00000080,#FFFFFF,4.5\nsolid black,#000000,#FFFFFF,4.5\n")
            rows = check_pairs.read_pairs(pairs)
            res = check_pairs.measure(rows)
            self.assertLess(res[0]["ratio"], res[1]["ratio"])
            self.assertEqual(res[0]["shown_fg"], "#7F7F7F")

    def test_contrast_reports_unknown_tokens_as_errors(self):
        res = check_pairs.measure([{"name": "x", "fg": "nope", "bg": "#FFFFFF", "need": "4.5"}], {"light": {}})
        self.assertFalse(res[0]["pass"])
        self.assertIn("unknown", res[0]["error"])

    def test_audit_groups_near_duplicates_and_counts_outside_token_files(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "src"))
            os.makedirs(os.path.join(d, "node_modules"))
            write(os.path.join(d, "src", "theme.css"), ":root{--brand:#3366FF}")
            write(os.path.join(d, "src", "Button.tsx"), "const a='#3366ff';const b='#3467FF';const c='rgb(51, 102, 255)';const d='#FF0000'")
            write(os.path.join(d, "node_modules", "x.css"), "a{color:#123456}")
            rep = audit_colors.audit(d)
            self.assertEqual(rep["files_scanned"], 2)
            lead = rep["clusters"][0]
            self.assertEqual(lead["lead"], "#3366FF")
            self.assertGreaterEqual(len(lead["members"]), 2)
            self.assertEqual(lead["outside_token_files"], 3)
            self.assertIn("Color audit", audit_colors.to_markdown(rep))

    def test_pairs_file_with_a_bom_reads_and_a_bad_file_fails_loudly(self):
        with tempfile.TemporaryDirectory() as d:
            ok = os.path.join(d, "ok.csv")
            with open(ok, "w", encoding="utf-8-sig") as f:
                f.write("name,fg,bg,need\nblack on white,#000000,#FFFFFF,4.5\n")
            rows = check_pairs.read_pairs(ok)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["name"], "black on white")
            bad = os.path.join(d, "bad.csv")
            write(bad, "title,color\nx,#000000\n")
            with self.assertRaises(ValueError):
                check_pairs.read_pairs(bad)
            empty = os.path.join(d, "empty.csv")
            write(empty, "name,fg,bg,need\n")
            with self.assertRaises(ValueError):
                check_pairs.read_pairs(empty)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(theme.main(["contrast", "--pairs", bad]), 2)
            res = check_pairs.measure([{"name": "x", "fg": "#000000", "bg": "#FFFFFF", "need": "AA"}])
            self.assertFalse(res[0]["pass"])
            self.assertIn("need must be a number", res[0]["error"])

    def test_translucent_ground_is_composited_over_the_page_ground_of_its_mode(self):
        scrim = [{"name": "scrim text", "fg": "#FFFFFF", "bg": "#00000099", "need": "4.5", "mode": "dark"}]
        res = check_pairs.measure(scrim, {"light": {}, "dark": {"background": "#101010"}}, "dark")
        self.assertTrue(res[0]["pass"], res[0])
        light = check_pairs.measure([{"name": "scrim text", "fg": "#FFFFFF", "bg": "#00000099", "need": "4.5", "mode": "light"}], None)
        self.assertLess(light[0]["ratio"], res[0]["ratio"])

    def test_from_brief_ignores_unknown_keys_and_rejects_a_missing_file_name(self):
        with tempfile.TemporaryDirectory() as d:
            brief = os.path.join(d, "b.json")
            write(brief, json.dumps({"brief": "fintech app", "stack": "swiftui", "modes": "light,dark", "mood": "trustworthy"}))
            err = io.StringIO()
            with redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                self.assertEqual(theme.main(["build", "--from-brief", brief, "--out", os.path.join(d, "o")]), 0)
            self.assertIn("'stack'", err.getvalue())
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    theme.main(["build", "--from-brief"])
                self.assertEqual(ctx.exception.code, 2)

    def test_audit_ignores_markdown_and_plain_hex_numbers(self):
        with tempfile.TemporaryDirectory() as d:
            write(os.path.join(d, "NOTES.md"), "Fixes #123 and #add")
            write(os.path.join(d, "a.kt"), "val a = Color(0xFF3B82F6)\nval max = 0x7FFFFFFF\nval b = 0xFFFFFFFF")
            rep = audit_colors.audit(d)
            self.assertEqual(rep["files_scanned"], 1)
            self.assertEqual([c["lead"] for c in rep["clusters"]], ["#3B82F6"])

    def test_audit_reads_android_xml_colors_as_argb_and_css_as_rgba(self):
        self.assertEqual(audit_colors.scan_text("<color>#FF3B82F6</color>", android_order=True), ["#3B82F6"])
        self.assertEqual(audit_colors.scan_text("a{color:#3B82F680}"), ["#3B82F6"])
        self.assertEqual(audit_colors.scan_text("val c = Color(0xFF3B82F6)"), ["#3B82F6"])

    def test_bind_writes_every_stack_with_both_modes(self):
        with tempfile.TemporaryDirectory() as d:
            out = self._build(d)
            tokens = os.path.join(out, "tokens.json")
            expect = {"flutter": ("app_theme.dart", "ColorScheme lightColorScheme"), "compose": ("AppColors.kt", "lightColorScheme("),
                      "swiftui": ("AppColors.swift", "enum AppColor"), "react-native": ("colors.ts", "export const darkColors"),
                      "vue": ("useTheme.ts", "data-theme")}
            for stack, (fname, needle) in expect.items():
                dest = os.path.join(d, stack)
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(theme.main(["bind", "--tokens", tokens, "--stack", stack, "--out", dest]), 0, stack)
                text = read(os.path.join(dest, fname))
                self.assertIn(needle, text, stack)
                self.assertNotIn("{{", text)
                if stack in ("flutter", "compose"):
                    for slot in ("surfaceContainerLowest", "surfaceContainerLow", "surfaceContainerHigh", "surfaceContainerHighest", "inversePrimary", "scrim"):
                        self.assertIn(slot, text, "%s lacks %s" % (stack, slot))
                    self.assertGreaterEqual(text.count("surfaceContainerHigh"), 2, stack)
                self.assertEqual(text.count("{"), text.count("}"), stack)
                self.assertEqual(text.count("("), text.count(")"), stack)

    def test_bind_rejects_an_unknown_stack(self):
        with tempfile.TemporaryDirectory() as d:
            out = self._build(d)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(theme.main(["bind", "--tokens", os.path.join(out, "tokens.json"), "--stack", "cobol", "--out", d]), 2)

    def test_from_brief_fills_flags_and_the_command_line_wins(self):
        with tempfile.TemporaryDirectory() as d:
            brief = os.path.join(d, "color-brief.json")
            write(brief, json.dumps({"brief": "a calming meditation app", "mood": "calm", "platform": "mobile", "seed": "7", "chroma": "low"}))
            out = os.path.join(d, "o")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(theme.main(["build", "--from-brief", brief, "--seed", "9", "--out", out]), 0)
            r = json.loads(read(os.path.join(out, "recipe.json")))
            self.assertEqual(r["moods"], ["calm"])
            self.assertEqual(r["platforms"], ["mobile"])
            self.assertEqual(r["seed"], "9")


class LiveAndTools(unittest.TestCase):
    def recipe(self, brief="fintech banking app", seed="2", **extra):
        return mixer.mix(brief, seed, overrides=dict({"platforms": ["web"]}, **extra), lib=LIB)

    def test_color_amount_scales_brand_chroma_and_keeps_the_gate(self):
        for brief in BRIEFS[:5]:
            lo = build.build(dict(self.recipe(brief), color_amount=0.0), LIB)
            hi = build.build(dict(self.recipe(brief), color_amount=1.0), LIB)
            c_lo = oklch.hex_to_oklch(lo["palettes"]["primary"][500])[1]
            c_hi = oklch.hex_to_oklch(hi["palettes"]["primary"][500])[1]
            self.assertLess(c_lo, 0.005, brief)
            self.assertGreater(c_hi, c_lo + 0.03, brief)
            for t in (lo, hi):
                self.assertEqual([c for c in t["checks"] if not c["pass"]], [], brief)

    def test_status_colors_do_not_scale_with_color_amount(self):
        a = build.build(dict(self.recipe(), color_amount=0.0), LIB)["palettes"]["danger"][500]
        b = build.build(dict(self.recipe(), color_amount=1.0), LIB)["palettes"]["danger"][500]
        self.assertEqual(a, b)

    def test_neutral_temp_moves_the_neutral_hue(self):
        base = self.recipe()
        cool = build.build(dict(base, neutral_temp="cool"), LIB)["palettes"]["neutral"][500]
        warm = build.build(dict(base, neutral_temp="warm"), LIB)["palettes"]["neutral"][500]
        self.assertNotEqual(cool, warm)
        self.assertGreater(oklch.hex_to_oklch(cool)[2], oklch.hex_to_oklch(warm)[2])

    def test_live_grid_has_every_knob_position_with_a_verdict(self):
        grid = build.live_grid(self.recipe(), LIB)
        self.assertEqual(len(grid), len(build.AMOUNTS) * len(build.TEMPS))
        for key, cell in grid.items():
            self.assertEqual(set(cell["light"]), set(cell["dark"]), key)
            self.assertEqual(len(cell["failing"]), min(cell["fails"], 4), key)

    def test_build_live_writes_a_page_whose_data_parses(self):
        with tempfile.TemporaryDirectory() as d:
            with redirect_stdout(io.StringIO()):
                theme.main(["build", "--brief", "calm meditation app", "--seed", "3", "--out", d, "--live", "--color-amount", "0.5", "--neutral-temp", "warm"])
            html = read(os.path.join(d, "live.html"))
            self.assertIn('id="amt"', html)
            self.assertNotIn("Live tuning", read(os.path.join(d, "preview.html")))
            data = html.split("var GRID=", 1)[1].split(",START=", 1)[0]
            self.assertEqual(len(json.loads(data.replace("<\\/", "</"))), 15)
            start = html.split(",START=", 1)[1].split(",$=", 1)[0]
            self.assertEqual(json.loads(start), {"amount": 0.5, "temp": "warm"})

    def test_color_amount_out_of_range_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            self.assertEqual(theme.main(["build", "--brief", "x", "--out", tempfile.gettempdir() + "/never-written", "--color-amount", "1.5"]), 2)

    def test_names_list_is_unique_and_exact_colors_match(self):
        entries = names._load()
        self.assertGreaterEqual(len(entries), 100)
        self.assertEqual(len({n for n, *_ in entries}), len(entries))
        for name, hx, _ in entries[:20]:
            top = names.nearest(hx)[0]
            self.assertEqual(top[0], name)
            self.assertLess(top[2], 0.01)
        self.assertEqual(names.describe("#FFFFFF"), "Snow")

    def test_mix_ends_and_spaces(self):
        for space in mixing.SPACES:
            self.assertEqual(mixing.mix("#1F6FEB", "#FFFFFF", 0, space), "#1F6FEB", space)
            self.assertEqual(mixing.mix("#1F6FEB", "#FFFFFF", 1, space), "#FFFFFF", space)
        self.assertEqual(mixing.mix("#000000", "#FFFFFF", 0.5, "srgb"), "#808080")
        mid = {r["space"]: r["L"] for r in mixing.compare("#FF0000", "#0000FF", 0.5)}
        self.assertLess(mid["srgb"], mid["oklab"])
        with self.assertRaises(ValueError):
            mixing.mix("#000000", "#FFFFFF", 0.5, "hsl")
        ramp = mixing.ramp("#000000", "#FFFFFF", 5, "oklab")
        lights = [oklch.hex_to_oklch(c)[0] for c in ramp]
        self.assertEqual(lights, sorted(lights))

    def test_sequential_moves_one_way_and_diverging_mirrors(self):
        for dark in (False, True):
            seq = scales.sequential(250, 7, dark=dark)
            self.assertTrue(all(ok for *_, ok in scales.check("sequential", seq, "#FFFFFF")), dark)
            div = scales.diverging(250, 40, 9, dark=dark)
            self.assertEqual(len(div), 9)
            self.assertTrue(all(ok for *_, ok in scales.check("diverging", div, "#FFFFFF")), dark)

    def test_categorical_stays_visible_and_apart_up_to_six(self):
        for hue in (20, 140, 250, 330):
            for ground, dark in (("#FFFFFF", False), ("#101010", True)):
                for n in (3, 4, 5, 6):
                    cols = scales.categorical(hue, n, ground, dark=dark)
                    self.assertEqual(len(set(cols)), n)
                    rows = scales.check("categorical", cols, ground)
                    self.assertTrue(all(ok for *_, ok in rows), (hue, ground, n, rows))
        with self.assertRaises(ValueError):
            scales.categorical(250, 11)

    def test_scale_command_reports_failure_in_its_exit_code(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(theme.main(["scale", "categorical", "--n", "5"]), 0)
            self.assertEqual(theme.main(["scale", "categorical", "--n", "10", "--mode", "light"]), 1)
        with contextlib.redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            self.assertEqual(theme.main(["scale", "categorical", "--n", "12"]), 2)

    def test_report_lists_plain_names(self):
        t = build.build(self.recipe(), LIB)
        self.assertIn("## Palette names", emit.report_md(t, LIB))


class ColorThemeData(unittest.TestCase):
    PAIRS = os.path.join(HERE, "..", "..", "..", "..", "..", "color-kit", "data", "essential-pairs.csv")

    def test_essential_pairs_pass_for_every_brief_platform_and_seed(self):
        if not os.path.exists(self.PAIRS):
            self.skipTest("color-kit is not installed next to design-system-kit")
        rows = check_pairs.read_pairs(self.PAIRS)
        failures = []
        for brief in BRIEFS:
            for plats in PLATFORMS:
                for seed in ("1", "2", "3"):
                    with tempfile.TemporaryDirectory() as d:
                        out = os.path.join(d, "o")
                        with redirect_stdout(io.StringIO()):
                            theme.main(["build", "--brief", brief, "--seed", seed, "--platform", ",".join(plats), "--out", out])
                        tokens = check_pairs.load_tokens(os.path.join(out, "tokens.json"))
                    bad = [r for r in check_pairs.measure(rows, tokens) if not r["pass"]]
                    if bad:
                        failures.append((brief, plats, seed, bad[0]["name"], bad[0]["mode"], bad[0]["ratio"]))
        self.assertEqual(failures, [], failures[:3])

    def test_roles_csv_names_exist_in_the_built_tokens(self):
        roles = os.path.join(os.path.dirname(self.PAIRS), "roles.csv")
        if not os.path.exists(roles):
            self.skipTest("color-kit is not installed next to design-system-kit")
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "o")
            with redirect_stdout(io.StringIO()):
                theme.main(["build", "--brief", "fintech app", "--out", out])
            tokens = check_pairs.load_tokens(os.path.join(out, "tokens.json"))
        with open(roles, encoding="utf-8", newline="") as f:
            import csv as _csv
            names = [r["role"] for r in _csv.DictReader(f)]
        missing = [n for n in names if n not in tokens["light"] and not n.startswith(("scrim", "chart"))]
        self.assertEqual(missing, [])


class Extractor(unittest.TestCase):
    HTML = """<html><head><title>Acme Pay | Home</title><meta name="description" content="Pay anyone fast.">
    <style>
    :root{--brand:#E4572E;--ink:#1B1B1F}
    body{color:var(--ink);background:#FFFFFF;font-family:'Poppins',sans-serif;font-size:16px}
    h1{font-family:'Poppins';font-size:48px;font-weight:700}
    .btn{background:var(--brand);color:#fff;border-radius:999px;padding:12px 24px;transition:all 200ms cubic-bezier(.2,0,0,1);box-shadow:0 2px 8px rgba(0,0,0,.12)}
    .card{background:#F6F4F1;border:1px solid #E7E2DC;border-radius:16px;padding:24px;margin:16px}
    a{color:#E4572E}
    </style></head><body><h1>Hi</h1><a class="btn">Pay</a></body></html>"""

    def test_extract_from_local_html(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "page.html")
            write(src, self.HTML)
            out = os.path.join(d, "ex.json")
            md = os.path.join(d, "as-found.md")
            with redirect_stdout(io.StringIO()):
                code = extract_site.main(["--html", src, "--base", "https://example.test/", "--out", out, "--design-md", md])
            self.assertEqual(code, 0)
            ex = json.loads(read(out))
            hexes = [c["hex"] for c in ex["colors"]]
            self.assertIn("#E4572E", hexes)
            s = ex["suggest"]
            self.assertTrue(10 < s["hue"] < 50, s)
            self.assertEqual(s["voice"], "geometric-modern")
            self.assertEqual(s["shape"], "pill")
            self.assertIn("Poppins", [f for f, _ in ex["fonts"]])
            text = read(md)
            self.assertIn("#E4572E", text)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(theme.main(["check", md]), 0)

    def test_remix_from_extract_keeps_the_hue(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "page.html")
            write(src, self.HTML)
            ex = os.path.join(d, "ex.json")
            with redirect_stdout(io.StringIO()):
                extract_site.main(["--html", src, "--out", ex])
                code = theme.main(["build", "--brief", "payments app", "--from-extract", ex, "--out", os.path.join(d, "o")])
            self.assertEqual(code, 0)
            recipe = json.loads(read(os.path.join(d, "o", "recipe.json")))
            self.assertTrue(10 < recipe["hue"] < 50, recipe["hue"])

    def test_browser_json_path(self):
        sample = {"url": "https://example.test", "title": "JS app", "text": {"#1B1B1F": 20}, "bg": {"#F6F3EE": 200, "#FFFFFF": 150, "#2F6F73": 4},
                  "border": {"#DDD5CB": 3}, "fonts": {"Georgia": 5}, "sizes": {"16": 8, "32": 1}, "weights": {"400": 8}, "radii": {"12": 2, "16": 1},
                  "shadows": {}, "gaps": {"12": 3, "24": 3}, "durations": [180], "easings": {"ease-out": 1}, "faces": [], "custom_props": {}, "dark_media": False}
        with tempfile.TemporaryDirectory() as d:
            src, out = os.path.join(d, "b.json"), os.path.join(d, "ex.json")
            write(src, json.dumps(sample))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(extract_site.main(["--browser-json", src, "--out", out]), 0)
            s = json.loads(read(out))["suggest"]
            self.assertTrue(180 < s["hue"] < 220, s)
            self.assertEqual(s["voice"], "classic-serif")
            self.assertEqual(s["ground"], "soft")

    def test_tokens_json_works_with_generate_tokens_script(self):
        import shutil
        import subprocess
        node = shutil.which("node")
        if not node:
            self.skipTest("node not found")
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "design")
            with redirect_stdout(io.StringIO()):
                theme.main(["build", "--brief", "fintech app", "--out", out])
            r = subprocess.run([node, os.path.join(HERE, "..", "generate-tokens.cjs"), "--config", os.path.join(out, "tokens.json")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("--color-primary:", r.stdout)
            self.assertIn(".dark {", r.stdout)

    def test_only_http_urls_are_allowed(self):
        with self.assertRaises(ValueError):
            extract_site.fetch("file:///etc/passwd")


if __name__ == "__main__":
    unittest.main()
