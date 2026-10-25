# Connect vs gRPC

Pick one RPC stack per service unless a gateway already translates.

| | Connect | gRPC |
|--|---------|------|
| Transports | HTTP/1.1 and HTTP/2; browsers without a special client | HTTP/2 (grpc-web for browsers) |
| Go plugin | `buf.build/connectrpc/go` | `buf.build/grpc/go` |
| TS plugin | `buf.build/connectrpc/es` | gRPC-web stacks |
| Auth | Ordinary HTTP headers | Metadata; still requires authz |
| Default for new work | Yes, especially browser or mixed HTTP | Yes, when the mesh/org is gRPC-only |

`.proto` services stay the same. The gen template chooses the stub. Do not generate both into the same `out` directory.

grpc-web is gRPC for browsers; it is still HTTP and needs the same authz as JSON APIs (`security.md`).

Templates: `assets/buf.gen.go-connect.yaml`, `assets/buf.gen.go.yaml`, `assets/buf.gen.ts.yaml`.
