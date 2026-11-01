# Changelog

All notable changes to this catalog are documented here. Version numbers follow [package.json](package.json) and ship on plugin manifests via `npm run sync`.

## Unreleased

---

## 1.3.0 — 2026-10-30
### Added
- Delivery‑and‑workflow‑skills group (code‑review, evidence, rumbling, etc.).
- New commands `evidence`, `rumbling` and related documentation.

### Updated
- **enhance‑skill**: clarified that we learn from upstream but do not copy text; upstream licenses are retained separately.
- **infographic** skill: removed upstream attribution and inlined MIT license header.

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
