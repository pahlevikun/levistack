# Quality attributes and system design

Architecture is the set of decisions that are expensive to reverse, made to satisfy quality attributes under constraints. Use this when the question is "design the system" rather than "structure the code".

## Contents
- Decision framework
- Quality attributes
- Trade-offs
- Deliverables
- Diagrams
- Principles

## Decision framework

1. **Goals.** What must the system do, and for whom?
2. **Quality attributes that matter, ranked.** Not all of them; the top three or four.
3. **Constraints.** Team skills, budget, deadline, regulation, existing systems, hosting.
4. **Options.** Two or three real candidates, including "the simple thing".
5. **Trade-offs.** What each option gives up.
6. **Decision.** One option, the reasons, and what would make you revisit it.
7. **Record it** as an ADR (`templates/adr.md`).

## Quality attributes

| Attribute | Question | Typical tactics |
|---|---|---|
| Performance | How fast, under what load? | Caching, indexing, async work, read models |
| Scalability | How does it grow? | Stateless services, partitioning, queues |
| Availability | How much downtime is acceptable? | Redundancy, health checks, graceful degradation |
| Reliability | Does it do the right thing despite failures? | Idempotency, retries with backoff, outbox, sagas |
| Security | What must be protected and from whom? | Least privilege, input validation at boundaries, secrets management, audit events |
| Maintainability | How cheap is the next change? | Clear boundaries, tests, small modules |
| Testability | Can parts be verified alone? | Ports and adapters, in-memory fakes |
| Observability | Can you tell what it is doing? | Structured logs, metrics, tracing |
| Deployability | How safely can you ship? | Small releases, feature flags, rollback path |
| Cost | What does it cost to build and run? | Right-sizing, managed services where they fit |

## Trade-offs

State them as pairs, not as virtues: eventual consistency buys scale and costs simplicity; more services buy independent deploys and cost operational load; abstraction buys flexibility and costs indirection. A recommendation without its cost is incomplete.

## Deliverables

For a design request, produce: the context and constraints, the ranked attributes, the chosen structure with a diagram, the decisions as ADRs, the main risks with mitigations, and the first slice to build.

## Diagrams

Use the C4 levels: System Context, Container, Component, and (rarely) Code. One diagram per question; label every arrow with what flows and in which direction. See `jobs/document.md`.

## Principles

- Decide late what you can; decide early what is expensive to change.
- Prefer boring, proven technology unless there is a stated reason.
- Make the failure modes explicit: what happens when each dependency is slow, down or wrong?
- Design for the next change you can name, not for every change you can imagine.
