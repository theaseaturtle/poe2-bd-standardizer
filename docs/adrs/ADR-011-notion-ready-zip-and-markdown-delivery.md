# ADR-011: Notion 專用導入包與標準 Markdown 雙軌交付架構

* **狀態**：Accepted (Amended by ADR-013, ADR-014, and ADR-015)
* **背景**：
  此前為滿足離線可讀性，系統曾引入 Word (.docx) 打包。但在實踐中發現：
  1. **跨平台排版痛點**：Word 排版易因字體缺失或邊界渲染產生意外換行；
  2. **計算資源開銷**：生成與解析 .docx 需消耗更多算力；
  3. **Notion 導入機制**：Notion 等雲端工具無法直接獲取本地硬碟的相對路徑圖片（會報 404），但原生支援「Markdown + 圖片資料夾」打成的 `.zip` 壓縮包一鍵導入。
* **決策**：
  1. **全面廢除 Word (.docx) 生成**：後續處理流程中不再呼叫 `export_docx.py` 生成 `.docx` 文件，節省算力並徹底排除字體與排版解析隱患。
  2. **確立雙產物標準交付規格 (Dual Lean Deliverables)**：
     - **產物 1：`output/[BD名稱]_標準化.md`**：本地標準 Markdown 檔案，圖片採用 `images/[BD名稱]/imageX.png` 相對路徑，在反重力 IDE、VS Code、Typora、Obsidian 中即開即看、零配置渲染。
     - **產物 2：`output/[BD名稱]_Notion導入包.zip`**：使用輕量腳本 `scripts/pack_notion_zip.py`（純 Python 標準庫，0.05 秒完成），將 `.md` 和引用的 `images/` 資料夾自動打包為 Notion 官方標準導入壓縮包，在 Notion 點擊「Import -> Markdown」選取該 zip 即可一鍵無損導入全部圖文。
  3. **交付目錄結構自包含規範**：
     ```
     output/
     ├── [BD名稱]_標準化.md
     ├── [BD名稱]_Notion導入包.zip
     └── images/
         └── [BD名稱]/
             ├── image1.png
             └── ...
     ```
* **後果**：
  - 極致輕量化，節省算力與執行時間。
  - 完美契合用戶以 Notion / 本地 IDE 為核心的使用習慣。
  - 徹底根治遠端 Notion 導入 404 與本地預覽裂圖的痛點。
