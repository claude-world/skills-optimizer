from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts/validate_project.py"
SPEC = importlib.util.spec_from_file_location("project_validator", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class ProjectValidatorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.skill_dir = self.root / ".claude/skills/semantic-compressor"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def create_verification_fixture(self, *, empty_candidate: bool = False) -> None:
        samples = self.skill_dir / "samples"
        cases = []
        for kind in ("skills", "agents"):
            original = write(
                samples / kind / "verbose/example.md",
                "Keep /demo with several extra words for ratio validation.\n",
            )
            candidate = write(
                samples / kind / "compressed/example.md",
                "" if empty_candidate else "Keep /demo.\n",
            )
            case_id = f"{kind}/example"
            artifact_name = f"inventories/{kind}--example.json"
            inventory = {
                "schema_version": validator.core.SCHEMA_VERSION,
                "status": "complete",
                "source_sha256": validator.core.sha256_file(original),
                "literals": {
                    category: (["/demo"] if category == "commands" else [])
                    for category in validator.core.INVENTORY_CATEGORIES
                },
                "category_attestations": {
                    category: True
                    for category in validator.core.INVENTORY_CATEGORIES
                },
                "concepts": [
                    {"id": "core-purpose", "description": "Keep demo behavior"}
                ],
            }
            inventory_path = write(
                samples / "verification" / artifact_name,
                json.dumps(inventory),
            )
            review = {
                "schema_version": validator.core.SCHEMA_VERSION,
                "id": case_id,
                "verdict": "PASS",
                "original_sha256": validator.core.sha256_file(original),
                "candidate_sha256": validator.core.sha256_file(candidate),
                "inventory_sha256": validator.core.sha256_file(inventory_path),
                "missing_concepts": [],
                "altered_meanings": [],
                "unsupported_additions": [],
                "evidence": ["Compared the source and candidate."],
                "reviewer": "validator-test-reviewer",
                "reviewer_mode": "independent-read-only",
                "concept_evidence": [
                    {
                        "concept_id": "core-purpose",
                        "source": "/demo",
                        "candidate": "/demo",
                    }
                ],
            }
            write(
                samples
                / "verification/reviews"
                / f"{case_id.replace('/', '--')}.json",
                json.dumps(review),
            )
            cases.append(
                {
                    "id": case_id,
                    "original_sha256": validator.core.sha256_file(original),
                    "compressed_sha256": validator.core.sha256_file(candidate),
                    "inventory": artifact_name,
                    "forbidden_literals": ["UNSUPPORTED_ADDITION"],
                    "min_word_ratio": 1.1,
                }
            )
        write(
            samples / "verification/cases.json",
            json.dumps({"schema_version": 1, "cases": cases}),
        )

    def test_non_object_case_is_reported_instead_of_filtered(self) -> None:
        self.create_verification_fixture()
        cases_path = self.skill_dir / "samples/verification/cases.json"
        payload = json.loads(cases_path.read_text(encoding="utf-8"))
        payload["cases"].append(42)
        cases_path.write_text(json.dumps(payload), encoding="utf-8")
        result = validator.Validation()
        with mock.patch.object(validator, "ROOT", self.root), mock.patch.object(
            validator, "SKILL_DIR", self.skill_dir
        ):
            validator.validate_cases(result)
        self.assertTrue(
            any("every cases.json entry is an object" in error for error in result.errors)
        )

    def test_undefined_ratio_is_a_validation_error_not_a_crash(self) -> None:
        self.create_verification_fixture(empty_candidate=True)
        result = validator.Validation()
        with mock.patch.object(validator, "ROOT", self.root), mock.patch.object(
            validator, "SKILL_DIR", self.skill_dir
        ):
            validator.validate_cases(result)
        self.assertTrue(any("word ratio undefined" in error for error in result.errors))

    def test_case_rejects_nonfinite_ratio_and_escaping_inventory(self) -> None:
        self.create_verification_fixture()
        cases_path = self.skill_dir / "samples/verification/cases.json"
        payload = json.loads(cases_path.read_text(encoding="utf-8"))
        payload["cases"][0]["min_word_ratio"] = float("nan")
        payload["cases"][1]["inventory"] = "../../../outside.json"
        cases_path.write_text(json.dumps(payload), encoding="utf-8")
        result = validator.Validation()
        with mock.patch.object(validator, "ROOT", self.root), mock.patch.object(
            validator, "SKILL_DIR", self.skill_dir
        ):
            validator.validate_cases(result)
        self.assertTrue(any("word ratio" in error for error in result.errors))
        self.assertTrue(
            any("inventory path stays" in error for error in result.errors)
        )

    def test_local_links_must_remain_inside_repository_root(self) -> None:
        outside = self.root.parent / f"{self.root.name}-outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        try:
            write(self.root / "README.md", f"[escape](../{outside.name})\n")
            result = validator.Validation()
            with mock.patch.object(validator, "ROOT", self.root):
                validator.validate_links(result)
            self.assertTrue(any("link target exists" in error for error in result.errors))
        finally:
            outside.unlink(missing_ok=True)

    def test_eval_suite_rejects_missing_or_escaping_fixtures(self) -> None:
        eval_root = self.skill_dir / "evals"
        entries = []
        for index, reference in enumerate(
            ("fixtures/present.md", "fixtures/missing.md", "../../escape.md"),
            start=1,
        ):
            entries.append(
                {
                    "id": index,
                    "name": f"eval-{index}",
                    "prompt": "Run the fixture.",
                    "expected_output": "An evidence-backed result.",
                    "files": [reference],
                    "expectations": ["The result is explicit."],
                }
            )
        write(eval_root / "fixtures/present.md", "present\n")
        write(eval_root / "evals.json", json.dumps({"evals": entries}))
        result = validator.Validation()
        with mock.patch.object(validator, "ROOT", self.root), mock.patch.object(
            validator, "SKILL_DIR", self.skill_dir
        ):
            validator.validate_eval_suite(result)
        fixture_errors = [
            error for error in result.errors if "fixture exists inside evals" in error
        ]
        self.assertEqual(len(fixture_errors), 2)


if __name__ == "__main__":
    unittest.main()
