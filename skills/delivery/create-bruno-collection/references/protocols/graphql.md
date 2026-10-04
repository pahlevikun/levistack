# GraphQL requests

`meta.type: graphql`. Endpoint is almost always a single HTTP URL (`POST`); Bruno stores query and variables in dedicated blocks.

## Query without variables

```bru
meta {
  name: List albums
  type: graphql
  seq: 1
}

post {
  url: {{graphqlUrl}}
  body: graphql
  auth: bearer
}

auth:bearer {
  token: {{accessToken}}
}

body:graphql {
  query {
    albums {
      data {
        id
        title
      }
    }
  }
}

docs {
  Public read of album list. Bearer optional if the gateway allows anonymous read.
}
```

## Query or mutation with variables

Use `body:graphql:vars` for JSON variables; reference `$name` in the operation.

```bru
meta {
  name: Get pokemon
  type: graphql
  seq: 2
}

post {
  url: {{graphqlUrl}}
  body: graphql
  auth: inherit
}

body:graphql {
  query GetPokemon($name: String!) {
    pokemon(name: $name) {
      id
      name
      height
      weight
    }
  }
}

body:graphql:vars {
  {
    "name": "{{pokemonName}}"
  }
}
```

Environment: `graphqlUrl` (often same host as REST `baseUrl` with a different path, e.g. `/graphql`). Reuse `accessToken` from HTTP login when the gateway shares auth.

## Auth and scripts

- **Bearer / basic / api-key** — same `auth:*` blocks as HTTP on the `post { }` section.
- **post-response** — `res.body` shape depends on the server; common pattern:

```bru
script:post-response {
  const data = res.body?.data;
  if (data?.createOrder?.id) {
    bru.setEnvVar("orderId", String(data.createOrder.id));
  }
}
```

## Documentation (`docs`)

Document GraphQL-specific failures, not only HTTP status:

- **200 with `errors` array** — partial or failed resolution; cite `errors[].message`, `path`, `extensions.code` from the real schema.
- **401 / 403** — gateway or field-level auth.
- **400** — malformed query or variables (validation).

Example fragment inside `docs { }`:

```bru
docs {
  Create an order via GraphQL mutation.

  ## Auth
  Bearer `accessToken`.

  ## Success
  - **200** — `data.createOrder { id, status }` with no top-level `errors`

  ## Errors
  - **200** with `errors`: e.g. `UNAUTHENTICATED`, `FORBIDDEN`, `BAD_USER_INPUT`
    ```json
    {
      "errors": [
        {
          "message": "Not authorized",
          "path": ["createOrder"],
          "extensions": { "code": "FORBIDDEN" }
        }
      ]
    }
    ```
}
```

Discover operations from `schema.graphql`, GraphQL codegen, or router config — not from REST path lists alone.
