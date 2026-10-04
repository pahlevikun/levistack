# Python TDD track

Apply the core loop from [SKILL.md](../../SKILL.md).

**Use when:** `.py`, pytest, `unittest`, `test_*.py`, or "Python TDD".

## Runner

Discover from `pyproject.toml`, `pytest.ini`, or CI. Typical focused: `pytest path/to/test_mod.py::test_name -q`. Do not assume `npm test`.

Use the project's venv or wrapper (`poetry run pytest`, `uv run pytest`, `./.venv/bin/pytest`) when one exists.

## Seams

Test public functions and module APIs. Prefer `pytest` fixtures that build real objects over patching every collaborator. Patch I/O and time at the edge.

## Green / refactor

Smallest function body that passes this case. After green, `super-refactor` for extracts; keep pytest green per step.
