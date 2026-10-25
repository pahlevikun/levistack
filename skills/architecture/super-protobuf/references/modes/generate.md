# Mode: generate

Configure buf and generate code. Prefer **buf**. EasyP only if `easyp.yaml` already exists.

## Steps

1. Detect: `buf.yaml` present → buf. Only `easyp.yaml` → EasyP. Only `protoc` in a Makefile → `protoc-toolchain.md` / `migration.md`.
2. New module: copy [templates/buf.yaml](../../templates/buf.yaml) or `assets/buf.yaml`. Add `buf.build/bufbuild/protovalidate` and run `buf dep update`.
3. Pick a gen template from `assets/`:

| File | Use |
|------|-----|
| `buf.gen.go-connect.yaml` | Go + Connect (preferred for new Go) |
| `buf.gen.go.yaml` | Go + gRPC |
| `buf.gen.ts.yaml` | TypeScript + Connect |
| `buf.gen.python.yaml` | Python + gRPC |
| `buf.gen.java.yaml` | Java + gRPC |
| `buf.gen.yaml` | Combined starter |

4. Enable managed mode so `.proto` files stay language-agnostic. Pin plugin versions; do not use `:latest` on published APIs.
5. Generate: `buf generate` (or `make generate`). Commit generated code when the repo already does.
6. Compare Connect vs gRPC in `connect-vs-grpc.md` before adding a second RPC stack.

## Commands

```bash
buf dep update
buf generate
buf build
```

Makefile starter: `assets/Makefile.example`.

## Done when

`buf generate` succeeds with the project's `buf.gen.yaml`, and language options are not scattered through every proto unless the repo already requires them.
