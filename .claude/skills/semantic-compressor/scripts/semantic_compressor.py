#!/usr/bin/env python3
"""Deterministic safety controls for the semantic-compressor skill.

The language model still writes and semantically reviews candidates.  This
module owns the parts that should not depend on model judgment: discovery,
path validation, metadata preservation, literal checks, metrics, backups,
atomic replacement, rollback, and reproducible sample reports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


SCHEMA_VERSION = 1
COMPRESSOR_VERSION = "2.0.0"
MARKER = "<!-- semantic-compressor: v2"
MARKER_RE = re.compile(
    r"^<!-- semantic-compressor: v2; source-sha256=([0-9a-f]{64}); "
    r"compressed-at=([^;]+); run-id=([A-Za-z0-9_.-]+) -->$",
    re.MULTILINE,
)
IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    "backups",
    "semantic-compressor-work",
    "semantic-compressor-workspace",
}
INVENTORY_CATEGORIES = (
    "triggers",
    "commands",
    "tools",
    "formats",
    "paths",
    "numbers",
    "error_messages",
    "security_rules",
)
MUTABLE_FRONTMATTER_KEYS = {"description", "when_to_use"}
HASH_RE = re.compile(r"[0-9a-f]{64}")
RUN_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s?(.*))?$")


class CompressorError(RuntimeError):
    """A user-facing, fail-closed validation error."""


@dataclass(frozen=True)
class TextMetrics:
    lines: int
    words: int
    characters: int
    bytes: int

    def as_dict(self) -> dict[str, int]:
        return {
            "lines": self.lines,
            "words": self.words,
            "characters": self.characters,
            "bytes": self.bytes,
        }


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def decode_utf8(data: bytes, path: Path) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CompressorError(f"file is not valid UTF-8: {path}") from exc


def load_json_bytes(data: bytes, path: Path) -> Any:
    try:
        return json.loads(decode_utf8(data, path))
    except json.JSONDecodeError as exc:
        raise CompressorError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def create_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{os.getpid()}-{os.urandom(3).hex()}"


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))


def resolve_root(value: str | os.PathLike[str]) -> Path:
    root = Path(value).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise CompressorError(f"project root is not a directory: {root}")
    return root


def is_within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def lexical_absolute(path: Path) -> Path:
    """Return an absolute normalized path without resolving symbolic links."""

    return Path(os.path.abspath(os.fspath(path)))


def reject_symlink_components(path: Path, root: Path) -> None:
    """Fail if an existing component below root is a symbolic link."""

    lexical_root = lexical_absolute(root)
    lexical_path = lexical_absolute(path)
    if not is_within(lexical_path, lexical_root):
        raise CompressorError(f"path escapes project root: {path}")
    current = lexical_root
    for part in lexical_path.relative_to(lexical_root).parts:
        current /= part
        if current.is_symlink():
            raise CompressorError(f"symbolic links are not supported: {current}")


def resolve_project_output(value: str | os.PathLike[str], root: Path) -> Path:
    raw = Path(value).expanduser()
    candidate = raw if raw.is_absolute() else root / raw
    lexical = lexical_absolute(candidate)
    reject_symlink_components(lexical, root)
    resolved = lexical.resolve(strict=False)
    if not is_within(resolved, root):
        raise CompressorError(f"output path escapes project root: {candidate}")
    if resolved.exists() and not resolved.is_file():
        raise CompressorError(f"output path is not a regular file: {candidate}")
    return resolved


def resolve_project_file(
    value: str | os.PathLike[str],
    root: Path,
    *,
    must_exist: bool = True,
    markdown_only: bool = True,
) -> Path:
    raw = Path(value).expanduser()
    candidate = raw if raw.is_absolute() else root / raw
    lexical = lexical_absolute(candidate)
    reject_symlink_components(lexical, root)
    try:
        resolved = lexical.resolve(strict=must_exist)
    except FileNotFoundError as exc:
        raise CompressorError(f"file does not exist: {candidate}") from exc
    if not is_within(resolved, root):
        raise CompressorError(f"path escapes project root: {candidate}")
    if must_exist and not resolved.is_file():
        raise CompressorError(f"path is not a regular file: {candidate}")
    if markdown_only and resolved.suffix.lower() != ".md":
        raise CompressorError(f"expected a Markdown file: {candidate}")
    return resolved


def is_canonical_relative_path(value: Any) -> bool:
    """Return whether a manifest path has one unambiguous project-relative form."""

    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return (
        not path.is_absolute()
        and path.as_posix() == value
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    return decode_utf8(path.read_bytes(), path)


def text_metrics(text: str) -> TextMetrics:
    return TextMetrics(
        lines=len(text.splitlines()),
        words=len(re.findall(r"\S+", text)),
        characters=len(text),
        bytes=len(text.encode("utf-8")),
    )


def ratio(original: int, candidate: int) -> float | None:
    if candidate == 0:
        return None
    return original / candidate


def metrics_from_texts(
    original_text: str,
    candidate_text: str,
    *,
    original_path: str,
    candidate_path: str,
) -> dict[str, Any]:
    original = text_metrics(original_text)
    candidate = text_metrics(candidate_text)
    return {
        "schema_version": SCHEMA_VERSION,
        "original": {"path": original_path, **original.as_dict()},
        "candidate": {"path": candidate_path, **candidate.as_dict()},
        "ratios": {
            "lines": ratio(original.lines, candidate.lines),
            "words": ratio(original.words, candidate.words),
            "characters": ratio(original.characters, candidate.characters),
            "bytes": ratio(original.bytes, candidate.bytes),
        },
    }


def metrics_payload(original_path: Path, candidate_path: Path) -> dict[str, Any]:
    return metrics_from_texts(
        read_text(original_path),
        read_text(candidate_path),
        original_path=str(original_path),
        candidate_path=str(candidate_path),
    )


def split_frontmatter(text: str) -> tuple[str | None, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    raise CompressorError("frontmatter opens with '---' but has no closing delimiter")


def flow_syntax_error(value: str) -> str | None:
    """Check quotes and flow-collection delimiters in the supported YAML subset."""

    stack: list[str] = []
    quote: str | None = None
    escaped = False
    pairs = {"]": "[", "}": "{"}
    for index, character in enumerate(value):
        if quote == '"' and escaped:
            escaped = False
            continue
        if quote == '"' and character == "\\":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = None
            continue
        if character in ('"', "'"):
            previous = value[index - 1] if index else " "
            if previous.isspace() or previous in ":,=[{-":
                quote = character
        elif character in "[{":
            stack.append(character)
        elif character in "]}":
            if not stack or stack.pop() != pairs[character]:
                return f"unmatched {character!r}"
    if quote:
        return "unterminated quoted scalar"
    if stack:
        return f"unterminated flow collection {stack[-1]!r}"
    return None


def frontmatter_syntax_errors(frontmatter: str) -> list[str]:
    """Validate a conservative, dependency-free YAML frontmatter subset.

    Claude metadata is a top-level mapping. Nested mappings/lists and block
    scalars are accepted, while malformed top-level lines, tabs, and unclosed
    quotes/flow collections fail closed.
    """

    errors: list[str] = []
    lines = frontmatter.splitlines()
    active_key: str | None = None
    active_is_block = False
    flow_fragments: list[str] = []

    def finish_flow() -> None:
        if not flow_fragments:
            return
        error = flow_syntax_error("\n".join(flow_fragments))
        if error:
            errors.append(f"frontmatter key {active_key!r}: {error}")
        flow_fragments.clear()

    for number, line in enumerate(lines, 1):
        if "\t" in line:
            errors.append(f"frontmatter line {number} contains a tab")
        if not line.strip() or line.lstrip().startswith("#"):
            if active_key and not active_is_block:
                flow_fragments.append(line)
            continue
        if line == line.lstrip(" "):
            finish_flow()
            match = FRONTMATTER_KEY_RE.fullmatch(line)
            if not match:
                errors.append(
                    f"frontmatter line {number} is not a top-level key/value"
                )
                active_key = None
                active_is_block = False
                continue
            active_key = match.group(1)
            value = (match.group(2) or "").strip()
            active_is_block = bool(re.fullmatch(r"[|>][+-]?[1-9]?", value))
            if active_key in MUTABLE_FRONTMATTER_KEYS:
                if not value:
                    errors.append(
                        f"frontmatter field {active_key} must be a scalar or block scalar"
                    )
                elif value.startswith(("[", "{")):
                    errors.append(f"frontmatter field {active_key} must be text")
            if not active_is_block:
                flow_fragments.append(value)
            continue
        if active_key is None:
            errors.append(f"frontmatter line {number} has no parent key")
        elif not active_is_block:
            flow_fragments.append(line.strip())
    finish_flow()
    return errors


def frontmatter_blocks(frontmatter: str) -> dict[str, str]:
    lines = frontmatter.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            starts.append((index, match.group(1)))
    blocks: dict[str, str] = {}
    for position, (start, key) in enumerate(starts):
        if key in blocks:
            raise CompressorError(f"duplicate top-level frontmatter key: {key}")
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        blocks[key] = "\n".join(lines[start:end]).rstrip()
    return blocks


def normalized_block(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines())


def validate_frontmatter(original_text: str, candidate_text: str) -> list[str]:
    errors: list[str] = []
    try:
        original_frontmatter, _ = split_frontmatter(original_text)
        candidate_frontmatter, _ = split_frontmatter(candidate_text)
    except CompressorError as exc:
        return [str(exc)]

    if (original_frontmatter is None) != (candidate_frontmatter is None):
        return ["frontmatter presence changed"]
    if original_frontmatter is None:
        return errors

    errors.extend(
        f"original {error}" for error in frontmatter_syntax_errors(original_frontmatter)
    )
    errors.extend(
        f"candidate {error}"
        for error in frontmatter_syntax_errors(candidate_frontmatter or "")
    )
    if errors:
        return errors

    try:
        original_blocks = frontmatter_blocks(original_frontmatter)
        candidate_blocks = frontmatter_blocks(candidate_frontmatter or "")
    except CompressorError as exc:
        return [str(exc)]

    if not original_blocks:
        errors.append("original frontmatter has no top-level keys")
        return errors
    if set(original_blocks) != set(candidate_blocks):
        missing = sorted(set(original_blocks) - set(candidate_blocks))
        added = sorted(set(candidate_blocks) - set(original_blocks))
        if missing:
            errors.append(f"frontmatter keys removed: {', '.join(missing)}")
        if added:
            errors.append(f"frontmatter keys added: {', '.join(added)}")

    for key in sorted(set(original_blocks) & set(candidate_blocks)):
        if key in MUTABLE_FRONTMATTER_KEYS:
            continue
        if normalized_block(original_blocks[key]) != normalized_block(
            candidate_blocks[key]
        ):
            errors.append(f"frontmatter field changed: {key}")
    return errors


def load_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise CompressorError(
            f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def validate_inventory_shape(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["inventory must be a JSON object"]
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"inventory schema_version must be {SCHEMA_VERSION}")
    if value.get("status") != "complete":
        errors.append("inventory status must be complete")
    source_hash = value.get("source_sha256")
    if not isinstance(source_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", source_hash):
        errors.append("inventory source_sha256 must be a lowercase SHA-256")
    literals = value.get("literals")
    if not isinstance(literals, dict):
        errors.append("inventory literals must be an object")
    else:
        extra = sorted(set(literals) - set(INVENTORY_CATEGORIES))
        missing = sorted(set(INVENTORY_CATEGORIES) - set(literals))
        if extra:
            errors.append(f"unknown inventory categories: {', '.join(extra)}")
        if missing:
            errors.append(f"missing inventory categories: {', '.join(missing)}")
        for category in INVENTORY_CATEGORIES:
            items = literals.get(category)
            if not isinstance(items, list) or any(
                not isinstance(item, str) or not item for item in items
            ):
                errors.append(f"literals.{category} must be an array of non-empty strings")
            elif len(items) != len(set(items)):
                errors.append(f"literals.{category} contains duplicates")
    attestations = value.get("category_attestations")
    if not isinstance(attestations, dict):
        errors.append("inventory category_attestations must be an object")
    else:
        extra = sorted(set(attestations) - set(INVENTORY_CATEGORIES))
        missing = sorted(set(INVENTORY_CATEGORIES) - set(attestations))
        if extra:
            errors.append(f"unknown category attestations: {', '.join(extra)}")
        if missing:
            errors.append(f"missing category attestations: {', '.join(missing)}")
        for category in INVENTORY_CATEGORIES:
            if attestations.get(category) is not True:
                errors.append(f"category_attestations.{category} must be true")
    concepts = value.get("concepts")
    if not isinstance(concepts, list):
        errors.append("inventory concepts must be an array")
    else:
        if not concepts:
            errors.append("inventory concepts must contain at least one reviewed concept")
        ids: set[str] = set()
        for item in concepts:
            if not isinstance(item, dict):
                errors.append("each concept must be an object")
                continue
            concept_id = item.get("id")
            description = item.get("description")
            if not isinstance(concept_id, str) or not re.fullmatch(
                r"[a-z0-9][a-z0-9-]*", concept_id
            ):
                errors.append("concept id must be unique kebab-case")
            elif concept_id in ids:
                errors.append(f"duplicate concept id: {concept_id}")
            else:
                ids.add(concept_id)
            if not isinstance(description, str) or not description.strip():
                errors.append(f"concept {concept_id!r} has no description")
    return errors


def validate_inventory(
    inventory: dict[str, Any], original_text: str, candidate_text: str
) -> list[str]:
    errors = validate_inventory_shape(inventory)
    if errors:
        return errors
    actual_hash = sha256_bytes(original_text.encode("utf-8"))
    if inventory["source_sha256"] != actual_hash:
        errors.append("inventory source_sha256 does not match original")
    for category in INVENTORY_CATEGORIES:
        for literal in inventory["literals"][category]:
            if literal not in original_text:
                errors.append(f"inventory literal absent from original ({category}): {literal!r}")
            if literal not in candidate_text:
                errors.append(f"required literal missing from candidate ({category}): {literal!r}")
    return errors


def inventory_template(original_path: Path) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "draft",
        "source_sha256": sha256_file(original_path),
        "literals": {category: [] for category in INVENTORY_CATEGORIES},
        "category_attestations": {
            category: False for category in INVENTORY_CATEGORIES
        },
        "concepts": [],
    }


def validate_semantic_review(
    value: Any,
    original_path: Path,
    candidate_path: Path,
    inventory_path: Path,
    *,
    original_sha256: str | None = None,
    candidate_sha256: str | None = None,
    inventory_sha256: str | None = None,
    inventory_value: dict[str, Any] | None = None,
    original_text: str | None = None,
    candidate_text: str | None = None,
) -> list[str]:
    if not isinstance(value, dict):
        return ["semantic review must be a JSON object"]
    errors: list[str] = []
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"semantic review schema_version must be {SCHEMA_VERSION}")
    if value.get("verdict") != "PASS":
        errors.append("semantic review verdict must be PASS")
    expected_original = original_sha256 or sha256_file(original_path)
    expected_candidate = candidate_sha256 or sha256_file(candidate_path)
    expected_inventory = inventory_sha256 or sha256_file(inventory_path)
    reviewed_original_text = original_text if original_text is not None else read_text(original_path)
    reviewed_candidate_text = (
        candidate_text if candidate_text is not None else read_text(candidate_path)
    )
    if value.get("original_sha256") != expected_original:
        errors.append("semantic review original_sha256 does not match source")
    if value.get("candidate_sha256") != expected_candidate:
        errors.append("semantic review candidate_sha256 does not match candidate")
    if value.get("inventory_sha256") != expected_inventory:
        errors.append("semantic review inventory_sha256 does not match inventory")
    for field in ("missing_concepts", "altered_meanings", "unsupported_additions"):
        if value.get(field) != []:
            errors.append(f"semantic review {field} must be an empty array")
    evidence = value.get("evidence")
    if not isinstance(evidence, list) or not evidence or any(
        not isinstance(item, str) or not item.strip() for item in evidence
    ):
        errors.append("semantic review evidence must be a non-empty string array")
    reviewer = value.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        errors.append("semantic review must identify the reviewer")
    if value.get("reviewer_mode") != "independent-read-only":
        errors.append("semantic review reviewer_mode must be independent-read-only")
    if inventory_value is None:
        loaded_inventory = load_json(inventory_path)
        inventory_value = loaded_inventory if isinstance(loaded_inventory, dict) else {}
    concept_ids = {
        item.get("id")
        for item in inventory_value.get("concepts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    concept_evidence = value.get("concept_evidence")
    if not isinstance(concept_evidence, list):
        errors.append("semantic review concept_evidence must be an array")
    else:
        reviewed_ids: list[str] = []
        for item in concept_evidence:
            if not isinstance(item, dict):
                errors.append("semantic review concept evidence entry must be an object")
                continue
            concept_id = item.get("concept_id")
            source = item.get("source")
            candidate = item.get("candidate")
            if not isinstance(concept_id, str):
                errors.append("semantic review concept evidence has no concept_id")
                continue
            reviewed_ids.append(concept_id)
            if not isinstance(source, str) or not source.strip():
                errors.append(f"semantic review concept {concept_id!r} has no source evidence")
            elif source not in reviewed_original_text:
                errors.append(
                    f"semantic review concept {concept_id!r} source evidence is not in source"
                )
            if not isinstance(candidate, str) or not candidate.strip():
                errors.append(
                    f"semantic review concept {concept_id!r} has no candidate evidence"
                )
            elif candidate not in reviewed_candidate_text:
                errors.append(
                    f"semantic review concept {concept_id!r} candidate evidence is not in candidate"
                )
        if len(reviewed_ids) != len(set(reviewed_ids)):
            errors.append("semantic review concept_evidence contains duplicate ids")
        if set(reviewed_ids) != concept_ids:
            errors.append("semantic review concept_evidence does not cover inventory concepts")
    return errors


def validate_candidate_texts(
    original_text: str,
    candidate_text: str,
    inventory_value: Any,
    *,
    original_path: Path,
    candidate_path: Path,
    min_word_ratio: float,
) -> dict[str, Any]:
    errors: list[str] = []
    valid_minimum = (
        isinstance(min_word_ratio, (int, float))
        and not isinstance(min_word_ratio, bool)
        and math.isfinite(min_word_ratio)
        and min_word_ratio > 1
    )
    if not valid_minimum:
        errors.append("minimum word compression ratio must be finite and greater than 1")
    if original_path == candidate_path:
        errors.append("candidate must not be the original file")
    if not candidate_text.strip():
        errors.append("candidate is empty")
    if MARKER_RE.search(original_text):
        errors.append("original already contains a valid semantic-compressor marker")
    if MARKER_RE.search(candidate_text):
        errors.append("candidate already contains a semantic-compressor marker")
    errors.extend(validate_frontmatter(original_text, candidate_text))

    if isinstance(inventory_value, dict):
        errors.extend(validate_inventory(inventory_value, original_text, candidate_text))
    else:
        errors.extend(validate_inventory_shape(inventory_value))

    metrics = metrics_from_texts(
        original_text,
        candidate_text,
        original_path=str(original_path),
        candidate_path=str(candidate_path),
    )
    word_ratio = metrics["ratios"]["words"]
    if valid_minimum and (word_ratio is None or word_ratio < min_word_ratio):
        rendered = "undefined" if word_ratio is None else f"{word_ratio:.3f}"
        errors.append(
            f"word compression ratio {rendered} is below minimum {min_word_ratio:.3f}"
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "metrics": metrics,
        "source_sha256": sha256_bytes(original_text.encode("utf-8")),
        "candidate_sha256": sha256_bytes(candidate_text.encode("utf-8")),
    }


def validate_candidate(
    original_path: Path,
    candidate_path: Path,
    inventory_path: Path,
    *,
    min_word_ratio: float,
) -> dict[str, Any]:
    return validate_candidate_texts(
        read_text(original_path),
        read_text(candidate_path),
        load_json(inventory_path),
        original_path=original_path,
        candidate_path=candidate_path,
        min_word_ratio=min_word_ratio,
    )


def should_prune(path: Path, root: Path) -> bool:
    if path == root:
        return False
    return path.name in IGNORED_DIRECTORY_NAMES


def discover_candidates(
    root: Path, *, exclude: Sequence[Path], include_compressed: bool
) -> dict[str, Any]:
    excluded = [path.resolve(strict=False) for path in exclude]
    candidates: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []

    for current, dirnames, _filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirnames[:] = sorted(
            name
            for name in dirnames
            if not should_prune(current_path / name, root)
            and not (current_path / name).is_symlink()
        )
        if current_path.name != ".claude":
            continue

        skills_dir = current_path / "skills"
        if skills_dir.is_dir() and not skills_dir.is_symlink():
            for skill_dir in sorted(skills_dir.iterdir(), key=lambda item: item.name):
                entrypoint = skill_dir / "SKILL.md"
                if (
                    not skill_dir.is_dir()
                    or skill_dir.is_symlink()
                    or not entrypoint.is_file()
                    or entrypoint.is_symlink()
                ):
                    continue
                resolved = entrypoint.resolve()
                if not is_within(resolved, skill_dir.resolve()) or not is_within(
                    resolved, root
                ):
                    skipped.append(
                        {
                            "path": lexical_absolute(entrypoint).relative_to(root).as_posix(),
                            "reason": "unsafe-path",
                        }
                    )
                    continue
                if any(is_within(resolved, item) for item in excluded):
                    skipped.append(
                        {"path": relative_posix(resolved, root), "reason": "self/excluded"}
                    )
                    continue
                text = read_text(resolved)
                if not include_compressed and MARKER_RE.search(text):
                    skipped.append(
                        {"path": relative_posix(resolved, root), "reason": "already-compressed"}
                    )
                    continue
                candidates.append(
                    {"path": relative_posix(resolved, root), "kind": "skill"}
                )

        agents_dir = current_path / "agents"
        if agents_dir.is_dir() and not agents_dir.is_symlink():
            for entrypoint in sorted(agents_dir.rglob("*.md")):
                if not entrypoint.is_file() or entrypoint.is_symlink():
                    continue
                resolved = entrypoint.resolve()
                if any(part in IGNORED_DIRECTORY_NAMES for part in resolved.parts):
                    continue
                if any(is_within(resolved, item) for item in excluded):
                    skipped.append(
                        {"path": relative_posix(resolved, root), "reason": "self/excluded"}
                    )
                    continue
                text = read_text(resolved)
                if not include_compressed and MARKER_RE.search(text):
                    skipped.append(
                        {"path": relative_posix(resolved, root), "reason": "already-compressed"}
                    )
                    continue
                candidates.append(
                    {"path": relative_posix(resolved, root), "kind": "agent"}
                )

        # Do not descend inside a .claude directory after processing its known roots.
        dirnames[:] = [name for name in dirnames if name not in {"skills", "agents"}]

    candidates.sort(key=lambda item: (item["path"], item["kind"]))
    skipped.sort(key=lambda item: (item["path"], item["reason"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "candidates": candidates,
        "skipped": skipped,
    }


def insert_marker(candidate_text: str, marker: str) -> str:
    lines = candidate_text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return f"{marker}\n{candidate_text}"
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        raise CompressorError("frontmatter opens with '---' but has no closing delimiter")
    prefix = "".join(lines[: closing + 1])
    body = "".join(lines[closing + 1 :])
    separator = "" if prefix.endswith(("\n", "\r")) else "\n"
    return f"{prefix}{separator}{marker}\n{body}"


def fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_exclusive(path: Path, data: bytes, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600 if mode is None else mode)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        fsync_directory(path.parent)
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def atomic_replace(path: Path, data: bytes, mode: int) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp, stat.S_IMODE(mode))
        os.replace(temp, path)
        fsync_directory(path.parent)
    finally:
        temp.unlink(missing_ok=True)


def apply_candidate(
    root: Path,
    original_path: Path,
    candidate_path: Path,
    inventory_path: Path,
    semantic_review_path: Path,
    *,
    min_word_ratio: float,
    run_id: str | None = None,
) -> dict[str, Any]:
    original_path = resolve_project_file(original_path, root)
    candidate_path = resolve_project_file(candidate_path, root)
    inventory_path = resolve_project_file(inventory_path, root, markdown_only=False)
    semantic_review_path = resolve_project_file(
        semantic_review_path, root, markdown_only=False
    )
    original_mode = stat.S_IMODE(original_path.stat().st_mode)
    original_bytes = original_path.read_bytes()
    candidate_bytes = candidate_path.read_bytes()
    inventory_bytes = inventory_path.read_bytes()
    semantic_review_bytes = semantic_review_path.read_bytes()
    original_text = decode_utf8(original_bytes, original_path)
    candidate_text = decode_utf8(candidate_bytes, candidate_path)
    inventory_value = load_json_bytes(inventory_bytes, inventory_path)
    semantic_review = load_json_bytes(semantic_review_bytes, semantic_review_path)

    validation = validate_candidate_texts(
        original_text,
        candidate_text,
        inventory_value,
        original_path=original_path,
        candidate_path=candidate_path,
        min_word_ratio=min_word_ratio,
    )
    if validation["status"] != "PASS":
        raise CompressorError(
            "candidate validation failed; original was not changed:\n- "
            + "\n- ".join(validation["errors"])
        )
    review_errors = validate_semantic_review(
        semantic_review,
        original_path,
        candidate_path,
        inventory_path,
        original_sha256=sha256_bytes(original_bytes),
        candidate_sha256=sha256_bytes(candidate_bytes),
        inventory_sha256=sha256_bytes(inventory_bytes),
        inventory_value=inventory_value if isinstance(inventory_value, dict) else {},
        original_text=original_text,
        candidate_text=candidate_text,
    )
    if review_errors:
        raise CompressorError(
            "semantic review validation failed; original was not changed:\n- "
            + "\n- ".join(review_errors)
        )

    run = run_id or create_run_id()
    if not RUN_ID_RE.fullmatch(run) or run in {".", ".."}:
        raise CompressorError(
            "run id must start with a letter or number, contain at most 128 "
            "letters/numbers/dots/underscores/hyphens, and not be dot segments"
        )
    relative = original_path.relative_to(root)
    backup_base = root / ".claude" / "backups"
    reject_symlink_components(backup_base, root)
    backup_root = backup_base / run
    if not is_within(lexical_absolute(backup_root), lexical_absolute(backup_base)):
        raise CompressorError("backup run path escapes the backup directory")
    backup_path = backup_root / "files" / relative
    manifest_path = backup_root / "manifest.json"
    if backup_root.exists():
        raise CompressorError(f"backup run already exists: {backup_root}")

    compressed_at = utc_now()
    marker = (
        f"<!-- semantic-compressor: v2; source-sha256={sha256_bytes(original_bytes)}; "
        f"compressed-at={compressed_at}; run-id={run} -->"
    )
    final_text = insert_marker(candidate_text, marker)
    final_bytes = final_text.encode("utf-8")
    final_errors = validate_frontmatter(original_text, final_text)
    if isinstance(inventory_value, dict):
        final_errors.extend(validate_inventory(inventory_value, original_text, final_text))
    marker_matches = list(MARKER_RE.finditer(final_text))
    if len(marker_matches) != 1 or marker_matches[0].group(1) != sha256_bytes(original_bytes):
        final_errors.append("final output does not contain exactly one source-bound marker")
    final_metrics = metrics_from_texts(
        original_text,
        final_text,
        original_path=str(original_path),
        candidate_path=str(original_path),
    )
    if final_errors:
        raise CompressorError(
            "final marked output validation failed; original was not changed:\n- "
            + "\n- ".join(final_errors)
        )

    source_replaced = False
    try:
        write_exclusive(backup_path, original_bytes, original_mode)
        if sha256_file(backup_path) != sha256_bytes(original_bytes):
            raise CompressorError("backup checksum verification failed")
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "compressor_version": COMPRESSOR_VERSION,
            "run_id": run,
            "created_at": compressed_at,
            "root": str(root),
            "status": "prepared",
            "files": [
                {
                    "path": relative.as_posix(),
                    "backup": backup_path.relative_to(root).as_posix(),
                    "before_sha256": sha256_bytes(original_bytes),
                    "candidate_sha256": validation["candidate_sha256"],
                    "after_sha256": sha256_bytes(final_bytes),
                    "mode": original_mode,
                }
            ],
            "inventory": {
                "path": inventory_path.relative_to(root).as_posix(),
                "sha256": sha256_bytes(inventory_bytes),
            },
            "semantic_review": {
                "path": semantic_review_path.relative_to(root).as_posix(),
                "sha256": sha256_bytes(semantic_review_bytes),
                "reviewer": semantic_review["reviewer"],
            },
        }
        write_exclusive(
            manifest_path,
            (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
        if sha256_file(original_path) != sha256_bytes(original_bytes) or stat.S_IMODE(
            original_path.stat().st_mode
        ) != original_mode:
            raise CompressorError(
                "source changed after validation; refusing to overwrite concurrent edits"
            )
        atomic_replace(original_path, final_bytes, original_mode)
        source_replaced = True
        if sha256_file(original_path) != sha256_bytes(final_bytes):
            raise CompressorError("post-write checksum failed")
        manifest["status"] = "applied"
        atomic_replace(
            manifest_path,
            (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            stat.S_IMODE(manifest_path.stat().st_mode),
        )
    except BaseException as exc:
        if source_replaced and original_path.exists():
            current_hash = sha256_file(original_path)
            if current_hash == sha256_bytes(final_bytes):
                atomic_replace(original_path, original_bytes, original_mode)
            elif current_hash != sha256_bytes(original_bytes):
                raise CompressorError(
                    "apply failed after replacement, but the source changed concurrently; "
                    "unknown bytes were not overwritten"
                ) from exc
        raise

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "APPLIED",
        "path": relative.as_posix(),
        "run_id": run,
        "backup": backup_path.relative_to(root).as_posix(),
        "manifest": manifest_path.relative_to(root).as_posix(),
        "before_sha256": sha256_bytes(original_bytes),
        "after_sha256": sha256_bytes(final_bytes),
        "validation": validation,
        "semantic_review": {
            "path": semantic_review_path.relative_to(root).as_posix(),
            "sha256": sha256_bytes(semantic_review_bytes),
            "reviewer": semantic_review["reviewer"],
        },
        "final_metrics": final_metrics,
    }


def restore_backup(root: Path, manifest_path: Path, *, apply: bool) -> dict[str, Any]:
    manifest_path = resolve_project_file(manifest_path, root, markdown_only=False)
    manifest_bytes = manifest_path.read_bytes()
    manifest_value = load_json_bytes(manifest_bytes, manifest_path)
    if not isinstance(manifest_value, dict):
        raise CompressorError("unsupported backup manifest")
    backup_base = root / ".claude" / "backups"
    reject_symlink_components(backup_base, root)
    try:
        manifest_relative = manifest_path.relative_to(root)
    except ValueError as exc:
        raise CompressorError("backup manifest is outside the project") from exc
    parts = manifest_relative.parts
    if (
        len(parts) != 4
        or parts[:2] != (".claude", "backups")
        or parts[3] != "manifest.json"
    ):
        raise CompressorError(
            "backup manifest must be .claude/backups/<run-id>/manifest.json"
        )
    run = parts[2]
    if not RUN_ID_RE.fullmatch(run) or run in {".", ".."}:
        raise CompressorError("backup manifest has an invalid run id")
    if manifest_value.get("schema_version") != SCHEMA_VERSION:
        raise CompressorError("unsupported backup manifest schema")
    if manifest_value.get("compressor_version") != COMPRESSOR_VERSION:
        raise CompressorError("backup manifest compressor version does not match")
    if manifest_value.get("run_id") != run:
        raise CompressorError("backup manifest run id does not match its directory")
    if manifest_value.get("root") != str(root):
        raise CompressorError("backup manifest project root does not match")
    if manifest_value.get("status") != "applied":
        raise CompressorError("backup manifest status must be applied")
    required_manifest_fields = {
        "schema_version",
        "compressor_version",
        "run_id",
        "created_at",
        "root",
        "status",
        "files",
        "inventory",
        "semantic_review",
    }
    if set(manifest_value) != required_manifest_fields:
        raise CompressorError("backup manifest has unexpected top-level fields")
    if not isinstance(manifest_value.get("created_at"), str) or not manifest_value[
        "created_at"
    ]:
        raise CompressorError("backup manifest created_at is invalid")
    for field in ("inventory", "semantic_review"):
        metadata = manifest_value.get(field)
        required = {"path", "sha256"} | ({"reviewer"} if field == "semantic_review" else set())
        if not isinstance(metadata, dict) or set(metadata) != required:
            raise CompressorError(f"backup manifest {field} metadata is invalid")
        metadata_path = metadata.get("path")
        if (
            not is_canonical_relative_path(metadata_path)
        ):
            raise CompressorError(f"backup manifest {field} path is not canonical")
        if not isinstance(metadata.get("sha256"), str) or not HASH_RE.fullmatch(
            metadata["sha256"]
        ):
            raise CompressorError(f"backup manifest {field} hash is invalid")
        if field == "semantic_review" and (
            not isinstance(metadata.get("reviewer"), str) or not metadata["reviewer"].strip()
        ):
            raise CompressorError("backup manifest reviewer is invalid")
    files = manifest_value.get("files")
    if not isinstance(files, list) or len(files) != 1:
        raise CompressorError("backup manifest must contain exactly one file")

    operations: list[dict[str, Any]] = []
    for item in files:
        if not isinstance(item, dict):
            raise CompressorError("backup manifest file entry must be an object")
        required_fields = {
            "path",
            "backup",
            "before_sha256",
            "candidate_sha256",
            "after_sha256",
            "mode",
        }
        if set(item) != required_fields:
            raise CompressorError("backup manifest file entry has unexpected fields")
        target_value = item.get("path")
        backup_value = item.get("backup")
        if (
            not is_canonical_relative_path(target_value)
        ):
            raise CompressorError("backup manifest target path is not canonical")
        expected_backup_value = (
            Path(".claude") / "backups" / run / "files" / target_value
        ).as_posix()
        if backup_value != expected_backup_value:
            raise CompressorError("backup manifest backup path does not match target")
        for field in ("before_sha256", "candidate_sha256", "after_sha256"):
            if not isinstance(item.get(field), str) or not HASH_RE.fullmatch(item[field]):
                raise CompressorError(f"backup manifest {field} is not a SHA-256")
        stored_mode = item.get("mode")
        if not isinstance(stored_mode, int) or isinstance(stored_mode, bool) or not (
            0 <= stored_mode <= 0o7777
        ):
            raise CompressorError("backup manifest mode is invalid")
        target = resolve_project_file(target_value, root)
        backup = resolve_project_file(backup_value, root, markdown_only=False)
        expected_backup_hash = item.get("before_sha256")
        expected_current_hash = item.get("after_sha256")
        backup_bytes = backup.read_bytes()
        current_bytes = target.read_bytes()
        if sha256_bytes(backup_bytes) != expected_backup_hash:
            raise CompressorError(f"backup hash mismatch: {backup}")
        current_hash = sha256_bytes(current_bytes)
        if current_hash != expected_current_hash:
            raise CompressorError(
                f"refusing to overwrite a file changed after compression: {target}"
            )
        current_mode = stat.S_IMODE(target.stat().st_mode)
        if current_mode != stored_mode:
            raise CompressorError(
                f"refusing to overwrite a file whose mode changed after compression: {target}"
            )
        operations.append(
            {
                "path": relative_posix(target, root),
                "backup": relative_posix(backup, root),
                "current_sha256": current_hash,
                "restore_sha256": expected_backup_hash,
                "restore_mode": stored_mode,
                "current_mode": current_mode,
                "current_bytes": current_bytes,
                "backup_bytes": backup_bytes,
            }
        )

    if apply:
        operation = operations[0]
        target = root / operation["path"]
        backup = root / operation["backup"]
        restored_target = False
        try:
            if sha256_file(manifest_path) != sha256_bytes(manifest_bytes):
                raise CompressorError("backup manifest changed during restore")
            if sha256_file(target) != operation["current_sha256"] or stat.S_IMODE(
                target.stat().st_mode
            ) != operation["current_mode"]:
                raise CompressorError(
                    f"refusing to overwrite a file changed during restore: {target}"
                )
            if sha256_file(backup) != operation["restore_sha256"]:
                raise CompressorError(f"backup changed during restore: {backup}")
            atomic_replace(
                target, operation["backup_bytes"], operation["restore_mode"]
            )
            restored_target = True
            if sha256_file(target) != operation["restore_sha256"]:
                raise CompressorError(f"restore checksum failed: {target}")
            if stat.S_IMODE(target.stat().st_mode) != operation["restore_mode"]:
                raise CompressorError(f"restore mode verification failed: {target}")
            manifest_value["status"] = "restored"
            manifest_value["restored_at"] = utc_now()
            atomic_replace(
                manifest_path,
                (json.dumps(manifest_value, indent=2, sort_keys=True) + "\n").encode(
                    "utf-8"
                ),
                stat.S_IMODE(manifest_path.stat().st_mode),
            )
        except BaseException as exc:
            if restored_target and target.exists():
                current_hash = sha256_file(target)
                if current_hash == operation["restore_sha256"]:
                    atomic_replace(
                        target,
                        operation["current_bytes"],
                        operation["current_mode"],
                    )
                elif current_hash != operation["current_sha256"]:
                    raise CompressorError(
                        "restore failed after replacement, but the target changed "
                        "concurrently; unknown bytes were not overwritten"
                    ) from exc
            raise

    public_operations = [
        {key: value for key, value in operation.items() if not key.endswith("_bytes")}
        for operation in operations
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "RESTORED" if apply else "DRY_RUN",
        "manifest": relative_posix(manifest_path, root),
        "operations": public_operations,
    }


def sample_pairs(samples_dir: Path) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for kind in ("skills", "agents"):
        verbose_dir = samples_dir / kind / "verbose"
        compressed_dir = samples_dir / kind / "compressed"
        if not verbose_dir.is_dir() or not compressed_dir.is_dir():
            raise CompressorError(f"missing {kind} verbose/compressed sample directories")
        originals = {path.name: path for path in verbose_dir.glob("*.md")}
        compressed = {path.name: path for path in compressed_dir.glob("*.md")}
        if not originals:
            raise CompressorError(f"no {kind} sample pairs were found")
        if set(originals) != set(compressed):
            missing = sorted(set(originals) - set(compressed))
            orphaned = sorted(set(compressed) - set(originals))
            raise CompressorError(
                f"unpaired {kind} samples; missing={missing}, orphaned={orphaned}"
            )
        for name in sorted(originals):
            metrics = metrics_payload(originals[name], compressed[name])
            metrics["original"]["path"] = originals[name].relative_to(
                samples_dir
            ).as_posix()
            metrics["candidate"]["path"] = compressed[name].relative_to(
                samples_dir
            ).as_posix()
            pairs.append(
                {
                    "id": f"{kind}/{name.removesuffix('.md')}",
                    "kind": kind.removesuffix("s"),
                    "original": originals[name].relative_to(samples_dir).as_posix(),
                    "compressed": compressed[name].relative_to(samples_dir).as_posix(),
                    "original_sha256": sha256_file(originals[name]),
                    "compressed_sha256": sha256_file(compressed[name]),
                    "metrics": metrics,
                }
            )
    return pairs


def benchmark_payload(samples_dir: Path) -> dict[str, Any]:
    pairs = sample_pairs(samples_dir)
    original_totals = {key: 0 for key in ("lines", "words", "characters", "bytes")}
    compressed_totals = dict(original_totals)
    for pair in pairs:
        for key in original_totals:
            original_totals[key] += pair["metrics"]["original"][key]
            compressed_totals[key] += pair["metrics"]["candidate"][key]
    ratios = {
        key: ratio(original_totals[key], compressed_totals[key])
        for key in original_totals
    }
    reductions = {
        key: (
            None
            if original_totals[key] == 0
            else 1 - (compressed_totals[key] / original_totals[key])
        )
        for key in original_totals
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "compressor_version": COMPRESSOR_VERSION,
        "measurement": {
            "ratio_gate": "whitespace-delimited words",
            "note": "These are deterministic text metrics, not Claude tokenizer counts.",
        },
        "summary": {
            "pairs": len(pairs),
            "original": original_totals,
            "compressed": compressed_totals,
            "ratios": ratios,
            "reductions": reductions,
        },
        "pairs": pairs,
    }


def benchmark_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Semantic Compressor Deterministic Benchmark",
        "",
        "> Generated from tracked sample files. Text metrics are deterministic and are not Claude tokenizer counts.",
        "",
        "## Summary",
        "",
        "| Metric | Original | Compressed | Ratio | Reduction |",
        "|---|---:|---:|---:|---:|",
    ]
    for metric in ("lines", "words", "characters", "bytes"):
        ratio_value = summary["ratios"][metric]
        reduction = summary["reductions"][metric]
        ratio_text = "N/A" if ratio_value is None else f"{ratio_value:.2f}:1"
        reduction_text = "N/A" if reduction is None else f"{reduction:.1%}"
        lines.append(
            f"| {metric.title()} | {summary['original'][metric]:,} | "
            f"{summary['compressed'][metric]:,} | {ratio_text} | {reduction_text} |"
        )
    lines.extend(
        [
            "",
            "## Sample pairs",
            "",
            "| Sample | Kind | Lines | Words | Word ratio |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for pair in payload["pairs"]:
        metrics = pair["metrics"]
        word_ratio = metrics["ratios"]["words"]
        word_ratio_text = "N/A" if word_ratio is None else f"{word_ratio:.2f}:1"
        lines.append(
            f"| `{pair['id']}` | {pair['kind']} | "
            f"{metrics['original']['lines']} → {metrics['candidate']['lines']} | "
            f"{metrics['original']['words']} → {metrics['candidate']['words']} | "
            f"{word_ratio_text} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This report proves file pairing and size measurements only. Semantic preservation is a separate gate: frontmatter and literal inventories are deterministic; conceptual equivalence is an LLM judgment and must be reported with model and evidence rather than as an absolute guarantee.",
            "",
        ]
    )
    return "\n".join(lines)


def command_discover(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    excludes = [Path(item).expanduser().resolve(strict=False) for item in args.exclude]
    print_json(
        discover_candidates(
            root, exclude=excludes, include_compressed=args.include_compressed
        )
    )
    return 0


def command_metrics(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    original = resolve_project_file(args.original, root)
    candidate = resolve_project_file(args.candidate, root)
    print_json(metrics_payload(original, candidate))
    return 0


def command_inventory(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    original = resolve_project_file(args.original, root)
    payload = json.dumps(inventory_template(original), indent=2, sort_keys=True) + "\n"
    if args.output:
        output = resolve_project_output(args.output, root)
        write_exclusive(output, payload.encode("utf-8"))
        print_json(
            {
                "schema_version": SCHEMA_VERSION,
                "status": "CREATED",
                "path": relative_posix(output, root),
            }
        )
    else:
        print(payload, end="")
    return 0


def command_workspace(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    session = re.sub(r"[^A-Za-z0-9_.-]+", "-", args.session_id).strip("-.")
    if not session:
        raise CompressorError("session id has no usable characters")
    if len(session) > 80:
        raise CompressorError("session id is longer than 80 usable characters")
    run_id = f"{session}-{create_run_id()}"
    workspace_base = root / ".claude" / "semantic-compressor-work"
    reject_symlink_components(workspace_base, root)
    workspace = workspace_base / run_id
    workspace.mkdir(parents=True, exist_ok=False, mode=0o700)
    print_json(
        {
            "schema_version": SCHEMA_VERSION,
            "status": "CREATED",
            "run_id": run_id,
            "workspace": relative_posix(workspace, root),
        }
    )
    return 0


def command_validate(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    original = resolve_project_file(args.original, root)
    candidate = resolve_project_file(args.candidate, root)
    inventory = resolve_project_file(
        args.inventory, root, markdown_only=False
    )
    result = validate_candidate(
        original, candidate, inventory, min_word_ratio=args.min_word_ratio
    )
    print_json(result)
    return 0 if result["status"] == "PASS" else 1


def command_apply(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    original = resolve_project_file(args.original, root)
    candidate = resolve_project_file(args.candidate, root)
    inventory = resolve_project_file(args.inventory, root, markdown_only=False)
    semantic_review = resolve_project_file(
        args.semantic_review, root, markdown_only=False
    )
    print_json(
        apply_candidate(
            root,
            original,
            candidate,
            inventory,
            semantic_review,
            min_word_ratio=args.min_word_ratio,
            run_id=args.run_id,
        )
    )
    return 0


def command_restore(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    manifest = resolve_project_file(args.manifest, root, markdown_only=False)
    print_json(restore_backup(root, manifest, apply=args.apply))
    return 0


def command_benchmark(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    samples_dir = Path(args.samples).expanduser().resolve(strict=True)
    if not samples_dir.is_dir():
        raise CompressorError(f"samples path is not a directory: {samples_dir}")
    payload = benchmark_payload(samples_dir)
    output = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.format == "json"
        else benchmark_markdown(payload)
    )
    if args.check and not args.output:
        raise CompressorError("benchmark --check requires --output")
    if args.output:
        output_path = resolve_project_output(args.output, root)
        if is_within(output_path, samples_dir):
            raise CompressorError("benchmark output must not overwrite bundled samples")
        if args.check:
            if not output_path.exists() or output_path.read_text(encoding="utf-8") != output:
                raise CompressorError(f"generated benchmark is stale: {output_path}")
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if output_path.exists():
                atomic_replace(output_path, output.encode("utf-8"), output_path.stat().st_mode)
            else:
                write_exclusive(output_path, output.encode("utf-8"))
    else:
        print(output, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail-closed controls for the semantic-compressor skill"
    )
    parser.add_argument("--version", action="version", version=COMPRESSOR_VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover", help="list safe compression candidates")
    discover.add_argument("--root", default=".")
    discover.add_argument("--exclude", action="append", default=[])
    discover.add_argument("--include-compressed", action="store_true")
    discover.set_defaults(func=command_discover)

    metrics = subparsers.add_parser("metrics", help="measure an original/candidate pair")
    metrics.add_argument("original")
    metrics.add_argument("candidate")
    metrics.add_argument("--root", default=".")
    metrics.set_defaults(func=command_metrics)

    workspace = subparsers.add_parser(
        "workspace", help="create a unique per-run workspace inside the project"
    )
    workspace.add_argument("--root", default=".")
    workspace.add_argument("--session-id", required=True)
    workspace.set_defaults(func=command_workspace)

    inventory = subparsers.add_parser(
        "inventory", help="create an empty, source-bound preservation inventory"
    )
    inventory.add_argument("original")
    inventory.add_argument("--root", default=".")
    inventory.add_argument("--output")
    inventory.set_defaults(func=command_inventory)

    validate = subparsers.add_parser("validate", help="validate without modifying files")
    validate.add_argument("original")
    validate.add_argument("candidate")
    validate.add_argument("--inventory", required=True)
    validate.add_argument("--root", default=".")
    validate.add_argument("--min-word-ratio", type=float, default=2.0)
    validate.set_defaults(func=command_validate)

    apply_parser = subparsers.add_parser(
        "apply", help="validate, back up, and atomically apply one candidate"
    )
    apply_parser.add_argument("original")
    apply_parser.add_argument("candidate")
    apply_parser.add_argument("--inventory", required=True)
    apply_parser.add_argument("--semantic-review", required=True)
    apply_parser.add_argument("--root", default=".")
    apply_parser.add_argument("--min-word-ratio", type=float, default=2.0)
    apply_parser.add_argument("--run-id")
    apply_parser.set_defaults(func=command_apply)

    restore = subparsers.add_parser("restore", help="verify or apply a manifest rollback")
    restore.add_argument("manifest")
    restore.add_argument("--root", default=".")
    restore.add_argument("--apply", action="store_true")
    restore.set_defaults(func=command_restore)

    benchmark = subparsers.add_parser("benchmark", help="measure bundled sample pairs")
    benchmark.add_argument("--samples", required=True)
    benchmark.add_argument("--root", default=".")
    benchmark.add_argument("--format", choices=("json", "markdown"), default="json")
    benchmark.add_argument("--output")
    benchmark.add_argument("--check", action="store_true")
    benchmark.set_defaults(func=command_benchmark)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "min_word_ratio") and (
        not math.isfinite(args.min_word_ratio) or args.min_word_ratio <= 1
    ):
        parser.error("--min-word-ratio must be finite and greater than 1")
    try:
        return int(args.func(args))
    except CompressorError as exc:
        print(f"semantic-compressor: error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"semantic-compressor: error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("semantic-compressor: interrupted; original files were not changed", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
