# Pipeline (pipes and filters)

Data moves through a sequence of discrete transformations. Each **filter** does one job with a declared input and output schema. **Pipes** carry records between filters and apply back-pressure.

## Pick when
- ETL, streaming analytics, log processing or CI/CD stages with a stable sequence of transforms.
- Stages should be reusable, scaled or failed independently.
- Isolation between stages matters more than a shared mutable working set.

## Avoid when
- Interactive request/response with a user in the loop (`styles/client-server/GUIDE.md`).
- Stages must share mutable in-memory state; the pattern cannot express that without cheating.
- A single function already does the whole transform and there is no reuse or scale split.

## Core idea

Filters are preferably **stateless**. Required state lives in an external store or at pipeline boundaries. Pipes are streams, queues or in-memory channels that buffer and push back when a downstream filter is slow. A bottleneck is scaled or split; it is not allowed to drop data silently.

## Layout

```
pipeline/
  filters/<name>/         one transform: schema in, schema out, contract tests
  pipes/                  queue or stream config: buffer, back-pressure, DLQ
  orchestration/          graph of filters, replay, deployment
```

## Build steps
1. Name each filter and its schemas. One responsibility per filter.
2. Choose pipe technology (in-memory, queue, log) that supports back-pressure and buffering.
3. Keep filters stateless; persist checkpoints at boundaries.
4. Instrument latency, throughput and error rate **per stage**.
5. Deploy and scale stages independently. Define replay (from offset, from DLQ, from object store).
6. Load-test at about twice expected peak and confirm no loss when a stage stalls.

## Testing
- Contract tests per filter on input and output schema.
- CI compatibility check between adjacent filters (schema drift fails the build).
- End-to-end runs on representative fixtures.
- Back-pressure and retry tests, including poison messages to the DLQ.

## Pitfalls
A god filter that does three transforms. Schema drift between stages. Unbounded buffers that hide a stuck stage until memory dies. Shared mutable state between filters. No replay. Treating the pipeline as a request/response app.

## Combines with
Functional-core (each filter is a pure function in a shell), event-driven (pipes are topics), serverless (each filter is a function), hexagonal (I/O adapters at the edges of a filter).
