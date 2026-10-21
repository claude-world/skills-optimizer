# Changelog

## [Unreleased]

## [2.1.0] - 2026-10-21

### Added

- Scan covers custom commands in `.claude/commands/`, which Claude Code treats as skills, and plugin entrypoints below a `.claude-plugin/plugin.json` root: the root `SKILL.md`, `skills/*/SKILL.md`, `commands/**/*.md`, and `agents/**/*.md`, including plugins kept in `.claude/skills/<plugin>/`
- Scan skip reasons `unsupported-name`, `not-an-agent`, `agent-missing-description`, `unsupported-frontmatter`, and `not-utf8` for files Claude Code would not load or the control script cannot validate, following the Claude Code 2.1.305 name and subagent rules
- Validation fails a skill or command candidate whose listing entry (`description`, plus ` - ` and `when_to_use`) grows past Claude Code's 1,536-character cap. Results also report `kind`, `listing`, and non-fatal `warnings` for a candidate still over the cap or a `SKILL.md` with 500 or more lines
- Project validation of the shipped skill against the documented Claude Code frontmatter fields, the Agent Skills name and description limits, the listing cap, the 500-line guidance, direct reference links, and version sync across the skill, script, changelog, and READMEs
- Dependabot configuration for monthly, grouped GitHub Actions updates

### Changed

- Moved the skill version from the undocumented `version` frontmatter field to the documented `metadata.version`
- Clarified that `/semantic-compressor` with no arguments runs `scan`
- Updated the frontmatter and subagent guidance in the references for Claude Code 2.1.305
- CI runs Python 3.10 through 3.15 with `actions/checkout@v7` and `actions/setup-python@v7` on pushes to `main` and on pull requests, and smoke-tests the control script

### Fixed

- `apply` no longer inserts the marker as the first body line of a skill or command without a `description`, where Claude Code would have listed the marker instead of the file's own first line
- Scan no longer drops every agent when the project path contains a folder named like an ignored directory, such as `build` or `dist`
- Scan no longer lists every entrypoint a second time from Claude Code worktrees in `.claude/worktrees/`
- `restore` accepts manifests written by any v2 release, so backups made with v2.0.0 stay restorable after upgrading
- Scan no longer aborts on a non-UTF-8 entrypoint

## [2.0.0] - 2026-07-19

### Added

- Dependency-free `semantic_compressor.py` control script for discovery, unique project-local workspaces, metrics, source-bound inventories, deterministic validation, hash-verified backups, atomic apply, restore, and reproducible benchmark output
- Independent read-only semantic review gate bound to source/candidate/inventory SHA-256 values, with exact locatable evidence for every concept and evidence-bearing `PASS` or `NEEDS_IMPROVEMENT` output
- Completed-inventory attestations plus inventory-bound, per-concept semantic-review evidence
- Explicit result states: `PASS`, `APPLIED`, `NOT_COMPRESSIBLE`, `REVIEW_REQUIRED`, `SKIPPED`, `FAIL`, `ERROR`, and `RESTORED`
- Unit coverage for discovery scope, unique project-local workspaces, idempotence, unsafe paths and symlinks, frontmatter preservation, inventory drift, literal loss, semantic-review binding/evidence, non-finite ratio rejection, backup/restore round trips, stale-state refusal, and deterministic benchmark ordering
- Personal and project installation, update, verification, uninstall, privacy, cost, testing, and manifest-based restore documentation

### Changed

- Replaced the prompt-only five-phase workflow with fail-closed `scan`, `compress`, `apply`, `verify`, `benchmark`, and `restore` modes
- Made scan, candidate drafting, verification, benchmark, and restore preview source-unmodified; only explicit apply and restore `--apply` may replace source files
- Limited discovery to Claude Code skill entrypoints and agent definitions while excluding the compressor, references, samples, backups, workspaces, symlinks, and v2-marked files
- Required every frontmatter value except `description` and `when_to_use`, plus all inventoried literal contracts, to remain equivalent
- Changed the reproducible ratio gate to whitespace-delimited words and stopped labeling estimates as Claude tokens
- Raised documented requirements to Claude Code 2.1.196+ and Python 3.10+, with provider-neutral Claude Code authentication
- Aligned English and Traditional Chinese documentation with the v2 command and safety contract
- Kept pre-release v2 installation on explicitly reviewed checkouts until the v2 public release

### Security

- Treat target and candidate content as untrusted data; embedded shell snippets, dynamic commands, hooks, URLs, and instructions are not executed during compression or review
- Bind inventories and rollback manifests to SHA-256 values and refuse apply/restore when validation, backup, current-file, or stale-state checks fail
- Require a fresh independent semantic reviewer before apply; return `REVIEW_REQUIRED` when one is unavailable
- Reject dot-segment run IDs, symlinked backup/workspace components, symlinked entrypoints, noncanonical restore manifests, and benchmark outputs outside the active project
- Snapshot all apply artifacts, compare-and-swap the source before replacement, preserve candidate indentation, and never roll unknown concurrent bytes back to stale content
- Restore only one root-bound manifest entry transactionally, using the recorded mode and refusing content or mode drift

### Removed

- Removed stale fixed benchmark totals, token-reduction percentages, sample line counts, and absolute semantic-preservation claims from the current READMEs
- Removed instructions that presented Claude Code slash commands as shell commands or implied that all modes mutate files

## [1.0.1] - 2026-03-14

### Changed

- Updated compatibility for Claude Code 2.1+ (closes #1)
- Added GitHub Stars, Latest Release badges to README (closes #2, #3)
- Fixed claude-skill-antivirus link reference

## [1.0.0] - 2026-01-20

### Added

- Initial release of Semantic Compressor skill
- Initial prompt-based quality loop with LLM verification (superseded by v2.0.0)
- MUST PRESERVE Checklist for semantic integrity
- Auto-scan mode for project-wide compression
- Bundled skill and agent sample pairs with an initial benchmark report
- Bilingual documentation (EN + ZH-TW)
- Benchmark report with detailed metrics
- Contributing guidelines
