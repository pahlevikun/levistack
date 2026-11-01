# Changelog

All notable changes to this catalog are documented here. Version numbers follow [package.json](package.json) and ship on plugin manifests via `npm run sync`.

## Unreleased

### Added

- `dev-cache-cleanup` cache catalog for Node.js, web, mobile (Android APK/AAB, iOS, Flutter), backend stacks (Go, Ruby, Elixir, Rust, Java, Python, PHP, .NET), Docker guidance, and matching scan and home-audit recognition.
- `create-readme`, `gap-analysis`, and `qa`. A project README, a gap or debug pass, and a test plan.
- `foundation` group: `use-levistack` now matches a situational playbook before its seven steps, `setup-levistack` checks the tools scripts call, and `help-levistack` answers which skill fits without starting work.
- `shape-and-build`, `blast-radius`, and `figure-it-out` for design shape, outside-the-diff risk, and auditable open-ended runs.
- `refresh-pr`, plus `code-review` watch and prep modes that stop before merge.
- `lane-lead` and `compare-models` under `workflow`. `dev-environment` exports or imports an agent setup and backs up or restores a Mac workstation. `setup-pack` is folded into it.

### Changed

- `use-levistack` checks this machine before it routes. A blocked check (`node` or `python3` missing) runs `setup-levistack` first and does not start the task until the check passes. Named gaps in optional tools do not stop the route.
- Glossary of how to start, each group, and every skill, in `help-levistack`, the README, and `docs/assets/levistack-glossary.png`. The catalog count is 68 skills.
- `find-skills` now really searches the levistack catalog (routing map, two keyword passes, full list) before anything else, browses skills.sh as its only external source, and after a yes installs the pick on this machine with `npx skills add -g`, verifies it landed, and invokes it in the same session.
- Moved `retrospective` from `agent-authoring` to `workflow`.
- Moved `figure-it-out` from `knowledge` to `workflow`, and `use-levistack` from `workflow` to `foundation`.
- Hunt now runs on every `use-levistack` run.
- Glossary and routing pictures now show 68 skills. knowledge 6, engineering 8, delivery 15, agent-authoring 9.

---

## 1.1.0 — 2026-10-26

### Added

- `retrospective` skill (session, repo, initiative, artifact, and environment modes).
- `research` sources mode: local changes, documents, web and read-only git history evidence channels.
- `diagram` and `infographic` under `product/` with handoff, Mermaid support, and CSS keyframe SVG motion guidance.
- `evals/evals.json` or `evals/cases.json` for every catalog skill; validate enforces coverage.

### Changed

- Renamed skill `retro` → `retrospective`.
- Moved `diagram` from `knowledge` to `product`.
- Repository and plugin package version set to **1.1.0**.
