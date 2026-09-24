# POE2 BD 規範化轉換器 (Path of Exile 2 Build Standardizer)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PoE2 Version](https://img.shields.io/badge/PoE2-0.5.x-blue.svg)](https://pathofexile2.com)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![0 External Dependencies](https://img.shields.io/badge/dependencies-0%20external-success.svg)](https://docs.python.org/3/)

專為《流放之路 2》（Path of Exile 2）打造的**高保真、防幻覺 BD 標準化與本地知識庫構建工具**（支援 AI Agent Skill 與獨立 CLI 工具）。

將來源各異（社群散文、影片逐字稿、本地 `.docx`、`.pdf` 文件、網頁長文或 poe.ninja 天梯鏡像）的散亂攻略，毫秒級提取並標準化轉換為結構嚴謹、機制透徹、**國際服官方繁體中文規範（對齊 poe2db.tw）**、且以「三大數值骨架（天賦路徑圖譜、技能連線矩陣、極致數值門檻）」徹底取代低效截圖的極致輕量純文本標準指南。

---

## ✨ 核心特性與設計原則 (Zero-Tolerance Rules)

1. **純文本零圖片激進架構（ADR-018 Pure-Text Radical Paradigm）**：
   - 徹底破除對遊戲截圖的盲目依賴，將 BD 中截圖所傳遞的核心資訊提煉為**「三大核心數值骨架」**（天賦樹全路徑、技能連線矩陣、數值門檻清單）。
   - 產出完全無圖的超輕量 Markdown（僅 20~50 KB，體積縮減 99.99%），秒速開啟、全局可檢索、零存儲負擔，完美支援 Notion MCP 直接寫入或剪貼簿秒貼。
2. **官方繁中單一可信源（SSOT: poe2db.tw）**：
   - 徹底杜絕機械簡轉繁造成的詞彙割裂（如：國服「宝石术士/雇佣兵/榴弹/极速攻击」一律自動精確對齊官方繁中正名「**古靈軍團/傭兵/擲彈/疾速攻擊**」）。
3. **實機技能表格矩陣（Skills Matrix）**：
   - 採開荒「分幕動態矩陣」（Act 1、Act 2、Act 3、Act 4~5），主動技能、等級/品質、1~5 顆輔助寶石、武器套組綁定與機制注意事項一目了然。
4. **天賦樹雙軌與加點檔自包含交付**：
   - 若作者提供 `.build` 文件或 Planner 鏈接，強制啟用「分幕走向文字階梯 + 外部模擬器代碼錨定」雙軌保障，代碼負責遊戲內一鍵亮線映射。
5. **探索彩蛋、數值檔位與邪道技巧強制提取**：
   - 主動收錄跑圖領取免費天賦點、首飾塗油卡額外技能槽、水晶化免疫藍寶石規則、怒火倍數臨界點、低成本淘寶技巧。
6. **本地自包含交付，自由選擇存儲路徑**：
   - **完全去耦第三方服務**：無需配置繁瑣的 Webhook，純 Markdown 天然相容 Obsidian、Notion、Logseq、Typora 與手機端。
   - **隨心存放**：生成的文件可直接存入你的 **Obsidian 知識庫**、本地自定義文件夾或雲盤同步盤。
7. **零外部依賴 (Zero External Dependencies)**：
   - 核心工具庫全部由 Python 標準庫實現，PDF 高清提取使用 macOS 原生 CoreGraphics/PDFKit，免除龐大環境配置。

---

## 📁 專案目錄結構

```text
.
├── SKILL.md                 # Antigravity / Claude Code 技能定義文件
├── CONTEXT.md               # 專案領域模型與規格說明
├── scripts/                 # 純 Python 標準庫自動化工具集
│   ├── standardize.py       # 全流程一鍵總控 CLI（支援自定義 -o 輸出路徑）
│   ├── read_docx.py         # Word 圖文交織時序解包器（0 外部依賴）
│   ├── extract_pdf_pages.py # PDF 雙軌高清頁面截圖與文字提取器
│   ├── extract_pdf.swift    # 原生 Swift 提取器源碼
│   ├── verify_bd.py         # 5 重防呆自動化質檢防線
│   └── pack_notion_zip.py   # Notion 平鋪導入包打包器
├── templates/               # 標準化 Markdown 模板骨架
├── references/              # 官方繁體中英名詞映射詞庫
├── docs/adrs/               # 架構決策記錄 (Architecture Decision Records)
├── input/                   # 原始待處理文檔放置目錄 (.docx / .pdf)
└── output/                  # 預設標準化成果交付目錄
```

---

## 🚀 使用指南

### 模式 A：作為 AI Agent Skill 使用 (推薦)

本專案原生適配 **Google Antigravity**、**Claude Code** 等 AI Coding Agent。

#### 1. 安裝 Skill
將本倉庫複製或軟連結至你的 Agent skills 目錄：

```bash
# 方式 1：直接克隆到本地技能目錄（以 Antigravity / Claude Code 為例）
git clone https://github.com/theaseaturtle/poe2-bd-standardizer.git ~/.gemini/config/skills/poe2-bd-standardizer
```

#### 2. 在對話中直接使用
只需在對話中呼叫 Agent，並可**自由指定儲存目錄**：
- **指定 Obsidian 筆記庫**：
  > 「幫我把 `input/旋風地煉.docx` 整理成標準 BD，存到 `/Users/yue/Documents/Obsidian/PoE2/`」
- **預設輸出**：
  > 「整理這篇 BD 攻略 /poe2-bd」*（將自動存入專案下的 `output/` 交付）*
- **網頁/天梯鏡像**：
  > 「解讀這個 poe.ninja 角色鏡像並按官方繁中標準化輸出」

---

### 模式 B：作為獨立命令行工具 (CLI) 使用

無需 AI Agent，也可以直接在終端執行全流程數據解包與驗收：

#### 1. 解包原始文檔 (Ingest)
支援 `.docx` 與 `.pdf`，支援自定義輸出路徑 `-o`：

```bash
# 解包 Word 文檔至預設 output/
python3 scripts/standardize.py ingest input/example.docx

# 解包 PDF 文檔至指定 Obsidian 庫
python3 scripts/standardize.py ingest input/guide.pdf -o ~/Documents/Obsidian/PoE2
```
*解包完成後，將在目標目錄生成高清截圖及包含時序錨點的 `document_flow.txt`。*

#### 2. 嚴格質量驗收 (Verify)
撰寫或生成 Markdown 後，運行 5 重防呆自動化驗收（檢查 0 孤兒圖片、0 未轉錄佔位符、表格完整性）：

```bash
python3 scripts/standardize.py verify output/0.55_傭兵古靈軍團_染色回旋斬_旋風地煉_標準化.md
```

#### 3. 可選：打包為 Notion 導入包 (Pack)
若需上傳至 Notion：

```bash
python3 scripts/standardize.py pack output/0.55_傭兵古靈軍團_染色回旋斬_旋風地煉_標準化.md
```

---

## 📜 開源許可

本專案基於 [MIT License](LICENSE) 開源。歡迎 PoE2 玩家與開源社群提交 Issue 與 PR 完善名詞詞庫！
