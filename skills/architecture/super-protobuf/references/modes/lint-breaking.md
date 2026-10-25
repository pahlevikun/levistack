# Mode: lint-breaking

Make lint and breaking checks pass. Prefer **buf**. EasyP if the repo already uses it.

## Steps

1. Format, then lint:

```bash
buf format -w
buf lint
```

2. If the schema already shipped:

```bash
buf breaking --against '.git#branch=main'
```

3. Fix naming and structure using `style.md` and `troubleshooting.md`.
4. Intentional breaks → new `vN` package, not a silenced rule. `breaking.ignore` is for generated or internal paths with a written reason.
5. EasyP-only repos: `easyp lint` and `easyp breaking --against main`. Same intent; do not add buf beside it.

## Config defaults

`lint.use: [STANDARD]` and `breaking.use: [FILE]` as in `assets/buf.yaml` / `templates/buf.yaml`.

Do not add a custom Python or ad-hoc proto linter.

## Done when

Format, lint, and (when required) breaking are clean, or each remaining ignore is documented.
