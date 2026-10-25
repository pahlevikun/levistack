# Stack: Java and Kotlin (Spring)

## Layout (hexagonal packages)

```
com.acme.orders
  domain/                       entities, value objects, domain services, events
  application/
    port/in/                    use-case interfaces
    port/out/                   repository and gateway interfaces
    usecase/                    use-case implementations
  adapter/
    in/web/                     controllers, request and response DTOs
    out/persistence/            JPA entities, Spring Data repositories, mappers
  config/                       Spring configuration and wiring
```

Multi-module builds (onion, clean, COLA) enforce direction with module dependencies: `domain` has no dependencies, `application` depends on `domain`, `infrastructure` on both, and a boot module wires them. See `styles/cola/GUIDE.md` for the COLA module set.

## Rules
- **The domain is framework-free.** No `@Entity`, `@Table`, `@Service`, `@Component` or Jackson annotations on domain classes, and no `javax.persistence` or `jakarta.persistence` imports in `domain`.
- **Separate persistence models.** JPA entities live in the adapter; a mapper converts to and from domain objects.
- **Ports are interfaces** in `application.port.*`. Use cases may be plain classes; Spring stereotypes are optional and, when used, belong in the config or adapter layer.
- **Controllers** only parse, call an inbound port and format. **DTOs** stay in the adapter.
- Wiring: Spring configuration or a manual wiring class; constructor injection throughout.

## Kotlin
Mirror the Java split. Use `data class` for immutable value objects, sealed classes for results and domain events, constructor injection (Spring, Koin or manual). Avoid service-locator style lookups.

## Enforce the boundaries
ArchUnit tests: domain does not depend on `org.springframework..`, `jakarta.persistence..` or adapter packages; application does not depend on adapter packages; adapters do not depend on each other; no package cycles. Run them as ordinary unit tests in the build.

## Tests
Domain: plain JUnit. Use cases: JUnit with in-memory ports. Adapters: slice tests (`@DataJpaTest`, `@WebMvcTest`) plus integration tests with a containerized database.

## Pitfalls
JPA annotations on domain classes, a Spring `@Transactional` boundary placed in the controller, repository interfaces in the infrastructure package, DTOs reaching the domain, business `if` in the controller or in an executor.
