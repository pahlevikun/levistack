# Stack: PHP (Symfony)

Targets PHP 8.3 or newer and Symfony 7. Concepts carry over to Laravel with different wiring.

## Layout

```
src/
  Domain/                     entities, value objects, domain services, repository interfaces, events
  Application/
    Command/ Query/           command and query classes with their handlers
    Port/                     outbound interfaces (clock, mailer, gateways)
  Infrastructure/
    Persistence/Doctrine/     repositories, mapping
    Messaging/ Http/ ...      adapters
  Presentation/               controllers, request DTOs
config/services.yaml          composition: bind ports to adapters
```

## Rules
- **Value objects are immutable:** `final readonly class` with validation in the constructor, so an invalid value cannot exist.
- **Domain is framework-free:** no Symfony, Doctrine or Laravel imports and no attributes from them. Keep ORM mapping outside the domain classes (XML or separate mapping in infrastructure).
- **Repository interfaces** in the domain (aggregate repositories) or application ports; Doctrine implementations in infrastructure.
- **Command and query buses:** Symfony Messenger with separate buses and handlers; handlers are the application layer's use cases. Queries return read DTOs; commands return nothing or an id.
- **Controllers are thin:** map the request DTO to a command, dispatch, map the result. Validation of input shape happens on the request DTO; business invariants stay in the domain.
- Wire with the service container; autowire interfaces to adapters in configuration, not inside domain or application classes.

## Enforce the boundaries
`deptrac` with layer definitions and rules that mirror `core/dependency-rule.md`, run in CI. PHPStan at a strict level helps with null safety and types.

## Tests
Domain and application tests without the kernel, using in-memory repositories; Doctrine repository integration tests against a real database; functional tests through the HTTP kernel for controllers.

## Pitfalls
Doctrine annotations on domain entities, mutable value objects, controllers holding business rules, entities passed straight to templates or JSON, handlers that call other handlers.
