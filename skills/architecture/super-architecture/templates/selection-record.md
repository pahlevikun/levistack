# Architecture selection record

## Context
- Team size and experience: <...>
- Business complexity: simple CRUD | moderate | dense and volatile
- Stack: <...>
- Infrastructure change frequency: low | medium | high
- Entry points: <HTTP, CLI, queue, gRPC, ...>
- Test, audit and compliance needs: <...>
- Read and write load, expected growth: <...>
- Deployable shape today: one process | modular monolith | service-based | microservices | serverless | space-based
- Network trust boundary (client vs server): yes | no
- Traffic pattern: steady | bursty | real-time
- Consistency need: strong | eventual | mixed

## Ranked quality attributes
1. <attribute and why>
2. <...>
3. <...>

## Candidates scored
Rate each 1 (poor) to 5 (strong) for this project.

| Dimension | Option A | Option B | Option C (the simple thing) |
|---|---|---|---|
| Fit for business complexity | | | |
| Learning cost for this team (5 = easy) | | | |
| Infrastructure replaceability | | | |
| Test friendliness | | | |
| Feature isolation | | | |
| Operational cost (5 = cheap) | | | |
| **Total** | | | |

## Subdomains
| Subdomain | Type (core, supporting, generic) | Style |
|---|---|---|
| <...> | <...> | <...> |

## Recommendation
- **Choice:** <in-process style, DDD yes/no, deployable shape, CQRS level>
- **Because:** <3 to 5 reasons tied to the context>
- **Costs:** <...>
- **Would change if:** <facts that would flip the choice>
- **First slice to build:** <...>
- **ADR:** <path>
