# Stack: Python

Applies to FastAPI, Flask, Django (with care) and plain services.

## Layout

```
src/orders/
  domain/               dataclasses or plain classes for entities and value objects; domain errors
  application/          use-case classes or functions; ports defined as Protocol or ABC
  adapters/
    api/                FastAPI routers, request and response models
    persistence/        SQLAlchemy models and repository implementations
  bootstrap.py          composition root
```

## Rules
- **Domain entities are plain.** Do not put SQLAlchemy `Column` definitions or Pydantic `Field` annotations on domain entities; that couples them to the framework. Keep ORM models and API schemas in adapters and map between them.
- **Validate in the constructor.** Use `__post_init__` (or a factory) so an invalid `Email` or `Money` cannot be created; prefer frozen dataclasses for value objects.
- **Ports** as `typing.Protocol` or abstract base classes in the application layer; use cases receive ports through their constructor or arguments.
- **Wiring:** a bootstrap function, or FastAPI's `Depends` at the edge. Keep the container out of domain and use-case modules.
- **Controllers (routers)** parse, call a use case and format. If a router grows past that, extract a use case.
- **Django:** treat the ORM as an adapter; keep business rules in plain modules rather than in models and views, and call them from views.

## Enforce the boundaries
`import-linter` contracts (layers and forbidden imports) in CI. A common symptom of a broken boundary is an `ImportError: cannot import name` cycle between `use_cases` and `adapters`; fix it by depending on the Protocol, not the concrete adapter.

## Tests
`pytest` unit tests for domain and use cases with in-memory implementations of the ports; integration tests for repositories with a real database in a container; API tests with the framework's test client.

## Pitfalls
ORM models used as domain entities, Pydantic models in the domain, business logic in routers, circular imports between layers, a module-level global session.
