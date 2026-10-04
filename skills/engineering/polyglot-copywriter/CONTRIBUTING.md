# Contributing to Polyglot Copywriter

Thank you for helping improve this skill. All **agent-facing** instructions must be in **English**. User-facing **examples** in target languages (Indonesian, Japanese, etc.) belong in example tables and quoted output samples — not in section headers or routing rules.

## Prerequisites

- Python 3.10+ (not installed? see [references/python-setup.md](references/python-setup.md))
- From the skill root (`skills/engineering/polyglot-copywriter`):

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -q
```

Both must pass before you open a pull request.

## Add a language

1. **Scaffold** — `python3 scripts/new_language.py <id> "<Name>"` (copies `_template/language/`).
2. **Fill packs** — edit `pack.md`, `registers.md`, `culture.md`. Add `speech-levels.md` or `overlays/` when needed.
   - Each `registers.md` needs one good + one bad example per register.
   - `culture.md` needs a **Natural grammar** section (agent instructions in English).
   - At least one regional overlay (`<id>-standard` or country code) unless umbrella/limited honesty applies.
3. **Register** — append one row to `references/registry.json` with `"status": "validated"`.
4. **Locale + profile** — run `python3 scripts/bulk_expand.py` to regenerate locale technique and profile index entries.
5. **Validate** — `python3 scripts/validate_skill.py`.

## Add a use case

1. `python3 scripts/new_usecase.py <id> "<Name>"`
2. Fill `references/usecases/<id>/pack.md` (structure only — language rules stay in language packs).
3. Register in `references/registry.json`.
4. If the use case needs a generic technique module, add `references/techniques/<name>.md` and an entry in `references/techniques/index.json`.

## Add a locale technique

Locale files live under `references/techniques/locales/<language_id>.md`.

- **Instructions** (headers, bullets, routing notes): English.
- **Examples** in the target language: OK in good/bad tables and quoted samples.
- Add a row to `references/techniques/index.json` under `locales`.
- Update routing in [references/core.md](references/core.md) § Technique routing and [references/techniques/README.md](references/techniques/README.md).

## Add an overlay profile

Profiles are short snapshots under `references/profiles/`. Authoritative rules stay in `references/languages/<lang>/overlays/<id>.md`.

1. Add `<id>.md` under `references/profiles/`.
2. Register in `references/profiles/index.json`.
3. Register in `references/profiles/index.json` (validated by `validate_skill.py` and `tests/test_profiles.py`).
4. Optionally document high-traffic overlays in [references/profiles/README.md](references/profiles/README.md).

## Add an eval case

Edit [evals/cases.json](evals/cases.json):

- `description` — English summary of what the case tests.
- `prompt` — may stay in any language when testing detection or locale output.
- `human_review` — English criteria for manual review.
- `checks` — `preserve`, `require`, `forbid_patterns`, `first_paragraph_require` as needed.

Mode-boundary and fidelity cases belong in `evals/cases.json` with optional
`mode` (`interview` | `rewrite` | `review`) and `category`
(`factual_fidelity` | `medium_fit` | `false_positive` | `authorship` |
`mode_boundary` | `instruction_integrity`). Put semantic rules in
`human_review`; keep `checks` automatically verifiable.

**`category: false_positive`** — cases that must **not** be over-edited:
earned triads, academic hedges, intentional quotes of slop phrases,
`robust` with mechanism, earned passive/adverb/Wh-opener, earned antithesis.
These guard against blanket bans; failures mean the agent flagged or rewrote
earned patterns. Register new false-positive ids in
`scripts/validate_skill.py` `required_eval_ids` and
`tests/test_eval_cases.py` `REQUIRED_INVARIANT_IDS` when they become
release invariants.

Run `python3 scripts/evaluate_output.py <case-id> <output-file>` to test a draft against automatic checks.

## Pull request expectations

- **English-only agent instructions** across `SKILL.md`, `references/**`, `evals/**`, `scripts/**`, `tests/**`, and docs.
- No links to removed docs (e.g. deleted competitor comparisons).
- `python3 scripts/validate_skill.py` passes (registry, links, technique index, profile index, eval schema).
- `python3 -m unittest discover -s tests -q` passes.
- Update [README.md](README.md) file tree or coverage table when you add languages, techniques, or profiles.

## License

By contributing, you agree that your contributions are licensed under the same terms as the repository root `LICENSE`.
