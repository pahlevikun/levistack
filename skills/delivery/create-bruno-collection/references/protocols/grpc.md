# gRPC requests

`meta.type: grpc`. Discover methods from `.proto` files and/or server reflection.

## Collection layout for protos

Commit protos next to the collection when possible:

```
docs/api/bruno/<service>/
├── bruno.json
├── proto/                    # optional; or point at repo api/proto
│   └── hello/v1/hello.proto
├── environments/
├── auth/                     # HTTP login if tokens are HTTP-only
└── grpc/
    └── hello/
        └── say-hello.bru
```

In **collection settings → Protobuf**, add collection-level proto files and **import paths** for shared types (`google/protobuf`, shared `common/`). Request-level `protoPath` in the `grpc { }` block overrides for one RPC. Bruno gRPC proto docs are listed in `references/bruno-documentation.md`.

## Unary RPC (with metadata and env token)

```bru
meta {
  name: Say hello
  type: grpc
  seq: 1
}

grpc {
  url: {{grpcHost}}
  method: /hello.HelloService/SayHello
  body: grpc
  auth: inherit
  methodType: unary
}

metadata {
  authorization: Bearer {{accessToken}}
  x-request-id: {{requestId}}
}

body:grpc {
  name: message 1
  content: '''
    {
      "greeting": "bruno"
    }
  '''
}

docs {
  Unary hello RPC. Run **auth/login** when `accessToken` is required.

  ## Success
  - gRPC status **OK (0)** — response message matches `SayHelloResponse`

  ## Errors
  - **UNAUTHENTICATED (16)** — missing or invalid bearer metadata
  - **INVALID_ARGUMENT (3)** — bad `greeting` field
  - **NOT_FOUND (5)** — resource does not exist (if applicable)
}
```

`grpcHost` examples: `grpc://localhost:50051`, `grpcs://api.example.com:443`. Use `protoPath: path/to/service.proto` on the `grpc { }` block when not using collection-level protos.

## Streaming

Set `methodType` to match the RPC:

| `methodType` | Pattern |
|---|---|
| `unary` | Single request, single response |
| `server-streaming` | One request, many responses |
| `client-streaming` | Many requests, one response |
| `bidi-streaming` | Multiple `body:grpc { }` blocks (one per outbound message) |

```bru
grpc {
  url: {{grpcHost}}
  method: /hello.HelloService/BidiHello
  body: grpc
  auth: inherit
  methodType: bidi-streaming
}

body:grpc {
  name: message 1
  content: '''
    { "greeting": "first" }
  '''
}

body:grpc {
  name: message 2
  content: '''
    { "greeting": "second" }
  '''
}
```

Document in `docs` how operators end the stream and what a successful timeline looks like.

## gRPC scripting (beta)

Interactive app only; collection runner / CLI coverage for gRPC scripts is limited. Prefer HTTP login + `bru.setEnvVar` for tokens, then pass `Bearer {{accessToken}}` in `metadata`.

For in-call hooks, use `script:grpc:*` blocks:

```bru
script:grpc:before-call-start {
  bru.grpc.request.metadata.upsert(
    "authorization",
    "Bearer " + bru.getEnvVar("accessToken")
  );
}

script:grpc:after-call-end {
  test("status is OK", function () {
    expect(bru.grpc.response.statusCode).to.equal(0);
  });
}
```

Writable metadata only in **before-call-start**. Status **0** means OK; document non-zero [gRPC status codes](https://grpc.io/docs/guides/status-codes/) in `docs`.

## Mixed HTTP + gRPC collections

Many products expose REST for auth and gRPC for internal APIs. Keep `auth/login.bru` as `type: http` with `bru.setEnvVar("accessToken", ...)`; gRPC requests read the same env vars in `metadata` or `script:grpc:before-call-start`.
