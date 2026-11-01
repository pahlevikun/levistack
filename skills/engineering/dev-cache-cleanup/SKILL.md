---
name: dev-cache-cleanup
description: "Audit project artifacts, explicitly selected home-cache locations and large files, create a reviewable cleanup plan, and delete only explicitly approved unchanged project-cache targets. Use when asked to reclaim development disk space, inspect Node.js, web, mobile, Docker-adjacent project dirs, or backend caches (Go, Ruby, Elixir, Rust, Java, Python, PHP, .NET), find large build artifacts, or safely clean old project outputs. Not for deleting arbitrary files, pruning Docker or container disks, uninstalling toolchains, or bypassing filesystem permissions."
metadata:
  version: 1.1.0
  author: levistack
  license: MIT
  group: engineering
  category: engineering
  department: engineering
  related_skills:
    - verify
    - handoff
    - mcp-management
  tags:
    - cleanup
    - disk-usage
    - cache
    - audit
    - dry-run
    - nodejs
    - mobile
    - backend
  capabilities:
    - artifact_inventory
    - exact_cleanup_plans
    - metadata_revalidation
    - guarded_cache_removal
    - ecosystem_cache_catalog
  languages:
    - en

---

# Development cache cleanup

Separate discovery, review and deletion. A directory name is a hint, not proof
that its contents are disposable. Inspect the exact paths and retain excluded
items in the report. Use [the safety boundary](references/safety.md) before the
first run; this skill never runs global package-cache or container-prune commands.

## Procedure

1. Infer bounded project roots from the request; ask only when scope is missing.
   Filesystem/home roots, toolchain stores and system paths are not cleanup roots.
   A requested global-cache audit uses the explicit `--audit-home` option below;
   it never expands deletion scope. Read project conventions before classifying
   build output as disposable.
2. Classify paths with the [cache catalog](references/caches.md) before treating
   a directory as disposable. The samples cover Node.js, web, Android APK/AAB,
   iOS, Flutter, Go, Ruby, Elixir, Rust, Java, Python, PHP, .NET, and Docker-adjacent
   project paths. Then run the bundled [cache CLI](scripts/cache_cleanup.py)
   in `scan` mode. It uses Python 3.9+ and the standard library. Large individual
   files, ambiguous build directories, packaged apps, toolchains, Go stores and
   VM/container stores remain manual-only.
3. Create the self-contained HTML report. Use its search/category filters and
   sortable eligible/manual tables; category totals keep estimates and unknown
   sizes separate. Read scan gaps and excluded entries; investigate
   permission failures or missing areas instead of calling a partial scan complete.
   Sizes estimate file bytes at scan time, not physical disk blocks reclaimed.
4. Review the exact eligible targets. Confirm they are regenerable, inactive and
   not source-controlled or uniquely valuable. Create a plan only for the paths
   the user selected. It requires the same explicit roots as the scan and rejects
   changed targets. Never approve a category summary in place of the actual list.
5. Run `apply` without `--confirm` and show the plan's exact paths and digest.
   Obtain an explicit instruction to delete this reviewed list before passing
   both `--approve` and `--confirm`. Creating a plan is not deletion authority.
6. Report removed, failed and unattempted targets separately. A failed target
   stops the destructive batch. Do not replay an expired or partly applied plan;
   rescan and obtain approval for a new exact list. Restore or repair an unexpected
   consequence within authorized scope and state the actual outcome.

## Commands

Set `CACHE_CLI` to this skill's `scripts/cache_cleanup.py`; set `PROJECT_ROOT` to
a real, bounded project path. Choose report/plan paths outside cleanup targets.
Outputs must not already exist. Commands below are patterns, not executed cleanup.

```sh
python3 "$CACHE_CLI" scan --root "$PROJECT_ROOT" --output audit.json
python3 "$CACHE_CLI" report audit.json --output audit.html
python3 "$CACHE_CLI" plan audit.json --root "$PROJECT_ROOT" \
  --select "$PROJECT_ROOT/node_modules" --output plan.json
python3 "$CACHE_CLI" apply plan.json
```

After the user approves the exact path list and digest:

```sh
python3 "$CACHE_CLI" apply plan.json --approve "$APPROVED_DIGEST" --confirm
```

`scan` accepts repeated `--root` and a positive `--large-file-bytes` threshold.
For an explicitly requested global-cache audit, provide `--audit-home` with the
chosen home directory, either alongside project roots or on its own:

```sh
python3 "$CACHE_CLI" scan --audit-home "$AUDIT_HOME" --output home-audit.json
```

This inspects only the closed subpaths in the [cache catalog](references/caches.md).
It never walks the whole home directory or inspects load-bearing sibling paths
such as `.cargo/bin`, the Android SDK, or emulator images. These rows are always
audit-only and cannot become cleanup-plan targets. A catalog row marked manual
or audit is rejected by `plan`.
Measurement is capped per cache; incomplete measurements stay unknown and their
reasons appear in scan gaps. Neither environment variables nor defaults enable
this audit implicitly.

`plan` accepts repeated `--select`; its default expiry is one hour, bounded to
60–86,400 seconds through `--expires-in`. Root identity and recursive target
metadata are checked again before mutation. Opened root/target descriptors must
match the approved device/inode, and deletion refuses filesystem boundaries. Internal links are removed as links;
links in the selected path or its ancestors are refused. No external link target
is traversed. Deletion requires descriptor-relative operations available on POSIX;
unsupported platforms can audit but fail closed on mutation.

Run the [synthetic safety tests](tests/test_cache_cleanup.py):

```sh
python3 -m unittest discover -s tests -v
```

Run that command from this skill directory. The tests use temporary project
fixtures only. The optional real-browser smoke is enabled with
`CACHE_BROWSER_SMOKE=1`; set `CHROME_BIN` when the browser is outside standard
locations. It fails when the requested browser cannot launch; a unit/helper pass
is not a visual-render pass. Behavioral prompts are in [evals/evals.json](evals/evals.json).

## Related skills

- `verify`: establish what ran and report actual outcomes.
- `handoff`: preserve the selected scope and unfinished work across sessions.
- `mcp-management`: tool-server setup is a separate operational task.
