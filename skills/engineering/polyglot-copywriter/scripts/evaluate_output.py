#!/usr/bin/env python3
"""Evaluate Polyglot Voice case output against evals/cases.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CASES = SCRIPT_DIR.parent / "evals" / "cases.json"


def load_cases(cases_path: Path = DEFAULT_CASES) -> list[dict]:
    payload = json.loads(cases_path.read_text(encoding="utf-8"))
    return payload["cases"]


def evaluate_output(test_case: dict, output: str) -> list[str]:
    failures: list[str] = []
    checks = test_case.get("checks") or {}
    first_paragraph = re.split(r"\r?\n\s*\r?\n", output.strip(), maxsplit=1)[0]

    for value in checks.get("preserve") or []:
        if value not in output:
            failures.append(f"Protected artifact missing or changed: {value}")
    for value in checks.get("require") or []:
        if value not in output:
            failures.append(f"Required substring missing: {value}")
    for value in checks.get("first_paragraph_require") or []:
        if value not in first_paragraph:
            failures.append(f"First paragraph missing: {value}")
    for pattern in checks.get("forbid_patterns") or []:
        if re.search(pattern, output, flags=re.IGNORECASE | re.UNICODE):
            failures.append(f"Forbidden pattern found: /{pattern}/iu")
    return failures


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 2:
        print(
            "Usage: python3 scripts/evaluate_output.py <case-id> <output-file>",
            file=sys.stderr,
        )
        return 2

    case_id, output_path = args[0], Path(args[1])
    test_case = next((item for item in load_cases() if item["id"] == case_id), None)
    if test_case is None:
        print(f"Case not found: {case_id}", file=sys.stderr)
        return 2

    output = output_path.resolve().read_text(encoding="utf-8")
    failures = evaluate_output(test_case, output)
    if failures:
        print(f"Evaluation {case_id} failed ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    review_count = len(test_case.get("human_review") or [])
    print(
        f"Automatic evaluation {case_id} passed. Continue with {review_count} human-review criteria."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
