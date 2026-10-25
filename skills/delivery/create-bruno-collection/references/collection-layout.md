# Collection layout

Default path in the service repo:

```
docs/api/bruno/<service>/
├── bruno.json
├── environments/
│   ├── Local.bru
│   └── Staging.bru
├── auth/                       # usually HTTP login; seq 1
│   ├── folder.bru
│   └── login.bru
├── proto/                      # optional; gRPC (collection-level imports)
├── rest/                       # or per-resource folders
│   └── orders/
│       └── get-order.bru
├── graphql/
│   └── queries/
│       └── list-orders.bru
├── grpc/
│   └── orders/
│       └── create-order.bru
└── websocket/
    └── events/
        └── subscribe.bru
```

Use **protocol folders** (`rest/`, `graphql/`, `grpc/`, `websocket/`) when a service exposes more than one surface; single-protocol APIs can keep resource-only folders (`orders/`, `users/`).

## bruno.json

```json
{
  "version": "1",
  "name": "My Service API",
  "type": "collection",
  "ignore": ["node_modules", ".git"]
}
```

Configure collection-level **gRPC proto files and import paths** in Bruno UI (collection settings) when using gRPC; commit matching `.proto` paths under `proto/` when the team wants protos versioned with the collection.

## Request types (`meta.type`)

| `meta.type` | Bru driver block |
|---|---|
| `http` | `get` / `post` / … |
| `graphql` | `post { body: graphql }` |
| `grpc` | `grpc { }` |
| `ws` | `ws { }` |

SOAP uses `type: http` + `body:xml`. Load the matching file from `references/protocols/` (linked from SKILL.md).

## Shared conventions

- Name requests by intent ("Get order"), not by raw path or RPC name alone.
- Path params and IDs: `{{orderId}}` in URL, metadata, or GraphQL variables.
- `seq` — auth and bootstrap requests lowest; dependents higher.
- Per-protocol examples and body tags live under `references/protocols/`.
