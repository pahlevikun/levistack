# Go track

Buf managed mode + remote plugins. Copy `assets/buf.gen.go-connect.yaml` (Connect) or `assets/buf.gen.go.yaml` (gRPC).

## Defaults

- `go_package_prefix` in `buf.gen.yaml`; keep `.proto` files free of `option go_package` unless the repo already has them.
- Disable managed `go_package_prefix` for `buf.build/bufbuild/protovalidate` (see the Go gen templates).
- New services: Connect (`buf.build/connectrpc/go`) unless the mesh already speaks gRPC-only.
- Go 1.21+: `default_api_level=API_OPAQUE` on `protocolbuffers/go` when starting fresh; do not flip opaque on an existing public generated API.
- `paths=source_relative`.
- Never use package segment `internal` (Go cannot import it as you intend).

## Verify

`buf generate` then `go test ./...` (or the module's test command). Do not edit files under `gen/`.
