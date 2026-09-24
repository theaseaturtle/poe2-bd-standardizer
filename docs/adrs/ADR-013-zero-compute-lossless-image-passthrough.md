# ADR-013: 零算力無損圖片透傳直出與死代碼清理規範 (Zero-Compute Lossless Image Pass-Through)

* **狀態**：Accepted (Complements ADR-011)
* **背景**：
  此前為滿足微軟 Word (OpenXML) 靜態排版需求，系統編寫了複雜的圖片尺寸解析與長寬比縮放邏輯（使用 `struct.unpack` 嗅探二進位檔案頭部、換算 914400 英制 EMU 單位並計算頁面限制）。
  在轉向「標準 Markdown + Notion 專用包 (.zip)」現代輕量架構後，圖片展示完全依賴 Notion、Obsidian、VS Code / 反重力 IDE 等現代客戶端的**自適應響應式佈局 (Responsive Auto-fit)**。
  後端進行任何圖片尺寸計算、長寬檢驗或二進位頭部解析均已淪為純粹的算力浪費與代碼冗餘。
* **決策**：
  1. **零算力無損透傳 (Zero-Compute Bit-Stream Pass-Through)**：
     解包 Word 資源時，僅做 100% 原始位元組串流複製（從 `word/media/` 直接寫入 `output/images/`），徹底廢除任何圖片寬高解析、等比縮放與二次壓縮代碼。
  2. **畫質保真與無依賴原則 (Lossless & Zero-Dependency)**：
     不引入任何第三方影像處理庫（如 Pillow/ImageMagick），保持 0 外部依賴與毫秒級解包速度。截圖中的裝備詞綴細節 1:1 無損保留。
  3. **死代碼徹底清理 (Dead Code Removal)**：
     徹底刪除為 Word 導出編寫的 `scripts/export_docx.py`（約 500 行），消除歷史技術債務。
  4. **專案工具鏈極簡鎖定 (Lean Tooling)**：
     專案腳本庫精確收斂為 2 個輕量化標準庫腳本：
     - `scripts/read_docx.py`（文本、超連結與原圖無損解包，~75 行）
     - `scripts/pack_notion_zip.py`（Notion / Obsidian 一鍵導入包打包，~50 行）
* **後果**：
  代碼庫極致精簡乾淨，圖片提取零畫質損耗、零算力開銷，執行速度提升至極致。
