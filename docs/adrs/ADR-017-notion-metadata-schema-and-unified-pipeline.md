# ADR-017: Notion 專用元數據標籤規範與一鍵總控流水線架構

* **狀態**：Accepted (Extends ADR-014 and ADR-016)
* **背景**：
  在系統演進至全量 BD 標準化後，用戶提出了兩大核心訴求：
  1. **多維檢索痛點**：隨著 BD 數量增加，傳統「以單一資料夾存放」無法滿足按「遊戲版本、職業、昇華、造價、核心暗金、傷害類型」等多維度檢索與篩選的需求。用戶明確指定其個人筆記環境**僅使用 Notion**。
  2. **工具鏈調用零散**：提取、轉換、打包與驗收分散在多個獨立腳本中，缺乏統一命令行入口。
  3. **PDF 盲區消除**：舊版 PDF 僅提取全頁截圖，缺乏底層文本串流，影響長文型 PDF 的檢索與校驗。
* **決策**：
  1. **制定 Notion 專用標籤體系元數據規範 (Notion YAML Metadata Schema)**：
     - 在所有標準化 Markdown 頂部強制規範標準 YAML Frontmatter：
       - `title`: BD 官方全名
       - `version`: 遊戲版本（如 `"0.55"`）
       - `class`: 官方繁中基礎職業
       - `ascendancy`: 官方繁中昇華
       - `stage`: 流派生命階段（開荒專屬 / 搬磚積累 / 終局大成）
       - `budget`: 預算區間（0門檻白手起家 / 中低造價 / 中高造價 / 頂級奢華）
       - `playstyle`: 玩法標籤數組（如 `[近戰位移, 旋風斬]`）
       - `damage_type`: 傷害類型數組（如 `[混沌, 點燃]`）
       - `defense`: 防禦體系數組（如 `[1血, 閃避, 偏斜, 結界]`）
       - `core_uniques`: 核心傳奇暗金與質變珠寶數組
       - `source`: 原創作者社群出處
       - `verified`: true
     - 當用戶將 Zip 或 Markdown 導入 Notion Database 時，Notion 自動解析為原生列屬性，賦予多維篩選能力。
  2. **PDF 雙軌提取落地 (Native macOS CoreGraphics + PDFKit Dual-Track)**：
     - 使用 macOS 原生編譯的 Swift 模組 (`scripts/extract_pdf`)，在 1 秒內並行提取高清 Retina 頁面截圖與原始文字層，產出 `document_flow.txt`。
  3. **封裝一鍵總控流水線 `scripts/standardize.py`**：
     - 提供 `ingest`、`pack`、`verify`、`batch-verify` 四大統一命令。
  4. **驗收防線升級**：
     - `scripts/verify_bd.py` 擴充第 5 項檢查（YAML Frontmatter 必備字段校驗）。
* **後果**：
  - 用戶在 Notion 中既可作為單頁閱讀，又可隨時拖入 Notion Database 作為結構化卡片進行多維檢索。
  - 工具鏈高度一體化，支持單命令完成解包、打包與全自動驗證。
