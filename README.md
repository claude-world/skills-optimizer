# Semantic Compressor

> A Claude Code skill that compresses agents and skills while preserving semantic understanding through LLM-verified quality assurance.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

English | [繁體中文](README.zh-TW.md)

## The Problem

Claude Code agents and skills can become token-heavy, increasing costs and latency. Simple regex-based compression loses semantic meaning.

## The Solution

Use **Claude itself** to verify that compressed versions retain full understanding:

```
Original (1,471 tokens) → Compressed (420 tokens) = 3.5:1 ratio
                                     ↓
                    Claude verifies: "Can I still understand everything?"
                                     ↓
                           ✓ PASS (100% understanding preserved)
```

## Key Features

- **5-Phase Quality Loop** - Extract → Compress → Verify → Compare → Report
- **LLM Verification** - Uses `claude -p` for semantic comparison
- **MUST PRESERVE Checklist** - Prevents semantic loss during compression
- **Auto-scan Mode** - Process all files in `.claude/skills/` and `.claude/agents/`
- **Automatic Backup** - Timestamped backups before any changes

## Benchmark Results

| Type | Files | Original | Compressed | Ratio |
|------|-------|----------|------------|-------|
| Skills | 4 | 30,480 tokens | 2,880 tokens | 10.6:1 |
| Agents | 4 | 20,776 tokens | 5,522 tokens | 3.8:1 |
| **Total** | **8** | **51,256 tokens** | **8,402 tokens** | **6.1:1** |

All files achieved **100% semantic understanding preservation**.

## Installation

```bash
# Clone
git clone https://github.com/claude-world/skills-optimizer.git

# Copy to your Claude Code config
cp -r skills-optimizer/.claude/skills/semantic-compressor ~/.claude/skills/
```

## Usage

```bash
# Compress all skills/agents in current project
/semantic-compressor

# Compress single file
/semantic-compressor path/to/skill.md

# Run benchmark on samples
/semantic-compressor benchmark

# Verify only (no changes)
/semantic-compressor verify path/to/skill.md
```

## Backup Mechanism

Before any compression, automatic backups are created to ensure safe rollback:

```bash
# Backup location
.claude/backups/YYYYMMDD_HHMMSS/
├── skills/          # Original skills before compression
└── agents/          # Original agents before compression
```

**How it works:**

1. **Auto-scan mode** (`/semantic-compressor`):
   - Creates timestamped backup of entire `.claude/skills/` and `.claude/agents/`
   - Compresses files in-place
   - Original files preserved in backup folder

2. **Single file mode** (`/semantic-compressor path/to/file.md`):
   - Creates `file.md.backup` alongside original
   - Or adds to timestamped backup folder if running multiple files

3. **Rollback**:
   ```bash
   # Restore from backup
   cp -r .claude/backups/20260120_143000/skills/ .claude/skills/
   cp -r .claude/backups/20260120_143000/agents/ .claude/agents/
   ```

4. **Skip already compressed**:
   - Files with `# Compressed by semantic-compressor` header are skipped
   - Prevents double-compression

## 5-Phase Workflow

| Phase | Action |
|-------|--------|
| 1. Original Verification | Extract understanding with `claude -p` |
| 2. Compress | Apply rules with MUST PRESERVE checklist |
| 3. Compressed Verification | Extract understanding from compressed |
| 4. Compare | Check for information loss |
| 5. Report | PASS → done, NEEDS_IMPROVEMENT → retry Phase 2 |

### MUST PRESERVE Checklist

Before compressing, verify these are preserved:

- ALL trigger keywords
- ALL command names
- ALL tool names
- ALL format/type names
- ALL feature categories
- NO "etc." or "and more" - list everything explicitly

## Sample Files

| File | Type | Original | Compressed | Ratio |
|------|------|----------|------------|-------|
| doc-processor | Skill | 153 lines | 42 lines | 3.6:1 |
| api-tester | Skill | 316 lines | 68 lines | 4.6:1 |
| code-analyzer | Skill | 349 lines | 65 lines | 5.4:1 |
| code-reviewer | Agent | 172 lines | 47 lines | 3.7:1 |
| db-specialist | Agent | 268 lines | 53 lines | 5.1:1 |
| security-auditor | Agent | 299 lines | 52 lines | 5.8:1 |
| devops-orchestrator | Agent | 1,737 lines | 515 lines | 3.4:1 |
| **full-stack-generator** | **Skill** | **2,757 lines** | **167 lines** | **16.5:1** |

## Project Structure

```
semantic-compressor/
├── README.md
├── README.zh-TW.md
├── BENCHMARK-REPORT.md
├── LICENSE
├── CONTRIBUTING.md
└── .claude/skills/semantic-compressor/
    ├── SKILL.md              # Main skill definition
    ├── samples/
    │   ├── skills/           # 4 verbose + 4 compressed
    │   ├── agents/           # 4 verbose + 4 compressed
    │   └── verification/     # LLM understanding extracts
    └── references/
        ├── examples.md       # Before/after examples
        └── strategies.md     # Compression algorithms
```

## Key Insights

1. **Simple tests miss semantic loss** - Keyword matching showed 83% pass, LLM found issues in 67%
2. **Checklist eliminates iteration** - Dropped from 67% to 0% rework rate
3. **Compression ratios** - 3.4:1 to 5.8:1 achieved with full understanding preserved

## Requirements

- Claude Code CLI with `claude -p` support
- Claude API access

## License

MIT - see [LICENSE](LICENSE)

---

Made with Claude Code by [Claude World](https://claude-world.com)
