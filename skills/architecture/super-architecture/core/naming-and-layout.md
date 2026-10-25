# Naming and layout

How folders and names should read. The structure should tell a newcomer what the system does before it tells them what it is built with.

## Contents
- Screaming structure
- Two ways to slice
- Naming
- Boundary object names
- Layout by size

## Screaming structure

Open the top-level folder of an architecture and it should "scream" its purpose: `orders/`, `billing/`, `shipping/`, not `controllers/`, `services/`, `models/`. Frameworks and delivery mechanisms are details and belong deeper or at the edge.

Test: delete the framework folder names from the tree. Can you still tell what the product does? If every top folder is a technical role, the structure hides the domain.

## Two ways to slice

| Slice by | Layout | Strength | Cost |
|---|---|---|---|
| Layer first | `domain/`, `application/`, `infrastructure/` then features inside | Boundaries are easy to enforce with one rule per folder | A single change touches several top-level folders |
| Feature first | `orders/`, `billing/` then layers inside each | A change stays in one folder; features read as capabilities | Needs discipline to keep each feature's dependency direction clean |

Neither is wrong. Match the project. Hybrid is common: feature folders at the top, a small layered shape inside each feature. Do not create a second parallel tree for the same code.

## Naming

- **Use cases and commands:** a verb phrase for the business intent. `PlaceOrder`, `DispatchShipment`, `CancelSubscription`. Avoid generic `Create`, `Update`, `Delete` when the business has a better word.
- **Queries:** a noun phrase for what is returned. `OrderSummary`, `OverdueInvoices`.
- **Aggregates and entities:** the business name (`Order`), not `OrderEntity` or `OrderModel`.
- **Value objects:** the concept (`Money`, `EmailAddress`).
- **Domain events:** past tense (`OrderPlaced`).
- **Ports:** the capability (`PaymentGateway`, `OrderRepository`, `Clock`). Add `Port` as a suffix only if the project already does.
- **Adapters:** the technology plus the port (`PostgresOrderRepository`, `StripePaymentGateway`).
- **No `Manager`, `Helper`, `Util` or `Common` buckets.** If you cannot name it by what it does, it has no owner yet.

## Boundary object names

Keep one convention and use it consistently:

| Shape | Suffix | Example |
|---|---|---|
| Incoming request | `Request` or `Command` | `CreateMemberRequest` |
| Outgoing response or view | `Response` or `View` | `OrderResponse` |
| Persistence record | `Record`, `Row`, `Dbo` or `Po` | `MemberRecord` |
| Domain object | no suffix | `Member` |

Conversions live at the edge: `MemberView.from(member)` going out, `request.toMember()` coming in. The domain never imports a DTO.

## Layout by size

- **Small service:** one module, feature folders, a thin `platform/` for shared technical code. No ports for stable internals.
- **Medium service:** feature folders, each with its own small layered shape; ports where integrations are volatile; one composition root.
- **Large system:** several modules or services along bounded-context lines; each follows the style that fits its subdomain; shared kernel kept small and explicit.

Shared code gets an owner and a reason. A `shared/` folder with no owner becomes a hidden layer that bypasses every boundary.
