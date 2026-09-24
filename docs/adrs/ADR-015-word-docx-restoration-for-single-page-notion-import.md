# ADR-015: 因應 Notion 5MB 單檔限制，永久定稿「標準 Markdown + 乾淨 Notion ZIP」交付體系

* **狀態**：Accepted (Supersedes ADR-011 Word exploration; solidifies ADR-014)
* **背景**：
  此前曾嘗試重新引入 Word (`.docx`) 作為單頁直出格式以規避 Notion ZIP 的資料夾套娃。
  但實測發現致命的平臺限制：
  1. **Notion 免費版 5MB 單檔上傳限制**：
     - Notion 對非付費工作區的單一文檔/檔案（包含 Word `.docx`、PDF 等）設有嚴格的 **5MB 上傳大小上限**。
     - POE2 的高質量 BD 攻略通常內嵌 15~20 張高清截圖，標準化 `.docx` 檔案大小普遍在 10MB ~ 15MB 之間，導入時會直接被 Notion 報錯攔截，無法上傳。
  2. **Notion ZIP 導入容量無上限（支持高達數 GB）**：
     - Notion 的「Import -> Markdown & CSV (ZIP)」採用工作區遷移管道，不受到 5MB 單檔限制約束，支持幾百 MB 甚至數 GB 的打包圖文完整上傳。
  3. **套娃本質與極簡消除操作**：
     - Notion ZIP 導入產生的外殼與 `images` 子頁面是 Notion 容器邏輯的副產物。
     - 用戶只需在 Notion 側邊欄將內層子頁面**向上拖拽一層（1 秒完成）**，並刪除外層容器，即可獲得 100% 扁平、圖文完全上傳雲端的獨立攻略頁面。
* **決策**：
  1. **徹底廢除並刪除所有 Word (.docx) 生成與腳本**：不再輸出任何 `.docx` 檔案，完全排除 5MB 報錯風險，保持代碼庫純粹輕量。
  2. **永久確立「標準 Markdown 底稿 + 乾淨 Notion ZIP」雙交付標準**：
     - **產物 1：`output/[四段式名稱]_標準化.md`**：本地標準 Markdown，圖片使用本地相對路徑，本地反重力 IDE / Obsidian 即開即讀。
     - **產物 2：`output/[四段式名稱].zip`**：使用純 Python 標準庫 `scripts/pack_notion_zip.py` 打包，內部主檔名與壓縮包完全對齊，無 `_Notion導入包` 贅詞。
  3. **固化 Notion 1 秒拖出提層 SOP**：
     - 導入後在 Notion 側邊欄點開箭頭，將裡面的攻略頁面拖至上一級目錄；
     - 刪除外層空殼（含 `images` 頁面）；
     - 獲得完美無套娃、圖片 100% 雲端託管的標準攻略頁面。
* **後果**：
  - 100% 兼容 Notion 免費版與所有付費版本，杜絕 5MB 上傳失敗。
  - 保留完整的高清原始截圖，不壓縮畫質。
  - 代碼庫回歸零外部依賴、純 Python 標準庫極簡架構。
