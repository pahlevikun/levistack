# Hexagonal architecture (ports and adapters)

Business logic is independent of frameworks, transport and persistence. The application core depends on abstract ports; adapters at the edge implement them. Anything that talks to the outside world goes through a port.

## Pick when
- Several entry points drive the same logic (HTTP, CLI, queue worker, scheduler, gRPC).
- Infrastructure is volatile or costly to test (databases, third-party APIs, brokers).
- Business rules are dense, or you want fast tests with no infrastructure.
- Standardizing the internal structure of many services.

## Avoid when
- Small CRUD apps, scripts or prototypes where the overhead is not repaid.
- The team cannot yet size ports sensibly; start layered and evolve.

## Core idea

The **hexagon** contains the domain **and** the application layer. Adapters are outside. **Driving (inbound, primary) ports** say what the application can do; **driven (outbound, secondary) ports** say what it needs from the world. The hexagon is conceptual: most apps have two to four ports, not six.

Deciding what is inside: "does it do I/O or run out of process, and what does it depend on?" If yes to either, it is an adapter.

## Layout

```
domain/                       entities, value objects, domain services
application/
  ports/inbound/              use-case interfaces (driving ports)
  ports/outbound/             repository, gateway, clock, event publisher (driven ports)
  usecases/                   orchestration; implements inbound ports
adapters/
  inbound/                    http, cli, queue consumers, schedulers
  outbound/                   persistence, external clients, messaging
composition/                  the single wiring location
```

Feature-first variants put `domain`, `application` and `adapters` inside each feature. Stack-specific packages are in `stacks/`.

## Dependency rules

| Piece | Depends on |
|---|---|
| Inbound adapter | An inbound port (the use case) |
| Use case | Domain, and outbound ports it needs |
| Domain | Nothing outside the domain |
| Outbound adapter | An outbound port and its technology |

Adapters never call each other; a controller never talks to a database adapter directly.

## Build steps

1. **Model one use case** with an input and output type. Keep request, response and message wrappers outside.
2. **Define outbound ports first.** Every side effect is a port: persistence, external calls, clock, id generation, logging. Model capabilities, not technologies.
3. **Implement the use case** as orchestration: validate application-level rules, coordinate domain behavior, return plain data.
4. **Write in-memory adapters** for each outbound port; use them in use-case tests.
5. **Write real adapters:** inbound converts protocol input to use-case input and results back; outbound maps port calls to the technology.
6. **Wire in the composition root.**
7. **Test per boundary** (below).

## Port rules

- A port is owned by the side that needs it. It lives in the application layer (or the domain when the abstraction is truly domain-level), **not** in an adapter folder.
- One capability per port, usually grouped around an aggregate or a use case, not around a technology. A port with ten or more methods is a "god port"; split it. Many tiny one-method ports are the opposite smell; coalesce related operations.
- No transport details in a port: no HTTP headers, SQL types or SDK classes. Use domain types or DTOs.
- Use wrapper objects for inputs so a signature does not break when a field is added.
- Explicit port interfaces are worth it with several adapters, a test seam or a team boundary. In a small codebase the use-case handler's public method can be the driving port.
- **Adapter drift:** when the database or vendor API changes, the adapter is what changes. Re-run that port's contract suite (and, for persistence, a check that migrations still satisfy the port) before merge.

## Example (TypeScript)

```typescript
// application/ports/outbound/order-repository.ts
export interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
}

// application/usecases/place-order.ts
export class PlaceOrder {
  constructor(private orders: OrderRepository, private payments: PaymentGateway) {}
  async execute(cmd: PlaceOrderCommand): Promise<PlaceOrderResult> {
    const order = Order.place(cmd.customerId, cmd.items);   // domain rules
    await this.payments.authorize(order.total());            // outbound port
    await this.orders.save(order);                           // outbound port
    return { orderId: order.id.value };
  }
}

// adapters/inbound/http/order-controller.ts  (thin)
router.post('/orders', async (req, res) => {
  const result = await placeOrder.execute(toCommand(req.body));
  res.status(201).json(toResponse(result));
});
```

## Testing

- Domain: pure unit tests, no doubles.
- Use cases: unit tests with fake ports; assert outcomes and port interactions.
- Outbound adapters: a shared contract suite per port, plus integration tests on real infrastructure.
- Inbound adapters: mapping tests (request to command, result and errors back to protocol).
- A few end-to-end journeys. Design check: you can run the whole application from tests with no database and no HTTP server.

## Pitfalls
Brittle port signatures, third-party types in the domain, use cases calling other use cases, anemic domain, designing the database before the model, adapters containing business logic, global singletons hiding wiring, adapters importing other adapters, ports stored next to the SQL client.

## Combines with
CQRS (separate command and query ports), vertical slice (ports and adapters per slice, not one global adapter folder), event-driven (outbox adapter), onion and clean (same dependency rule, different vocabulary), functional-core (the shell implements driven ports), domain-driven (ports named in the ubiquitous language).
