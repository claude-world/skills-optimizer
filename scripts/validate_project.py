#!/usr/bin/env python3
"""Validate repository format, benchmark integrity, evidence, and docs drift."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).parents[1].resolve()
SKILL_DIR = ROOT / ".claude/skills/semantic-compressor"
CORE_PATH = SKILL_DIR / "scripts/semantic_compressor.py"
SPEC = importlib.util.spec_from_file_location("semantic_compressor_core", CORE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import {CORE_PATH}")
core = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = core
SPEC.loader.exec_module(core)

# Skill frontmatter fields documented for Claude Code 2.1.305
# (https://code.claude.com/docs/en/skills#frontmatter-reference).
CLAUDE_CODE_SKILL_FIELDS = {
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "background",
    "hooks",
    "paths",
    "shell",
    "metadata",
    "license",
    "compatibility",
}
# Limits from the Agent Skills specification (https://agentskills.io/specification).
SPEC_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SPEC_NAME_LIMIT = 64
SPEC_DESCRIPTION_LIMIT = 1024
# Claude Code reads these spellings as booleans since v2.1.218.
BOOLEAN_VALUES = {
    "true": True,
    "yes": True,
    "on": True,
    "1": True,
    "false": False,
    "no": False,
    "off": False,
    "0": False,
}


class Validation:
    def __init__(self, *, verbose: bool = False) -> None:
        self.errors: list[str] = []
        self.checks = 0
        self.verbose = verbose

    def require(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)
        elif self.verbose:
            print(f"ok: {message}")

    def extend(self, errors: Iterable[str], prefix: str) -> None:
        for error in errors:
            self.require(False, f"{prefix}: {error}")


def parse_frontmatter(path: Path, validation: Validation) -> dict[str, str]:
    try:
        frontmatter, _body = core.split_frontmatter(core.read_text(path))
    except core.CompressorError as exc:
        validation.require(False, f"{path.relative_to(ROOT)}: {exc}")
        return {}
    validation.require(
        frontmatter is not None,
        f"{path.relative_to(ROOT)} starts with YAML frontmatter",
    )
    if frontmatter is None:
        return {}
    try:
        return core.frontmatter_blocks(frontmatter)
    except core.CompressorError as exc:
        validation.require(False, f"{path.relative_to(ROOT)}: {exc}")
        return {}


def frontmatter_scalar(blocks: dict[str, str], key: str) -> str | None:
    block = blocks.get(key)
    return None if block is None else core.scalar_text(block)


def frontmatter_bool(blocks: dict[str, str], key: str) -> bool | None:
    value = frontmatter_scalar(blocks, key)
    return None if value is None else BOOLEAN_VALUES.get(value.strip().lower())


def metadata_value(blocks: dict[str, str], key: str) -> str | None:
    """Return one first-level string from the frontmatter ``metadata`` map."""
    lines = blocks.get("metadata", "").splitlines()[1:]
    indents = [len(line) - len(line.lstrip(" ")) for line in lines if line.strip()]
    for line in lines:
        match = re.fullmatch(r"( +)([A-Za-z0-9_.-]+):(.*)", line)
        if match and len(match.group(1)) == min(indents) and match.group(2) == key:
            return core.scalar_text(f"{key}:{match.group(3)}")
    return None


def validate_main_skill(validation: Validation) -> None:
    """Check the shipped skill against current Claude Code and spec rules."""
    skill_path = SKILL_DIR / "SKILL.md"
    main = parse_frontmatter(skill_path, validation)
    if not main:
        return
    name = frontmatter_scalar(main, "name")
    validation.require(name == SKILL_DIR.name, "main skill name matches its directory")
    validation.require(
        name is not None
        and len(name) <= SPEC_NAME_LIMIT
        and SPEC_NAME_RE.fullmatch(name) is not None,
        "main skill name follows the Agent Skills naming rule",
    )
    unknown = sorted(set(main) - CLAUDE_CODE_SKILL_FIELDS)
    validation.require(
        not unknown,
        "main skill uses only documented Claude Code frontmatter fields"
        + (f" (unknown: {', '.join(unknown)})" if unknown else ""),
    )
    description = (frontmatter_scalar(main, "description") or "").strip()
    validation.require(bool(description), "main skill has a description")
    validation.require(
        len(description) <= SPEC_DESCRIPTION_LIMIT,
        f"main skill description fits the {SPEC_DESCRIPTION_LIMIT:,}-character spec limit",
    )
    validation.require(
        "<" not in description and ">" not in description,
        "main skill description has no angle brackets",
    )
    skill_text = core.read_text(skill_path)
    validation.require(
        core.utf16_length(core.listing_entry(skill_text))
        <= core.SKILL_LISTING_CHARACTER_CAP,
        f"main skill listing fits Claude Code's {core.SKILL_LISTING_CHARACTER_CAP:,}-character cap",
    )
    validation.require(
        core.text_metrics(skill_text).lines < core.SKILL_LINE_LIMIT,
        f"SKILL.md stays under {core.SKILL_LINE_LIMIT} lines",
    )
    validation.require(
        frontmatter_bool(main, "disable-model-invocation") is True,
        "mutating skill disables model invocation",
    )
    validation.require(
        frontmatter_bool(main, "user-invocable") is True,
        "main skill remains user invocable",
    )
    validation.require("argument-hint" in main, "main skill declares argument-hint")
    validation.require(
        metadata_value(main, "version") == core.COMPRESSOR_VERSION,
        "SKILL.md metadata.version matches the control script version",
    )
    linked = set(markdown_links(skill_text))
    for reference in sorted((SKILL_DIR / "references").glob("*.md")):
        relative = reference.relative_to(SKILL_DIR).as_posix()
        validation.require(
            relative in linked, f"SKILL.md links {relative} directly"
        )


def validate_formats(validation: Validation) -> None:
    validate_main_skill(validation)

    samples = SKILL_DIR / "samples"
    pairs = core.sample_pairs(samples)
    validation.require(len(pairs) == 8, "exactly 8 sample pairs exist")
    for pair in pairs:
        original = samples / pair["original"]
        compressed = samples / pair["compressed"]
        original_fields = parse_frontmatter(original, validation)
        compressed_fields = parse_frontmatter(compressed, validation)
        validation.require(
            set(original_fields) == set(compressed_fields),
            f"{pair['id']} preserves all frontmatter keys",
        )
        validation.extend(
            core.validate_frontmatter(
                core.read_text(original), core.read_text(compressed)
            ),
            f"{pair['id']} frontmatter",
        )
        for required in ("name", "description"):
            validation.require(
                required in original_fields and required in compressed_fields,
                f"{pair['id']} has required {required} metadata",
            )
        if pair["kind"] == "agent":
            validation.require(
                "tools" in original_fields and "tools" in compressed_fields,
                f"{pair['id']} has operational tools metadata",
            )
        else:
            try:
                entry = core.utf16_length(core.listing_entry(core.read_text(compressed)))
            except core.CompressorError:
                entry = None
            validation.require(
                entry is not None and entry <= core.SKILL_LISTING_CHARACTER_CAP,
                f"{pair['id']} compressed listing fits Claude Code's "
                f"{core.SKILL_LISTING_CHARACTER_CAP:,}-character cap",
            )
        expected_name = pair["id"].split("/", 1)[1]
        validation.require(
            frontmatter_scalar(original_fields, "name") == expected_name,
            f"{pair['id']} frontmatter name matches filename",
        )


def load_json(path: Path, validation: Validation) -> Any:
    validation.require(path.is_file(), f"{path.relative_to(ROOT)} exists")
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        validation.require(
            False,
            f"{path.relative_to(ROOT)} is valid JSON ({exc.msg} at {exc.lineno}:{exc.colno})",
        )
        return None


def validate_cases(validation: Validation) -> None:
    samples = SKILL_DIR / "samples"
    verification_root = (samples / "verification").resolve()
    manifest_path = samples / "verification/cases.json"
    manifest = load_json(manifest_path, validation)
    if not isinstance(manifest, dict):
        return
    validation.require(
        manifest.get("schema_version") == core.SCHEMA_VERSION,
        "cases.json schema version is supported",
    )
    cases = manifest.get("cases")
    validation.require(isinstance(cases, list), "cases.json has a cases array")
    if not isinstance(cases, list):
        return
    validation.require(
        all(isinstance(case, dict) for case in cases),
        "every cases.json entry is an object",
    )

    expected_pairs = {pair["id"]: pair for pair in core.sample_pairs(samples)}
    actual_ids = [case.get("id") for case in cases if isinstance(case, dict)]
    validation.require(
        len(actual_ids) == len(set(actual_ids)), "cases.json ids are unique"
    )
    validation.require(
        set(actual_ids) == set(expected_pairs), "cases.json covers every sample pair exactly"
    )

    for case in cases:
        if not isinstance(case, dict) or case.get("id") not in expected_pairs:
            continue
        case_id = case["id"]
        pair = expected_pairs[case_id]
        original = samples / pair["original"]
        compressed = samples / pair["compressed"]
        validation.require(
            case.get("original_sha256") == core.sha256_file(original),
            f"{case_id} original hash matches cases.json",
        )
        validation.require(
            case.get("compressed_sha256") == core.sha256_file(compressed),
            f"{case_id} compressed hash matches cases.json",
        )
        inventory_reference = case.get("inventory")
        validation.require(
            isinstance(inventory_reference, str) and bool(inventory_reference),
            f"{case_id} names an inventory artifact",
        )
        inventory_path = (verification_root / str(inventory_reference)).resolve(
            strict=False
        )
        safe_inventory_path = (
            isinstance(inventory_reference, str)
            and core.is_canonical_relative_path(inventory_reference)
            and core.is_within(inventory_path, verification_root)
        )
        validation.require(
            safe_inventory_path,
            f"{case_id} inventory path stays inside sample verification artifacts",
        )
        if not safe_inventory_path:
            continue
        inventory = load_json(inventory_path, validation)
        if not isinstance(inventory, dict):
            continue
        validation.extend(
            core.validate_inventory(
                inventory, core.read_text(original), core.read_text(compressed)
            ),
            case_id,
        )
        forbidden = case.get("forbidden_literals")
        validation.require(
            isinstance(forbidden, list)
            and all(isinstance(item, str) and item for item in forbidden),
            f"{case_id} forbidden_literals is an explicit string array",
        )
        if isinstance(forbidden, list):
            candidate_text = core.read_text(compressed)
            for item in forbidden:
                validation.require(
                    item not in candidate_text,
                    f"{case_id} does not invent forbidden literal {item!r}",
                )
        minimum = case.get("min_word_ratio")
        word_ratio = pair["metrics"]["ratios"]["words"]
        rendered_ratio = "undefined" if word_ratio is None else f"{word_ratio:.3f}"
        validation.require(
            isinstance(minimum, (int, float))
            and not isinstance(minimum, bool)
            and math.isfinite(minimum)
            and minimum > 1
            and word_ratio is not None
            and word_ratio >= minimum,
            f"{case_id} word ratio {rendered_ratio} meets manifest minimum {minimum}",
        )

        review_path = samples / "verification/reviews" / f"{case_id.replace('/', '--')}.json"
        review = load_json(review_path, validation)
        if not isinstance(review, dict):
            continue
        validation.require(
            review.get("schema_version") == core.SCHEMA_VERSION,
            f"{case_id} semantic review schema is supported",
        )
        validation.require(review.get("id") == case_id, f"{case_id} review id matches")
        validation.extend(
            core.validate_semantic_review(
                review, original, compressed, inventory_path
            ),
            f"{case_id} semantic review",
        )


def validate_generated_benchmark(validation: Validation) -> None:
    samples = SKILL_DIR / "samples"
    payload = core.benchmark_payload(samples)
    expected_json = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    expected_markdown = core.benchmark_markdown(payload)
    results = ROOT / "benchmark-results.json"
    report = ROOT / "BENCHMARK-REPORT.md"
    validation.require(
        results.is_file() and results.read_text(encoding="utf-8") == expected_json,
        "benchmark-results.json is reproducible and current",
    )
    validation.require(
        report.is_file() and report.read_text(encoding="utf-8") == expected_markdown,
        "BENCHMARK-REPORT.md is reproducible and current",
    )


def markdown_links(text: str) -> Iterable[str]:
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        yield target


def validate_links(validation: Validation) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "semantic-compressor-workspace"} for part in path.parts):
            continue
        for target in markdown_links(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative or any(char in relative for char in ("<", ">", "*")):
                continue
            resolved = (path.parent / relative).resolve(strict=False)
            validation.require(
                core.is_within(resolved, ROOT) and resolved.exists(),
                f"{path.relative_to(ROOT)} link target exists: {target}",
            )


def validate_eval_suite(validation: Validation) -> None:
    eval_root = SKILL_DIR / "evals"
    evals = load_json(eval_root / "evals.json", validation)
    valid_suite = (
        isinstance(evals, dict)
        and isinstance(evals.get("evals"), list)
        and len(evals["evals"]) >= 3
    )
    validation.require(valid_suite, "eval suite contains at least 3 realistic cases")
    if not valid_suite:
        return

    entries = evals["evals"]
    validation.require(
        all(isinstance(entry, dict) for entry in entries),
        "every eval suite entry is an object",
    )
    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    names = [entry.get("name") for entry in entries if isinstance(entry, dict)]
    validation.require(len(ids) == len(set(ids)), "eval ids are unique")
    validation.require(len(names) == len(set(names)), "eval names are unique")
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        label = entry.get("name", entry.get("id", "unknown"))
        for field in ("id", "name", "prompt", "expected_output"):
            value = entry.get(field)
            validation.require(
                (isinstance(value, int) and not isinstance(value, bool))
                if field == "id"
                else isinstance(value, str) and bool(value.strip()),
                f"eval {label!r} has valid {field}",
            )
        expectations = entry.get("expectations")
        validation.require(
            isinstance(expectations, list)
            and bool(expectations)
            and all(isinstance(item, str) and item.strip() for item in expectations),
            f"eval {label!r} has explicit expectations",
        )
        files = entry.get("files")
        validation.require(
            isinstance(files, list)
            and bool(files)
            and all(isinstance(item, str) and item for item in files),
            f"eval {label!r} names fixture paths",
        )
        if not isinstance(files, list):
            continue
        for reference in files:
            if not isinstance(reference, str):
                continue
            fixture = (eval_root / reference).resolve(strict=False)
            validation.require(
                core.is_canonical_relative_path(reference)
                and core.is_within(fixture, eval_root)
                and fixture.exists(),
                f"eval {label!r} fixture exists inside evals: {reference}",
            )


def validate_docs_and_assets(validation: Validation) -> None:
    required = [
        ROOT / "README.md",
        ROOT / "README.zh-TW.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CHANGELOG.md",
        ROOT / "tests/test_semantic_compressor.py",
        SKILL_DIR / "references/inventory-schema.md",
        SKILL_DIR / "references/strategies.md",
        SKILL_DIR / "references/examples.md",
        SKILL_DIR / "evals/evals.json",
        ROOT / ".github/workflows/ci.yml",
    ]
    for path in required:
        validation.require(path.is_file(), f"{path.relative_to(ROOT)} exists")
    version = core.COMPRESSOR_VERSION
    for path in (ROOT / "README.md", ROOT / "README.zh-TW.md"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for stale in ("6.1:1", "84%", "100% semantic", "100% 語義"):
            validation.require(stale not in text, f"{path.name} removes stale claim {stale!r}")
        validation.require(
            "disable-model-invocation" in text,
            f"{path.name} documents manual-only invocation safety",
        )
        validation.require("restore" in text, f"{path.name} documents restoration")
        validation.require(
            f"`{version}`" in text, f"{path.name} names the current script version {version}"
        )
    changelog = ROOT / "CHANGELOG.md"
    validation.require(
        changelog.is_file() and f"## [{version}]" in changelog.read_text(encoding="utf-8"),
        f"CHANGELOG.md has a {version} entry",
    )
    contributing = ROOT / "CONTRIBUTING.md"
    validation.require(
        contributing.is_file() and f"v{version}" in contributing.read_text(encoding="utf-8"),
        f"CONTRIBUTING.md names the current release v{version}",
    )
    validate_eval_suite(validation)
    validate_links(validation)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format-only", action="store_true")
    parser.add_argument(
        "--skills-only",
        action="store_true",
        help="alias for format-only skill/frontmatter validation",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    validation = Validation(verbose=args.verbose)
    validate_formats(validation)
    if not (args.format_only or args.skills_only):
        validate_cases(validation)
        validate_generated_benchmark(validation)
        validate_docs_and_assets(validation)

    if validation.errors:
        print(
            f"FAILED: {len(validation.errors)} error(s) across {validation.checks} checks",
            file=sys.stderr,
        )
        for error in validation.errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"PASS: {validation.checks} checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
