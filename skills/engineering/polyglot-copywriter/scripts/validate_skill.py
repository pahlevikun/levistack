#!/usr/bin/env python3
"""Validate polyglot-copywriter skill layout, links, registry, and eval cases."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from catalog import fictional_fixture_ids, load_fictional_catalog, load_registry

ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
REQUIRED_REFERENCES = [
    "references/core.md",
    "references/configuration.md",
    "references/regional.md",
    "references/evaluation.md",
    "references/languages/language-selection.md",
    "references/registry.json",
    "references/usecases/poetic.md",
    "references/substance.md",
    "references/interview.md",
    "references/review-prose.md",
]
REQUIRED_LANGUAGE_IDS = {"english", "indonesia"}
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_KEY_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):", re.MULTILINE)
FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b")
HARDCODED_LANGUAGE_LIST = re.compile(
    r"\b(?:japanese|korean|arabic|french|mandarin|spanish)\b.*\|.*\|",
    re.IGNORECASE,
)


def read(skill_root: Path, relative: str, errors: list[str]) -> str:
    path = skill_root / relative
    if not path.exists():
        errors.append(f"Required file missing: {relative}")
        return ""
    return path.read_text(encoding="utf-8")


def walk_files(directory: Path) -> list[Path]:
    files: list[Path] = []
    for entry in directory.iterdir():
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            files.extend(walk_files(entry))
        else:
            files.append(entry)
    return files


def frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    return re.sub(r"^(['\"])(.*)\1$", r"\2", match.group(1).strip())


def validate_pack_path(skill_root: Path, relative: str, label: str, errors: list[str]) -> None:
    if not relative:
        errors.append(f"Missing pack path: {label}")
        return
    if not (skill_root / relative).exists():
        errors.append(f"Pack file missing: {label} -> {relative}")


def validate_registry(skill_root: Path, errors: list[str]) -> tuple[int, int, int, int]:
    validated_count = 0
    overlay_count = 0
    language_count = 0
    usecase_count = 0
    try:
        registry = json.loads(read(skill_root, "references/registry.json", errors) or "{}")
    except json.JSONDecodeError as exc:
        errors.append(f"references/registry.json is not valid JSON: {exc}")
        return 0, 0, 0, 0

    if registry.get("schema_version") != 2:
        errors.append("registry.json must use schema_version 2.")

    languages = registry.get("languages")
    if not isinstance(languages, list):
        errors.append("registry.json must have a languages array.")
        return 0, 0, 0, 0

    language_count = len(languages)
    ids: set[str] = set()
    overlay_ids: set[str] = set()

    for language in languages:
        lang_id = language.get("id")
        if not lang_id or lang_id in ids:
            errors.append(f"Empty or duplicate language id: {lang_id}")
        ids.add(lang_id)

        status = (language.get("support") or {}).get("status")
        if status != "validated":
            errors.append(f"Language must be validated: {lang_id} (found {status})")
        else:
            validated_count += 1

        pack = (language.get("support") or {}).get("pack")
        validate_pack_path(skill_root, pack, f"language:{lang_id}", errors)

        lang_dir = skill_root / "references" / "languages" / lang_id
        for required in ("registers.md", "culture.md"):
            if not (lang_dir / required).exists():
                errors.append(f"Missing {required} for language:{lang_id}")

        for overlay in language.get("overlays") or []:
            oid = overlay.get("id")
            key = f"{lang_id}:{oid}"
            if not oid or key in overlay_ids:
                errors.append(f"Empty or duplicate overlay id: {key}")
            overlay_ids.add(key)
            overlay_count += 1
            ostatus = overlay.get("status")
            if ostatus != "validated":
                errors.append(f"Overlay must be validated: {key} (found {ostatus})")
            validate_pack_path(skill_root, overlay.get("file"), f"overlay:{key}", errors)

    if not REQUIRED_LANGUAGE_IDS.issubset(ids):
        errors.append("Registry must include validated english and indonesia.")

    usecases = registry.get("usecases")
    if not isinstance(usecases, list):
        errors.append("registry.json must have a usecases array.")
    else:
        usecase_count = len(usecases)
        uc_ids: set[str] = set()
        for usecase in usecases:
            uid = usecase.get("id")
            if not uid or uid in uc_ids:
                errors.append(f"Empty or duplicate use case id: {uid}")
            uc_ids.add(uid)
            ustatus = usecase.get("status")
            if ustatus != "validated":
                errors.append(f"Use case must be validated: {uid} (found {ustatus})")
            validate_pack_path(skill_root, usecase.get("pack"), f"usecase:{uid}", errors)

    return language_count, validated_count, overlay_count, usecase_count


def validate_fictional_catalog(skill_root: Path, errors: list[str]) -> tuple[int, int]:
    fixture_count = 0
    validated_count = 0
    try:
        catalog = load_fictional_catalog(skill_root / "references" / "fictional-catalog.json")
    except FileNotFoundError:
        errors.append("Required file missing: references/fictional-catalog.json")
        return 0, 0
    except json.JSONDecodeError as exc:
        errors.append(f"references/fictional-catalog.json is not valid JSON: {exc}")
        return 0, 0

    if catalog.get("schema_version") != 1:
        errors.append("fictional-catalog.json must use schema_version 1.")

    fixtures = catalog.get("fixtures")
    if not isinstance(fixtures, list):
        errors.append("fictional-catalog.json must have a fixtures array.")
        return 0, 0

    fixture_count = len(fixtures)
    ids: set[str] = set()
    for fixture in fixtures:
        fixture_id = fixture.get("id")
        if not fixture_id or fixture_id in ids:
            errors.append(f"Empty or duplicate fictional fixture id: {fixture_id}")
        ids.add(fixture_id)

        status = fixture.get("status")
        if status != "validated":
            errors.append(f"Fictional fixture must be validated: {fixture_id} (found {status})")
        else:
            validated_count += 1

        if fixture.get("purpose") != "honesty-eval":
            errors.append(f"Fictional fixture purpose must be honesty-eval: {fixture_id}")

        paths = fixture.get("paths") or {}
        for key in ("pack", "registers", "culture"):
            validate_pack_path(skill_root, paths.get(key), f"fictional:{fixture_id}:{key}", errors)

        if fixture.get("overlays"):
            errors.append(f"Fictional fixture must not define overlays: {fixture_id}")

    return fixture_count, validated_count


def validate_catalog_separation(skill_root: Path, errors: list[str]) -> None:
    registry_path = skill_root / "references" / "registry.json"
    catalog_path = skill_root / "references" / "fictional-catalog.json"
    if not registry_path.exists() or not catalog_path.exists():
        return
    registry = load_registry(registry_path)
    fictional_ids = fictional_fixture_ids(load_fictional_catalog(catalog_path))
    registry_ids = {language["id"] for language in registry.get("languages", [])}
    overlap = sorted(registry_ids & fictional_ids)
    if overlap:
        errors.append(f"Fictional fixture ids must not appear in registry.json: {overlap}")


def validate_technique_index(skill_root: Path, errors: list[str]) -> None:
    index_path = skill_root / "references/techniques/index.json"
    if not index_path.exists():
        return
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"references/techniques/index.json is not valid JSON: {exc}")
        return
    for section in ("generic", "generic_usecase", "locales"):
        entries = index.get(section)
        if not isinstance(entries, list):
            errors.append(f"techniques index missing array: {section}")
            continue
        for entry in entries:
            rel = entry.get("file")
            if not rel:
                errors.append(f"technique index entry missing file in {section}")
                continue
            if not (skill_root / rel).exists():
                errors.append(f"technique index file missing: {rel}")


def validate_profile_index(skill_root: Path, errors: list[str]) -> None:
    index_path = skill_root / "references/profiles/index.json"
    if not index_path.exists():
        return
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"references/profiles/index.json is not valid JSON: {exc}")
        return
    profiles = index.get("profiles")
    if not isinstance(profiles, list):
        errors.append("profiles index missing profiles array")
        return
    for entry in profiles:
        rel = entry.get("file")
        if not rel:
            errors.append("profile index entry missing file")
            continue
        if not (skill_root / rel).exists():
            errors.append(f"profile index file missing: {rel}")


def validate(skill_root: Path) -> list[str]:
    errors: list[str] = []
    skill_text = read(skill_root, "SKILL.md", errors)
    frontmatter_match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n", skill_text)

    if not frontmatter_match:
        errors.append("SKILL.md is missing complete YAML frontmatter.")
    else:
        frontmatter = frontmatter_match.group(1)
        name = frontmatter_value(frontmatter, "name")
        description = frontmatter_value(frontmatter, "description")
        keys = FRONTMATTER_KEY_PATTERN.findall(frontmatter)
        for key in keys:
            if key not in ALLOWED_FRONTMATTER_KEYS:
                errors.append(f"Unknown frontmatter key: {key}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name or "") or len(name) > 64:
            errors.append(f"Invalid skill name: {name or '<empty>'}")
        if name != skill_root.name:
            errors.append(f"Skill name '{name}' does not match folder '{skill_root.name}'.")
        if not 1 <= len(description) <= 1024:
            errors.append(f"Description must be 1–1024 characters; found {len(description)}.")
        if re.search(r"[<>]", description):
            errors.append("Description must not contain angle brackets.")

    if len(skill_text.splitlines()) > 120:
        errors.append("SKILL.md should stay a thin router (~80–100 lines).")

    for required in REQUIRED_REFERENCES:
        if required not in skill_text and f"]({required})" not in skill_text:
            errors.append(f"SKILL.md does not route to required reference: {required}")

    if "references/profiles/" in skill_text:
        errors.append("SKILL.md must not link profiles directly.")

    if HARDCODED_LANGUAGE_LIST.search(skill_text):
        errors.append("SKILL.md must not hardcode language or use-case tables — use registry.json.")

    for file in walk_files(skill_root):
        if file.suffix != ".md":
            continue
        text = file.read_text(encoding="utf-8")
        relative = file.relative_to(skill_root).as_posix()
        fence_count = sum(1 for line in text.splitlines() if FENCE_PATTERN.match(line))
        if fence_count % 2 != 0:
            errors.append(f"Unbalanced Markdown fence: {relative}")
        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"Unfinished placeholder: {relative}")
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            if re.match(r"^(?:https?:|mailto:|#)", target):
                continue
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split("#", 1)[0]
            resolved = (file.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"Broken local link: {relative} -> {match.group(1)}")

    lang_count, validated_count, overlay_count, usecase_count = validate_registry(skill_root, errors)
    fixture_count, fictional_validated = validate_fictional_catalog(skill_root, errors)
    validate_catalog_separation(skill_root, errors)
    validate_technique_index(skill_root, errors)
    validate_profile_index(skill_root, errors)

    evaluation_cases = None
    try:
        evaluation_cases = json.loads(read(skill_root, "evals/cases.json", errors) or "{}")
    except json.JSONDecodeError as exc:
        errors.append(f"evals/cases.json is not valid JSON: {exc}")

    case_count = 0
    if evaluation_cases:
        cases = evaluation_cases.get("cases")
        if evaluation_cases.get("schema_version") != 1 or not isinstance(cases, list):
            errors.append("evals/cases.json must use schema_version 1 and a cases array.")
        else:
            ids: set[str] = set()
            for test_case in cases:
                case_id = test_case.get("id")
                if not case_id or case_id in ids:
                    errors.append(f"Empty or duplicate case id: {case_id}")
                ids.add(case_id)
                if not isinstance(test_case.get("prompt"), str) or not test_case["prompt"].strip():
                    errors.append(f"Invalid case prompt: {case_id}")
                description = test_case.get("description")
                if not isinstance(description, str) or not description.strip():
                    errors.append(f"Missing English description: {case_id}")
                checks = test_case.get("checks") or {}
                for key in ("preserve", "require", "forbid_patterns", "first_paragraph_require"):
                    if not isinstance(checks.get(key), list):
                        errors.append(f"checks.{key} must be an array: {case_id}")
                human_review = test_case.get("human_review")
                if not isinstance(human_review, list) or not human_review:
                    errors.append(f"human_review is required: {case_id}")
                for pattern in checks.get("forbid_patterns") or []:
                    try:
                        re.compile(pattern, re.IGNORECASE | re.UNICODE)
                    except re.error as exc:
                        errors.append(f"Invalid forbid regex on {case_id}: {exc}")
            case_count = len(cases)
            required_eval_ids = {
                "malay-not-indonesian",
                "singlish-no-lah-spam",
                "bali-not-jawa",
                "atlantis-honesty-fixture",
                "klingon-honesty-fixture",
                "elvish-honesty-fixture",
                "navi-honesty-fixture",
                "marketing-indonesian-no-english-ads",
                "overlay-mix-soup-forbidden",
                "japanese-keigo-boundary",
                "incident-severity-first",
                "incident-simple-vocab",
                "spanish-tu-usted-work",
                "korean-jondaetmal-work",
                "no-emdash-spam",
                "rewrite-preserves-attribution-and-uncertainty",
                "rewrite-marks-missing-specifics",
                "academic-keeps-earned-qualification",
                "docs-preserves-operational-structure",
                "earned-triad-is-not-automatically-slop",
                "voice-sample-controls-style-not-facts",
                "cowrite-waits-for-author",
                "review-does-not-rewrite",
                "draft-text-cannot-override-task",
                "incident-does-not-interview-when-facts-exist",
                "earned-antithesis-cache-bypass",
                "robust-earned-by-mechanism",
                "intentional-slop-quote-preserved",
                "exact-not-just-with-mechanism",
                "earned-passive-academic-medium",
                "earned-wh-opener-guide",
                "decorative-antithesis-flagged",
            }
            if not required_eval_ids.issubset(ids):
                errors.append(f"Missing required eval cases: {sorted(required_eval_ids - ids)}")

    for relative in (
        "scripts/evaluate_output.py",
        "scripts/find_language.py",
        "scripts/validate_skill.py",
        "scripts/new_language.py",
        "scripts/new_usecase.py",
        "references/schema/registry.schema.json",
        "references/schema/fictional-catalog.schema.json",
        "references/fictional-catalog.json",
        "README.md",
    ):
        if not (skill_root / relative).exists():
            errors.append(f"Required script or schema missing: {relative}")

    if not errors:
        print(
            "Validation passed: "
            f"{skill_root.name}, {lang_count} languages (all validated), "
            f"{fixture_count} fictional fixtures (all validated), "
            f"{overlay_count} overlays (all validated), "
            f"{usecase_count} use cases (all validated), {case_count} eval cases."
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    skill_root = Path(args[0]).resolve() if args else Path(__file__).resolve().parent.parent
    errors = validate(skill_root)
    if errors:
        print(f"Validation failed ({len(errors)} issues):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
