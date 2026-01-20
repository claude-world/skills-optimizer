# Semantic Compressor

> 使用 LLM 品質保證壓縮 Claude Code agents/skills。5 階段迭代流程確保語義理解完整保留。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | 繁體中文

## 為什麼需要這個方法？

簡單的 pattern-based 壓縮會丟失語義。這個 skill 使用 **Claude 自己** 來驗證壓縮版本是否保留完整理解：

```
原始 (1,471 tokens) → 壓縮 (420 tokens) = 3.5:1 比例
                                     ↓
                    Claude 驗證：「我還能完全理解嗎？」
                                     ↓
                           ✓ PASS (100% 理解保留)
```

**關鍵洞察**：Python 關鍵字測試顯示 83% 通過率，但 LLM 語義比對在 67% 的檔案中發現真正問題。加入「必須保留清單」後，迭代率降至 **0%**。

## 功能特色

- **5 階段品質迴圈** - 提取 → 壓縮 → 驗證 → 比對 → 報告
- **LLM 驗證** - 使用 `claude -p` 進行語義比對
- **必須保留清單** - 防止壓縮過程中的語義損失
- **自動掃描模式** - 自動處理 `.claude/skills/` 和 `.claude/agents/`
- **自動備份** - 變更前建立時間戳記備份
- **平行驗證** - 使用 sub-agents 加速 4 倍

## 安裝

將 skill 複製到你的 Claude Code 設定：

```bash
# Clone 專案
git clone https://github.com/claude-world/skills-optimizer.git

# 複製到 .claude 目錄
cp -r skills-optimizer/.claude/skills/semantic-compressor ~/.claude/skills/
```

或作為 git submodule 加入專案：

```bash
git submodule add https://github.com/claude-world/skills-optimizer.git .claude/skills/semantic-compressor
```

## 使用方式

### 壓縮所有專案檔案

```bash
# 自動掃描並壓縮當前專案的所有 skills/agents
/semantic-compressor
```

這會：
1. 探索 `.claude/skills/` 和 `.claude/agents/` 中的所有 `.md` 檔案
2. 在 `.claude/backups/YYYYMMDD_HHMMSS/` 建立備份
3. 對每個檔案執行 5 階段壓縮
4. 產生壓縮報告

### 壓縮單一檔案

```bash
/semantic-compressor path/to/skill.md
```

### 執行基準測試

```bash
/semantic-compressor benchmark
```

### 僅驗證（不壓縮）

```bash
/semantic-compressor verify path/to/skill.md
```

## 5 階段品質保證迴圈

對每個要壓縮的檔案：

| 階段 | 名稱 | 動作 |
|------|------|------|
| 1 | 原始驗證 | 使用 `claude -p` 提取理解 |
| 2 | 壓縮 | 套用壓縮規則與必須保留清單 |
| 3 | 壓縮驗證 | 從壓縮版本提取理解 |
| 4 | 比對決定 | 比較階段 1 vs 階段 3 |
| 5 | 報告 | PASS → 完成，NEEDS_IMPROVEMENT → 回到階段 2 |

### 必須保留清單（階段 2）

壓縮前，提取並驗證這些項目被保留：

```
□ ALL triggers（每個關鍵字都必須保留）
□ ALL commands（每個指令都必須列出）
□ ALL tools（每個工具都必須列出）
□ ALL supported formats/types（檔案格式、輸出格式、協議）
□ ALL feature categories（功能分類不能省略）
□ ALL specific names（絕對不用「等」來取代具體名稱）
```

## 基準測試結果

| 類型 | 原始 Tokens | 壓縮後 | 比例 | 理解度 |
|------|-------------|--------|------|--------|
| Skills (3) | 6,480 | 1,480 | 4.4:1 | 100% ✓ |
| Agents (4) | 20,776 | 5,522 | 3.8:1 | 100% ✓ |
| **總計** | **27,256** | **7,002** | **3.9:1** | **100% ✓** |

### 迭代率改善

| 規則版本 | 迭代率 | 需要返工的檔案 |
|----------|--------|----------------|
| 舊規則 | 67% | 4/6 |
| 新規則（含清單） | **0%** | 0/3 |

## 專案結構

```
semantic-compressor/
├── README.md                       # 英文說明
├── README.zh-TW.md                 # 繁體中文說明
├── BENCHMARK-REPORT.md             # 詳細基準測試結果
├── LICENSE                         # MIT 授權
├── CONTRIBUTING.md                 # 貢獻指南
└── .claude/
    └── skills/
        └── semantic-compressor/
            ├── SKILL.md            # 主要 skill 定義
            ├── samples/
            │   ├── skills/
            │   │   ├── verbose/    # 原始冗長版 skills (3 檔案)
            │   │   └── compressed/ # 壓縮版 skills (3 檔案)
            │   ├── agents/
            │   │   ├── verbose/    # 原始冗長版 agents (4 檔案)
            │   │   └── compressed/ # 壓縮版 agents (4 檔案)
            │   └── verification/   # LLM 理解提取結果
            └── references/
                ├── examples.md     # 壓縮前後範例
                └── strategies.md   # 壓縮演算法
```

## 壓縮規則

### 要移除的內容
- 填充詞：「這個 skill/agent 提供...」、「comprehensive」、「advanced」
- 冗餘解釋
- 多個範例（保留最佳單一範例）
- 冗長列表 → 簡潔條列

### 絕對不能移除的內容
- Trigger 關鍵字
- Command 名稱
- Tool 名稱
- 具體格式/類型名稱

### 絕對不能使用的詞
- 「etc.」、「and more」、「such as」- 必須明確列出所有項目

## 關鍵發現

1. **簡單關鍵字測試會遺漏語義損失** - Python 測試顯示 83% 通過，LLM 在 67% 中發現問題

2. **迭代流程是必要的** - 4/6 檔案在加入清單前需要 2 次迭代

3. **必須保留清單消除迭代** - 從 67% 降至 0% 迭代率

4. **平行驗證更快** - Sub-agents 減少約 4 倍驗證時間

## 需求

- Claude Code CLI 支援 `claude -p`
- Claude API 用於 LLM 驗證

## 貢獻

請參閱 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 授權

MIT License - 詳見 [LICENSE](LICENSE)。

## 相關資源

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)

---

Made with Claude Code by [Claude World](https://claude-world.com)
