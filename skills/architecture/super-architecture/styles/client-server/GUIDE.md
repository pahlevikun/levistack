# Client-server (and peer-to-peer)

A network trust boundary sits between the user-facing process and the authoritative backend. The server owns invariants and durable state; the client owns presentation, local cache and, if designed for it, offline work.

## Pick when
- Web, mobile or desktop clients talk to a centralized API.
- You must document trust boundaries, authentication, API evolution or client/server version skew.
- Offline-first or peer-to-peer sync is in scope (conflict resolution is then a first-class design).

## Avoid when
- UI and logic share one process with no network boundary: a modular monolith or layered service is simpler.
- The "server" is only a static file host and there is no contract to version.

## Core idea

| Side | Owns | Must not own |
|---|---|---|
| Client | Rendering, navigation, optimistic UI, local cache, request batching | Authoritative business invariants, secrets, other tenants' data |
| Server | Invariants, authorization, durable writes, audit | Pixel layout, one-off view composition the client can do |
| Peer (optional) | Local replica, sync protocol, membership | Unilateral conflict resolution without a named strategy |

Minimize duplicated rules. If a rule must run on both sides (for example format checks), share one package or treat the server copy as source of truth.

## Layout

```
apps/web/                 or apps/mobile/     client process
apps/api/                 server process
packages/api-contract/    OpenAPI, protobuf or shared types
packages/validation/      optional shared shape checks (not domain invariants)
```

The client never imports server internals. The server never imports UI widgets.

## Build steps
1. Draw the trust boundary: what runs where, what is secret, what is cached.
2. Write the contract first (OpenAPI, protobuf or equivalent) and a compatibility test suite.
3. Choose a version-skew strategy before code: semantic versions, `Accept` headers, or feature flags for incomplete clients.
4. Put authorization, rate limits and TLS on every endpoint; log enough to debug a client release wave.
5. If the app is not always online, name the conflict strategy (CRDT, last-write-wins with a clock, or a merge UI) in the ADR.
6. Test the contract from both sides, including an older client against a newer server.

## Version skew
Clients in the wild lag server deploys (app stores, IT lockstep). Additive changes first; breaking changes behind a flag or a new path. Support N-1 clients until the rollout wave finishes. Document the wave in a runbook: who ships first, how long the old path lives, how to abort.

## Testing
- Contract tests (consumer-driven or schema) on CI; they fail the build on an unregistered breaking change.
- Client mapping tests: DTO to view model, error codes to UI states.
- Server authorization tests per endpoint.
- Offline: replay concurrent edits and assert the named conflict strategy.

## Pitfalls
Chatty clients (many small calls): façade or BFF, plus cache. Thick clients that reimplement server rules and drift. Shipping a client that cannot talk to the current API. P2P without a conflict strategy. Sharing a type across the wire that includes fields the other side must not see (`core/domain-modeling.md` IO boundary).

## Combines with
Layered or hexagonal on the server, vertical slice per BFF, CQRS when read models serve the client, serverless for bursty APIs, modular monolith when the "server" is still one deployable.
