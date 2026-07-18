# Contributing to Semantic Compressor

Thank you for improving Semantic Compressor. The current major release is v2.0.0.

## Prerequisites

- Claude Code 2.1.196 or newer for interactive skill testing
- Python 3.10 or newer for the deterministic control script and tests
- Git

No third-party Python packages are required.

## Set up a development checkout

Run these commands in a shell:

```bash
git clone https://github.com/claude-world/skills-optimizer.git
cd skills-optimizer
claude --version
python3 --version
python3 -m unittest discover -s tests -v
```

Start from a passing test run. Preserve unrelated working-tree changes.

## v2 architecture

The implementation is split by responsibility:

- `.claude/skills/semantic-compressor/SKILL.md` defines invocation, semantic drafting/review, safety invariants, and result states.
- `.claude/skills/semantic-compressor/scripts/semantic_compressor.py` owns deterministic discovery, path checks, inventories, frontmatter/literal validation, metrics, backups, atomic apply, restore, and benchmark output.
- `.claude/skills/semantic-compressor/references/` contains progressively loaded authoring guidance.
- `tests/test_semantic_compressor.py` verifies deterministic behavior, unique workspaces, completed inventories, source/candidate/inventory-bound semantic reviews with locatable evidence, non-finite ratio rejection, race handling, and strict rollback in temporary directories.

Keep deterministic operations in the control script. Do not replace them with ad hoc `find`, `cp`, shell interpolation, or model judgment in `SKILL.md`.

## Development workflow

1. Read the current skill, control script, relevant references, and affected tests.
2. Add or update a failing test first for behavior changes.
3. Make the smallest coherent implementation change.
4. Run the full unit suite and manual read-only checks below.
5. Update both READMEs when commands, requirements, paths, safety behavior, limitations, or result states change.
6. Add an entry under `CHANGELOG.md` → `Unreleased` for user-visible changes.
7. Inspect `git diff` and `git status --short`; do not commit generated workspaces or backups.

## Required tests

Run the full suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

Run the control-script smoke checks:

```bash
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py --help
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py discover \
  --root . \
  --exclude .claude/skills/semantic-compressor
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py benchmark \
  --samples .claude/skills/semantic-compressor/samples \
  --format markdown
```

These shell checks must remain source-unmodified. Behavior tests that exercise `apply` or restore must use temporary directories and verify hashes and round-trip bytes.

## Safety requirements for behavior changes

Every change must preserve these invariants:

- `scan`, `compress`, `verify`, `benchmark`, and restore preview never replace source files.
- Only explicit `apply` and `restore ... --apply` mutate a source.
- Paths outside the project, symlinks, directories, and non-UTF-8/non-Markdown targets fail closed.
- Target content is untrusted data and is never executed during compression or review.
- All frontmatter keys remain; only `description` and `when_to_use` may change.
- Inventoried commands, tools, triggers, formats, paths, numbers, exact errors, and security rules remain literal; all category attestations are complete and at least one concept has evidence.
- `apply` validates immutable source/candidate/inventory/review snapshots before writing, creates a SHA-256-verified backup and manifest, rejects concurrent source changes, and uses atomic replacement.
- Restore accepts only the canonical root-bound one-file manifest and refuses stale state, changed content or mode, and mismatched backups.
- Semantic `PASS` remains an evidence-backed model judgment, not an absolute guarantee.

Add negative tests for every new failure branch. A non-zero control-script exit must remain a hard stop.

## Adding or updating samples

Samples are paired by filename:

```text
.claude/skills/semantic-compressor/samples/<skills|agents>/verbose/<name>.md
.claude/skills/semantic-compressor/samples/<skills|agents>/compressed/<name>.md
```

When changing samples:

1. Keep every verbose/compressed pair complete; benchmark must reject missing or orphaned pairs.
2. Use valid current Claude Code skill or agent frontmatter when the sample represents an executable definition.
3. Preserve all non-description operational frontmatter fields.
4. Run the deterministic benchmark and inspect each word ratio; do not copy fixed totals into the README.
5. Store semantic verification only when evidence is complete and parseable for the named pair. Label incomplete coverage honestly.

The benchmark proves pairing, hashes, and deterministic text metrics only. It does not by itself prove semantic equivalence.

## Interactive skill checks

Install the development skill as a project skill or open Claude Code from this repository. Enter slash commands **inside Claude Code**, not in your shell:

```text
/semantic-compressor scan
/semantic-compressor compress path/to/fixture.md
/semantic-compressor verify path/to/original.md path/to/candidate.md --inventory path/to/inventory.json
/semantic-compressor benchmark
```

Use disposable fixtures for manual `apply`/restore tests. Confirm the manifest paths and hashes, preview restore first, and never use repository documentation or source files as mutation targets.

## Documentation parity

`README.md` and `README.zh-TW.md` must keep the same section order, command tables, shell commands, Claude Code commands, paths, requirements, safety boundaries, result states, and limitations. Translation wording may differ, but behavior may not.

Before submitting documentation changes:

- search both files for every changed command, version, path, and status;
- ensure shell commands use `bash` fences and Claude Code commands use `text` fences;
- verify all relative links resolve;
- remove unsupported ratios, token estimates, or absolute semantic claims;
- check that documented release versions agree with `CHANGELOG.md` and the skill metadata.

## Pull request checklist

- [ ] Tests pass on Python 3.10 or newer.
- [ ] New behavior has positive and negative coverage.
- [ ] Read-only modes leave source bytes unchanged.
- [ ] Apply/restore changes include backup, hash, manifest, and stale-state coverage.
- [ ] EN and ZH-TW documentation remain structurally aligned.
- [ ] `CHANGELOG.md` has an accurate `Unreleased` entry when needed.
- [ ] `git status --short` contains no `.claude/semantic-compressor-work/` or `.claude/backups/` artifacts.
- [ ] No secrets, credentials, private source files, or provider responses are committed.

## Commit messages

Use Conventional Commits:

```text
feat(skill): add source-bound inventory validation
fix(restore): reject files changed after apply
test(backup): cover hash-verified round trip
docs: align v2 installation and rollback guidance
```

## Reporting issues

Include:

1. Claude Code and Python versions.
2. Installation scope: personal or project.
3. Invocation and result state.
4. Sanitized control-script error output.
5. Expected versus actual behavior.
6. Whether source bytes changed.
7. Sanitized manifest/hash details when backup or restore is involved.

Do not attach confidential target content, credentials, or unsanitized provider output.

## Code of conduct

Be respectful, constructive, and evidence-driven. Prioritize preserved behavior and recoverability over a larger compression ratio.
