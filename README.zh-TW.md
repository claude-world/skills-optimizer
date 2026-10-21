# Semantic Compressor

> 一個採失敗即停止設計的 Claude Code skill，用來縮減 skill 與 agent Markdown，同時避免悄悄改變行為。

[![CI](https://github.com/claude-world/skills-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/claude-world/skills-optimizer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%89%A52.1.196-blueviolet)](https://code.claude.com/docs/en/skills)
[![Python](https://img.shields.io/badge/Python-3.10%E2%80%933.15-blue)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/claude-world/skills-optimizer)](https://github.com/claude-world/skills-optimizer/stargazers)
[![Latest Release](https://img.shields.io/github/v/release/claude-world/skills-optimizer)](https://github.com/claude-world/skills-optimizer/releases/latest)

[English](README.md) | 繁體中文

> [!IMPORTANT]
> v2.1.0 讓 discovery 與 frontmatter 檢查對齊 Claude Code 2.1.305，並修正多個 v2.0.0 的錯誤。v2.0.0 建立的備份仍可還原。若從 v1 升級，請先閱讀 [CHANGELOG.md](CHANGELOG.md)。

## v2.1.0 新功能

- Scan 涵蓋 Claude Code 目前會載入的位置：`.claude/commands/` 中的自訂 command、plugin 的 skill、command 與 agent（包含放在 `.claude/skills/<plugin>/` 的 plugin），且只納入 Claude Code 會載入為 agent 的檔案。
- Scan 會略過並附上原因：Claude Code 拒絕的名稱、它不會載入的 agent 檔案、超出支援 YAML 子集的 frontmatter，以及非 UTF-8 檔案。
- 當 skill 或 command 候選檔的 `description` 與 `when_to_use` 長度增加並超過 Claude Code 1,536 字元的 listing 上限時，驗證會失敗；候選檔仍超過上限，或 `SKILL.md` 達 500 行以上時則會發出警告。
- 修正：對沒有 `description` 的 skill 或 command，`apply` 不再把 marker 放在 Claude Code 讀取 listing 文字的位置。
- 修正：專案路徑包含 `build` 或 `dist` 等名稱的資料夾時，agent 不再被遺漏；`.claude/worktrees/` 中的 Claude Code worktree 也不再讓每個 entrypoint 重複列出。
- 修正：`restore` 接受任何 v2 版本寫入的備份，升級後 v2.0.0 的備份仍可使用。

## v2 的改變

Semantic Compressor 現在將草擬與實際修改分開：

- `scan`、`compress`、`verify`、`benchmark` 與 restore 預覽不會修改來源檔案。
- 只有明確執行 `apply` 與 `restore ... --apply` 才能取代來源檔案。
- 無第三方相依的 Python 控制腳本負責驗證路徑、frontmatter、保存清單、比例、hash、備份、manifest 與 rollback 狀態。
- deterministic 檢查通過後，由全新的唯讀 reviewer 判斷概念是否等價。
- 語義審查會以附證據的模型判斷呈現，絕不做絕對保證。

此 skill 只能由使用者呼叫；frontmatter 設為 `disable-model-invocation: true`，所以 Claude 不會自動觸發。
Scan、compress、verify、benchmark 與 restore 預覽都是來源不變的 dry run。

## 安全模型

| 邊界 | v2 行為 |
|---|---|
| 目標範圍 | 僅限目前專案內的 regular UTF-8 Markdown 檔案 |
| 探索範圍 | 專案或巢狀 `.claude/skills/*/SKILL.md` root 的 skill entrypoint、`.claude/commands/` 的自訂 command、`.claude/agents/` 的 agent，以及具有 `.claude-plugin/plugin.json` manifest 的 plugin 中的 skill、command 與 agent |
| 不可信內容 | 壓縮或審查時絕不執行目標內的 code block、hook、URL 或嵌入指令 |
| Frontmatter | 保留所有頂層欄位；只有 `description` 與 `when_to_use` 可改寫 |
| Listing 上限 | Skill 或 command 候選檔的 `description` 與 `when_to_use` 不得增長到超過 Claude Code 1,536 字元的 listing 上限 |
| 字面契約 | command、tool、trigger、format、path、number、精確錯誤訊息與安全規則必須原樣保留 |
| 草稿上限 | 每個檔案最多三次候選版本 |
| Apply gate | deterministic 驗證加上獨立語義 `PASS` |
| Rollback | 綁定 SHA-256 的備份 manifest；拒絕 stale 或後續已修改的檔案 |

## 系統需求

- Claude Code **2.1.196 或更新版本**（frontmatter 已用 Claude Code 2.1.305 檢查）
- Python **3.10 或更新版本**（CI 測試 3.10 至 3.15）
- 從此 repository 安裝時需要 Git
- 已登入的 Claude Code session，可使用任何支援的訂閱、API 或雲端 provider 設定

如果 Claude Code 已透過其他受支援的 provider 完成驗證，就不需要直接的 Anthropic API key。
如果第一次啟動顯示 `Not logged in`，請在 Claude Code 內執行 `/login`，或先完成 provider 對應的驗證，再呼叫此 skill。

在 shell 中確認本機版本：

```bash
claude --version
python3 --version
```

以下 shell 範例使用 macOS、Linux 或 WSL 語法。

## 安裝

以下指令會從 public default branch 安裝 v2.1.0。

### 個人安裝

個人安裝可讓此 skill 在所有本機專案中使用：

```bash
git clone https://github.com/claude-world/skills-optimizer.git skills-optimizer
test -f skills-optimizer/.claude/skills/semantic-compressor/scripts/semantic_compressor.py
mkdir -p ~/.claude/skills
cp -R skills-optimizer/.claude/skills/semantic-compressor ~/.claude/skills/
```

安裝路徑：

```text
~/.claude/skills/semantic-compressor/SKILL.md
```

### 專案安裝

若 repository 應固定版本並與協作者共享此 skill，請使用專案安裝：

```bash
test -f /path/to/skills-optimizer/.claude/skills/semantic-compressor/scripts/semantic_compressor.py
mkdir -p .claude/skills
cp -R /path/to/skills-optimizer/.claude/skills/semantic-compressor .claude/skills/
```

接受 Claude Code workspace trust 前，請先檢查專案 skill；如果團隊應共用它，再 commit 已安裝的目錄。

### 驗證安裝並啟動 Claude Code

個人安裝請在 shell 中驗證 bundled 控制腳本：

```bash
python3 ~/.claude/skills/semantic-compressor/scripts/semantic_compressor.py --version
```

專案安裝請使用：

```bash
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py --version
```

腳本預期版本為 `2.1.0`。安裝或更新後，啟動新的 Claude Code session：

```bash
claude
```

接著在 **Claude Code 內**呼叫 skill，不要在 shell 執行：

```text
/semantic-compressor scan
```

### 更新

先更新 checkout：

```bash
git -C skills-optimizer pull --ff-only
```

保留可復原的舊個人安裝，再複製新版：

```bash
mkdir -p "$HOME/.claude/disabled-skills"
SEMANTIC_COMPRESSOR_PREVIOUS="$(mktemp -d "$HOME/.claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv "$HOME/.claude/skills/semantic-compressor" "$SEMANTIC_COMPRESSOR_PREVIOUS/"
cp -R skills-optimizer/.claude/skills/semantic-compressor "$HOME/.claude/skills/"
```

專案安裝請使用：

```bash
mkdir -p .claude/disabled-skills
SEMANTIC_COMPRESSOR_PREVIOUS="$(mktemp -d ".claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv .claude/skills/semantic-compressor "$SEMANTIC_COMPRESSOR_PREVIOUS/"
cp -R /path/to/skills-optimizer/.claude/skills/semantic-compressor .claude/skills/
```

重新執行版本檢查並啟動新的 Claude Code session。

### 解除安裝

將 skill 移出 discovery 目錄，讓解除安裝仍可復原：

```bash
mkdir -p "$HOME/.claude/disabled-skills"
SEMANTIC_COMPRESSOR_DISABLED="$(mktemp -d "$HOME/.claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv "$HOME/.claude/skills/semantic-compressor" "$SEMANTIC_COMPRESSOR_DISABLED/"
```

專案安裝請使用：

```bash
mkdir -p .claude/disabled-skills
SEMANTIC_COMPRESSOR_DISABLED="$(mktemp -d ".claude/disabled-skills/semantic-compressor-XXXXXXXX")"
mv .claude/skills/semantic-compressor "$SEMANTIC_COMPRESSOR_DISABLED/"
```

解除安裝後請啟動新的 Claude Code session。確認不再需要時，才刪除移出的目錄。

## 使用方式

以下所有 command 都要在 Claude Code 互動 session 中執行：

| Claude Code command | 行為 | 會寫入來源檔案？ |
|---|---|---:|
| `/semantic-compressor` 或 `/semantic-compressor scan` | 探索並回報符合條件的檔案 | 否 |
| `/semantic-compressor compress <path>` | 在 run workspace 中草擬並驗證候選檔 | 否 |
| `/semantic-compressor <path>` | `compress <path>` 的向下相容別名 | 否 |
| `/semantic-compressor apply <path>` | 草擬、驗證、獨立審查、備份並原子取代一個檔案 | 是 |
| `/semantic-compressor verify <original> <candidate> --inventory <inventory.json>` | 比較 original/candidate 配對 | 否 |
| `/semantic-compressor benchmark` | 測量已安裝的 sample 配對 | 否 |
| `/semantic-compressor restore <manifest>` | 驗證 rollback hash 並預覽操作 | 否 |
| `/semantic-compressor restore <manifest> --apply` | 只有 manifest hash 仍相符時才還原 | 是 |

Path 可以是絕對路徑或專案相對路徑，但解析後必須位於目前專案內。以 dash 開頭的 path 前要加上 `--`。

### 掃描

```text
/semantic-compressor scan
```

Scan 會回報 `candidates` 與 `skipped`。每個 candidate 都有 `kind`：`skill`、`command` 或 `agent`。它會排除 compressor 自身、supporting reference、sample、backup、workspace、`.claude/worktrees/` 中的 Claude Code worktree、symlink，以及已有 v2 marker 的檔案。每個被略過的檔案都附有原因：

| 原因 | 意義 |
|---|---|
| `self/excluded` | Compressor 自身，或傳給 `--exclude` 的路徑 |
| `already-compressed` | 檔案已帶有 v2 marker |
| `unsafe-path` | Entrypoint 解析後位於其資料夾或專案之外 |
| `unsupported-name` | Claude Code 拒絕該 skill 資料夾、command 檔案或 agent 名稱 |
| `not-an-agent` | `.claude/agents/` 中沒有 frontmatter `name` 的檔案，Claude Code 會視為文件 |
| `agent-missing-description` | 有 `name` 但沒有 `description` 的專案 agent，Claude Code 會略過 |
| `unsupported-frontmatter` | Frontmatter 超出控制腳本支援的 YAML 子集 |
| `not-utf8` | 檔案不是有效的 UTF-8 |

### 壓縮但不修改來源

```text
/semantic-compressor compress .claude/skills/my-skill/SKILL.md
```

來源檔案會維持 byte-for-byte 不變。Skill 會在下列位置建立綁定來源的 inventory 與 candidate：

```text
.claude/semantic-compressor-work/<workspace-id>/
```

接著執行 deterministic 驗證與全新的唯讀語義審查。對 skill 與 command，驗證也會回報 `listing` 長度：Claude Code 會列出 `description`，加上 ` - ` 與 `when_to_use`，超過 1,536 字元的部分會被截斷。增長到超過上限的 candidate 會失敗；仍超過上限的 candidate，或達 500 行以上的 `SKILL.md`，會收到不改變結果的警告。Apply 前請檢查回報的 candidate、hash、證據、比例、警告與最終狀態。

### 套用已接受的候選檔

```text
/semantic-compressor apply .claude/skills/my-skill/SKILL.md
```

`apply` 會 snapshot source、candidate、已完成的 inventory 與獨立 review；驗證其綁定 hash 與逐 concept 證據；建立並驗證 backup；寫入 manifest；在不改變 candidate body 縮排的前提下插入 v2 idempotence marker；檢查 concurrent source edit；最後 atomic replace。任何 gate 失敗時，本次執行都不會取代來源。

Marker 會放在 frontmatter 之後。沒有 `description` 的 skill 或 command 則會把 marker 放在檔案結尾，因為 Claude Code 會以 body 第一個非空白行取代 description 列出。

### 驗證 original/candidate 配對

```text
/semantic-compressor verify .claude/skills/my-skill/SKILL.md .claude/semantic-compressor-work/<workspace-id>/candidate.md --inventory .claude/semantic-compressor-work/<workspace-id>/inventory.json
```

Verify 是唯讀操作。它會分開回報 deterministic 保存、語義判斷與比例狀態；語義可接受但低於設定比例的 candidate，不會被誤標成成功壓縮。

### Benchmark bundled samples

```text
/semantic-compressor benchmark
```

Benchmark 會相對於已安裝 skill 定位 sample，而不是使用目前專案。它回報可重現的 line、word、character、byte、hash 與 pairing 資料。比例 gate 使用空白分隔的 word；這些 metric **不是 Claude tokenizer token 數**，也不能證明語義等價。

### 預覽並套用還原

先預覽：

```text
/semantic-compressor restore .claude/backups/<run-id>/manifest.json
```

檢查操作後才套用：

```text
/semantic-compressor restore .claude/backups/<run-id>/manifest.json --apply
```

Restore 只接受同一 project root 下、由 v2 版本寫入的 `.claude/backups/<run-id>/manifest.json`，且必須符合目前的單檔 schema 與 `applied` 狀態。壓縮後已修改的 target、已改變的 file mode，或 SHA-256 不再符合 manifest 的 backup 都會被拒絕。

## 備份與 manifest

成功的 `apply` 會建立：

```text
.claude/backups/<run-id>/
├── manifest.json
└── files/
    └── <project-relative-source-path>
```

Manifest 會記錄來源路徑、備份路徑、file mode、project root、compressor 版本、completed-inventory path/hash、semantic-review path/hash/reviewer，以及壓縮前、已驗證 candidate、插入 marker 後的 SHA-256。取代來源前會先驗證備份 bytes 與綁定 source/candidate/inventory 的 review artifact。回報的 manifest path 才是 authoritative rollback handle；不要把 manifest 移到其他 project root，也不要自行猜測時間戳記目錄。

## 結果狀態

| 狀態 | 意義 |
|---|---|
| `PASS` | Candidate 通過 deterministic 與獨立語義 gate；來源未修改 |
| `APPLIED` | 明確 apply 已完成，且備份 manifest 驗證成功 |
| `NOT_COMPRESSIBLE` | 安全保留語義，但三次草稿內無法達到比例目標 |
| `REVIEW_REQUIRED` | Deterministic 檢查通過，但沒有可用的獨立 reviewer |
| `SKIPPED` | 檔案已壓縮、被排除、不支援或明確省略 |
| `FAIL` | Preservation、inventory、metadata 或 format 驗證失敗 |
| `ERROR` | Parser、path、backup、checksum、runtime 或其他 tool 發生錯誤 |
| `RESTORED` | 明確 restore 已完成，且還原後 hash 符合 manifest |

只有 `PASS`、`APPLIED` 與 `RESTORED` 分別是其對應操作的成功狀態。

## 限制、成本與隱私

- Semantic Compressor 處理 Claude Code skill、command 與 agent Markdown，不適用任意文件或 source code。
- Symlink、directory、非 UTF-8 檔案，以及專案外路徑都會被拒絕。
- Scan 涵蓋預設的 plugin 結構。`plugin.json` 宣告的自訂路徑中的元件不會被掃描，但可以指定路徑壓縮。
- Listing 檢查使用 Claude Code 預設的 1,536 字元上限。`skillListingMaxDescChars` 設定不會改變此 gate。
- 預設最低壓縮比例是以空白分隔 word 計算的 `2.0:1`。已經精簡的檔案可能正確回傳 `NOT_COMPRESSIBLE`。
- Candidate 草擬與獨立審查會使用模型呼叫。成本與延遲會隨檔案大小與重試增加，每檔最多三次 candidate 草稿。
- Source、candidate 與 inventory 內容會進入已設定的 Claude Code 模型 context，並由你所設定的 provider 處理。不要用於 provider 未獲授權接收的資料。
- 本機 Python 控制腳本執行 deterministic 檢查，但概念等價仍是模型判斷。`apply` 前請檢查證據。
- 腳本可驗證 reviewer attestation 與 artifact binding，無法證明 reviewer 的真實身分。Claude Code orchestration 必須指派真正全新的唯讀 reviewer；使用者自行偽造 review JSON 不在此 trust boundary 內。
- 若沒有全新的獨立 reviewer，skill 會回傳 `REVIEW_REQUIRED`，且不得 apply。
- Workspace 與 backup 會刻意保留在磁碟上供檢查與 rollback。Commit 前請檢查 `git status` 與 repository ignore policy。

## Deterministic 控制腳本

Bundled 腳本可用於診斷與 CI 類型檢查：

```bash
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py --help
python3 .claude/skills/semantic-compressor/scripts/semantic_compressor.py benchmark \
  --samples .claude/skills/semantic-compressor/samples \
  --format markdown
```

直接執行腳本只提供 deterministic control，不能取代 skill 要求的獨立語義審查。

## 測試

在 repository root 執行：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py
```

測試涵蓋 skill、command、agent 與 plugin 的 discovery scope；Claude Code 的名稱、agent 與 listing 規則；唯一且位於專案內的 workspace；idempotence marker 及其位置；symlink component 與 backup path safety；保守的 frontmatter validation；已完成且綁定 source 的 inventory；literal failure；綁定 source/candidate/inventory 的 review；apply race 與 unknown-byte rollback refusal；跨 v2 版本的 strict manifest restore；file mode；以及 deterministic benchmark edge case。專案驗證器會依目前的 Claude Code frontmatter 規則檢查出貨的 skill，並檢查 sample 證據、benchmark 輸出與文件落差。

## 專案結構

```text
skills-optimizer/
├── README.md
├── README.zh-TW.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── BENCHMARK-REPORT.md
├── benchmark-results.json
├── scripts/
│   ├── validate_project.py
│   └── validate-format.sh
├── tests/
│   ├── test_project_validator.py
│   └── test_semantic_compressor.py
└── .claude/skills/semantic-compressor/
    ├── SKILL.md
    ├── scripts/
    │   └── semantic_compressor.py
    ├── references/
    │   ├── inventory-schema.md
    │   ├── strategies.md
    │   └── examples.md
    ├── evals/
    └── samples/
        ├── skills/
        ├── agents/
        └── verification/
```

## 貢獻

請參閱 [CONTRIBUTING.md](CONTRIBUTING.md)。行為變更必須加入測試；影響 command 或 safety 的文件變更必須同步更新兩份 README。

## 授權

MIT — 詳見 [LICENSE](LICENSE)。
