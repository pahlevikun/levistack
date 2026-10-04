# Stack: Dart and Flutter

## Layout (feature-first clean architecture)

```
lib/
  features/orders/
    presentation/       widgets, pages, BLoC or other state objects
    domain/             entities, use cases, repository interfaces, failures
    data/               repository implementations, data sources, DTO models
  core/                 shared utilities, error types, network setup
  main.dart             composition root and dependency injection
```

## Rules
- **Three layers per feature:** presentation depends on domain; data depends on domain; domain depends on nothing outside Dart.
- **Domain defines** entities, use cases (one class per action) and repository interfaces. It has no Flutter, HTTP or database imports.
- **Data implements** the repository interfaces with remote and local data sources and maps DTO models to entities.
- **Presentation** holds widgets and state management (BLoC, Riverpod or similar); state objects call use cases, never data sources.
- **Errors:** return an `Either<Failure, Success>`-style result (or a sealed result class) from use cases and repositories, not raw exceptions across layers.
- **Dependency injection** at startup (for example `get_it` or Riverpod providers); keep it in the composition root.
- Keep each feature self-contained; share through `core/` only what has identical meaning.

## Enforce the boundaries
A dependency lint or a small test that parses `import` lines to assert `domain/` imports neither `package:flutter` nor `data/` nor `presentation/`. Review new imports across features.

## Tests
Unit tests for use cases and domain with fake repositories; bloc tests with fake use cases; widget tests for presentation; integration tests for data sources against a mock server.

## Pitfalls
Widgets calling data sources, DTO models used as domain entities, exceptions leaking across layers, one global state object for the whole app, a `core/` that becomes a dumping ground.
