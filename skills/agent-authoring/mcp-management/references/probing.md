# Diagnose the missing layer

| Observation | Check next |
|---|---|
| Executable not found | Actual binary, environment, working directory and platform |
| Process exits cleanly | Protocol initialization; success may mean it did no work |
| Initialize fails | Transport/framing, supported protocol version, credentials and capability response |
| Initialize works but tool is absent | Declared tools capability, pagination, disabled features and expected name |
| Direct probe works but host has no tools | Host's effective scope/config, refresh behavior and discovery filters |
| Tool is listed but task fails | Input schema, upstream authorization, operation semantics and result/error contract |

Stdio carries one UTF-8 JSON-RPC message per line. Non-protocol stdout breaks the
channel. Logging belongs on stderr, but private logs must not be copied into a
report. Remote Streamable HTTP is an independent transport with its own
initialization, session, media type, authentication and timeout behavior.

## Bounded stdio probe

Select a protocol date supported by the intended host and server. The script does
not assume it knows the latest version, and rejects a different negotiated version.
For a server that supports the illustrated version:

```sh
python3 scripts/mcp_ops.py probe-stdio --protocol-version 2025-06-18 --timeout 5 --require-tool echo_message -- python3 example_server.py
```

The sequence is initialize -> notifications/initialized -> tools/list. Inventory
pagination, inbound/outbound frame size, aggregate stdout, queue depth and total
runtime have bounds, including a peer that stops reading stdin. The helper uses
nonblocking process pipes; if the platform cannot provide them, use the official
SDK client instead of treating a skipped probe as a pass.
A server callback receives an unsupported-method response, except a protocol ping.
No sampling, filesystem root disclosure or elicitation is provided. The script
terminates the child after probing, including on error. Stderr is drained without
retaining or echoing its contents.

A safe operation must be chosen and authorized separately. Tool annotations are
untrusted hints and do not authorize execution. With a small local argument file:

```sh
python3 scripts/mcp_ops.py probe-stdio --protocol-version 2025-06-18 --call-tool echo_message --arguments arguments.json --allow-tool-call -- python3 example_server.py
```

The probe requires server name/version and object-shaped tool input schemas.
For called tools it checks supported text, image/audio, resource-link and embedded
resource block structures, including binary encoding. Unsupported content types
fail rather than receiving a green receipt. These are protocol structure checks;
full JSON Schema/business-result validation belongs in the chosen SDK and operation
tests.

A receipt reports protocol success and tool names/counts, not result contents.
If a schema or tool name itself is sensitive, keep the receipt private as well.
A direct successful probe still does not establish host registration, user-visible
discovery or production readiness.

## HTTP and host discovery

The bundled probe is stdio-only. Use the chosen SDK client or official Inspector
for remote HTTP. Verify TLS, auth negotiation, agreed protocol header, session
identity where used, JSON/SSE responses and an authorized operation. Do not turn
an HTTPS endpoint into HTTP because local testing is easier. Bind development
listeners to loopback and check origin handling before exposing an endpoint.

After a configuration change, inspect the host's actual tools in the active
session. Use its supported refresh mechanism or a new session if required. Do not
promise that an install or config change updates a session's tool list immediately.

Primary protocol references:
[Lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle),
[transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports),
and [tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools).
These versioned references explain the probe; validate the target's chosen version.
