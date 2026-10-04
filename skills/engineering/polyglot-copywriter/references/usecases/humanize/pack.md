# humanize — use case pack

**Status:** `validated`

Load [humanize-workflow.md](../../techniques/humanize-workflow.md) — detect → rewrite → verify loop.

Also [humanizer-patterns.md](../../humanizer-patterns.md) (the 26 numbered tells, strongest first), [noslop-doctrine.md](../../noslop-doctrine.md) (principles and critique format), [english-humanizer.md](../english-humanizer.md) (EN worked examples) and [noslop-prose.md](../../noslop-prose.md).

**Output modes:** pasted text returns draft, remaining patterns, final. A named file gets only the final text, prose only (code, commands, paths, YAML, link targets untouched). Embedded use (PR, commit, MR comment, doc) returns only the final text. A reply in a thread leads with the decision (§26).

**Optional show-work:** for paste-in humanize tasks, agent may output flagged patterns → draft rewrite → final after survivor scan (see humanize-workflow § Show-work output). Default remains edited draft + what changed.

**Inline rules:** minimum effective edit; preserve voice; no invented facts; detect-only if user asked to audit.

## Default register

`santai`
