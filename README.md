# Semantic Compressor

> Compress Claude Code agents/skills with LLM-based quality assurance. Iterative 5-phase process ensures understanding is preserved.

English | [繁體中文](README.zh-TW.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Approach?

Simple pattern-based compression loses semantic meaning. This skill uses **Claude itself** to verify that compressed versions retain full understanding:

```
Original (1,471 tokens) → Compressed (420 tokens) = 3.5:1 ratio
                                     ↓
                    Claude verifies: "Can I still understand everything?"
                                     ↓
                           ✓ PASS (100% understanding preserved)
```

**Key insight**: Python keyword tests showed 83% pass rate, but LLM semantic comparison caught real issues in 67% of files. After adding the "MUST PRESERVE checklist", iteration rate dropped to **0%**.

## Features

- **5-Phase Quality Loop** - Extract → Compress → Verify → Compare → Report
- **LLM-based Verification** - Uses `claude -p` for semantic comparison
- **MUST PRESERVE Checklist** - Prevents semantic loss during compression
- **Auto-scan Mode** - Automatically process `.claude/skills/` and `.claude/agents/`
- **Automatic Backup** - Creates timestamped backups before any changes
- **Parallel Verification** - Uses sub-agents for 4x faster processing

## Installation

Copy the skill to your Claude Code configuration:

```bash
# Clone the repository
git clone https://github.com/claude-world/skills-optimizer.git

# Copy to your .claude directory
cp -r semantic-compressor/.claude/skills/semantic-compressor ~/.claude/skills/
```

Or add as a git submodule to your project:

```bash
git submodule add https://github.com/claude-world/skills-optimizer.git .claude/skills/semantic-compressor
```

## Usage

### Compress All Project Files

```bash
# Auto-scan and compress all skills/agents in current project
/semantic-compressor
```

This will:
1. Discover all `.md` files in `.claude/skills/` and `.claude/agents/`
2. Create backup in `.claude/backups/YYYYMMDD_HHMMSS/`
3. Run 5-phase compression on each file
4. Generate compression report

### Compress Single File

```bash
/semantic-compressor path/to/skill.md
```

### Run Benchmark

```bash
/semantic-compressor benchmark
```

### Verify Only (No Compression)

```bash
/semantic-compressor verify path/to/skill.md
```

## 5-Phase Quality Assurance Loop

For each file to compress:

| Phase | Name | Action |
|-------|------|--------|
| 1 | Original Verification | Extract understanding using `claude -p` |
| 2 | Compress | Apply compression rules with MUST PRESERVE checklist |
| 3 | Compressed Verification | Extract understanding from compressed version |
| 4 | Compare & Decide | Compare Phase 1 vs Phase 3 |
| 5 | Report | PASS → done, NEEDS_IMPROVEMENT → back to Phase 2 |

### MUST PRESERVE Checklist (Phase 2)

Before compressing, extract and verify these items are preserved:

```
□ ALL triggers (every keyword must be preserved)
□ ALL commands (every command must be listed)
□ ALL tools (every tool must be listed)
□ ALL supported formats/types (file formats, output formats, protocols)
□ ALL feature categories (capabilities must not be omitted)
□ ALL specific names (never use "etc." to replace concrete names)
```

## Benchmark Results

| Type | Original Tokens | Compressed | Ratio | Understanding |
|------|-----------------|------------|-------|---------------|
| Skills | 6,480 | 1,480 | 4.4:1 | 100% ✓ |
| Agents | 5,776 | 1,122 | 5.1:1 | 100% ✓ |
| **Total** | **12,256** | **2,602** | **4.7:1** | **100% ✓** |

### Iteration Rate Improvement

| Rule Version | Iteration Rate | Files Needing Rework |
|--------------|----------------|----------------------|
| Old rules | 67% | 4/6 |
| New rules (with checklist) | **0%** | 0/3 |

## Project Structure

```
semantic-compressor/
├── README.md                       # This file
├── BENCHMARK-REPORT.md             # Detailed benchmark results
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
└── .claude/
    └── skills/
        └── semantic-compressor/
            ├── SKILL.md            # Main skill definition
            ├── samples/
            │   ├── skills/
            │   │   ├── verbose/    # Original verbose skills (3 files)
            │   │   └── compressed/ # Compressed skills (3 files)
            │   ├── agents/
            │   │   ├── verbose/    # Original verbose agents (3 files)
            │   │   └── compressed/ # Compressed agents (3 files)
            │   └── verification/   # LLM understanding extracts
            └── references/
                ├── examples.md     # Before/after examples
                └── strategies.md   # Compression algorithms
```

## Sample Files

### Verbose (Before)
- `doc-processor.md` (153 lines)
- `api-tester.md` (316 lines)
- `code-analyzer.md` (349 lines)
- `code-reviewer.md` (172 lines)
- `db-specialist.md` (268 lines)
- `security-auditor.md` (299 lines)

### Compressed (After)
Same names, 70-80% smaller, 100% understanding preserved.

## Compression Rules

### What to Remove
- Filler phrases: "This skill/agent provides...", "comprehensive", "advanced"
- Redundant explanations
- Multiple examples (keep best single example)
- Verbose lists → terse bullet points

### What to NEVER Remove
- Trigger keywords
- Command names
- Tool names
- Specific format/type names
- Feature category names

### What to NEVER Use
- "etc.", "and more", "such as" - always list ALL items explicitly

## Key Findings

1. **Simple keyword tests miss semantic loss** - Python tests showed 83% pass, LLM caught issues in 67%

2. **Iterative process is essential** - 4/6 files needed 2 iterations before adding checklist

3. **MUST PRESERVE checklist eliminates iterations** - Dropped from 67% to 0% iteration rate

4. **Parallel verification is faster** - Sub-agents reduce verification time by ~4x

## Requirements

- Claude Code CLI with `claude -p` support
- Claude API access for LLM verification

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)

---

Made with Claude Code by [Claude World](https://claude-world.com)
