# Semantic Compressor

> 一個 Claude Code skill，透過 LLM 驗證的品質保證機制，在壓縮 agents 和 skills 的同時保留語義理解。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | 繁體中文

## 問題

Claude Code 的 agents 和 skills 可能變得 token 量很大，增加成本和延遲。簡單的 regex 壓縮會丟失語義。

## 解決方案

使用 **Claude 自己** 來驗證壓縮版本是否保留完整理解：

```
原始 (1,471 tokens) → 壓縮 (420 tokens) = 3.5:1 比例
                                     ↓
                    Claude 驗證：「我還能完全理解嗎？」
                                     ↓
                           ✓ PASS (100% 理解保留)
```

## 主要功能

- **5 階段品質迴圈** - 提取 → 壓縮 → 驗證 → 比對 → 報告
- **LLM 驗證** - 使用 `claude -p` 進行語義比對
- **必須保留清單** - 防止壓縮過程中的語義損失
- **自動掃描模式** - 處理 `.claude/skills/` 和 `.claude/agents/` 中的所有檔案
- **自動備份** - 變更前建立時間戳記備份

## 基準測試結果

| 類型 | 檔案數 | 原始 | 壓縮後 | 比例 |
|------|--------|------|--------|------|
| Skills | 4 | 30,480 tokens | 2,880 tokens | 10.6:1 |
| Agents | 4 | 20,776 tokens | 5,522 tokens | 3.8:1 |
| **總計** | **8** | **51,256 tokens** | **8,402 tokens** | **6.1:1** |

所有檔案皆達成 **100% 語義理解保留**。

## 安裝

```bash
# Clone
git clone https://github.com/claude-world/skills-optimizer.git

# 複製到你的 Claude Code 設定
cp -r skills-optimizer/.claude/skills/semantic-compressor ~/.claude/skills/
```

## 使用方式

```bash
# 壓縮當前專案的所有 skills/agents
/semantic-compressor

# 壓縮單一檔案
/semantic-compressor path/to/skill.md

# 執行基準測試
/semantic-compressor benchmark

# 僅驗證（不變更）
/semantic-compressor verify path/to/skill.md
```

## 備份機制

在任何壓縮操作前，自動建立備份以確保可安全回復：

```bash
# 備份位置
.claude/backups/YYYYMMDD_HHMMSS/
├── skills/          # 壓縮前的原始 skills
└── agents/          # 壓縮前的原始 agents
```

**運作方式：**

1. **自動掃描模式** (`/semantic-compressor`):
   - 建立整個 `.claude/skills/` 和 `.claude/agents/` 的時間戳記備份
   - 原地壓縮檔案
   - 原始檔案保留在備份資料夾

2. **單一檔案模式** (`/semantic-compressor path/to/file.md`):
   - 在原始檔案旁建立 `file.md.backup`
   - 或加入時間戳記備份資料夾（批次處理時）

3. **回復**:
   ```bash
   # 從備份還原
   cp -r .claude/backups/20260120_143000/skills/ .claude/skills/
   cp -r .claude/backups/20260120_143000/agents/ .claude/agents/
   ```

4. **跳過已壓縮檔案**:
   - 含 `# Compressed by semantic-compressor` 標頭的檔案會被跳過
   - 防止重複壓縮

## 5 階段流程

| 階段 | 動作 |
|------|------|
| 1. 原始驗證 | 用 `claude -p` 提取理解 |
| 2. 壓縮 | 套用規則與必須保留清單 |
| 3. 壓縮驗證 | 從壓縮版本提取理解 |
| 4. 比對 | 檢查資訊損失 |
| 5. 報告 | PASS → 完成，NEEDS_IMPROVEMENT → 重試階段 2 |

### 必須保留清單

壓縮前，確認這些被保留：

- 所有 trigger 關鍵字
- 所有 command 名稱
- 所有 tool 名稱
- 所有格式/類型名稱
- 所有功能分類
- 禁用「等」或「and more」- 必須明確列出所有項目

## 範例檔案

| 檔案 | 類型 | 原始 | 壓縮後 | 比例 |
|------|------|------|--------|------|
| doc-processor | Skill | 153 行 | 42 行 | 3.6:1 |
| api-tester | Skill | 316 行 | 68 行 | 4.6:1 |
| code-analyzer | Skill | 349 行 | 65 行 | 5.4:1 |
| code-reviewer | Agent | 172 行 | 47 行 | 3.7:1 |
| db-specialist | Agent | 268 行 | 53 行 | 5.1:1 |
| security-auditor | Agent | 299 行 | 52 行 | 5.8:1 |
| devops-orchestrator | Agent | 1,737 行 | 515 行 | 3.4:1 |
| **full-stack-generator** | **Skill** | **2,757 行** | **167 行** | **16.5:1** |

## 專案結構

```
semantic-compressor/
├── README.md
├── README.zh-TW.md
├── BENCHMARK-REPORT.md
├── LICENSE
├── CONTRIBUTING.md
└── .claude/skills/semantic-compressor/
    ├── SKILL.md              # 主要 skill 定義
    ├── samples/
    │   ├── skills/           # 4 verbose + 4 compressed
    │   ├── agents/           # 4 verbose + 4 compressed
    │   └── verification/     # LLM 理解提取結果
    └── references/
        ├── examples.md       # 壓縮前後範例
        └── strategies.md     # 壓縮演算法
```

## 關鍵洞察

1. **簡單測試會遺漏語義損失** - 關鍵字匹配顯示 83% 通過，LLM 在 67% 中發現問題
2. **清單消除迭代** - 返工率從 67% 降至 0%
3. **壓縮比例** - 達成 3.4:1 到 5.8:1，完整保留理解

## 需求

- 支援 `claude -p` 的 Claude Code CLI
- Claude API 存取權限

## 授權

MIT - 詳見 [LICENSE](LICENSE)

---

Made with Claude Code by [Claude World](https://claude-world.com)
