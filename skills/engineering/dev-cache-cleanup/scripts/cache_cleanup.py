#!/usr/bin/env python3
"""Audit project artifacts, approve exact targets, and remove only unchanged targets.

Python 3.9+, standard library. No global cache command is invoked.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

SCHEMA = 1
GLOBAL_CACHE_SUBPATHS = (
    ".npm", ".cache/pip", ".cache/yarn", ".cache/pnpm", ".cache/go-build", ".cache/composer",
    ".cargo/registry", ".bun/install/cache", ".gradle/caches", ".m2/repository", ".nuget/packages",
    ".pub-cache", ".composer/cache", ".mix", ".hex", ".gem", "go/pkg/mod",
    ".android/cache", ".android/build-cache", "Library/Caches",
    "Library/pnpm/store", "Library/Developer/Xcode/DerivedData", ".local/share/pnpm/store",
)
CACHE_NAMES = {
    "node_modules", ".next", ".nuxt", ".output", ".svelte-kit", ".parcel-cache", ".turbo", ".vite", ".swc",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".nox", ".hypothesis",
    ".phpunit.cache",
}
BUILD_NAMES = {
    "target": {"Cargo.toml", "pom.xml"},
    "_build": {"mix.exs"},
    ".dart_tool": {"pubspec.yaml"},
    ".angular": {"angular.json"},
    ".cxx": {"build.gradle", "build.gradle.kts"},
}
REVIEW_NAMES = {
    "build", "dist", "bin", "obj", "out", "coverage", "Pods", ".gradle", ".cache", "vendor", "deps",
    "DerivedData", "Carthage", ".yarn", ".expo", ".bundle", "storybook-static", "playwright-report",
    "test-results", "cover",
}
PACKAGE_SUFFIXES = {".apk", ".aab", ".apks", ".ipa"}
PACKAGE_PARENTS = {"build", "dist", "bin", "obj", "DerivedData", "Carthage"}
PACKAGE_WALK_NAMES = {"outputs", "apk", "bundle", "release", "debug", "ipa", "products", "build", "archives", "app"}
PROTECTED_NAMES = {".git", ".cargo", ".rustup", ".asdf", ".bun", ".fvm", ".docker",
                   ".colima", ".orbstack", ".minikube", "go"}
NAME_CATEGORIES = {
    "node_modules": "JavaScript", ".yarn": "Node.js",
    ".next": "Web", ".nuxt": "Web", ".output": "Web", ".svelte-kit": "Web", ".parcel-cache": "Web",
    ".turbo": "Web", ".vite": "Web", ".swc": "Web", ".angular": "Web", "storybook-static": "Web",
    "playwright-report": "Web", "test-results": "Web", "coverage": "Test coverage",
    "__pycache__": "Python", ".pytest_cache": "Python", ".mypy_cache": "Python", ".ruff_cache": "Python",
    ".tox": "Python", ".nox": "Python", ".hypothesis": "Python", ".phpunit.cache": "PHP",
    "vendor": "Backend dependencies", "deps": "Elixir", ".bundle": "Ruby", "target": "Marked build output",
    "_build": "Elixir", "cover": "Elixir", ".dart_tool": "Dart / Flutter",
    "build": "Unverified build directories", "dist": "Unverified build directories",
    "bin": "Unverified build directories", "obj": "Unverified build directories",
    "out": "Unverified build directories", ".cache": "Unverified build directories",
    "Pods": "iOS", "DerivedData": "iOS", "Carthage": "iOS", ".gradle": "Android / Gradle",
    ".cxx": "Android", ".expo": "Mobile",
}
SYSTEM_TREES = [Path(p) for p in ("/System", "/Library", "/Applications", "/usr", "/bin", "/sbin",
                                  "/etc", "/dev", "/proc", "/sys", "/private/var/db")]


class Refused(ValueError):
    """The reviewed scope or current filesystem does not meet the safety checks."""


def canonical(value):
    path = Path(os.path.abspath(os.path.expanduser(str(value))))
    for part in [path] + list(path.parents):
        if part.is_symlink():
            raise Refused("symlink path component: " + str(part))
    return path


def within(path, root):
    return path != root and root in path.parents


def root_path(value):
    root = canonical(value)
    home = Path.home().resolve()
    if root == Path(root.anchor) or root == home or root in home.parents:
        raise Refused("choose a bounded project root, not a filesystem/home root")
    if str(root) in ("/private", "/private/tmp", "/tmp", "/opt", "/Volumes"):
        raise Refused("choose a project directory below the shared parent")
    if any(root == p or p in root.parents for p in SYSTEM_TREES):
        raise Refused("system paths are not cleanup roots")
    if any(part in PROTECTED_NAMES for part in root.parts) or not root.is_dir():
        raise Refused("protected or missing root: " + str(root))
    return root


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(raw).hexdigest()


def identity(path):
    info = path.lstat()
    return [info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns]


def versioned(path):
    for parent in [path.parent] + list(path.parent.parents):
        if not (parent / ".git").exists():
            continue
        try:
            result = subprocess.run(["git", "--no-optional-locks", "-C", str(parent), "ls-files", "-z", "--", str(path.relative_to(parent))],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            raise Refused("cannot check source-control ownership: " + str(path))
        if result.returncode:
            raise Refused("source-control check failed: " + str(path))
        return bool(result.stdout)
    return False


def is_candidate_dir(name):
    return (name in CACHE_NAMES or name in BUILD_NAMES or name in REVIEW_NAMES
            or name in PROTECTED_NAMES or name.endswith(".xcarchive"))


def directory_category(path):
    name = path.name
    if name in PROTECTED_NAMES:
        return "Protected runtime/toolchain"
    if name.endswith(".xcarchive"):
        return "Packaged app"
    if name == "target":
        parent = path.parent
        rust = (parent / "Cargo.toml").is_file()
        maven = (parent / "pom.xml").is_file()
        if rust and not maven:
            return "Rust"
        if maven and not rust:
            return "Java / Maven"
    return NAME_CATEGORIES.get(name, "Other review items")


def packaged_files(path, max_entries=500):
    found, seen, capped = [], 0, False
    pending = [path]
    while pending:
        current = pending.pop()
        try:
            with os.scandir(str(current)) as entries:
                for entry in entries:
                    seen += 1
                    if seen > max_entries:
                        capped = True
                        pending.clear()
                        break
                    if entry.is_symlink():
                        continue
                    child = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        if child.name.lower() in PACKAGE_WALK_NAMES and child.name not in PROTECTED_NAMES:
                            pending.append(child)
                        continue
                    if entry.is_file(follow_symlinks=False) and child.suffix.lower() in PACKAGE_SUFFIXES:
                        found.append((child, entry.stat(follow_symlinks=False).st_size))
        except OSError:
            continue
    return found, capped


def eligibility(path, root):
    path = canonical(path)
    if not within(path, root):
        raise Refused("target must be a descendant of its approved root")
    if any(part in PROTECTED_NAMES for part in path.relative_to(root).parts):
        return False, "toolchain, repository, VM or Go cache: manual operation only"
    if path.name.endswith(".xcarchive"):
        return False, "Xcode archive: manual review only; may be a release"
    if path.is_file():
        if path.suffix.lower() in PACKAGE_SUFFIXES:
            return False, "packaged app artifact: manual review only; may be a release binary"
        return False, "individual file: manual review only; never batch-deleted"
    if not path.is_dir():
        return False, "missing or unsupported filesystem object"
    if path.lstat().st_dev != root.lstat().st_dev:
        return False, "target crosses an approved-root filesystem boundary"
    if path.name in REVIEW_NAMES:
        return False, "ambiguous name: source/build review needed"
    allowed = path.name in CACHE_NAMES
    if path.name in BUILD_NAMES:
        allowed = any((path.parent / marker).is_file() for marker in BUILD_NAMES[path.name])
    if not allowed:
        return False, "not a recognized generated artifact"
    if versioned(path):
        return False, "contains tracked source-control content"
    return True, "generated artifact candidate; inspect exact path before approval"


def snapshot(path):
    """Hash names/lstat metadata without following links; refuse special objects."""
    device = path.lstat().st_dev
    rows = []
    total = 0

    def visit(item):
        nonlocal total
        info = item.lstat()
        if info.st_dev != device or (item != path and item.name == ".git"):
            raise Refused("repository or filesystem boundary in target: " + str(item))
        if stat.S_ISLNK(info.st_mode):
            rows.append([str(item.relative_to(path))] + identity(item) + [os.readlink(str(item))])
            return
        if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
            raise Refused("special filesystem object in target: " + str(item))
        rows.append([str(item.relative_to(path))] + identity(item))
        if stat.S_ISREG(info.st_mode):
            total += info.st_size
        else:
            for child in sorted(item.iterdir(), key=lambda p: p.name):
                visit(child)
    visit(path)
    return {"fingerprint": digest(rows), "estimated_bytes": total, "objects": len(rows),
            "identity": identity(path)[:2]}


def audit_home_path(value):
    """Validate an explicit audit location without making it a deletion root."""
    home = canonical(value)
    actual_home = Path.home().resolve()
    if home == Path(home.anchor) or home in actual_home.parents or not home.is_dir():
        raise Refused("home audit needs an explicit existing home directory")
    if any(home == p or p in home.parents for p in SYSTEM_TREES):
        raise Refused("system paths are not home-audit locations")
    return home


def measure_audit(path, max_entries=2000, max_seconds=0.5):
    """Bound metadata-only measurement; incomplete totals remain unknown."""
    started = time.monotonic()
    seen, observed = 0, 0
    issues = []
    pending = [path]
    while pending:
        current = pending.pop()
        if seen >= max_entries or time.monotonic() - started >= max_seconds:
            issues.append("audit measurement budget reached: " + str(path))
            break
        try:
            info = current.lstat()
            seen += 1
            if stat.S_ISLNK(info.st_mode):
                issues.append("audit skipped symlink: " + str(current))
            elif stat.S_ISREG(info.st_mode):
                observed += info.st_size
            elif stat.S_ISDIR(info.st_mode):
                with os.scandir(str(current)) as entries:
                    for entry in entries:
                        if seen + len(pending) >= max_entries or time.monotonic() - started >= max_seconds:
                            issues.append("audit measurement budget reached: " + str(path))
                            pending.clear()
                            break
                        pending.append(Path(entry.path))
            else:
                issues.append("audit skipped special object: " + str(current))
        except OSError as exc:
            issues.append("audit measurement failed for " + str(current) + ": " + str(exc))
    complete = not issues
    return {"estimated_bytes": observed if complete else None, "observed_file_bytes": observed,
            "inspected_objects": seen, "measurement_complete": complete}, issues


def audit_global_caches(home_value):
    home = audit_home_path(home_value)
    entries, issues = [], []
    for relative in GLOBAL_CACHE_SUBPATHS:
        path = home / relative
        details = {"estimated_bytes": None, "measurement_complete": False}
        reason = "global cache: audit-only; never a scripted cleanup target"
        try:
            canonical(path)
            if not stat.S_ISDIR(path.lstat().st_mode):
                raise Refused("global cache location is not a directory: " + str(path))
            details, gaps = measure_audit(path)
            issues.extend(gaps)
            if gaps:
                reason += "; measurement incomplete (see scan gaps)"
        except FileNotFoundError:
            continue
        except (OSError, Refused) as exc:
            issues.append(str(exc))
            reason += "; measurement unavailable (see scan gaps)"
        entries.append({"path": str(path), "root": str(home), "scope": "global-audit",
                        "eligible": False, "kind": "directory", "reason": reason, **details})
    return entries, issues, str(home)


def scan(roots, threshold, audit_home=None):
    if threshold < 1:
        raise Refused("large-file threshold must be positive")
    if not roots and audit_home is None:
        raise Refused("supply a bounded --root or an explicit --audit-home")
    roots = sorted(set(root_path(r) for r in roots))
    for a in roots:
        if any(a != b and b in a.parents for b in roots):
            raise Refused("scan roots must not overlap")
    entries, issues = [], []
    for root in roots:
        def error(exc):
            issues.append(str(exc))
        for parent, dirs, files in os.walk(str(root), followlinks=False, onerror=error):
            parent = Path(parent)
            for name in list(dirs):
                path = parent / name
                if path.is_symlink():
                    issues.append("skipped symlink: " + str(path)); dirs.remove(name); continue
                if is_candidate_dir(name):
                    dirs.remove(name)
                    try:
                        ok, reason = eligibility(path, root)
                        details = snapshot(path) if ok else {"estimated_bytes": None}
                        entries.append({"path": str(path), "root": str(root), "eligible": ok,
                                        "reason": reason, "kind": "directory", **details,
                                        "category": directory_category(path)})
                        if path.name in PACKAGE_PARENTS:
                            packages, capped = packaged_files(path)
                            if capped:
                                issues.append("packaged-app search stopped early: " + str(path))
                            for packaged, size in packages:
                                entries.append({"path": str(packaged), "root": str(root), "eligible": False,
                                                "reason": "packaged app artifact: manual review only; may be a release binary",
                                                "kind": "file", "category": "Packaged app", "estimated_bytes": size})
                    except (OSError, Refused) as exc:
                        issues.append(str(exc))
            for name in files:
                path = parent / name
                try:
                    info = path.lstat()
                    packaged = path.suffix.lower() in PACKAGE_SUFFIXES
                    if stat.S_ISREG(info.st_mode) and (info.st_size >= threshold or packaged):
                        entries.append({"path": str(path), "root": str(root), "eligible": False,
                                        "reason": ("packaged app artifact: manual review only; may be a release binary"
                                                   if packaged else
                                                   "large file: inspect manually; never batch-deleted"),
                                        "kind": "file",
                                        "category": "Packaged app" if packaged else "Large individual files",
                                        "estimated_bytes": info.st_size})
                except OSError as exc:
                    issues.append(str(exc))
    audited_home = None
    if audit_home is not None:
        global_entries, global_issues, audited_home = audit_global_caches(audit_home)
        entries.extend(global_entries)
        issues.extend(global_issues)
    return {"schema": SCHEMA, "created_at": time.time(), "roots": [str(r) for r in roots],
            "audit_home": audited_home, "entries": entries, "issues": issues}


def make_plan(report, approved_roots, selected, ttl=3600):
    if report.get("schema") != SCHEMA or not 60 <= ttl <= 86400:
        raise Refused("unsupported report or expiry (60..86400 seconds)")
    roots = sorted(str(root_path(p)) for p in approved_roots)
    if roots != sorted(report.get("roots", [])):
        raise Refused("explicit roots must match the scanned roots")
    if not selected or len(selected) != len(set(selected)):
        raise Refused("select one or more unique exact paths")
    entries = {e["path"]: e for e in report["entries"]}
    targets = []
    for value in selected:
        path = canonical(value)
        entry = entries.get(str(path))
        if not entry:
            raise Refused("target was not in the scanned report")
        if entry.get("scope") == "global-audit":
            raise Refused("global cache audit entries cannot become cleanup targets")
        root = root_path(entry["root"])
        if str(root) not in roots:
            raise Refused("target names an unapproved root")
        ok, reason = eligibility(path, root)
        if not ok:
            raise Refused(reason + ": " + str(path))
        details = snapshot(path)
        if details.get("fingerprint") != entry.get("fingerprint"):
            raise Refused("target changed after scanning; rescan: " + str(path))
        targets.append({"path": str(path), "root": str(root), **details})
    for entry in targets:
        if any(within(Path(entry["path"]), Path(other["path"])) for other in targets):
            raise Refused("selected targets overlap")
    now = time.time()
    plan = {"schema": SCHEMA, "created_at": now, "expires_at": now + ttl,
            "roots": roots, "root_identities": {r: identity(Path(r))[:2] for r in roots},
            "targets": targets}
    plan["approval_digest"] = digest(plan)
    return plan


def validate_plan(plan, approval=None):
    if plan.get("schema") != SCHEMA or not plan.get("targets"):
        raise Refused("invalid or empty plan")
    unsigned = {k: v for k, v in plan.items() if k != "approval_digest"}
    expected = digest(unsigned)
    if expected != plan.get("approval_digest") or (approval is not None and approval != expected):
        raise Refused("plan integrity/approval mismatch")
    if not plan["created_at"] <= time.time() <= plan["expires_at"] or plan["expires_at"] - plan["created_at"] > 86400:
        raise Refused("plan expired or has invalid dates; rescan")
    for value in plan["roots"]:
        root = root_path(value)
        if identity(root)[:2] != plan["root_identities"].get(value):
            raise Refused("approved root identity changed")
    seen = []
    for entry in plan["targets"]:
        path = canonical(entry["path"])
        if entry["root"] not in plan["roots"]:
            raise Refused("target names an unapproved root")
        root = root_path(entry["root"])
        ok, reason = eligibility(path, root)
        if not ok:
            raise Refused(reason)
        if snapshot(path)["fingerprint"] != entry["fingerprint"]:
            raise Refused("target changed since approval: " + str(path))
        if path in seen or any(within(path, other) or within(other, path) for other in seen):
            raise Refused("duplicate or overlapping targets")
        seen.append(path)


def remove_target(path, root, approved_root_identity, approved_target_identity):
    """Anchor mutation to the approved root object and its filesystem device."""
    if (not hasattr(os, "O_NOFOLLOW") or
            any(operation not in os.supports_dir_fd for operation in (os.open, os.unlink, os.rmdir, os.stat)) or
            os.listdir not in os.supports_fd):
        raise Refused("safe descriptor-relative deletion is unavailable on this platform")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(str(root), flags)
    opened = [fd]
    try:
        root_info = os.fstat(fd)
        if [root_info.st_dev, root_info.st_ino] != approved_root_identity:
            raise Refused("approved root changed before descriptor open")
        device = root_info.st_dev

        def open_child(name, parent_fd):
            child_fd = os.open(name, flags, dir_fd=parent_fd)
            try:
                if os.fstat(child_fd).st_dev != device:
                    raise Refused("filesystem boundary encountered during deletion")
                return child_fd
            except Exception:
                os.close(child_fd)
                raise

        relative = path.relative_to(root).parts
        for name in relative[:-1]:
            fd = open_child(name, fd)
            opened.append(fd)

        def empty(parent_fd, name, expected_identity=None):
            child_fd = open_child(name, parent_fd)
            try:
                opened_info = os.fstat(child_fd)
                if expected_identity is not None and [opened_info.st_dev, opened_info.st_ino] != expected_identity:
                    raise Refused("approved target changed before descriptor open")
                for item in os.listdir(child_fd):
                    info = os.stat(item, dir_fd=child_fd, follow_symlinks=False)
                    if info.st_dev != device:
                        raise Refused("filesystem boundary encountered during deletion")
                    if stat.S_ISDIR(info.st_mode):
                        empty(child_fd, item)
                    elif stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
                        os.unlink(item, dir_fd=child_fd)
                    else:
                        raise Refused("target acquired a special object; stopped")
            finally:
                os.close(child_fd)
            os.rmdir(name, dir_fd=parent_fd)
        empty(fd, relative[-1], approved_target_identity)
    finally:
        for item in reversed(opened):
            os.close(item)


def apply_plan(plan, approval=None, confirm=False):
    if confirm and not approval:
        raise Refused("deletion needs --approve with the exact reviewed digest and --confirm")
    validate_plan(plan, approval)
    results = []
    if not confirm:
        return {"dry_run": True, "approval_digest": plan["approval_digest"], "targets": plan["targets"]}
    for entry in plan["targets"]:
        try:
            # Recheck the whole remaining object immediately before removal.
            path, root = canonical(entry["path"]), root_path(entry["root"])
            ok, reason = eligibility(path, root)
            if not ok or snapshot(path)["fingerprint"] != entry["fingerprint"]:
                raise Refused("target changed before removal: " + reason)
            remove_target(path, root, plan["root_identities"][entry["root"]], entry["identity"])
            results.append({"path": str(path), "status": "removed", "estimated_bytes": entry["estimated_bytes"]})
        except (OSError, Refused) as exc:
            results.append({"path": entry["path"], "status": "failed", "error": str(exc)})
            break  # Do not continue a partly failed destructive batch.
    return {"dry_run": False, "results": results,
            "completed": len(results) == len(plan["targets"]) and all(e["status"] == "removed" for e in results),
            "remaining": [e["path"] for e in plan["targets"][len(results):]]}


def category(entry):
    if entry.get("category"):
        return entry["category"]
    path = Path(str(entry.get("path", "")))
    if entry.get("scope") == "global-audit":
        return "Global cache audit"
    if path.suffix.lower() in PACKAGE_SUFFIXES or path.name.endswith(".xcarchive"):
        return "Packaged app"
    if entry.get("kind") == "file":
        return "Large individual files"
    if path.name in PROTECTED_NAMES:
        return "Protected runtime/toolchain"
    return NAME_CATEGORIES.get(path.name, "Other review items")


def known_size(entry):
    value = entry.get("estimated_bytes")
    return value if type(value) is int and value >= 0 else None


def report_totals(report):
    """Keep eligible estimates separate from manual-only and unmeasured entries."""
    groups = {}
    for entry in report["entries"]:
        group = groups.setdefault(category(entry), {"eligible_count": 0, "eligible_bytes": 0,
                                  "manual_count": 0, "manual_bytes": 0, "unmeasured": 0})
        size = known_size(entry)
        prefix = "eligible" if entry.get("eligible") is True else "manual"
        group[prefix + "_count"] += 1
        if size is None:
            group["unmeasured"] += 1
        else:
            group[prefix + "_bytes"] += size
    return groups


REPORT_SCRIPT = r"""
function filterMatch(text, category, query, selected) {
  return String(text).toLowerCase().includes(String(query).toLowerCase()) &&
    (!selected || category === selected);
}
function compareValues(left, right, key, direction) {
  if (key === 'bytes') {
    const a = Number(left), b = Number(right);
    return ((Number.isFinite(a) ? a : -1) - (Number.isFinite(b) ? b : -1)) * direction;
  }
  return String(left).localeCompare(String(right), undefined, {numeric: true}) * direction;
}
if (typeof document !== 'undefined') {
  const query = document.getElementById('filter-query');
  const category = document.getElementById('filter-category');
  const rows = Array.from(document.querySelectorAll('table.targets tbody tr'));
  function filter() {
    let shown = 0;
    rows.forEach(row => {
      row.hidden = !filterMatch(row.textContent, row.dataset.category, query.value, category.value);
      if (!row.hidden) shown += 1;
    });
    document.getElementById('filter-status').textContent = `${shown} of ${rows.length} items shown`;
  }
  query.addEventListener('input', filter);
  category.addEventListener('change', filter);
  document.querySelectorAll('table.targets').forEach(table => {
    table.querySelectorAll('button[data-key]').forEach(button => {
      button.addEventListener('click', () => {
        const direction = button.dataset.direction === 'asc' ? -1 : 1;
        table.querySelectorAll('th').forEach(th => th.removeAttribute('aria-sort'));
        button.dataset.direction = direction === 1 ? 'asc' : 'desc';
        button.parentElement.setAttribute('aria-sort', direction === 1 ? 'ascending' : 'descending');
        const body = table.tBodies[0];
        Array.from(body.rows).sort((a, b) => compareValues(a.dataset[button.dataset.key],
          b.dataset[button.dataset.key], button.dataset.key, direction)).forEach(row => body.appendChild(row));
      });
    });
  });
  filter();
}
"""


def report_html(report):
    escape = lambda value: html.escape(str(value), quote=True)
    totals = report_totals(report)
    summary_rows = []
    for name, group in sorted(totals.items()):
        values = [name, group["eligible_count"], group["eligible_bytes"], group["manual_count"],
                  group["manual_bytes"], group["unmeasured"]]
        summary_rows.append("<tr>" + "".join("<td>" + escape(v) + "</td>" for v in values) + "</tr>")
    eligible_count = sum(g["eligible_count"] for g in totals.values())
    eligible_bytes = sum(g["eligible_bytes"] for g in totals.values())
    manual_count = sum(g["manual_count"] for g in totals.values())
    manual_bytes = sum(g["manual_bytes"] for g in totals.values())
    unmeasured = sum(g["unmeasured"] for g in totals.values())

    def table(entries, caption):
        rows = []
        for entry in entries:
            size = known_size(entry)
            values = {"path": entry.get("path", ""), "category": category(entry),
                      "bytes": -1 if size is None else size, "reason": entry.get("reason", "")}
            attrs = " ".join('data-' + key + '="' + escape(value) + '"' for key, value in values.items())
            cells = [values["path"], values["category"], "Unmeasured" if size is None else size, values["reason"]]
            rows.append("<tr " + attrs + ">" + "".join("<td>" + escape(v) + "</td>" for v in cells) + "</tr>")
        headers = "".join('<th scope="col"><button type="button" data-key="' + key + '">' + label + '</button></th>'
                          for key, label in [("path", "Path"), ("category", "Category"), ("bytes", "Estimated bytes"), ("reason", "Reason")])
        return '<div class="table-scroll"><table class="targets"><caption>' + escape(caption) + '</caption><thead><tr>' + headers + '</tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'

    eligible = [e for e in report["entries"] if e.get("eligible") is True]
    manual = [e for e in report["entries"] if e.get("eligible") is not True]
    issues = "".join("<li>" + escape(e) + "</li>" for e in report.get("issues", [])) or "<li>No recorded scan gaps.</li>"
    options = '<option value="">All categories</option>' + "".join('<option value="' + escape(c) + '">' + escape(c) + '</option>' for c in sorted(totals))
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Artifact audit</title>
<style>body{font:16px system-ui;margin:2rem;color:#1b2430;background:#fafbfc}main{max-width:1300px;margin:auto}table{border-collapse:collapse;width:100%;background:white}td,th{padding:.65rem;text-align:left;border-bottom:1px solid #ccd3dc;vertical-align:top}td:first-child{overflow-wrap:anywhere;max-width:38rem}caption{text-align:left;font-weight:700;padding:.75rem 0}button,input,select{font:inherit;padding:.4rem}button{cursor:pointer}.table-scroll{overflow:auto}label{display:inline-block;margin:.5rem 1rem .5rem 0}.notice{border-left:4px solid #52677d;padding:.8rem;background:#eef3f8}[hidden]{display:none!important}h2{margin-top:2rem}</style><main><h1>Artifact audit</h1>
<p class="notice">Sizes are file-byte estimates at scan time, not measured disk recovery. Eligibility identifies a review candidate, never deletion approval. Manual-only entries do not contribute to eligible totals. Unmeasured entries have unknown size.</p>
''' + '<p id="eligible-summary"><strong>Eligible candidates:</strong> ' + str(eligible_count) + ' items; ' + str(eligible_bytes) + ' estimated bytes.</p><p id="manual-summary"><strong>Manual review:</strong> ' + str(manual_count) + ' items; ' + str(manual_bytes) + ' known estimated bytes. ' + str(unmeasured) + ' items remain unmeasured.</p>' + '''
<h2>Category totals</h2><div class="table-scroll"><table id="category-totals"><caption>Totals across all scan entries; filtering below does not change these totals</caption><thead><tr><th>Category</th><th>Eligible items</th><th>Eligible bytes</th><th>Manual items</th><th>Known manual bytes</th><th>Unmeasured items</th></tr></thead><tbody>''' + "".join(summary_rows) + '''</tbody></table></div>
<h2>Inspect exact paths</h2><label>Search <input id="filter-query" type="search" placeholder="Path, category or reason"></label><label>Category <select id="filter-category">''' + options + '''</select></label><p id="filter-status" role="status" aria-live="polite"></p><p>Click a column heading to sort its table. Search and category filters apply to both lists.</p>''' + table(eligible, "Eligible candidates — review before approving") + table(manual, "Manual-review-only items — excluded from scripted cleanup") + '<h2>Scan gaps</h2><ul>' + issues + '</ul></main><script>' + REPORT_SCRIPT + '</script></html>'

def load(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def output(path, data):
    target = Path(path)
    if target.exists() or target.is_symlink():
        raise Refused("output already exists; choose a new path")
    descriptor = os.open(str(target), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(data if isinstance(data, str) else json.dumps(data, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("scan"); p.add_argument("--root", action="append", default=[]); p.add_argument("--audit-home"); p.add_argument("--large-file-bytes", type=int, default=500_000_000); p.add_argument("--output", required=True)
    p = commands.add_parser("report"); p.add_argument("input"); p.add_argument("--output", required=True)
    p = commands.add_parser("plan"); p.add_argument("input"); p.add_argument("--root", action="append", required=True); p.add_argument("--select", action="append", required=True); p.add_argument("--expires-in", type=int, default=3600); p.add_argument("--output", required=True)
    p = commands.add_parser("apply"); p.add_argument("input"); p.add_argument("--approve"); p.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "scan":
            value = scan(args.root, args.large_file_bytes, args.audit_home); output(args.output, value)
            print(json.dumps({"entries": len(value["entries"]), "issues": len(value["issues"]), "output": args.output}))
            return 1 if value["issues"] else 0
        if args.command == "report":
            output(args.output, report_html(load(args.input))); print(args.output); return 0
        if args.command == "plan":
            value = make_plan(load(args.input), args.root, args.select, args.expires_in); output(args.output, value)
            print(json.dumps({"approval_digest": value["approval_digest"], "targets": value["targets"]}, indent=2)); return 0
        result = apply_plan(load(args.input), args.approve, args.confirm); print(json.dumps(result, indent=2))
        return 0 if result.get("dry_run") or result.get("completed") else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Refused: " + str(exc), file=sys.stderr); return 2


if __name__ == "__main__":
    sys.exit(main())
