# Job: evaluate

Assess an existing design: how healthy it is, how mature the domain modeling is, how much structural debt there is, and what to fix first. Evidence first; the scores are aids to judgment, not a verdict.

## Contents
- Procedure
- Quick diagnostic
- Maturity levels
- Fitness assessment
- Debt score
- Roadmap
- Cadence

## Procedure

1. **Detect** the style and stack (`jobs/detect.md`). Run `node scripts/arch-scan.mjs check <dir>`.
2. **Confirm** the violation candidates by reading the code. Count only the confirmed ones.
3. **Run the quick diagnostic** below for a fast verdict.
4. **For a full assessment,** score maturity, fitness and debt.
5. **Prioritize** with the fix order in `core/anti-patterns.md`.
6. **Report** with `templates/evaluation-report.md`. Name the evidence for every score.

## Quick diagnostic

One point for each yes, out of seven:

| Question | If no |
|---|---|
| Can business rules be tested without a database, web server or framework? | Extract entities and use cases behind interfaces |
| Do all source dependencies point inward? | Invert the offending dependency |
| Can the database be swapped without touching business logic? | Isolate persistence in an adapter |
| Are use cases independent of the delivery mechanism? | Use plain DTOs in use-case signatures |
| Is the framework confined to the outermost ring? | Wrap framework calls; push them to the edge |
| Is the component graph free of cycles? | Break each cycle by inversion or extraction |
| Does one composition root build the dependencies? | Move construction out of inner layers |

6 to 7: boundaries hold. 4 to 5: the core is testable but details leak inward. 2 to 3: the framework or the database dictates the structure. 0 to 1: no real boundaries; business rules live in controllers and ORM models. Report the failed rows and the inversion that fixes each.

If the system is distributed, add these and score them separately (yes/no): each service owns its data (or a named schema); every inter-service call has a timeout and a contract test; a consumer has a DLQ; change-coupling does not show lockstep releases. Two or more "no" means the deployable shape is a distributed monolith, regardless of repo count.

## Maturity levels

| Level | Name | What it looks like |
|---|---|---|
| L1 | Ad hoc | Three layers, anemic entities, all logic in services |
| L2 | Aware | Some rich entities, value objects in use, the team uses the vocabulary |
| L3 | Applied | Aggregate boundaries, domain with zero framework dependencies, repositories per aggregate |
| L4 | Scaled | Several bounded contexts, CQRS where needed, automated architecture tests in CI |
| L5 | Optimized | Continuous evolution, event sourcing where warranted, ADRs kept, a debt dashboard |

L3 is enough for most business systems. Aim higher only for core financial or transaction-critical systems. Report the current level, the target level, and the key gaps.

## Fitness assessment

Score 1 to 5 on each, weighted:

| Dimension | Weight | Ask |
|---|---|---|
| Business alignment | 25% | Does the architecture match the domain's complexity? Over- or under-engineered? |
| Team fit | 25% | Does the team understand and follow the conventions? Violation rate? |
| Technology fit | 20% | Does the stack support the structure, or fight it? |
| Evolution capability | 15% | Can a new context or feature be added cheaply? Module coupling? |
| Delivery efficiency | 15% | Is feature cycle time reasonable? How much overhead does the structure add? |

Calibration: 5 enables agility; 4 has minor friction; 3 neither helps nor hinders; 2 causes noticeable friction; 1 is a blocker. Total is the weighted sum. A total near 3 or below means act.

## Debt score

| Category | Weight | Measures |
|---|---|---|
| Structural (P0) | 0.5 | Layer-violation ratio, cycles, anemic entity share, framework leaks into the core |
| Design (P1) | 0.3 | Oversized aggregates, missing domain events, missing value objects, cross-aggregate references |
| Testing (P2) | 0.2 | Domain unit-test coverage, aggregate-root coverage, integration coverage |

Normalize each category to 0 to 100 (higher is worse) from counted evidence, then compute the weighted total. Bands: up to 20 healthy, 21 to 40 mild (repay regularly), 41 to 60 moderate (plan this quarter), above 60 severe (start now). State how each number was counted so it can be repeated.

## Roadmap

| Phase | Typical span | Focus |
|---|---|---|
| 1. Stop the bleeding | 1 to 2 weeks | Fix P0: framework in the core, outward dependencies, cycles, skipped use cases |
| 2. Micro-refactor | 2 to 4 weeks | Make core aggregates rich, add value objects, add domain events |
| 3. Upgrade | 1 to 3 months | Split into contexts, adopt CQRS L1, move to the fitting style |
| 4. Continuous | Ongoing | Periodic fitness check, ADRs, a debt trend, team training |

Spans are typical, not promises; size them to the team.

## Cadence

Reassess quarterly, and whenever features are repeatedly blocked, debt slows delivery, or the business changes shape. Keep the first assessment as a baseline and compare each later one to it: maturity change, debt score, and the share of agreed improvements completed. Never compare two scores built from different evidence.
