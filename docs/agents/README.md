# Agents

Eleven generic subagents. They carry no project names; project specifics come from the project's own `AGENTS.md`, rules and playbooks.

| Agent | Use it to | Tools | Model |
|---|---|---|---|
| `explorer` | Locate code, investigate a bounded question, look up one fact. Read-only | Read, Grep, Glob, Bash | default |
| `bulk-reader` | Summarize big files into `path:line` bullets without flooding context | Read, Grep, Glob | haiku |
| `context-harvester` | Search project knowledge (rules, docs, ADRs) and return a compact sourced summary | Read, Grep, Glob, Bash | default |
| `planner` | Write the plan, evals and open decisions. Never implements | Read, Grep, Glob, Write, Edit | default |
| `coordinator` | Route a task (JSON) or run a plan: task cards, dispatch, evaluate, escalate | Read, Grep, Glob, Bash | default |
| `implementer` | Bounded edits on paths the caller owns | Read, Grep, Glob, Write, Edit, Bash | default |
| `scaffolder` | New module or feature skeleton from templates, plus registration wiring | Read, Grep, Glob, Write, Edit | default |
| `template-writer` | Mechanical placeholder substitution into files | Read, Grep, Glob, Write, Edit | haiku |
| `tdd-runner` | Red-green loop that never weakens a test | Read, Grep, Glob, Write, Edit, Bash | default |
| `reviewer` | Score against evals, then review the diff for silent failures and principles | Read, Grep, Glob, Bash | default |
| `security-reviewer` | STRIDE-style review of trust boundaries, PII, secrets, injection | Read, Grep, Glob | default |

## Typical flow
`context-harvester` (alone, first) → `planner` → `coordinator` → `explorer` / `scaffolder` → `implementer` / `tdd-runner` → `reviewer` (+ `security-reviewer` on trust boundaries).

The two cheap agents (`bulk-reader`, `template-writer`) are pinned to a small model on purpose. Keep judgment work off them.

## What was merged
| New | Replaces | Abilities kept |
|---|---|---|
| `explorer` | code-locator, teamonia-explorer, teamonia-researcher | locate, bounded investigation with git history, single-question lookup with provenance |
| `bulk-reader` | teamonia-bulk-reader, service-bulk-reader | `path:line` bullets only, no contents, surface-check disclaimer |
| `context-harvester` | teamonia-recall | precheck, small-task shortcut, double-pass search, relevance judgment, gap reporting, size caps |
| `planner` | teamonia-planner | one recommended approach, evals, blocked/ready, decision tickets |
| `coordinator` | teamonia-coordinator, teamonia-orchestration-router, teamonia-auto-orchestrator | task cards, escalation, failure strategy; routing is now a JSON-only mode |
| `implementer` | teamonia-implementer, service-dev, teamonia-repo-maintainer | ownership list, focused verification, scaffolder/implementer split |
| `scaffolder` | teamonia-scaffolder, service-workflow-scaffolder | minimum files, registration wiring (unwired trap), placeholder hosts, typed errors |
| `template-writer` | teamonia-template-writer, service-template-writer | literal substitution, file tree output, stop on missing placeholder |
| `tdd-runner` | teamonia-tdd-runner, service-tdd-runner | scoped runs, never weaken a test, races are real, no hand-edited mocks |
| `reviewer` | teamonia-reviewer, teamonia-evaluator, service-workflow-reviewer | eval scoring, silent-failure checklist, principles gate, priority output |
| `security-reviewer` | teamonia-security-reviewer, service-go-security-reviewer | STRIDE checklist, constant-time compare, header forwarding, SSRF, severity scale |

## What did not carry over
Stack- and product-specific detail was dropped from the agents on purpose. The originals are kept locally and are not published.

Agents reference each other by these names only. Skills and rules imported earlier may still name the old agents; fix them during the publish cleanup.
