# Job: detect

Name the architecture of an existing codebase, say where code belongs, and find boundary violations. The result is evidence, not an opinion.

## Contents
- Procedure
- Signals by style
- Violation candidates
- Where does this code belong
- Report

## Procedure

1. **Scan.** `node scripts/arch-scan.mjs detect <dir>` lists the stack, the style signals found and a ranked guess. `node scripts/arch-scan.mjs check <dir>` lists boundary-violation candidates with `file:line`. Both accept `--json`.
2. **Sample.** Open two or three files on the main request path: an entry point, a use case or service, a data access class. Follow one request from the edge to storage.
3. **Check direction from imports,** not from folder names. A `domain/` folder that imports the web framework is not a domain layer. A `features/` folder whose features import each other's internals is slice theater.
4. **Name the style, with a confidence and the evidence,** and say where the code deviates. Real projects are hybrids; report the primary style and the local variations.
5. **Confirm violations by reading the code.** A candidate is a place to look, never a finding.

## Signals by style

| Style | Typical evidence |
|---|---|
| Layered (traditional) | Top-level `controllers/`, `services/`, `repositories/`, `models/`; controllers call services call repositories |
| Layered (DDD four-layer) | `interface` or `presentation`, `application`, `domain`, `infrastructure` |
| Onion | `core/domain`, `core/application`, `infrastructure`, `api`, a `composition` module |
| Hexagonal | `ports/` and `adapters/` (inbound and outbound, driving and driven, primary and secondary), or `application/port/in` and `port/out` |
| Clean | `entities/`, `usecases/` or `interactors/`, `gateways/`, `presenters/`, `controllers/`, a `frameworks` ring |
| COLA diamond | Maven modules `*-adapter`, `*-app`, `*-domain`, `*-infrastructure`, `*-client`; `@ExtensionPoint` |
| Vertical slice | `features/<capability>/<operation>/` holding handler, request, validator, tests; `Features/` in .NET |
| CQRS | `commands/`, `queries/`, handlers, a command or query bus, read models or projections |
| Event sourcing | Event store, `events/`, aggregates that apply events, projections, snapshots |
| Event-driven | Topics or queues, producers and consumers, an outbox table, a broker client |
| Plugin | A manifest, discovery of extensions, a stable host API |
| Microkernel | `kernel/` plus `plugins/`, capability descriptors, sandbox, compatibility matrix |
| Functional core | `core/` of pure functions next to a `shell/` that performs I/O; core has no framework imports |
| Domain-driven | Glossary, context map, ubiquitous-language names in types; not a folder template |
| Modular monolith | `modules/<capability>/` with façades; CI forbids cross-module internals |
| Service-based | A few coarse `services/` deployables; shared database with schema owners |
| Microservices | Many independently deployed units, each with its own store; platform repo or charts |
| Serverless | `functions/` or `lambdas/`, `serverless.yml` / SAM / CDK; handlers plus managed triggers |
| Pipeline | `filters/` and pipes or stages; per-stage schemas |
| Client-server | Separate client and API apps, a shared contract package, version-skew docs |
| Space-based | Processing units, in-memory grid, partition routing, write-behind |
| Game | Systems, components, state machines, object pools, an event bus |

One signal is weak, three agreeing signals are good. Folder names without matching import direction are weak.

## Violation candidates

| Candidate | Severity |
|---|---|
| Domain or application imports infrastructure or an adapter | Critical |
| Business logic in an adapter (`if` or `switch` on rules) | Critical |
| Use case calls an external service directly (no port) | Critical |
| Framework or ORM types in the domain | Warning |
| Port signature uses database, HTTP or SDK types | Warning |
| Controller calls a repository directly (adapter without a port or use case) | Warning |
| One adapter imports another adapter | Warning |
| A feature imports another feature's internals | Warning |
| A module imports another module's internals (modular monolith) | Warning |
| A service reads another service's tables | Warning |
| A `shared` or `common` folder imported by everything | Info |

Full symptoms, confirmation steps and fixes are in `core/anti-patterns.md`.

## Where does this code belong

For any class or function, ask: **does it do I/O or run out of process, and what does it depend on?**

- No I/O and no framework dependency: inside. Business rule: domain. Orchestration: application.
- I/O, a framework, a database driver or an SDK: outside, as an adapter.
- If it depends on something outside, it is outside, even if its own logic is trivial.
- A shared type used by several features belongs to a feature until two real consumers prove identical meaning.

## Report

```
Style: <primary style>, with <variation>   Confidence: high | medium | low
Stack: <language, framework, build>
Evidence: <3 to 5 signals, each with a path>
Deviations: <where the code departs from the style, with paths>
Violations (confirmed): <file:line, rule broken, severity>
Candidates not confirmed: <file:line>
Suggested next step: <evaluate | migrate | none>
```

Say "unclear" when the evidence does not settle it, and name the one file or question that would.
