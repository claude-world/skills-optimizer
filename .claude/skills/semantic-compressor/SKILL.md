---
name: semantic-compressor
description: |
  Compress agents/skills with quality assurance loop. Iterative 5-phase process ensures understanding preserved.
  TRIGGERS: semantic-compressor, compress skill, optimize agent, reduce tokens, benchmark, 壓縮, 優化
user-invocable: true
---

# Semantic Compressor

Compress agents/skills while preserving understanding. Uses 5-phase iterative quality assurance.

## Workflow: 5-Phase Quality Loop

For EACH file to compress, execute ALL phases in order:

### Phase 1: Original Verification (原始確認)

**Goal**: Confirm Claude understands the original file correctly.

```bash
# Extract understanding from original
claude -p "Read this and answer:
1. What is the main purpose? (1 sentence)
2. What are the key features? (bullet list)
3. What commands/tools are available?
4. What triggers should activate this?

<file content here>

Output as structured YAML."
```

Save output as `<name>.original-understanding.yaml`

### Phase 2: Compress (壓縮)

**Goal**: Apply compression rules to create compressed version.

**⚠️ 必須保留清單 (MUST PRESERVE - 67% 的檔案因遺漏這些而需要迭代)**

```
BEFORE compressing, extract and LIST these from original:
□ ALL triggers (每個關鍵字都要保留)
□ ALL commands (每個指令都要列出)
□ ALL tools (每個工具都要列出)
□ ALL supported formats/types (檔案格式、輸出格式、協議)
□ ALL feature categories (功能分類不能省略)
□ ALL database/language names (具體名稱不能用 "etc." 取代)
```

**Compression Rules:**

```
FOR descriptions (frontmatter):
  - Remove: "This skill/agent provides...", "comprehensive", "advanced"
  - Remove: "Use this when...", "is designed to", "enables users to"
  - Keep: ALL trigger keywords, file extensions, action verbs
  - Format: [Purpose <15 words]. [Features as list]. TRIGGERS: [keywords]
  - Target: 3:1 ratio

FOR body content:
  - Paragraphs → single sentences
  - Verbose lists → terse bullet points
  - Multiple examples → best single example
  - Keep: code blocks, tables (condensed), commands
  - ⚠️ NEVER use "etc.", "and more", "such as" - list ALL items
  - Target: 2:1 ratio

FOR agents:
  - Description: 1-2 sentences max
  - Tools: list ALL, no descriptions
  - Process: numbered one-liners
  - Output: template only
  - Target: 2:1 ratio
```

**Phase 2 Checklist (壓縮前檢查)**
```
Before writing compressed version, verify:
✓ Every trigger from original appears in compressed
✓ Every command from original appears in compressed
✓ Every tool from original appears in compressed
✓ Every feature category is mentioned (can be brief)
✓ All specific names (DBs, languages, formats) are listed
```

Write compressed version to `<name>.compressed.md`

### Phase 3: Compressed Verification (壓縮後確認)

**Goal**: Confirm Claude understands the compressed version correctly.

```bash
# Extract understanding from compressed
claude -p "Read this and answer:
1. What is the main purpose? (1 sentence)
2. What are the key features? (bullet list)
3. What commands/tools are available?
4. What triggers should activate this?

<compressed content here>

Output as structured YAML."
```

Save output as `<name>.compressed-understanding.yaml`

### Phase 4: Compare & Decide (是否需改善)

**Goal**: Compare original vs compressed understanding.

```bash
claude -p "Compare these two understanding extracts.

ORIGINAL:
<original-understanding.yaml>

COMPRESSED:
<compressed-understanding.yaml>

Questions:
1. Is the purpose identical? (yes/no)
2. Are all key features preserved? (list any missing)
3. Are all commands/tools preserved? (list any missing)
4. Are all triggers preserved? (list any missing)
5. Overall: PASS or NEEDS_IMPROVEMENT?

If NEEDS_IMPROVEMENT, specify what to add back."
```

**Decision:**
- If PASS → Phase 5 (Report)
- If NEEDS_IMPROVEMENT → Return to Phase 2 with feedback

### Phase 5: Report (產生報告)

**Goal**: Generate final comparison report.

```markdown
## <name>

| Metric | Original | Compressed | Ratio |
|--------|----------|------------|-------|
| Lines | X | Y | X:Y |
| Tokens (est.) | X | Y | X:Y |

### Understanding Comparison
- Purpose: ✓ Preserved
- Features: ✓ All preserved / × Missing: [list]
- Commands: ✓ All preserved / × Missing: [list]
- Triggers: ✓ All preserved / × Missing: [list]

### Quality: PASS ✓ / FAIL ×
```

---

## Quick Commands

| Command | Action |
|---------|--------|
| `/semantic-compressor` | Auto-scan project `.claude/skills/` and `.claude/agents/`, compress all |
| `/semantic-compressor <file>` | Run 5-phase loop on single file |
| `/semantic-compressor benchmark` | Run 5-phase loop on all samples |
| `/semantic-compressor verify <file>` | Phase 1 + 3 only (no compression) |

---

## Project Directory Auto-Scan Mode

When running `/semantic-compressor` without arguments:

### Step 1: Discovery
```bash
# Find all skill and agent files in project
find .claude/skills -name "*.md" -o -name "SKILL.md"
find .claude/agents -name "*.md"
```

### Step 2: Backup (Required)
```bash
# Create timestamped backup before any changes
BACKUP_DIR=".claude/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r .claude/skills "$BACKUP_DIR/"
cp -r .claude/agents "$BACKUP_DIR/"
echo "✓ Backup created: $BACKUP_DIR"
```

### Step 3: Process Each File
For each discovered file:
1. Skip files already compressed (check for `# Already compressed` comment)
2. Run 5-phase workflow
3. Replace original with compressed version (original in backup)
4. Add `# Compressed by semantic-compressor on <date>` header

### Step 4: Generate Report
```markdown
## Compression Report

| File | Original | Compressed | Ratio | Iterations | Status |
|------|----------|------------|-------|------------|--------|
| skill-a.md | 500 | 120 | 4.2:1 | 1 | ✓ PASS |
| agent-b.md | 300 | 80 | 3.8:1 | 2 | ✓ PASS |

Total: X files compressed, Y tokens saved
Backup: .claude/backups/YYYYMMDD_HHMMSS/
```

---

## Sample Files

Located in `.claude/skills/semantic-compressor/samples/`:

```
samples/
├── skills/
│   ├── verbose/        # Original verbose versions
│   └── compressed/     # Compressed versions
└── agents/
    ├── verbose/        # Original verbose versions
    └── compressed/     # Compressed versions
```

## DO NOT Compress

- Error messages (need exact text)
- Security instructions
- Code syntax
- Numerical thresholds
- File paths

## Quality Thresholds

| Type | Min Ratio | Max Info Loss |
|------|-----------|---------------|
| Skill description | 2.5:1 | 0% triggers |
| Skill body | 2:1 | 0% commands |
| Agent | 2:1 | 0% tools |

If ratio < threshold OR info loss > 0%, mark as NEEDS_IMPROVEMENT.
