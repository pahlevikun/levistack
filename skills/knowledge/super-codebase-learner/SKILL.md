---
name: super-codebase-learner
description: "Learn a project's current state: deep-read, recon onboarding, ARCHITECTURE.md of what exists, diagnose layering and architecture smells, extract .claude/rules conventions, or plan site IA of an existing product. Use when onboarding, priming context, mapping modules and data flow, reviewing current architecture friction, generating CLAUDE.md, or planning sitemap of the product as built. Not for choosing a target stack, TCO, greenfield design, or a migration blueprint — use super-tech-blueprint."
---

# Super codebase learner

Answers **what is this codebase today?** Current-state only: onboarding, deep-read, architecture docs of what exists, smells and layering of existing code, conventions, site IA of the product as built.

**Not for** inventing a target stack, TCO, greenfield design, or a migration blueprint — use `super-tech-blueprint`. After this skill maps current state, hand off there for *what to build toward*.

Pick a mode from the user's words; load only that reference. Combine modes only when the user asks for both.

## Router

| If the user wants… | Mode | Load |
|---|---|---|
| Read everything, prime, get up to speed on code | **deep-read** | [deep-read-protocol](references/deep-read-protocol.md) |
| Join repo, onboarding guide, understand codebase, CLAUDE.md | **onboard** | [onboarding-flow](references/onboarding-flow.md) |
| Document architecture, ARCHITECTURE.md, map the system, "edit here for X" | **summarize** | [architecture-doc-template](references/architecture-doc-template.md) |
| Current architecture friction, shallow modules, layering smells, HTML architecture review | **diagnose** | [diagnose-current-architecture](references/diagnose-current-architecture.md) |
| Learn from project, extract rules, discover conventions | **extract-rules** | [extract-project-rules](references/extract-project-rules.md) |
| Sitemap, site structure, page hierarchy, IA, nav design, URL plan (marketing site as it exists or should be organized) | **site-ia** | [site-information-architecture](references/site-information-architecture.md) |
| Compare frameworks, pick a stack, TCO, greenfield blueprint, migrate *to* X | **not this skill** | `super-tech-blueprint` |

**Precedence:** explicit user wording beats defaults. If unclear, prefer **onboard** for new repos, **summarize** when they ask for a durable doc, **diagnose** when they ask what is wrong with the architecture *as it is*.

**Disambiguation**

- Repo folders, APIs, modules → **onboard**, **summarize**, **diagnose**, or **deep-read** — not **site-ia**.
- Marketing pages, header nav, `/blog/slug` URLs → **site-ia** — not **summarize**.
- "Learn the codebase" without "every file" → **onboard**; with insistence on exhaustive read → **deep-read**.
- "Create onboarding docs" for developers → **summarize** (file) or **onboard** (chat guide); ask if they want `ARCHITECTURE.md` on disk.
- "Improve the architecture" that means *document or smell the current tree* → **diagnose** (optionally after **summarize**). If they mean *pick a new stack or target shape* → **not this skill**; load `super-tech-blueprint`.

## Mode summaries

### deep-read

Full-file read of source tree. Highest token cost; use when fidelity matters more than speed. See protocol reference.

### onboard

Fast recon with Glob/Grep; onboarding guide in chat plus optional `CLAUDE.md`. Does not require reading every file. Stack facts here are *detected*, not recommended.

### summarize

Produces or updates `ARCHITECTURE.md` (or equivalent) with diagrams, entry points, how-to sections, and checklist from the template. Describes what the code does today. Do not invent a next stack in that file.

### diagnose

Scan existing code for architectural friction (shallow modules, leaked seams, hot spots). Present candidates as a temp HTML report. In-place deepening stays here and in `super-challenge-me` (**grill-docs**); a new stack or migration target is a handoff to `super-tech-blueprint`. Report scaffold: [html-architecture-report](references/html-architecture-report.md).

### extract-rules

Evidence-based convention discovery; optional delegate to `learn-analyst`; writes `.claude/rules/` only after user approval.

### site-ia

Business-site planning: ASCII hierarchy, Mermaid visual sitemap, URL map, nav spec, internal linking. Deep dives: [site-type-templates](references/site-type-templates.md), [navigation-patterns](references/navigation-patterns.md), [mermaid-templates](references/mermaid-templates.md). Site-IA eval scenarios: [evals/evals.json](evals/evals.json).

## Combined flows

| Request | Order |
|---|---|
| "Onboard me and write architecture docs" | **onboard** → **summarize** (reuse recon; avoid re-scanning) |
| "Learn everything then extract rules" | **deep-read** → **extract-rules** |
| "Document the app and plan our marketing site" | **summarize** then **site-ia** (separate deliverables) |
| "Review architecture then propose a target stack" | **diagnose** (and **summarize** if no current-state doc) → hand off to `super-tech-blueprint` |

## References (bulk detail)

| File | Origin |
|---|---|
| [deep-read-protocol.md](references/deep-read-protocol.md) | learn-codebase |
| [onboarding-flow.md](references/onboarding-flow.md) | codebase-onboarding |
| [architecture-doc-template.md](references/architecture-doc-template.md) | codebase-summarizer |
| [diagnose-current-architecture.md](references/diagnose-current-architecture.md) | improve-codebase-architecture (current-state) |
| [html-architecture-report.md](references/html-architecture-report.md) | improve-codebase-architecture (current-state) |
| [extract-project-rules.md](references/extract-project-rules.md) | learn |
| [site-information-architecture.md](references/site-information-architecture.md) | site-architecture |
| [site-type-templates.md](references/site-type-templates.md) | site-architecture |
| [navigation-patterns.md](references/navigation-patterns.md) | site-architecture |
| [mermaid-templates.md](references/mermaid-templates.md) | site-architecture |

## Breaking renames

These skill folders were merged and removed:

- `learn` → **extract-rules** mode
- `learn-codebase` → **deep-read** mode
- `codebase-onboarding` → **onboard** mode
- `codebase-summarizer` → **summarize** mode
- `site-architecture` → **site-ia** mode
- `improve-codebase-architecture` → **diagnose** mode for *current* smells and layering; target stack / migration blueprint → `super-tech-blueprint`

Load `skills/knowledge/super-codebase-learner/SKILL.md` instead of any of the above (except the target-stack half of `improve-codebase-architecture`, which is `super-tech-blueprint`).
