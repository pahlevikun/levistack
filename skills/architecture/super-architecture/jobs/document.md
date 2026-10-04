# Job: document

Write down an architecture so the next person can use it: decisions, diagrams and a blueprint. Document what the code shows and what was decided, nothing invented.

## Contents
- Rules
- Records (ADR)
- C4 diagrams
- Domain model docs
- API and event docs
- Architecture blueprint
- Maintenance

## Rules

1. **Ground every claim in the code or a decision.** Name the file or the ADR. A diagram that no file supports is fiction.
2. **Detect before you describe.** Run `jobs/detect.md` first; document the actual structure, noting where it deviates from the intended one.
3. **Every architecture decision gets an ADR.** No decision yet means no ADR; make the decision first (`jobs/select.md`).
4. **One diagram, one question.** Label every arrow with what flows and which way.
5. **For stack facts** (frameworks, versions, licenses) use the `super-tech-blueprint` skill; this guide covers structure and decisions.

## Records (ADR)

Use `templates/adr.md`: title, status, context, decision, alternatives, consequences, and what would trigger a revisit. Statuses: proposed, accepted, superseded (link the replacement), deprecated. Never edit an accepted ADR's decision; supersede it. Keep a central index (number, title, status, date) so decisions are easy to find.

## C4 diagrams

| Level | Shows | Audience |
|---|---|---|
| 1. System context | The system, its users and external systems | Everyone |
| 2. Container | Deployable units (services, databases, queues) and how they talk | Engineers, ops |
| 3. Component | The major parts inside one container (use cases, ports, adapters) | Engineers on that container |
| 4. Code | Class-level detail; only for the hardest parts | Rarely needed |

Mapping from domain design: a bounded context is usually one container; its aggregates and use cases appear at level 3. Write diagrams as text (Mermaid) so they live in version control and review. Do not mix levels in one diagram.

## Domain model docs

For each aggregate: its root, the invariants it enforces, its commands and events, and the repository. For each bounded context: its language (a short glossary a domain expert would sign) and its relationships to other contexts (shared kernel, customer/supplier, anticorruption layer). If domain-driven is in play, the glossary and context map are first-class artifacts, not an appendix.

## API and event docs

For command-query separated systems, document commands (intent, who may send, outcome, errors), queries (parameters, result shape, freshness) and events (name in past tense, payload, producer, consumers, schema version). Mark which operations are eventually consistent.

For client-server systems, document the contract, the version-skew strategy and the trust boundary. For pipelines, document each filter's schema, the pipe technology and the replay path. For plugin or microkernel hosts, document the contract, the permission model and the compatibility matrix.

## Architecture blueprint

When asked for a full blueprint, follow `templates/architecture-blueprint.md`. It covers: detected stack and style, overview, diagrams, core components, layers and dependencies, data architecture, cross-cutting concerns, service communication, technology-specific patterns, implementation patterns, testing, deployment, extension points, decision records, and a guide for adding a feature. Fill only the sections the code supports, cite paths, and label inferences as inferences.

## Maintenance

| What | When | Owner |
|---|---|---|
| ADRs | With the decision | The author of the change |
| C4 level 1 and 2 | When containers or integrations change | Tech lead |
| Component diagrams and blueprint | Quarterly, or when a style rule changes | The team |
| Index of decisions | With each ADR | Whoever merges it |

Treat stale documentation as a defect: if a diagram no longer matches the code, fix it or delete it.
