# Secrets and configuration

## Where secrets may live

| Place | Verdict |
|---|---|
| `config/runtime.exs`, read with `System.fetch_env!/1` | Correct. Evaluated at boot, so it can differ per deployment |
| Environment variables, a secret manager, a mounted file | Correct |
| `config/config.exs`, `dev.exs`, `prod.exs` | Not for secrets. These are evaluated at **compile time** and baked into the release |
| Module attributes (`@api_key System.get_env(...)`) | Wrong. The value is read at compile time and frozen in the compiled code |
| Source code, tests, fixtures, `.env` files in git | A finding if it is a real credential |

## Checklist

### Critical
- [ ] No real credential in source, in `config/*.exs`, in test files or in git history
- [ ] `secret_key_base`, signing salts and API keys are not literals outside `runtime.exs`
- [ ] No secret in a log line, an error message, a telemetry event or a crash report

### Major
- [ ] Runtime values come through `Application.fetch_env!/2` inside functions, not `Application.compile_env` for secrets
- [ ] Token and signature comparison uses `Plug.Crypto.secure_compare/2`, not `==`
- [ ] `Logger` calls do not `inspect` a whole `conn`, `socket`, `params` or config map
- [ ] Phoenix `:filter_parameters` covers the sensitive parameter names
- [ ] Production does not expose `Plug.Debugger` or detailed error pages

### Operations
- [ ] Remote shell, `:observer` and the Erlang distribution port are not reachable from outside; the cookie is not the default
- [ ] A rotation path exists for each secret
- [ ] Release configuration comes from `releases` and `runtime.exs`, not from a committed file

## Valid patterns (do not flag)

- Test-only dummy values in `config/test.exs`, clearly not real
- `System.get_env/2` with a non-secret default (a port, a pool size)
- A literal in `dev.exs` for a local-only service with no real data

## Verify before reporting

Follow [verification protocol](../../../references/verification-protocol.md). For a hard-coded secret, confirm it is a real credential and name where it is used.
