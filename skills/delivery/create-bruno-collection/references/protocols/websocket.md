# WebSocket requests

`meta.type: ws`. Use for real-time, bidirectional messaging (not SSE — SSE stays on HTTP `type: http`).

## Basic connection and message

```bru
meta {
  name: Echo with auth
  type: ws
  seq: 1
}

ws {
  url: {{wsUrl}}
  auth: inherit
}

headers {
  Authorization: Bearer {{accessToken}}
  Sec-WebSocket-Protocol: json
}

body:ws {
  name: message 1
  content: '''
    {
      "action": "subscribe",
      "channel": "{{channelId}}"
    }
  '''
}

docs {
  Opens a WebSocket and sends a subscribe payload.

  ## Auth
  Bearer `accessToken` in `Authorization` header; run **auth/login** first if required.

  ## Success
  - Connection established; server ack message documented below

  ## Errors
  - Connection refused or TLS failure — check `wsUrl` (`ws://` vs `wss://`)
  - **401** during handshake — invalid token
  - Server JSON error frame — document `code` / `message` fields from the API spec
}
```

Environment vars:

- `wsUrl` — e.g. `wss://api.example.com/ws` or `wss://echo.{{host}}.org` with interpolated env vars.
- Reuse `accessToken`, `apiKey`, and IDs from HTTP or GraphQL flows via `bru.setEnvVar`.

## Multiple outbound messages

Add more `body:ws { name: ... content: ''' ... ''' }` blocks when the protocol sends a sequence (handshake, subscribe, ping). Document order and expected inbound frames in `docs`.

## Scripts

WebSocket requests use HTTP-style `script:pre-request` / `script:post-response` where Bruno supports them for WS; use pre-request to warn when `accessToken` is empty (same guard as HTTP login chaining). Long-lived sockets are **manual** in the UI — do not assume collection runner will hold connections open.

## Settings (operator notes)

Document in `docs` when relevant: connection timeout, auto-reconnect, subprotocol via `Sec-WebSocket-Protocol`, custom `User-Agent`. Bruno exposes these in the request **Settings** tab.
