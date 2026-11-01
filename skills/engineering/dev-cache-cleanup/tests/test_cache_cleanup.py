import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cache_cleanup.py"
BROWSER = next((p for p in [os.environ.get("CHROME_BIN"), shutil.which("chromium"),
                           shutil.which("google-chrome"),
                           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
                if p and Path(p).is_file()), None)
spec = importlib.util.spec_from_file_location("cache_cleanup", str(SCRIPT))
cache = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cache)


class CacheCleanupTests(unittest.TestCase):
    def setUp(self):
        # Resolve the platform temp parent before creating fixtures (macOS aliases /tmp).
        self.temp = tempfile.TemporaryDirectory(dir=str(Path(tempfile.gettempdir()).resolve()))
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        self.target = self.root / "node_modules"
        self.target.mkdir()
        (self.target / "package.txt").write_text("generated fixture")

    def tearDown(self):
        self.temp.cleanup()

    def plan(self, paths=None):
        report = cache.scan([str(self.root)], 10_000)
        return cache.make_plan(report, [str(self.root)], paths or [str(self.target)])

    def test_catalog_documents_every_home_audit_path(self):
        catalog = Path(__file__).resolve().parents[1] / "references" / "caches.md"
        text = catalog.read_text()
        for relative in cache.GLOBAL_CACHE_SUBPATHS:
            self.assertIn("`" + relative + "`", text)

    def test_ecosystem_samples_keep_packages_and_ambiguous_builds_manual(self):
        web = self.root / "web"
        web.mkdir()
        for name in (".next", ".turbo", ".vite", ".output"):
            (web / name).mkdir()
        android = self.root / "android" / "app"
        android.mkdir(parents=True)
        (android / "build.gradle.kts").write_text("plugins {}\n")
        cxx = android / ".cxx"
        cxx.mkdir()
        build = android / "build"
        apk = build / "outputs" / "apk" / "release"
        apk.mkdir(parents=True)
        (apk / "app-release.apk").write_bytes(b"apk-bytes")
        (build / "intermediates" / "huge").mkdir(parents=True)
        (android.parent / ".gradle").mkdir()
        ios = self.root / "ios"
        ios.mkdir()
        (ios / "Pods").mkdir()
        (ios / "Runner.xcarchive").mkdir()
        java = self.root / "service"
        java.mkdir()
        (java / "pom.xml").write_text("<project/>")
        (java / "target").mkdir()
        (java / "build").mkdir()
        rust = self.root / "crate"
        rust.mkdir()
        (rust / "Cargo.toml").write_text("[package]\nname='c'\n")
        (rust / "target").mkdir()
        unmarked = self.root / "notes" / "target"
        unmarked.parent.mkdir()
        unmarked.mkdir()
        (self.root / "App.ipa").write_bytes(b"ipa")

        report = cache.scan([str(self.root)], 10_000_000)
        entries = {e["path"]: e for e in report["entries"]}

        def entry(path):
            self.assertIn(str(path), entries)
            return entries[str(path)]

        for path in (web / ".next", web / ".turbo", web / ".vite", web / ".output", cxx, java / "target", rust / "target"):
            self.assertTrue(entry(path)["eligible"], path)
        self.assertEqual(entry(rust / "target")["category"], "Rust")
        self.assertEqual(entry(java / "target")["category"], "Java / Maven")
        self.assertFalse(entry(unmarked)["eligible"])
        for path in (build, android.parent / ".gradle", ios / "Pods", ios / "Runner.xcarchive", java / "build"):
            self.assertFalse(entry(path)["eligible"], path)
        packaged = entry(apk / "app-release.apk")
        self.assertFalse(packaged["eligible"])
        self.assertEqual(packaged["category"], "Packaged app")
        self.assertEqual(packaged["estimated_bytes"], len(b"apk-bytes"))
        self.assertFalse(entry(self.root / "App.ipa")["eligible"])
        self.assertNotIn(str(build / "intermediates"), entries)
        with self.assertRaises(cache.Refused):
            cache.make_plan(report, [str(self.root)], [str(apk / "app-release.apk")])
        with self.assertRaises(cache.Refused):
            cache.make_plan(report, [str(self.root)], [str(build)])

    def test_scans_expected_cache_and_reports_manual_files(self):
        (self.root / "model.bin").write_bytes(b"x" * 20)
        report = cache.scan([str(self.root)], 10)
        by_path = {e["path"]: e for e in report["entries"]}
        self.assertTrue(by_path[str(self.target)]["eligible"])
        self.assertFalse(by_path[str(self.root / "model.bin")]["eligible"])

    def test_explicit_home_audit_checks_only_closed_cache_subpaths(self):
        home = self.root.parent / "fake-home"
        home.mkdir()
        for relative in cache.GLOBAL_CACHE_SUBPATHS:
            candidate = home / relative
            candidate.mkdir(parents=True, exist_ok=True)
            (candidate / "cached.bin").write_bytes(b"cache")
        binary = home / ".cargo" / "bin" / "keep-cli"
        binary.parent.mkdir()
        binary.write_text("load-bearing shell tool")
        unrelated = home / "private-material" / "must-not-scan"
        unrelated.parent.mkdir()
        unrelated.write_bytes(b"private")
        opened = []
        actual_scandir = cache.os.scandir
        def observed_scandir(path):
            opened.append(Path(path))
            return actual_scandir(path)
        with mock.patch.object(cache.os, "scandir", side_effect=observed_scandir):
            report = cache.scan([], 1, str(home))
        self.assertEqual(report["roots"], [])
        self.assertEqual(report["audit_home"], str(home))
        self.assertEqual({e["path"] for e in report["entries"]},
                         {str(home / p) for p in cache.GLOBAL_CACHE_SUBPATHS})
        self.assertTrue(all(e["eligible"] is False and e["scope"] == "global-audit" for e in report["entries"]))
        self.assertNotIn(home, opened)
        self.assertNotIn(home / ".cargo", opened)
        self.assertNotIn(binary.parent, opened)
        self.assertNotIn(unrelated.parent, opened)
        self.assertEqual(binary.read_text(), "load-bearing shell tool")

    def test_home_audit_is_opt_in_and_global_rows_never_become_plans(self):
        home = self.root.parent / "fake-home"
        candidate = home / ".npm"
        candidate.mkdir(parents=True)
        (candidate / "entry.bin").write_bytes(b"cache")
        default_report = cache.scan([str(self.root)], 1)
        self.assertIsNone(default_report["audit_home"])
        self.assertFalse(any(e.get("scope") == "global-audit" for e in default_report["entries"]))
        report = cache.scan([str(self.root)], 1, str(home))
        self.assertEqual(report["roots"], [str(self.root)])
        with self.assertRaisesRegex(cache.Refused, "global cache audit"):
            cache.make_plan(report, [str(self.root)], [str(candidate)])
        # Even an explicit fake-home root does not upgrade the audit-only entry.
        report["roots"] = [str(home)]
        with self.assertRaisesRegex(cache.Refused, "global cache audit"):
            cache.make_plan(report, [str(home)], [str(candidate)])

    def test_home_cache_measurement_is_bounded_and_gaps_are_visible(self):
        home = self.root.parent / "fake-home"
        candidate = home / ".npm"
        candidate.mkdir(parents=True)
        for i in range(10):
            (candidate / str(i)).write_bytes(b"cache")
        measured, issues = cache.measure_audit(candidate, max_entries=2, max_seconds=30)
        self.assertFalse(measured["measurement_complete"])
        self.assertIsNone(measured["estimated_bytes"])
        self.assertLessEqual(measured["inspected_objects"], 2)
        self.assertTrue(any("budget" in e for e in issues))
        with mock.patch.object(cache, "measure_audit", return_value=(measured, issues)):
            report = cache.scan([], 1, str(home))
        self.assertTrue(report["issues"])
        self.assertIsNone(report["entries"][0]["estimated_bytes"])
        self.assertIn("measurement incomplete", report["entries"][0]["reason"])
        self.assertEqual(cache.report_totals(report)["Global cache audit"]["unmeasured"], 1)

    def test_home_audit_skips_symlinks_and_exposes_permission_errors(self):
        home = self.root.parent / "fake-home"
        home.mkdir()
        external = self.root.parent / "external-cache"
        external.mkdir()
        (external / "keep.txt").write_text("must survive")
        (home / ".npm").symlink_to(external, target_is_directory=True)
        report = cache.scan([], 1, str(home))
        self.assertEqual(len(report["entries"]), 1)
        self.assertFalse(report["entries"][0]["eligible"])
        self.assertIsNone(report["entries"][0]["estimated_bytes"])
        self.assertTrue(any("symlink" in e for e in report["issues"]))
        self.assertTrue((external / "keep.txt").exists())
        (home / ".npm").unlink()
        (home / ".npm").mkdir()
        real_scandir = cache.os.scandir
        def denied(path):
            if Path(path) == home / ".npm":
                raise PermissionError("synthetic cache read denial")
            return real_scandir(path)
        with mock.patch.object(cache.os, "scandir", side_effect=denied):
            report = cache.scan([], 1, str(home))
        self.assertTrue(any("synthetic cache read denial" in e for e in report["issues"]))
        self.assertFalse(report["entries"][0]["measurement_complete"])

    def test_cli_home_only_audit_without_any_deletable_roots(self):
        home = self.root.parent / "fake-home"
        (home / ".npm").mkdir(parents=True)
        (home / ".npm" / "cached.txt").write_text("cache")
        report_path = self.root.parent / "home-audit.json"
        completed = subprocess.run([sys.executable, str(SCRIPT), "scan", "--audit-home", str(home),
                                    "--output", str(report_path)], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(report_path.read_text())
        self.assertEqual(report["roots"], [])
        self.assertFalse(report["entries"][0]["eligible"])
        self.assertTrue((home / ".npm" / "cached.txt").exists())
        with self.assertRaises(cache.Refused):
            cache.scan([], 1)

    def test_unsafe_root_is_refused(self):
        for root in ["/", str(Path.home()), str(Path.home().parent), "/usr", "/private/tmp"]:
            with self.subTest(root=root), self.assertRaises(cache.Refused):
                cache.root_path(root)

    def test_root_and_target_symlinks_refused(self):
        alias = self.root.parent / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(cache.Refused):
            cache.scan([str(alias)], 10)
        plan = self.plan()
        moved = self.root / "old-artifact"
        self.target.rename(moved)
        self.target.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(cache.Refused):
            cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertTrue((moved / "package.txt").exists())

    def test_internal_symlink_is_unlinked_without_touching_target(self):
        outside = self.root.parent / "kept.txt"
        outside.write_text("must remain")
        (self.target / "linked.txt").symlink_to(outside)
        plan = self.plan()
        result = cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertTrue(result["completed"])
        self.assertEqual(outside.read_text(), "must remain")

    def test_explicit_roots_are_required_and_cannot_be_changed_by_report(self):
        report = cache.scan([str(self.root)], 10_000)
        report["roots"] = [str(self.root.parent)]
        with self.assertRaises(cache.Refused):
            cache.make_plan(report, [str(self.root)], [str(self.target)])

    def test_report_target_outside_approved_root_refused(self):
        other = self.root.parent / "node_modules"
        other.mkdir()
        report = cache.scan([str(self.root)], 10_000)
        report["entries"].append({"path": str(other), "root": str(self.root), "eligible": True})
        with self.assertRaises(cache.Refused):
            cache.make_plan(report, [str(self.root)], [str(other)])

    def test_root_itself_cannot_be_deleted(self):
        report = cache.scan([str(self.root)], 10_000)
        report["entries"].append({"path": str(self.root), "root": str(self.root), "eligible": True})
        with self.assertRaises(cache.Refused):
            cache.make_plan(report, [str(self.root)], [str(self.root)])

    def test_stale_scan_and_stale_plan_refused(self):
        report = cache.scan([str(self.root)], 10_000)
        (self.target / "new.txt").write_text("new")
        with self.assertRaises(cache.Refused):
            cache.make_plan(report, [str(self.root)], [str(self.target)])
        plan = self.plan()
        (self.target / "other.txt").write_text("newer")
        with self.assertRaises(cache.Refused):
            cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertTrue(self.target.exists())

    def test_plan_tampering_or_wrong_approval_is_refused(self):
        plan = self.plan()
        with self.assertRaises(cache.Refused):
            cache.apply_plan(plan, "0" * 64, True)
        approved = plan["approval_digest"]
        plan["targets"][0]["estimated_bytes"] += 1
        with self.assertRaises(cache.Refused):
            cache.apply_plan(plan, approved, True)

    def test_expired_plan_refused(self):
        plan = self.plan()
        with mock.patch.object(cache.time, "time", return_value=plan["expires_at"] + 1):
            with self.assertRaises(cache.Refused):
                cache.apply_plan(plan, plan["approval_digest"], True)

    def test_dry_run_preserves_files_and_confirm_requires_digest(self):
        plan = self.plan()
        self.assertTrue(cache.apply_plan(plan)["dry_run"])
        self.assertTrue(self.target.exists())
        with self.assertRaises(cache.Refused):
            cache.apply_plan(plan, confirm=True)
        self.assertTrue(self.target.exists())

    def test_ambiguous_toolchain_go_and_large_file_are_not_plan_candidates(self):
        report = cache.scan([str(self.root)], 1)
        for name in ["build", ".cargo", "go"]:
            (self.root / name).mkdir()
        report = cache.scan([str(self.root)], 1)
        entries = {e["path"]: e for e in report["entries"]}
        for name in ["build", ".cargo", "go"]:
            path = self.root / name
            self.assertFalse(entries[str(path)]["eligible"])
            with self.assertRaises(cache.Refused):
                cache.make_plan(report, [str(self.root)], [str(path)])
        self.assertFalse(cache.versioned(self.target))

    def test_nested_repository_is_refused(self):
        (self.target / ".git").mkdir()
        report = cache.scan([str(self.root)], 10_000)
        self.assertTrue(report["issues"])
        self.assertFalse(any(e["path"] == str(self.target) for e in report["entries"]))

    def test_tracked_content_blocks_plan(self):
        with mock.patch.object(cache, "versioned", return_value=True):
            report = cache.scan([str(self.root)], 10_000)
            self.assertFalse(report["entries"][0]["eligible"])
            with self.assertRaises(cache.Refused):
                cache.make_plan(report, [str(self.root)], [str(self.target)])

    def test_full_batch_is_preflighted_before_removal(self):
        other = self.root / "__pycache__"
        other.mkdir()
        plan = self.plan([str(self.target), str(other)])
        (other / "new.txt").write_text("changed")
        with self.assertRaises(cache.Refused):
            cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertTrue(self.target.exists())

    def test_partial_failure_stops_batch_and_reports_unattempted(self):
        second = self.root / "__pycache__"
        third = self.root / ".pytest_cache"
        second.mkdir(); third.mkdir()
        plan = self.plan([str(self.target), str(second), str(third)])
        original = cache.remove_target
        def delete(path, root, root_identity, target_identity):
            if path == second:
                raise PermissionError("synthetic denial")
            original(path, root, root_identity, target_identity)
        with mock.patch.object(cache, "remove_target", side_effect=delete):
            result = cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertFalse(result["completed"])
        self.assertEqual([r["status"] for r in result["results"]], ["removed", "failed"])
        self.assertEqual(result["remaining"], [str(third)])
        self.assertTrue(third.exists())

    def test_html_escapes_untrusted_paths(self):
        report = {"entries": [{"path": "<script>alert(1)</script>", "reason": "<bad>"}], "issues": ["<error>"]}
        rendered = cache.report_html(report)
        self.assertNotIn("<script>alert(1)</script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_report_totals_separate_manual_unknown_and_eligible(self):
        report = {"entries": [
            {"path": "/fixture/node_modules", "kind": "directory", "eligible": True, "estimated_bytes": 120},
            {"path": "/fixture/archive.bin", "kind": "file", "eligible": False, "estimated_bytes": 500},
            {"path": "/fixture/.cargo", "kind": "directory", "eligible": False, "estimated_bytes": None},
        ], "issues": []}
        totals = cache.report_totals(report)
        self.assertEqual(totals["JavaScript"]["eligible_bytes"], 120)
        self.assertEqual(totals["Large individual files"]["manual_bytes"], 500)
        self.assertEqual(totals["Protected runtime/toolchain"]["unmeasured"], 1)
        result = cache.report_html(report)
        self.assertIn('id="eligible-summary"', result)
        self.assertIn('id="manual-summary"', result)
        self.assertIn('id="category-totals"', result)
        self.assertEqual(result.count('<table class="targets">'), 2)
        self.assertIn('id="filter-query"', result)
        self.assertIn('data-key="bytes"', result)
        self.assertIn('Unmeasured', result)

    @unittest.skipUnless(shutil.which("node"), "Node is needed to exercise report browser helpers")
    def test_report_search_category_and_numeric_sort_helpers(self):
        code = cache.REPORT_SCRIPT + r'''
const assert = require('node:assert/strict');
assert.equal(filterMatch('/a/node_modules generated', 'JavaScript', 'NODE_MODULES', ''), true);
assert.equal(filterMatch('/a/node_modules generated', 'JavaScript', 'node', 'Python'), false);
assert.equal(filterMatch('/a/cache', 'Python', '', 'Python'), true);
assert.equal(compareValues('100', '20', 'bytes', 1) > 0, true);
assert.equal(compareValues('100', '20', 'bytes', -1) < 0, true);
assert.equal(compareValues('-1', '0', 'bytes', 1) < 0, true);
assert.equal(compareValues('b', 'a', 'path', 1) > 0, true);
'''
        result = subprocess.run([shutil.which("node"), "-e", code], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.environ.get("CACHE_BROWSER_SMOKE") == "1" and BROWSER,
                         "Optional UI smoke: set CACHE_BROWSER_SMOKE=1 with a working local Chromium browser")
    def test_report_filters_and_sort_in_headless_browser(self):
        report = {"entries": [
            {"path": "/demo/node_modules", "kind": "directory", "eligible": True, "estimated_bytes": 120},
            {"path": "/demo/_build", "kind": "directory", "eligible": True, "estimated_bytes": 20},
            {"path": "/demo/model.bin", "kind": "file", "eligible": False, "estimated_bytes": 500},
            {"path": "/demo/.cargo", "kind": "directory", "eligible": False, "estimated_bytes": None},
        ], "issues": []}
        ui_check = r'''<script>
const result = document.createElement('p'); result.id = 'browser-result';
try {
 const assert = (condition, message) => { if (!condition) throw Error(message); };
 const query = document.getElementById('filter-query');
 const category = document.getElementById('filter-category');
 const shown = () => Array.from(document.querySelectorAll('table.targets tbody tr')).filter(r => !r.hidden);
 query.value = 'model'; query.dispatchEvent(new Event('input'));
 assert(shown().length === 1 && shown()[0].textContent.includes('model.bin'), 'text filter');
 query.value = ''; category.value = 'JavaScript'; category.dispatchEvent(new Event('change'));
 assert(shown().length === 1 && shown()[0].textContent.includes('node_modules'), 'category filter');
 category.value = ''; category.dispatchEvent(new Event('change'));
 const table = document.querySelector('table.targets');
 const button = table.querySelector('button[data-key="bytes"]');
 button.click(); assert(table.tBodies[0].rows[0].dataset.bytes === '20', 'numeric ascending');
 button.click(); assert(table.tBodies[0].rows[0].dataset.bytes === '120', 'numeric descending');
 assert(document.querySelectorAll('table.targets').length === 2, 'separate manual table');
 assert(document.getElementById('eligible-summary').textContent.includes('140 estimated bytes'), 'eligible total');
 assert(document.getElementById('manual-summary').textContent.includes('500 known estimated bytes'), 'manual total');
 result.textContent = 'PASS';
} catch (error) { result.textContent = 'FAIL: ' + error.message; }
document.body.appendChild(result);
</script>'''
        page = self.root.parent / "report-browser.html"
        page.write_text(cache.report_html(report).replace("</html>", ui_check + "</html>"))
        completed = subprocess.run([BROWSER, "--headless", "--disable-gpu", "--no-first-run",
                                    "--no-default-browser-check", "--disable-background-networking",
                                    "--disable-component-update", "--user-data-dir=" + str(self.root.parent / "browser-profile"),
                                    "--dump-dom", "--virtual-time-budget=1000", page.as_uri()],
                                   capture_output=True, text=True, timeout=30)
        self.assertEqual(completed.returncode, 0, completed.stderr[-2000:])
        self.assertIn('<p id="browser-result">PASS</p>', completed.stdout)

    def test_root_replacement_is_refused(self):
        plan = self.plan()
        moved = self.root.parent / "previous-project"
        self.root.rename(moved)
        self.root.mkdir()
        with self.assertRaises(cache.Refused):
            cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertTrue((moved / "node_modules" / "package.txt").exists())

    def test_root_swapped_after_preflight_before_open_is_refused(self):
        plan = self.plan()
        original_remove = cache.remove_target
        moved = self.root.parent / "original-project"
        def replace_then_remove(path, root, root_identity, target_identity):
            root.rename(moved)
            root.mkdir()
            replacement = root / "node_modules"
            replacement.mkdir()
            (replacement / "keep.txt").write_text("replacement must survive")
            return original_remove(path, root, root_identity, target_identity)
        with mock.patch.object(cache, "remove_target", side_effect=replace_then_remove):
            result = cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertFalse(result["completed"])
        self.assertIn("approved root changed", result["results"][0]["error"])
        self.assertTrue((self.root / "node_modules" / "keep.txt").exists())
        self.assertTrue((moved / "node_modules" / "package.txt").exists())

    def test_target_swapped_after_preflight_before_open_is_refused(self):
        plan = self.plan()
        original_remove = cache.remove_target
        moved = self.root / "previous-cache"
        def replace_then_remove(path, root, root_identity, target_identity):
            path.rename(moved)
            path.mkdir()
            (path / "keep.txt").write_text("replacement must survive")
            return original_remove(path, root, root_identity, target_identity)
        with mock.patch.object(cache, "remove_target", side_effect=replace_then_remove):
            result = cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertFalse(result["completed"])
        self.assertIn("approved target changed", result["results"][0]["error"])
        self.assertTrue((self.target / "keep.txt").exists())
        self.assertTrue((moved / "package.txt").exists())

    def test_opened_target_device_changed_after_preflight_is_refused(self):
        plan = self.plan()
        actual_fstat = cache.os.fstat
        count = [0]
        def boundary(fd):
            info = actual_fstat(fd)
            count[0] += 1
            if count[0] == 2:
                values = list(info)
                values[2] = info.st_dev + 1
                return os.stat_result(values)
            return info
        with mock.patch.object(cache.os, "fstat", side_effect=boundary):
            result = cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertFalse(result["completed"])
        self.assertIn("filesystem boundary", result["results"][0]["error"])
        self.assertTrue((self.target / "package.txt").exists())

    def test_nested_opened_directory_device_boundary_is_refused(self):
        nested = self.target / "nested"
        nested.mkdir()
        (nested / "preserve.txt").write_text("mounted content")
        # Keep parent empty until the nested directory is checked: no partial work is needed.
        (self.target / "package.txt").unlink()
        plan = self.plan()
        actual_fstat = cache.os.fstat
        count = [0]
        def boundary(fd):
            info = actual_fstat(fd)
            count[0] += 1
            if count[0] == 4:
                values = list(info)
                values[2] = info.st_dev + 1
                return os.stat_result(values)
            return info
        with mock.patch.object(cache.os, "fstat", side_effect=boundary):
            result = cache.apply_plan(plan, plan["approval_digest"], True)
        self.assertFalse(result["completed"])
        self.assertIn("filesystem boundary", result["results"][0]["error"])
        self.assertTrue((nested / "preserve.txt").exists())

    def test_output_never_overwrites_and_uses_private_permissions(self):
        destination = self.root / "receipt.json"
        cache.output(destination, {"result": "ok"})
        self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
        with self.assertRaises(cache.Refused):
            cache.output(destination, {"result": "changed"})
        self.assertEqual(json.loads(destination.read_text())["result"], "ok")

    def test_cli_roundtrip_on_synthetic_project(self):
        report = self.root.parent / "audit.json"
        plan_path = self.root.parent / "plan.json"
        html_path = self.root.parent / "audit.html"
        def command(*args):
            result = subprocess.run([sys.executable, str(SCRIPT)] + list(args), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout
        command("scan", "--root", str(self.root), "--output", str(report))
        command("report", str(report), "--output", str(html_path))
        self.assertIn("Artifact audit", html_path.read_text())
        command("plan", str(report), "--root", str(self.root), "--select", str(self.target), "--output", str(plan_path))
        dry = json.loads(command("apply", str(plan_path)))
        self.assertTrue(dry["dry_run"])
        self.assertTrue(self.target.exists())
        result = json.loads(command("apply", str(plan_path), "--approve", dry["approval_digest"], "--confirm"))
        self.assertTrue(result["completed"])
        self.assertFalse(self.target.exists())

    def test_cli_bad_input_and_help(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "apply", str(self.root / "missing.json")], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"Refused:", result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    import sys
    unittest.main()
