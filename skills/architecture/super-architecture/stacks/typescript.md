# Stack: TypeScript and Node

Applies to Express, Fastify, NestJS, Hono and similar. For Node-specific service patterns (middleware, auth, async) also see the `super-nodejs` skill.

## Layout

```
src/
  features/orders/           feature-first; or layer folders if the project is layer-first
    domain/                  entities, value objects (plain classes or types, no framework imports)
    application/
      ports/                 interfaces (inbound use cases, outbound capabilities)
      usecases/              classes or functions taking ports as arguments
    adapters/
      inbound/http/          controllers, route handlers, request mapping
      outbound/persistence/  repositories (Prisma, TypeORM, SQL client, ...)
  platform/                  config, logging, error handling, db client
  main.ts                    composition root
```

## Wiring
- Constructor or argument injection with an explicit factory module. No hidden global singletons, no service locator.
- NestJS: modules are the composition root; keep providers for adapters in the outer module and depend on ports by token, not on concrete classes.
- Keep framework decorators out of domain classes; map ORM models to domain objects in the adapter.

## Idioms
- Ports as `interface` or `type`; use cases as classes with a single `execute` or as functions returning a function.
- Validate input at the edge with a schema library; pass plain typed commands inward.
- Errors: return a result type or throw domain-specific errors; map them to HTTP in one handler.
- Use branded or small value-object types for ids and money.

## Enforce the boundaries
- `dependency-cruiser` or `eslint-plugin-boundaries` with rules matching `core/dependency-rule.md`; fail CI on violation.
- TypeScript path aliases per layer make imports explicit and greppable.
- `node scripts/arch-scan.mjs check <dir>` for a first look.

## Tests
Unit tests for domain and use cases with in-memory ports; integration tests for repositories against a real database in a container; HTTP tests through the framework's test client for inbound adapters.

## Pitfalls
ORM entities returned from use cases, `req` and `res` passed into use cases, decorators on domain classes, barrel files that create cycles, one `utils` folder imported by everything.
