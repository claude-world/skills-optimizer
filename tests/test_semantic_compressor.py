from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = (
    Path(__file__).parents[1]
    / ".claude/skills/semantic-compressor/scripts/semantic_compressor.py"
)
SPEC = importlib.util.spec_from_file_location("semantic_compressor", SCRIPT)
assert SPEC and SPEC.loader
compressor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = compressor
SPEC.loader.exec_module(compressor)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def inventory_for(original: Path, *, literals: dict[str, list[str]] | None = None) -> dict:
    categories = {category: [] for category in compressor.INVENTORY_CATEGORIES}
    categories.update(literals or {})
    return {
        "schema_version": compressor.SCHEMA_VERSION,
        "status": "complete",
        "source_sha256": compressor.sha256_file(original),
        "literals": categories,
        "category_attestations": {
            category: True for category in compressor.INVENTORY_CATEGORIES
        },
        "concepts": [
            {"id": "core-purpose", "description": "Preserve the fixture's purpose"}
        ],
    }


def review_for(original: Path, candidate: Path, inventory: Path) -> dict:
    original_evidence = next(
        line for line in original.read_text(encoding="utf-8").splitlines() if line
    )
    candidate_evidence = next(
        line for line in candidate.read_text(encoding="utf-8").splitlines() if line
    )
    return {
        "schema_version": compressor.SCHEMA_VERSION,
        "verdict": "PASS",
        "original_sha256": compressor.sha256_file(original),
        "candidate_sha256": compressor.sha256_file(candidate),
        "inventory_sha256": compressor.sha256_file(inventory),
        "missing_concepts": [],
        "altered_meanings": [],
        "unsupported_additions": [],
        "evidence": ["Independent fixture review found equivalent behavior."],
        "reviewer": "unit-test-reviewer",
        "reviewer_mode": "independent-read-only",
        "concept_evidence": [
            {
                "concept_id": "core-purpose",
                "source": original_evidence,
                "candidate": candidate_evidence,
            }
        ],
    }


class CompressorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_apply_fixture(
        self, *, name: str = "fixture"
    ) -> tuple[Path, Path, Path, Path]:
        original = write(
            self.root / f"{name}.md",
            "---\nname: fixture\ndescription: A deliberately verbose fixture.\n---\n"
            "Keep /fixture safe and retain FIXTURE_ERROR. Extra words make this "
            "fixture sufficiently verbose for deterministic compression checks.\n",
        )
        candidate = write(
            self.root / f"{name}-candidate.md",
            "---\nname: fixture\ndescription: Concise fixture.\n---\n"
            "Keep /fixture safe and retain FIXTURE_ERROR.\n",
        )
        inventory = write(
            self.root / f"{name}-inventory.json",
            json.dumps(
                inventory_for(
                    original,
                    literals={
                        "commands": ["/fixture"],
                        "error_messages": ["FIXTURE_ERROR"],
                    },
                )
            ),
        )
        review = write(
            self.root / f"{name}-review.json",
            json.dumps(review_for(original, candidate, inventory)),
        )
        return original, candidate, inventory, review

    def test_discovery_only_returns_entrypoints_and_agents(self) -> None:
        target_skill = write(
            self.root / ".claude/skills/target/SKILL.md", "---\nname: target\n---\nBody\n"
        )
        write(self.root / ".claude/skills/target/reference.md", "Reference\n")
        self_skill = write(
            self.root / ".claude/skills/semantic-compressor/SKILL.md",
            "---\nname: semantic-compressor\n---\nBody\n",
        )
        agent = write(
            self.root / ".claude/agents/reviewer.md",
            "---\nname: reviewer\ndescription: Reviews code\n---\nBody\n",
        )
        write(
            self.root / ".claude/backups/old/.claude/agents/ignored.md", "ignored\n"
        )

        result = compressor.discover_candidates(
            self.root,
            exclude=[self_skill.parent],
            include_compressed=False,
        )

        self.assertEqual(
            result["candidates"],
            [
                {"path": ".claude/agents/reviewer.md", "kind": "agent"},
                {"path": ".claude/skills/target/SKILL.md", "kind": "skill"},
            ],
        )
        self.assertEqual(result["skipped"][0]["reason"], "self/excluded")
        self.assertTrue(target_skill.exists())
        self.assertTrue(agent.exists())

    def test_discovery_skips_marker_and_is_idempotent(self) -> None:
        write(
            self.root / ".claude/skills/done/SKILL.md",
            "---\nname: done\n---\n\n"
            "<!-- semantic-compressor: v2; source-sha256="
            + "a" * 64
            + "; compressed-at=2026-01-01T00:00:00Z; run-id=test -->\nBody\n",
        )
        write(
            self.root / ".claude/skills/prose/SKILL.md",
            "---\nname: prose\n---\nMention <!-- semantic-compressor: v2 in prose.\n",
        )
        result = compressor.discover_candidates(
            self.root, exclude=[], include_compressed=False
        )
        self.assertEqual(
            result["candidates"],
            [{"path": ".claude/skills/prose/SKILL.md", "kind": "skill"}],
        )
        self.assertEqual(result["skipped"][0]["reason"], "already-compressed")

    def test_symlink_and_project_escape_are_rejected(self) -> None:
        outside = write(self.root.parent / f"{self.root.name}-outside.md", "outside\n")
        try:
            link = self.root / "linked.md"
            link.symlink_to(outside)
            with self.assertRaises(compressor.CompressorError):
                compressor.resolve_project_file(link, self.root)
            with self.assertRaises(compressor.CompressorError):
                compressor.resolve_project_file(outside, self.root)
        finally:
            outside.unlink(missing_ok=True)

    def test_direct_apply_and_restore_reject_symlinked_inputs(self) -> None:
        original, candidate, inventory, review = self.make_apply_fixture(
            name="direct-symlink"
        )
        candidate_link = self.root / "candidate-link.md"
        candidate_link.symlink_to(candidate)
        with self.assertRaisesRegex(compressor.CompressorError, "symbolic links"):
            compressor.apply_candidate(
                self.root,
                original,
                candidate_link,
                inventory,
                review,
                min_word_ratio=1.1,
                run_id="direct-symlink",
            )

        applied = compressor.apply_candidate(
            self.root,
            original,
            candidate,
            inventory,
            review,
            min_word_ratio=1.1,
            run_id="direct-manifest",
        )
        manifest = self.root / applied["manifest"]
        manifest_copy = write(
            self.root / "manifest-copy.json", manifest.read_text(encoding="utf-8")
        )
        manifest.unlink()
        manifest.symlink_to(manifest_copy)
        with self.assertRaisesRegex(compressor.CompressorError, "symbolic links"):
            compressor.restore_backup(self.root, manifest, apply=False)

    def test_symlinked_parent_and_skill_entrypoint_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as outside_name:
            outside = Path(outside_name)
            write(outside / "target.md", "outside\n")
            parent_link = self.root / "linked-parent"
            parent_link.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(compressor.CompressorError, "symbolic links"):
                compressor.resolve_project_file(
                    parent_link / "target.md", self.root
                )

        skill_dir = self.root / ".claude/skills/linked"
        skill_dir.mkdir(parents=True)
        real = write(self.root / "real.md", "---\nname: linked\n---\nBody\n")
        (skill_dir / "SKILL.md").symlink_to(real)
        result = compressor.discover_candidates(
            self.root, exclude=[], include_compressed=False
        )
        self.assertEqual(result["candidates"], [])

    def test_validation_preserves_control_frontmatter(self) -> None:
        original = write(
            self.root / ".claude/skills/demo/SKILL.md",
            "---\n"
            "name: demo\n"
            "description: A deliberately verbose description for the demo.\n"
            "disable-model-invocation: true\n"
            "allowed-tools:\n"
            "  - Read\n"
            "---\n"
            "Run /demo verify and preserve ERROR-17. "
            "This sentence is intentionally verbose and repetitive.\n",
        )
        candidate = write(
            self.root / "work/candidate.md",
            "---\n"
            "name: demo\n"
            "description: Concise demo.\n"
            "disable-model-invocation: false\n"
            "allowed-tools:\n"
            "  - Read\n"
            "---\n"
            "Run /demo verify; preserve ERROR-17.\n",
        )
        data = inventory_for(
            original,
            literals={"commands": ["/demo verify"], "error_messages": ["ERROR-17"]},
        )
        inventory = write(self.root / "work/inventory.json", json.dumps(data))

        result = compressor.validate_candidate(
            original, candidate, inventory, min_word_ratio=1.1
        )

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("frontmatter field changed: disable-model-invocation", result["errors"])

    def test_inventory_template_is_complete_and_source_bound(self) -> None:
        original = write(self.root / "source.md", "source text\n")
        template = compressor.inventory_template(original)
        self.assertEqual(template["source_sha256"], compressor.sha256_file(original))
        self.assertEqual(template["status"], "draft")
        self.assertEqual(
            set(template["literals"]), set(compressor.INVENTORY_CATEGORIES)
        )
        self.assertEqual(
            set(template["category_attestations"]),
            set(compressor.INVENTORY_CATEGORIES),
        )
        self.assertFalse(any(template["category_attestations"].values()))
        self.assertEqual(template["concepts"], [])

    def test_malformed_frontmatter_and_draft_inventory_fail_closed(self) -> None:
        original = write(
            self.root / "source.md",
            "---\nname: safe\ndescription: A verbose safe skill.\n---\n"
            "Keep /safe and several extra words for this validation fixture.\n",
        )
        candidate = write(
            self.root / "candidate.md",
            "---\nname: safe\ndescription: [unterminated\n---\nKeep /safe.\n",
        )
        complete = write(
            self.root / "complete.json",
            json.dumps(inventory_for(original, literals={"commands": ["/safe"]})),
        )
        result = compressor.validate_candidate(
            original, candidate, complete, min_word_ratio=1.1
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("unterminated" in error for error in result["errors"]))

        valid_candidate = write(
            self.root / "valid-candidate.md",
            "---\nname: safe\ndescription: Safe.\n---\nKeep /safe.\n",
        )
        draft = write(
            self.root / "draft.json",
            json.dumps(compressor.inventory_template(original)),
        )
        result = compressor.validate_candidate(
            original, valid_candidate, draft, min_word_ratio=1.1
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("inventory status must be complete", result["errors"])

    def test_nonfinite_ratio_and_unlocatable_review_evidence_fail_closed(self) -> None:
        original, candidate, inventory, review_path = self.make_apply_fixture(
            name="finite-evidence"
        )
        result = compressor.validate_candidate(
            original, candidate, inventory, min_word_ratio=float("nan")
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "minimum word compression ratio must be finite and greater than 1",
            result["errors"],
        )

        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["concept_evidence"][0]["source"] = "invented source evidence"
        errors = compressor.validate_semantic_review(
            review, original, candidate, inventory
        )
        self.assertIn(
            "semantic review concept 'core-purpose' source evidence is not in source",
            errors,
        )

    def test_workspace_paths_are_unique_and_project_local(self) -> None:
        first_args = type("Args", (), {"root": str(self.root), "session_id": "abc/123"})
        second_args = type("Args", (), {"root": str(self.root), "session_id": "abc/123"})
        # The command prints JSON; uniqueness is asserted from the created directories.
        with contextlib.redirect_stdout(io.StringIO()):
            compressor.command_workspace(first_args)
            compressor.command_workspace(second_args)
        work_root = self.root / ".claude/semantic-compressor-work"
        paths = sorted(work_root.iterdir())
        self.assertEqual(len(paths), 2)
        self.assertNotEqual(paths[0].name, paths[1].name)
        self.assertTrue(all(path.name.startswith("abc-123-") for path in paths))

    def test_validation_fails_on_missing_literal_and_stale_inventory(self) -> None:
        original = write(self.root / "source.md", "Use /deploy and retain Security Rule 7.\n")
        candidate = write(self.root / "candidate.md", "Deploy safely.\n")
        data = inventory_for(
            original,
            literals={
                "commands": ["/deploy"],
                "security_rules": ["Security Rule 7"],
            },
        )
        data["source_sha256"] = "0" * 64
        inventory = write(self.root / "inventory.json", json.dumps(data))

        result = compressor.validate_candidate(
            original, candidate, inventory, min_word_ratio=1.1
        )

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("inventory source_sha256 does not match original", result["errors"])
        self.assertTrue(
            any("required literal missing" in error for error in result["errors"])
        )

    def test_apply_creates_verified_backup_and_restore_round_trip(self) -> None:
        original_text = (
            "---\nname: demo\ndescription: A very long description for a demo skill.\n"
            "disable-model-invocation: true\n---\n"
            "Use /demo run. Keep ERR_DEMO. Extra filler words for a compressible body.\n"
        )
        original = write(self.root / ".claude/skills/demo/SKILL.md", original_text)
        candidate = write(
            self.root / ".claude/semantic-compressor-work/candidate.md",
            "---\nname: demo\ndescription: Demo skill.\n"
            "disable-model-invocation: true\n---\nUse /demo run. Keep ERR_DEMO.\n",
        )
        data = inventory_for(
            original,
            literals={"commands": ["/demo run"], "error_messages": ["ERR_DEMO"]},
        )
        inventory = write(
            self.root / ".claude/semantic-compressor-work/inventory.json",
            json.dumps(data),
        )
        semantic_review = write(
            self.root / ".claude/semantic-compressor-work/review.json",
            json.dumps(review_for(original, candidate, inventory)),
        )

        applied = compressor.apply_candidate(
            self.root,
            original,
            candidate,
            inventory,
            semantic_review,
            min_word_ratio=1.1,
            run_id="round-trip",
        )
        compressed_text = original.read_text(encoding="utf-8")
        self.assertTrue(compressed_text.startswith("---\n"))
        self.assertIn(compressor.MARKER, compressed_text)
        backup = self.root / applied["backup"]
        self.assertEqual(backup.read_text(encoding="utf-8"), original_text)

        manifest = self.root / applied["manifest"]
        dry_run = compressor.restore_backup(self.root, manifest, apply=False)
        self.assertEqual(dry_run["status"], "DRY_RUN")
        self.assertNotEqual(original.read_text(encoding="utf-8"), original_text)

        restored = compressor.restore_backup(self.root, manifest, apply=True)
        self.assertEqual(restored["status"], "RESTORED")
        self.assertEqual(original.read_text(encoding="utf-8"), original_text)

    def test_marker_insertion_preserves_indented_body_bytes(self) -> None:
        candidate = "---\nname: demo\n---\n    indented code\n\nBody\n"
        marker = (
            "<!-- semantic-compressor: v2; source-sha256="
            + "a" * 64
            + "; compressed-at=2026-01-01T00:00:00Z; run-id=test -->"
        )
        final = compressor.insert_marker(candidate, marker)
        self.assertIn("\n    indented code\n", final)
        self.assertEqual(final.replace(f"{marker}\n", "", 1), candidate)

    def test_apply_rejects_dot_run_id_and_backup_symlink(self) -> None:
        original, candidate, inventory, review = self.make_apply_fixture(name="paths")
        with self.assertRaisesRegex(compressor.CompressorError, "run id"):
            compressor.apply_candidate(
                self.root,
                original,
                candidate,
                inventory,
                review,
                min_word_ratio=1.1,
                run_id="..",
            )
        self.assertFalse((self.root / ".claude/manifest.json").exists())

        with tempfile.TemporaryDirectory() as outside_name:
            outside = Path(outside_name)
            claude_dir = self.root / ".claude"
            claude_dir.mkdir(exist_ok=True)
            (claude_dir / "backups").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(compressor.CompressorError, "symbolic links"):
                compressor.apply_candidate(
                    self.root,
                    original,
                    candidate,
                    inventory,
                    review,
                    min_word_ratio=1.1,
                    run_id="safe-run",
                )
            self.assertEqual(list(outside.iterdir()), [])

    def test_apply_uses_reviewed_snapshot_when_candidate_changes(self) -> None:
        original, candidate, inventory, review = self.make_apply_fixture(name="race")
        reviewed_candidate = candidate.read_text(encoding="utf-8")
        real_validator = compressor.validate_semantic_review

        def swap_candidate(*args, **kwargs):
            candidate.write_text("MALICIOUS UNREVIEWED CONTENT\n", encoding="utf-8")
            return real_validator(*args, **kwargs)

        with mock.patch.object(
            compressor, "validate_semantic_review", side_effect=swap_candidate
        ):
            compressor.apply_candidate(
                self.root,
                original,
                candidate,
                inventory,
                review,
                min_word_ratio=1.1,
                run_id="candidate-race",
            )
        applied_text = original.read_text(encoding="utf-8")
        self.assertIn("Keep /fixture safe", applied_text)
        self.assertNotIn("MALICIOUS", applied_text)
        self.assertIn(reviewed_candidate.splitlines()[-1], applied_text)

    def test_apply_does_not_overwrite_concurrent_source_edit(self) -> None:
        original, candidate, inventory, review = self.make_apply_fixture(name="source-race")
        real_write = compressor.write_exclusive

        def edit_after_manifest(path, data, mode=None):
            result = real_write(path, data, mode)
            if path.name == "manifest.json":
                original.write_text("concurrent user edit\n", encoding="utf-8")
            return result

        with mock.patch.object(
            compressor, "write_exclusive", side_effect=edit_after_manifest
        ):
            with self.assertRaisesRegex(compressor.CompressorError, "source changed"):
                compressor.apply_candidate(
                    self.root,
                    original,
                    candidate,
                    inventory,
                    review,
                    min_word_ratio=1.1,
                    run_id="source-race",
                )
        self.assertEqual(
            original.read_text(encoding="utf-8"), "concurrent user edit\n"
        )

    def test_failed_apply_never_rolls_back_unknown_post_replace_bytes(self) -> None:
        original, candidate, inventory, review = self.make_apply_fixture(
            name="post-replace-race"
        )
        real_replace = compressor.atomic_replace

        def mutate_after_source_replace(path, data, mode):
            result = real_replace(path, data, mode)
            if path == original and compressor.MARKER.encode("utf-8") in data:
                original.write_text("concurrent edit after replacement\n", encoding="utf-8")
            return result

        with mock.patch.object(
            compressor, "atomic_replace", side_effect=mutate_after_source_replace
        ):
            with self.assertRaisesRegex(compressor.CompressorError, "unknown bytes"):
                compressor.apply_candidate(
                    self.root,
                    original,
                    candidate,
                    inventory,
                    review,
                    min_word_ratio=1.1,
                    run_id="post-replace-race",
                )
        self.assertEqual(
            original.read_text(encoding="utf-8"),
            "concurrent edit after replacement\n",
        )

    def test_apply_requires_inventory_bound_independent_review(self) -> None:
        original, candidate, inventory, review_path = self.make_apply_fixture(
            name="review-binding"
        )
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review.pop("inventory_sha256")
        review["reviewer_mode"] = "same-agent"
        review_path.write_text(json.dumps(review), encoding="utf-8")
        with self.assertRaisesRegex(compressor.CompressorError, "inventory_sha256"):
            compressor.apply_candidate(
                self.root,
                original,
                candidate,
                inventory,
                review_path,
                min_word_ratio=1.1,
                run_id="review-binding",
            )
        self.assertNotIn(compressor.MARKER, original.read_text(encoding="utf-8"))

    def test_restore_refuses_post_compression_edits(self) -> None:
        original = write(self.root / "target.md", "many words in the original target file\n")
        candidate = write(self.root / "candidate.md", "target file\n")
        inventory = write(
            self.root / "inventory.json", json.dumps(inventory_for(original))
        )
        semantic_review = write(
            self.root / "review.json", json.dumps(review_for(original, candidate, inventory))
        )
        applied = compressor.apply_candidate(
            self.root,
            original,
            candidate,
            inventory,
            semantic_review,
            min_word_ratio=1.1,
            run_id="changed-after",
        )
        original.write_text("user changed this after compression\n", encoding="utf-8")
        with self.assertRaisesRegex(
            compressor.CompressorError, "changed after compression"
        ):
            compressor.restore_backup(
                self.root, self.root / applied["manifest"], apply=True
            )

    def test_restore_rejects_forged_layout_and_preserves_original_mode(self) -> None:
        original, candidate, inventory, review = self.make_apply_fixture(
            name="restore-schema"
        )
        os.chmod(original, 0o640)
        applied = compressor.apply_candidate(
            self.root,
            original,
            candidate,
            inventory,
            review,
            min_word_ratio=1.1,
            run_id="restore-schema",
        )
        manifest = self.root / applied["manifest"]
        os.chmod(original, 0o600)
        with self.assertRaisesRegex(compressor.CompressorError, "mode changed"):
            compressor.restore_backup(self.root, manifest, apply=False)
        os.chmod(original, 0o640)
        restored = compressor.restore_backup(self.root, manifest, apply=True)
        self.assertEqual(restored["status"], "RESTORED")
        self.assertEqual(stat.S_IMODE(original.stat().st_mode), 0o640)

        forged = write(
            self.root / "forged-manifest.json",
            json.dumps({"schema_version": compressor.SCHEMA_VERSION, "files": []}),
        )
        with self.assertRaisesRegex(compressor.CompressorError, "must be .claude/backups"):
            compressor.restore_backup(self.root, forged, apply=False)

    def test_apply_rejects_stale_or_failed_semantic_review(self) -> None:
        original = write(self.root / "source.md", "one two three four five six\n")
        candidate = write(self.root / "candidate.md", "one two\n")
        inventory = write(
            self.root / "inventory.json", json.dumps(inventory_for(original))
        )
        review = review_for(original, candidate, inventory)
        review["verdict"] = "NEEDS_IMPROVEMENT"
        review_path = write(self.root / "review.json", json.dumps(review))
        with self.assertRaisesRegex(compressor.CompressorError, "verdict must be PASS"):
            compressor.apply_candidate(
                self.root,
                original,
                candidate,
                inventory,
                review_path,
                min_word_ratio=1.1,
                run_id="bad-review",
            )
        self.assertEqual(original.read_text(encoding="utf-8"), "one two three four five six\n")

    def test_benchmark_is_sorted_and_deterministic(self) -> None:
        samples = self.root / "samples"
        for kind in ("skills", "agents"):
            write(samples / kind / "verbose/example.md", "one two three four\n")
            write(samples / kind / "compressed/example.md", "one two\n")
        first = compressor.benchmark_payload(samples)
        second = compressor.benchmark_payload(samples)
        self.assertEqual(first, second)
        self.assertEqual(first["summary"]["pairs"], 2)
        self.assertEqual(first["summary"]["ratios"]["words"], 2.0)
        self.assertEqual(
            [pair["id"] for pair in first["pairs"]],
            ["skills/example", "agents/example"],
        )
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_benchmark_rejects_empty_samples_and_unsafe_output_contracts(self) -> None:
        empty = self.root / "empty-samples"
        for kind in ("skills", "agents"):
            (empty / kind / "verbose").mkdir(parents=True)
            (empty / kind / "compressed").mkdir(parents=True)
        with self.assertRaisesRegex(compressor.CompressorError, "no skills sample"):
            compressor.benchmark_payload(empty)

        samples = self.root / "samples"
        for kind in ("skills", "agents"):
            write(samples / kind / "verbose/example.md", "one two three four\n")
            write(samples / kind / "compressed/example.md", "one two\n")
        args = type(
            "Args",
            (),
            {
                "root": str(self.root),
                "samples": str(samples),
                "format": "json",
                "output": None,
                "check": True,
            },
        )
        with self.assertRaisesRegex(compressor.CompressorError, "requires --output"):
            compressor.command_benchmark(args)

        with tempfile.TemporaryDirectory() as outside_name:
            args.output = str(Path(outside_name) / "benchmark.json")
            args.check = False
            with self.assertRaisesRegex(compressor.CompressorError, "escapes project root"):
                compressor.command_benchmark(args)

        for kind in ("skills", "agents"):
            (samples / kind / "compressed/example.md").write_text("", encoding="utf-8")
        markdown = compressor.benchmark_markdown(
            compressor.benchmark_payload(samples)
        )
        self.assertIn("N/A", markdown)


if __name__ == "__main__":
    unittest.main()
