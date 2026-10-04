# Architecture blueprint: <project>

Fill only the sections the code supports. Cite a path for every claim and label inferences as inferences. Delete empty sections.

## 1. Detection
- Stack and frameworks: <language, framework, build, versions with the file they came from>
- Architectural style: <in-process style, modeling, deployable shape; confidence; evidence paths>

## 2. Overview
<The approach in one paragraph: guiding principles, boundaries, how it is organized.>

## 3. Diagrams
- System context (C4 level 1)
- Containers (level 2)
- Components of the main container (level 3)
- One sequence for the most important flow
Text diagrams (Mermaid), one question each.

## 4. Core components
For each: purpose, location, responsibilities, interfaces it exposes, dependencies, how it is wired, how it is extended.

## 5. Layers and dependencies
Layer map as implemented, dependency direction, boundary enforcement, any violations found (`file:line`).

## 6. Data architecture
Domain model structure and aggregates, persistence mapping, repositories, data access patterns, caching, migrations.

## 7. Cross-cutting concerns
Authentication and authorization, error handling and mapping, logging, configuration, validation, resilience (timeouts, retries, circuit breaking), observability.

## 8. Communication
Service boundaries, protocols, synchronous versus asynchronous, events and their schemas, versioning.

## 9. Technology-specific patterns
Per detected stack: the patterns in use (dependency injection, mediator, endpoint conventions, and so on).

## 10. Implementation patterns
How a use case, a repository, an adapter and a controller are written in this codebase, with a short real example each.

## 11. Testing architecture
Test layers, doubles, contract tests, architecture tests, what runs in CI.

## 12. Deployment
Topology derived from configuration, environments, configuration sources.

## 13. Extension and evolution
Extension points, feature-flag use, how a new feature is added, how a legacy part is replaced.

## 14. Decisions
Index of ADRs: number, title, status.

## 15. Adding a feature (guide)
The ordered steps for a new feature in this codebase, naming rules, and the checks to run.
