# Style and lint workflow

Naming and structure so `buf lint` stays green. Lint is a **command in CI**, not a custom script.

## Naming

| Element | Style | Example |
|---------|-------|---------|
| Files | `lower_snake_case.proto` | `book_service.proto` |
| Packages | `org.product.domain.v1` | `acme.library.v1` |
| Messages | `PascalCase` singular | `Book` |
| Fields | `snake_case` | `display_name` |
| Services | `PascalCase`, `Service` suffix | `BookService` |
| RPCs | `PascalCase` verbs | `GetBook` |
| Enums | `PascalCase` | `BookGenre` |
| Enum values | `ENUM_NAME_VALUE` | `BOOK_GENRE_FICTION` |

Zero enum value: `*_UNSPECIFIED = 0` with no business meaning. Prefix values with the enum name.

Package directory matches the package. Avoid language keywords in package segments (`internal` breaks Go).

## Structure

- One service per file; resource messages in a sibling file.
- Unique `{Method}Request` / `{Method}Response` per RPC.
- Comments on public RPCs, messages, and fields that are not self-explanatory.
- Soft line length 80, hard 120; 2-space indent; `//` comments.

## Default toolchain: buf

```bash
buf format -w
buf lint
buf breaking --against '.git#branch=main'
```

`buf.yaml` lint: `STANDARD` (includes PROTOVALIDATE). Do not add `PROTOVALIDATE` again. Optional extras: `COMMENTS`, `UNARY_RPC`.

Ignore a rule only with a documented exception (`lint.ignore_only` or `// buf:lint:ignore` if the module allows comment ignores).

## EasyP (alternative)

If the repo already has `easyp.yaml`, use EasyP the same way: lint, generate, breaking, deps. Map mentally to buf (`easyp lint` ≈ `buf lint`). Do not introduce EasyP into a buf repo, and do not run both as competing truth.

## Do not add a custom linter

Prefer `buf lint` (or the project's existing EasyP/buf wrap). Do not add a Python or ad-hoc naming checker unless this repository already owns one.

## Common lint fixes

| Rule | Fix |
|------|-----|
| `ENUM_VALUE_PREFIX` | Prefix with enum name |
| `ENUM_ZERO_VALUE_SUFFIX` | `*_UNSPECIFIED` |
| `PACKAGE_VERSION_SUFFIX` | Add `.v1` |
| `FIELD_LOWER_SNAKE_CASE` | `user_name` |
| `SERVICE_SUFFIX` | `FooService` |
| `RPC_REQUEST_RESPONSE_UNIQUE` | Per-method request/response types |
| `RPC_REQUEST_STANDARD_NAME` | `GetBookRequest` not `BookRequest` |
