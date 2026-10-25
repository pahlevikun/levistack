# Microkernel (plugin platform)

A small, stable kernel plus plugins that extend it without changing it. The kernel owns lifecycle, discovery, permissions and a versioned contract. Features live in plugins, including first-party ones.

## Pick when
- Building a platform, IDE, marketplace, ingestion pipeline or product where third parties (or other teams) add capabilities.
- The core must stay extremely stable while features change quickly.
- Untrusted or optional code must be sandboxed so a bad plugin cannot take down the host.

## Avoid when
- A closed application with one team and no extension need. Plain modules are simpler (`styles/modular-monolith/GUIDE.md`).
- Every feature is core and tightly coupled by design.

For the concrete shape of a Claude Code (or similar) extension host, also read `styles/plugin/GUIDE.md`. This guide is the general platform architecture.

## Core idea

The **kernel** does as little as possible: load, start, stop, route messages, enforce permissions, version the contract. **Plugins** register capabilities through that contract. Isolation is a product requirement: load failure is reported, not fatal.

## Layout

```
kernel/                   lifecycle, registry, permissions, messaging primitives
contracts/                plugin API: registration, capability descriptors, hooks
plugins/<name>/           one plugin per capability; depends only on contracts
sdk/                      templates, test harness, compatibility checker
sandbox/                  isolation and resource limits
```

## Build steps
1. Write down the kernel's minimal responsibilities. Everything else is a plugin, including features you will ship yourself.
2. Specify the plugin contract: registration, capability descriptors, start/stop hooks, permission model.
3. Build the loader: discovery, version check, capability negotiation, sandbox.
4. Ship an SDK (template, harness, compatibility check) before inviting third parties.
5. Publish a compatibility matrix (kernel version × plugin API version) and a certification pipeline: lint, test, sandbox run.
6. Version the contract with SemVer. Breaking changes get a new API major and a shim only when you must keep old plugins alive.

## Testing
- Kernel tests with fake plugins: load, fail-to-load, permission denied, crash isolation.
- Contract tests in the SDK that every plugin must pass.
- Regression suite: core journeys against a set of certified plugins.
- Chaos: kill a plugin mid-request; the host stays up.

## Pitfalls
Kernel bloat (new features land in the kernel "just this once"). Uncurated plugin explosion. Version skew with no matrix. Plugins that import kernel internals. A host that dies when one plugin throws.

## Combines with
Plugin (host packaging and discovery), hexagonal (the contract is a set of ports), event-driven (plugins subscribe to kernel events), modular monolith (first-party plugins as modules until you need isolation).
