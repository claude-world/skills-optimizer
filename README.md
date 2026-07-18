# Semantic Compressor

> A fail-closed Claude Code skill for reducing skill and agent Markdown without silently changing behavior.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A52.1.196-blueviolet)](https://code.claude.com/docs/en/skills)
[![GitHub Stars](https://img.shields.io/github/stars/claude-world/skills-optimizer)](https://github.com/claude-world/skills-optimizer/stargazers)
[![Latest Release](https://img.shields.io/github/v/release/claude-world/skills-optimizer)](https://github.com/claude-world/skills-optimizer/releases/latest)

English | [繁體中文](README.zh-TW.md)

> [!IMPORTANT]
> v2.0.0 is a major workflow and safety upgrade. Existing users should review [CHANGELOG.md](CHANGELOG.md) before updating.

## What v2 changes

Semantic Compressor now separates drafting from mutation:

- `scan`, `compress`, `verify`, `benchmark`, and restore preview are read-only for source files.
- Only explicit `apply` and `restore ... --apply` can replace a source file.
- A dependency-free Python control script validates paths, frontmatter, preservation inventories, ratios, hashes, backups, manifests, and rollback state.
- A fresh read-only reviewer judges conceptual equivalence after deterministic checks pass.
- Semantic review is reported as model judgment with evidence, never as an absolute guarantee.

The skill is user-invocable only. Its frontmatter sets `disable-model-invocation: true`, so Claude does not trigger it automatically.
Use scan, compress, verify, benchmark, and restore preview as source-unmodified dry runs.

## Safety model

| Boundary | v2 behavior |
|---|---|
| Target scope | Regular UTF-8 Markdown inside the active project only |
| Discovery | Skill entrypoints in project or nested `.claude/skills/*/SKILL.md` roots, plus agent files under `.claude/agents/` |
| Untrusted content | Target code blocks, hooks, URLs, and embedded instructions are never executed during compression or review |
| Frontmatter | All top-level fields remain; only `description` and `when_to_use` may be rewritten |
| Literal contracts | Commands, tools, triggers, formats, paths, numbers, exact errors, and security rules must remain literal |
| Draft limit | At most three candidate iterations per file |
| Apply gate | Deterministic validation plus an independent semantic `PASS` |
| Rollback | SHA-256-bound backup manifest; stale or edited files are refused |

## Requirements

- Claude Code **2.1.196 or newer**
- Python **3.10 or newer**
- Git for installation from this repository
- An authenticated Claude Code session using any supported subscription, API, or cloud provider configuration

A direct Anthropic API key is not required if Claude Code is already authenticated through another supported provider.
If the first session reports `Not logged in`, run `/login` inside Claude Code or complete your provider-specific authentication before invoking the skill.

Check your local versions in a shell:

```bash
claude --version
python3 --version
```

The shell examples below use macOS, Linux, or WSL syntax.

## Installation

The commands below install v2.0.0 from the public default branch.

### Personal installation

Use a personal installation to make the skill available in every local project:

```bash
git clone https://github.com/claude-world/skills-optimizer.git skills-optimizer
test -f skills-optimizer/.claude/skills/semantic-compressor/scripts/semantic_compressor.py
mkdir -p ~/.claude/skills
cp -R skills-optimizer/.claude/skills/semantic-compressor ~/.claude/skills/
```

Installed path:

```text
~/.claude/skills/semantic-compressor/SKILL.md
```

### Project installation

Use a project installation when the repository should pin and share the skill with collaborators:

```bash
test -f /path/to/skills-optimizer/.claude/skills/semantic-compressor/scripts/semantic_compressor.py
mkdir -p .claude/skills
cp -R /path/to/skills-optimizer/.claude/skills/semantic-compressor .claude/skills/
```

Review project skills before accepting Claude Code workspace trust, then commit the installed directory if the team should share it.

### Verify the installation and launch Claude Code

For a personal installation, verify the bundled control script in a shell:

```bash
python3 ~/.claude/skills/semantic-compressor/scripts/semantic_compressor.py --version
```

For a project installation, use:

```bash
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py --version
```

The expected v2 script version is `2.0.0`. Start a fresh Claude Code session after installation or update:

```bash
claude
```

Then invoke the skill **inside Claude Code**, not in your shell:

```text
/semantic-compressor scan
```

### Update

Update the checkout first:

```bash
git -C skills-optimizer pull --ff-only
```

Keep the previous personal installation recoverable, then copy the new one:

```bash
mkdir -p "$HOME/.claude/disabled-skills"
SEMANTIC_COMPRESSOR_PREVIOUS="$(mktemp -d "$HOME/.claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv "$HOME/.claude/skills/semantic-compressor" "$SEMANTIC_COMPRESSOR_PREVIOUS/"
cp -R skills-optimizer/.claude/skills/semantic-compressor "$HOME/.claude/skills/"
```

For a project installation:

```bash
mkdir -p .claude/disabled-skills
SEMANTIC_COMPRESSOR_PREVIOUS="$(mktemp -d ".claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv .claude/skills/semantic-compressor "$SEMANTIC_COMPRESSOR_PREVIOUS/"
cp -R /path/to/skills-optimizer/.claude/skills/semantic-compressor .claude/skills/
```

Re-run the version check and start a fresh Claude Code session.

### Uninstall

Move the skill outside the discovery directory so the uninstall remains recoverable:

```bash
mkdir -p "$HOME/.claude/disabled-skills"
SEMANTIC_COMPRESSOR_DISABLED="$(mktemp -d "$HOME/.claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv "$HOME/.claude/skills/semantic-compressor" "$SEMANTIC_COMPRESSOR_DISABLED/"
```

For a project installation:

```bash
mkdir -p .claude/disabled-skills
SEMANTIC_COMPRESSOR_DISABLED="$(mktemp -d ".claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv .claude/skills/semantic-compressor "$SEMANTIC_COMPRESSOR_DISABLED/"
```

Start a fresh Claude Code session after uninstalling. Delete the moved directory later only if you no longer need it.

## Usage

Run all commands in an interactive Claude Code session:

| Claude Code command | Behavior | Writes source files? |
|---|---|---:|
| `/semantic-compressor` or `/semantic-compressor scan` | Discover and report eligible files | No |
| `/semantic-compressor compress <path>` | Draft and validate a candidate in the run workspace | No |
| `/semantic-compressor <path>` | Backward-compatible alias for `compress <path>` | No |
| `/semantic-compressor apply <path>` | Draft, validate, independently review, back up, and atomically replace one file | Yes |
| `/semantic-compressor verify <original> <candidate> --inventory <inventory.json>` | Compare an original/candidate pair | No |
| `/semantic-compressor benchmark` | Measure installed sample pairs | No |
| `/semantic-compressor restore <manifest>` | Verify rollback hashes and preview operations | No |
| `/semantic-compressor restore <manifest> --apply` | Restore only when manifest hashes still match | Yes |

Paths may be absolute or project-relative, but they must resolve inside the active project. Put `--` before a path beginning with a dash.

### Scan

```text
/semantic-compressor scan
```

Scan reports `candidates` and `skipped`. It excludes the compressor itself, supporting references, samples, backups, workspaces, symlinks, and files already carrying the v2 marker.

### Compress without changing the source

```text
/semantic-compressor compress .claude/skills/my-skill/SKILL.md
```

The source remains byte-for-byte unchanged. The skill creates a source-bound inventory and candidate below:

```text
.claude/semantic-compressor-work/<workspace-id>/
```

It then runs deterministic validation and a fresh read-only semantic review. Inspect the reported candidate, hashes, evidence, ratio, and final state before applying.

### Apply an accepted candidate

```text
/semantic-compressor apply .claude/skills/my-skill/SKILL.md
```

`apply` snapshots the source, candidate, completed inventory, and independent review; validates their bound hashes and per-concept evidence; creates and verifies a backup; writes a manifest; inserts the v2 idempotence marker without changing candidate body indentation; checks for concurrent source edits; and atomically replaces the source. If any gate fails, this run does not replace the source.

### Verify an original/candidate pair

```text
/semantic-compressor verify .claude/skills/my-skill/SKILL.md .claude/semantic-compressor-work/<workspace-id>/candidate.md --inventory .claude/semantic-compressor-work/<workspace-id>/inventory.json
```

Verify is read-only. It reports deterministic preservation separately from semantic judgment and ratio status. A semantically acceptable candidate below the configured ratio is not mislabeled as a successful compression.

### Benchmark bundled samples

```text
/semantic-compressor benchmark
```

Benchmark locates samples relative to the installed skill, not the current project. It reports reproducible line, word, character, byte, hash, and pairing data. The ratio gate uses whitespace-delimited words; these metrics are **not Claude tokenizer counts** and do not prove semantic equivalence.

### Preview and apply a restore

Preview first:

```text
/semantic-compressor restore .claude/backups/<run-id>/manifest.json
```

Apply only after reviewing the operations:

```text
/semantic-compressor restore .claude/backups/<run-id>/manifest.json --apply
```

Restore accepts only `.claude/backups/<run-id>/manifest.json` from the same project root, with the current one-file schema and `applied` state. It refuses a target changed after compression, a changed file mode, or a backup whose SHA-256 no longer matches the manifest.

## Backups and manifests

Successful `apply` creates:

```text
.claude/backups/<run-id>/
├── manifest.json
└── files/
    └── <project-relative-source-path>
```

The manifest records the source path, backup path, file mode, project root, compressor version, completed-inventory path/hash, semantic-review path/hash/reviewer, and SHA-256 values before compression, for the validated candidate, and after marker insertion. Backup bytes and the source/candidate/inventory-bound review artifact are verified before source replacement. Reported manifest paths are the authoritative rollback handles; do not move a manifest between project roots or guess a timestamped directory.

## Result states

| State | Meaning |
|---|---|
| `PASS` | Candidate passed deterministic and independent semantic gates; source unchanged |
| `APPLIED` | Explicit apply completed and its backup manifest was verified |
| `NOT_COMPRESSIBLE` | Safe meaning was retained, but the ratio target was not reachable in three drafts |
| `REVIEW_REQUIRED` | Deterministic checks passed, but no independent reviewer was available |
| `SKIPPED` | File was already compressed, excluded, unsupported, or omitted |
| `FAIL` | Preservation, inventory, metadata, or format validation failed |
| `ERROR` | A parser, path, backup, checksum, runtime, or other tool error occurred |
| `RESTORED` | Explicit restore completed and the restored hash matches the manifest |

Only `PASS`, `APPLIED`, and `RESTORED` are success states for their respective operations.

## Limitations, cost, and privacy

- Semantic Compressor handles Claude Code skill and agent Markdown, not arbitrary documents or source code.
- Symlinks, directories, non-UTF-8 files, and paths outside the active project are rejected.
- The default minimum compression ratio is `2.0:1` by whitespace-delimited words. Already-concise files may correctly return `NOT_COMPRESSIBLE`.
- Candidate drafting and independent review use model calls. Cost and latency grow with file size and retries, with at most three candidate drafts per file.
- Source, candidate, and inventory content enters the configured Claude Code model context and is processed by your configured provider. Do not use the skill on data that provider is not authorized to receive.
- The local Python control script performs deterministic checks, but conceptual equivalence remains a model judgment. Review evidence before `apply`.
- The script can verify reviewer attestation and artifact bindings, not the reviewer's actual identity. Claude Code orchestration must assign a genuinely fresh read-only reviewer; a user-fabricated review JSON is outside this trust boundary.
- If a fresh independent reviewer is unavailable, the skill returns `REVIEW_REQUIRED` and must not apply.
- Workspaces and backups intentionally remain on disk for inspection and rollback. Check `git status` and your repository ignore policy before committing.

## Deterministic control script

The bundled script is useful for diagnostics and CI-style checks:

```bash
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py --help
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py benchmark \
  --samples .claude/skills/semantic-compressor/samples \
  --format markdown
```

Direct script execution provides deterministic controls only. It does not replace the skill's independent semantic review requirement.

## Tests

From the repository root:

```bash
python3 -m unittest discover -s tests -v
```

The suite covers discovery scope, unique project-local workspaces, idempotence markers, symlink-component and backup-path safety, conservative frontmatter validation, completed source-bound inventories, literal failures, source/candidate/inventory-bound reviews, apply races and unknown-byte rollback refusal, strict manifest restore, file modes, and deterministic benchmark edge cases.

## Project structure

```text
skills-optimizer/
├── README.md
├── README.zh-TW.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── tests/
│   └── test_semantic_compressor.py
└── .claude/skills/semantic-compressor/
    ├── SKILL.md
    ├── scripts/
    │   └── semantic_compressor.py
    ├── references/
    │   ├── inventory-schema.md
    │   ├── strategies.md
    │   └── examples.md
    └── samples/
        ├── skills/
        ├── agents/
        └── verification/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Behavior changes must include tests; documentation changes affecting commands or safety must update both READMEs.

## License

MIT — see [LICENSE](LICENSE).
