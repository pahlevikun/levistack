---
description: "Processes, supervision, PubSub, Oban workers and Mnesia: when to add a process and how to keep them honest."
globs: "**/*.{ex,exs}"
alwaysApply: false
---

# Elixir OTP, PubSub, Oban and Mnesia

## Processes
- **Plain functions first.** Add a process only for bounded runtime state, a resource, concurrency, a timer or fault isolation.
- **Supervise everything long-lived.** A bare `GenServer.start_link`, `Agent.start_link` or `Task.start` outside a supervisor compiles, then crashes silently with no restart or log. Use `Task.Supervisor.start_child` for fire-and-forget work, and list long-lived processes in the application's supervision tree.
- **No process per subscriber.** A stream or channel connection already is a process: subscribe it directly. Add an intermediary only for a real runtime reason beyond relaying messages.

## Phoenix.PubSub
- One PubSub server per app. Namespace by topic, not by starting a second server.
- Topic names: `<context>:<entity>:<id>`, lowercase and colon-separated (`accounts:account:<uuid>`, `market:prices:BTCUSD`). Extend the pattern; do not invent another per feature.
- Broadcast from the module that owns the state; subscribe from the transport. Domain code never subscribes (subscription is a transport-lifecycle concern).
- Broadcast the minimal shape, never the full struct with sensitive fields.
- Every stream or channel needs an explicit disconnect and backpressure story before it ships. A subscription that outlives its process leaks memory, and so does an unbounded queue to a slow consumer.

## Oban workers
- `perform/1` is transport: validate args, call the domain, translate the result (`:ok`, `{:error, r}`, `{:snooze, n}`). No business logic inside.
- Every worker is safe to run twice with the same args.
- Name queues for bounded contexts (`:accounts`, `:notifications`), not `:default`, beyond trivial jobs.
- Args are persisted in plain form: no PII or secrets in them.
- Do not catch every exception and return `:ok`. That silently drops real failures. Swallow only an error you deliberately decided is non-retryable.
- Permanent failures cancel the job; transient ones return an error for backoff.

## Mnesia
- Access is confined to the persistence app; the domain never calls `:mnesia`.
- Treat it as derived or explicitly ephemeral state. Never let the only copy of durable data live there.
- If an entity exists in both a durable store and Mnesia, document which is authoritative in `@moduledoc` and how the other stays consistent.
- Create tables in an explicit `init/0` called at application start, never lazily on first request.
- Clustering is a separate decision. `ram_copies` on several nodes must not sneak in without scoped node-discovery work.

## Supervision checks in review
A new process with no runtime reason, an unsupervised process, a worker that returns `:ok` on every error, or a subscription with no cleanup are all findings.
