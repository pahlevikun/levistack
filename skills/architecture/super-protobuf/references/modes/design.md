# Mode: design

Write or change `.proto` files. Match the repo; if empty, use the defaults in `design.md`.

## Steps

1. List packages and services already in the tree. Reuse names and field-order conventions.
2. Place files as `org/product/domain/v1/*.proto` with `package org.product.domain.v1;`.
3. **One service per file.** Resource + enums in a sibling `book.proto`; RPCs in `book_service.proto`.
4. Use AIP-style standard methods without `google.api` annotations unless the project already transcodes HTTP.
5. Unique `{Method}Request` / `{Method}Response` types. Unary for CRUD; streaming only for watch/log/chat.
6. Add protovalidate on production fields (`protovalidate.md`).
7. Copy [templates/resource.proto](../../templates/resource.proto) and [templates/service.proto](../../templates/service.proto), or the book example under `assets/proto/example/v1/`.
8. Run `buf format -w && buf lint`.

## Defaults

- proto3. Version in the package, not in the message name.
- Prefer `optional` over wrapper types. Prefer custom empty responses over `google.protobuf.Empty`.
- Avoid `map<>` when order or per-entry metadata will matter; use `repeated` messages instead.
- Do not invent timestamps; use `google.protobuf.Timestamp`.

## Done when

Messages and RPCs compile under `buf lint`, validation is present, and the file layout matches the package.
