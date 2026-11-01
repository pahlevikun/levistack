# Build a server around a task contract

Start from the actual external API, data boundaries and caller tasks. Define the
smallest useful operations, each operation's side effects, permissions, input and
output schema, pagination, timeout, retry policy and safe failure behavior. Resources
represent readable material; prompts expose reusable interaction templates; tools
perform bounded operations. Choose the surface for its semantics.

Prefer the existing project's SDK and pinned dependencies. For a new project,
inspect the current official SDK documentation and choose a supported environment.
Do not copy a sample written for another major API or silently migrate dependencies.
Keep transport adapters separate from API clients, schema validation and handlers.

## Reusable Python starter

The bundled generator supports two explicit import profiles:

- `mcpserver`: `mcp.server.MCPServer`.
- `fastmcp`: `mcp.server.fastmcp.FastMCP`, for an environment where that interface
  has been verified. This is not the separate similarly named package.

```sh
python3 scripts/mcp_ops.py scaffold-python --name example-server --sdk-profile mcpserver --out ./example-server
```

It creates a fresh directory containing `server.py` and `README.md`. No dependency
is installed. The starter's only tool echoes a bounded message without remote
calls or persistence. The profile must match an SDK installed in the target
project. Run the documented SDK CLI there, then use the protocol probe with the
version that environment supports. A syntax check alone is not SDK compatibility.

The `MCPServer` example was checked against the
[official Python SDK](https://github.com/modelcontextprotocol/python-sdk) and
[its documentation](https://py.sdk.modelcontextprotocol.io/) during this skill's
implementation. Recheck the installed imports and CLI before using it in a new
project. Do not pin an inferred current package version from this prose.

## Implement actual integration behavior

1. Wrap the upstream API with explicit credentials, timeout and bounded responses.
   Do not allow arbitrary hostnames or filesystem paths unless the contract needs
   them and provides a concrete access policy.
2. Define discoverable tool names and schemas. Reject unknown/invalid inputs;
   support stable cursor behavior for collections. Avoid huge unbounded inventories
   and over-compressed tools whose arguments hide unrelated operations.
3. Return documented structures and useful, bounded errors. Distinguish protocol
   failures from operation errors. Never return raw stack traces, upstream tokens
   or complete request/response dumps.
4. Expose effect annotations when supported, but enforce authorization independently.
   Repeating a mutation must have explicit idempotency semantics where needed.
5. Use SDK transports rather than rolling a production JSON-RPC or HTTP stack.
   Stdio stdout remains protocol-only. Remote listeners require the actual origin,
   authentication, session and exposure policy; a development example supplies none
   of those business decisions.
6. Add resources/prompts only when a named task needs them. Validate URI templates,
   resource ownership, size bounds and provenance of returned content.

A TypeScript project follows the same contract and proof. Generate its scaffold
from the installed official SDK API/examples, choose one compatible import family,
and check compilation plus protocol behavior. This helper does not fabricate a
TypeScript template across unknown SDK versions.
