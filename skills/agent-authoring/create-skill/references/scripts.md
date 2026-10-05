# Scripts, templates and secrets

## Contents
- When a script beats instructions
- Writing a script the agent can trust
- Validators that fix themselves
- Runtime and dependencies
- Referencing MCP tools
- Templates
- Calls that need credentials

## When a script beats instructions

Bundle a script when the same code would be regenerated on every run, when a step is fragile, or when the result must be identical each time. A script that runs costs only its output in context; code the model writes costs the code and the risk of a new bug.

Say in the skill whether the agent should **run** it (the usual case) or **read** it (when the logic is the point). One-off operations do not deserve a script.

## Writing a script the agent can trust

- A purpose comment and usage line at the top.
- Validate inputs first and fail with a message that names the problem.
- Handle the errors you can handle. A missing optional file becomes a default, not a stack trace for the agent to interpret.
- Idempotent where possible, so re-running after a failure is safe.
- A `--dry-run` for anything that deletes or overwrites.
- No hard-coded secrets; read environment variables.
- Justify constants. `REQUEST_TIMEOUT = 30  # most calls finish in under 30 s` is documentation; `TIMEOUT = 47` is a mystery.
- Shell scripts start with `set -euo pipefail` and are executable (`chmod +x`). Prefer Node or Python for anything with logic.

```javascript
// Solve the problem instead of passing it on.
function readOrDefault(path) {
  try { return readFileSync(path, 'utf8'); }
  catch (e) {
    if (e.code === 'ENOENT') { console.error(`${path} not found, using empty default`); return ''; }
    throw e;
  }
}
```

## Validators that fix themselves

A validator is only as useful as its message. The agent should be able to repair the problem in one pass.

| Weak | Strong |
|---|---|
| `Invalid field` | `Field 'signature_date' not found. Available: customer_name, order_total, signature_date_signed` |
| `XML syntax error` | `Line 47: expected </paragraph>, found </section>` |
| `Missing required field` | `Required field 'customer_name' is missing. Add {"customer_name": "<value>"}` |
| `Invalid status` | `Invalid status 'pending_review'. Valid: active, paused, archived` |

Say what, where, and what would be valid. Wire the validator into the skill as a loop: run, fix, run again, proceed only on a clean exit.

## Runtime and dependencies

- List every package the script needs in the skill body, with the install command. "Use the pdf library" fails; `pip install pypdf` works.
- Environments differ. Some can install from a registry; some have no network and no installs. State the assumption or make the script degrade (skip an optional parser with a hint, as `extract_document.py` does).
- Use forward slashes in every path.

## Referencing MCP tools

Use the fully qualified name, `ServerName:tool_name` (for example `GitHub:create_issue`). Without the server prefix the agent may fail to find the tool when several servers are connected. In Claude Code the tool id is `mcp__<server>__<tool>`.

## Templates

A template is an output shape the agent copies and fills. Use one when structure matters more than prose and filling placeholders is more reliable than a blank page: plans, specs, reports, configs, scaffolds.

- Mark placeholders one way throughout (`<like-this>` or `{{like_this}}`).
- Put a few words of guidance beside any section that could be misread.
- Keep it complete but minimal. Example content that is too good gets copied verbatim.
- Do not template creative output or over-constrain with sections nobody needs.
- Update the template when the requirement changes, or the skill and its output drift apart.

Say in the workflow when to use it: "Copy `templates/plan.md`, fill every placeholder, then check the plan against the checklist."

## Calls that need credentials

A command with an expanded secret appears in the transcript:

```bash
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/data   # the key is now in the chat
```

Do this instead:

1. Put the call behind a wrapper script that loads credentials itself (from the environment or a local file outside the repo) and takes only non-secret arguments: `./scripts/api.sh list-items`.
2. Give the wrapper one subcommand per operation, so the skill never contains a raw `curl` with a variable.
3. Add the credential names to a local template (`.env.example`) with empty values, never real ones.
4. Check that a credential is set without printing it: `test -n "$API_KEY" && echo set || echo missing`.
5. When there are several accounts, have the skill ask which profile to use, say which one it is using before the call, and reuse it for the session.
6. Treat an authentication error as a normal gate, not a failure: stop, tell the user the exact login step, wait, verify (`<tool> whoami`), then retry the original call. Do not retry in a loop.

Never write a secret or a personal path into a shared skill.
