# Service-based

A handful of **coarse** deployable services, often still sharing a database under explicit schema ownership. Independent deploys without the mesh of many microservices.

## Pick when
- Several teams want to ship on their own cadence but cannot yet (or should not) give every capability its own store and platform.
- An ERP-like core or a legacy database makes full data autonomy unrealistic.
- You need published contracts for partner teams without splitting into dozens of processes.

## Avoid when
- One team and a small product: stay a modular monolith.
- Latency cannot afford extra hops.
- You pretend this is microservices while every release still locks together (distributed monolith).

## Core idea

Bundle related capabilities into **few** services with named owners. Contracts (OpenAPI or AsyncAPI) are the integration surface. A gateway or registry handles routing, auth and telemetry. A shared database is allowed only with **table or schema owners**, views or replicas for readers, and a deprecation schedule for breaking schema changes.

This sits between modular monolith (one process) and microservices (one store per service).

## Layout

```
services/<coarse-name>/   deployable: several modules inside
gateway/                  routing, auth, observability
contracts/                OpenAPI / AsyncAPI, versioning, SLAs
db/                       schema ownership map, views, deprecation notes
```

## Build steps
1. Group capabilities into a small set of services; name an owner for each.
2. Publish contracts with versioning and SLAs before independent deploys start.
3. Write down schema or table ownership. Gate breaking DDL.
4. Put a gateway or registry in front: routing, auth, traces.
5. Add consumer-driven contract tests; they fail on unnoticed breaks.
6. Mark hotspots that might later split into finer services; do not split yet.

## Testing
- Contract tests per published API.
- Integration tests against the shared database using only owned schemas.
- Gateway tests for auth and routing.
- Coupling review: a service that reads another owner's tables without a view is a violation.

## Pitfalls
Shared-table writes from two services. No owner for a schema. Network plus a monolith's coupling. Skipping contracts because "we all know the tables." Growing to twenty tiny services without a platform (`styles/microservices/GUIDE.md`).

## Combines with
Modular monolith inside each coarse service, domain-driven for the cuts, client-server at the gateway, event-driven for the flows that cannot share a transaction.
