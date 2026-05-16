# 客製化股票 Dashboard 製作流程樣板

> **用途**：為任何美股（或台股）快速產出「即時監控 Dashboard HTML」+ 每日報告 PDF 的標準作業流程（SOP）。  
> **基於**：ONDS（Ondas Inc.）Dashboard 製作過程整理（2026-05-16）。

---

## 📋 使用說明

1. 複製此檔，重新命名為 `【股票代碼】_Dashboard製作.md`
2. 將所有 `【】` 括號內的文字替換成目標股票的實際資料
3. 依照流程逐步執行，每完成一步打 ✅
4. 完成後將 HTML 檔案放入 `pagaya/` 或對應目錄並 push 到 GitHub Pages

---

## 第一步：確認股票基本資訊

```
股票全名：【公司完整英文名稱】
股票代碼：【NASDAQ/NYSE/TSE: 代碼】
主要業務：【一句話描述核心業務】
行業分類：【例：國防科技 / 金融科技 / 生技 / 半導體】
總部所在：【城市 / 國家】
上市時間：【YYYY-MM-DD】
```

---

## 第二步：資料蒐集清單

> 請依序搜尋以下關鍵字，蒐集足夠資料後再開始填寫 Dashboard。

### 🔍 必搜關鍵字（填入搜尋引擎或 WebSearch 工具）

```
【代碼】 stock price 2026
【代碼】 【公司名】 financial results earnings 2026
【代碼】 stock technical analysis analyst rating May 2026
【公司名】 business news partnerships contracts 2026
【代碼】 52 week high low insider trading history
```

### 📦 需要收集的資料欄位

#### A. 股價資訊
- [ ] 最新收盤價：`$___`
- [ ] 今日漲跌幅：`+/- ____%`
- [ ] 52 週高點：`$___`
- [ ] 52 週低點：`$___`
- [ ] 52 週漲跌幅：`+/- ____%`
- [ ] 日內振幅：`$___ ~ $___`
- [ ] 市值：`$___B / $___M`

#### B. 分析師資訊
- [ ] 分析師評級共識：`Strong Buy / Buy / Hold / Sell`
- [ ] 分析師人數：`___ 位`
- [ ] 均值目標價：`$___`
- [ ] 最高目標價：`$___`
- [ ] 最低目標價：`$___`
- [ ] 買入人數 / 賣出人數：`___ / ___`

#### C. 最新財報（最近一季）
- [ ] 財報季度：`Q___ 20__`
- [ ] 財報公告日：`20__-__-__`
- [ ] 總營收：`$___M`（YoY `+/-___%`）
- [ ] 毛利率：`___%`（前季 `___%`）
- [ ] 調整後 EBITDA：`$___M`（正 / 負）
- [ ] GAAP 淨利潤：`$___M`
- [ ] EPS：`$___`（vs 預期 `$___`）
- [ ] 主要業務指標（依公司類型填入）：
  - 金融科技：撮合量 / ABS 規模
  - 無人機/國防：積壓訂單 / 合約規模
  - SaaS：ARR / NRR / 客戶數
  - 生技：FDA 進程 / 臨床試驗

#### D. 全年業績指引
- [ ] 全年營收指引：`$___M ~ $___M`
- [ ] YoY 成長率：`+/-___%`
- [ ] EBITDA 指引：`$___M ~ $___M`
- [ ] 是否上調/下調：`⬆️ 上調 / ➡️ 維持 / ⬇️ 下調`

#### E. 重大事件 / 催化劑（近 6 個月）
- [ ] 事件1（日期 + 內容 + 影響）
- [ ] 事件2
- [ ] 事件3（依實際數量增減）

#### F. 商業模式與合作夥伴
- [ ] 核心商業模式：`___`
- [ ] 主要合作夥伴 / 客戶（3–10 個）：`___`
- [ ] 護城河描述：`___`

#### G. 技術指標（截至最新交易日）
- [ ] RSI (14)：`___`
- [ ] MA5：`$___`
- [ ] MA20：`$___`
- [ ] MA50：`$___`
- [ ] MA200：`$___`
- [ ] 主要支撐位：`$___ / $___`
- [ ] 主要壓力位：`$___ / $___`

#### H. 法人動向 / 高管交易
- [ ] 近期法人評級變化
- [ ] 高管買賣記錄（SEC Form 4）

---

## 第三步：Dashboard HTML 結構規劃

> 根據公司類型選擇要保留/替換的區塊。

### 通用區塊（所有股票都要）
- [x] Header（股價 + 徽章）
- [x] 核心指標卡片（4 個數字）
- [x] 漲跌分析（AI 三方觀點）
- [x] 即時新聞（外部連結按鈕）
- [x] 重要事件時間軸
- [x] 財務表現（表格 + 圖表）
- [x] 技術面分析
- [x] 分析師評級
- [x] 催化劑 / 風險提示
- [x] 投資論點
- [x] AI 辯論交鋒

### 依公司類型選填
| 公司類型 | 特有區塊 | 替換掉的區塊 |
|---------|---------|------------|
| 金融科技（如 PGY）| ABS 發行記錄 / 違約率追蹤 / 合作夥伴網路 | 無人機業務 / 積壓訂單 |
| 無人機/國防（如 ONDS）| 重大合約 / 積壓訂單 / 業務板塊（OAS/Networks/Capital）| ABS / 違約率 |
| SaaS / 雲端 | ARR 追蹤 / NRR 趨勢 / 客戶留存 | 金融/合約特有指標 |
| 生技/藥廠 | 管線進度 / 臨床數據 / FDA 時間軸 | 業務合作夥伴 |
| 半導體 | 產品世代 / 設計勝率 / 大客戶曝露度 | 金融/服務特有指標 |

---

## 第四步：Dashboard 主題色設定

> 在 HTML 的 CSS `:root` 中調整主題色，讓 Dashboard 有專屬品牌感。

```css
/* 通用深色基底（不變） */
--bg:#0d1117;  /* 背景 */
--s:#161b22;   /* 卡片背景 */
--s2:#1c2128;  /* 次要背景 */
--bd:#30363d;  /* 邊框 */
--t:#e6edf3;   /* 主文字 */
--m:#8b949e;   /* 次要文字 */

/* 依股票/產業客製化強調色 */
/* 金融科技（藍綠）：--bl:#58a6ff → 主色 */
/* 國防無人機（橙色）：--o:#ffa657 → 主色  ← ONDS 採用 */
/* 生技（紫色）：--p:#bc8cff → 主色 */
/* 半導體（青色）：自訂 #00d4ff → 主色 */
/* 能源（金黃）：--y:#d29922 → 主色 */
```

**強調色選用原則**：
- 選一個產業感強、視覺辨識度高的顏色作為 `主色`
- 將 Header 的 `.ticker` 文字色、nav hover 色、`.live-badge` 邊框色、`.nlink-btn` 連結色統一改為主色
- 背景的 `radial-gradient` 光暈也改為主色的低透明度版本

---

## 第五步：AI 三方觀點撰寫指引

> 以下是撰寫 Gemini / ChatGPT / Grok 三方觀點的框架。

### Gemini（數量分析角色）
- 重點：量化數據、比率、技術指標、統計模型
- 必包含：① 超預期幅度量化 ② 估值比率（P/E / P/S / EV/EBITDA）③ 技術目標位
- 語氣：客觀、數字驅動、結論明確

```
【具體數字】的超預期幅度符合【量化邏輯說明】。
技術面：RSI 約【數值】，【超買/超賣/中性】。
估值：P/S 約【X.X×】，在【同業賽道】中【高估/低估/合理】。
量化評分：【最主要的 2–3 個量化訊號說明】。
```

### ChatGPT（基本面/敘事角色）
- 重點：商業模式轉型、護城河、敘事升級、管理層信譽
- 必包含：① 公司敘事定位 ② 核心護城河描述 ③ 為什麼現在是轉折點
- 語氣：宏觀、有說服力、強調「why now」

```
【公司名】的敘事已從「【舊定位】」升級為「【新定位】」。
【最亮眼的基本面數據】是敘事轉型的第一個量化確認。
核心護城河：【1–2 句描述差異化優勢】。
【為什麼現在是機會而非陷阱】。
```

### Grok（市場結構/籌碼角色）
- 重點：流動性、籌碼結構、做空比率、機構持倉、等待的時間成本
- 必包含：① 籌碼面質疑或支持點 ② 最重要的觀察指標 ③ 操作建議（含風險）
- 語氣：現實、有點懷疑、但給出具體可操作建議

```
【基本面雖好，但以下籌碼問題需要注意】。
最重要的觀察指標是：① 【指標1】 ② 【指標2】。
操作建議：【等待何種條件 / 進場位 / 止損位】。
```

### AI 辯論交鋒格式
```
Gemini→GPT：【對 GPT 觀點的質疑或補充，聚焦量化面】
GPT→Gemini：【以敘事/基本面反駁，強調方向比精確度重要】
Grok→全體：【提出其他兩者都忽略的市場結構問題】
GPT→Grok：【承認流動性問題，但提出催化劑時間軸反駁】
```

---

## 第六步：HTML 檔案命名與存放規則

```
檔案命名：【股票代碼小寫】_dashboard.html
存放路徑：pagaya/【股票代碼小寫】_dashboard.html
範例：pagaya/onds_dashboard.html
      pagaya/pgy_live_dashboard.html
```

**nav 導覽列第一個連結**統一指向：
```html
<a href="../index.html" style="font-weight:700;color:var(--主色);margin-right:8px">← 分析中心</a>
```

---

## 第七步：PDF 報告生成（可選）

> 若需要同時輸出 PDF 版分析報告，依照以下流程：

### 7-1. 先產出 Markdown 報告
- 使用 `templates/股票樣板.md` 填寫
- 命名：`【代碼】_【YYYY-MM-DD】_report.md`
- 存放：`C:\tmp\SHIHWEI\reports\`

### 7-2. 轉換為 PDF
```powershell
# 確認 NODE_PATH 設定
$env:NODE_PATH = "C:\Users\User\AppData\Roaming\npm\node_modules"

# 執行轉換（md_to_pdf.js 已放在 reports 目錄）
node "C:\tmp\SHIHWEI\reports\md_to_pdf.js" `
  "C:\tmp\SHIHWEI\reports\【代碼】_【日期】_report.md" `
  "C:\tmp\SHIHWEI\reports\【代碼】_【日期】_report.pdf"
```

> **注意**：`md_to_pdf.js` 使用 Microsoft Edge 作為渲染引擎，需確認 Edge 存在於：  
> `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`

### 7-3. 開啟確認
```powershell
start "" "C:\tmp\SHIHWEI\reports\【代碼】_【日期】_report.pdf"
```

---

## 第八步：品質檢查清單

完成後對照以下清單確認：

### HTML Dashboard
- [ ] Header 顯示正確股價、漲跌幅、公司名
- [ ] 徽章（badges）內容符合該公司最新亮點
- [ ] AI 三方觀點文字已根據公司特性客製化（非通用廢話）
- [ ] 即時新聞的 4 個連結都指向正確的該股票資訊頁
- [ ] 事件時間軸包含最新 3–5 個重要事件，且有正確日期
- [ ] 財務表格數字與官方財報一致
- [ ] 分析師評級人數、目標價均值正確
- [ ] 催化劑 / 風險各至少 4–5 項，有高/中/低嚴重度標籤
- [ ] 主題色統一（nav / header / badge / 按鈕 / 光暈）
- [ ] Chart.js 圖表有正確的歷史數據
- [ ] 所有超連結可正常開啟（target="_blank"）
- [ ] 手機版顯示正常（`.g2/.g3/.g4` 在 `≤700px` 單欄）

### PDF 報告
- [ ] 中文字體正常顯示（無亂碼方塊）
- [ ] 表格結構完整，無斷行錯誤
- [ ] Emoji 正常渲染
- [ ] 頁面邊距合理（建議 15mm）
- [ ] 所有來源連結列於報告末尾

---

## 附錄 A：常用資料來源

| 資料類型 | 建議來源 |
|---------|---------|
| 即時股價 / 歷史數據 | Yahoo Finance、TradingView |
| 分析師評級 / 目標價 | stockanalysis.com、public.com/forecast |
| 財報原文 / 新聞稿 | ir.【公司網域】.com、businesswire.com |
| 法說會逐字稿 | Motley Fool、Seeking Alpha、investing.com |
| 高管交易 | SEC EDGAR Form 4 |
| 即時新聞 | Yahoo Finance News、stockanalysis.com/news |
| 技術指標 | TradingView、stockanalysis.com |
| 積壓訂單 / 合約 | 公司 IR、SEC 8-K 申報 |

---

## 附錄 B：常見問題排除

### Q：PDF 出現亂碼方塊
**A**：Edge 渲染引擎支援 `Microsoft JhengHei`，確認 CSS 字體設定包含：
```css
font-family: "Microsoft JhengHei", "微軟正黑體", Arial, sans-serif;
```

### Q：md-to-pdf 指令卡住不動
**A**：md-to-pdf 第一次執行會嘗試下載 Chromium，在沒有直連網路的環境下會無限等待。  
改用本專案已測試過的方法：
```powershell
$env:NODE_PATH = "C:\Users\User\AppData\Roaming\npm\node_modules"
node "C:\tmp\SHIHWEI\reports\md_to_pdf.js" "input.md" "output.pdf"
```

### Q：HTML Dashboard 在 GitHub Pages 圖表不顯示
**A**：確認 `<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js">` 是 HTTPS URL 且版本存在。

### Q：搜尋不到該股票的完整財報資料
**A**：優先查 `ir.【公司domain】.com` → press releases → 最近一筆財報新聞稿。  
備用：SEC EDGAR → `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=【代碼】&type=10-Q`

---

## 附錄 C：ONDS Dashboard 製作時間記錄（參考）

| 步驟 | 耗時 | 工具 |
|------|------|------|
| 研究 ONDS 基本資訊（5 次 WebSearch）| ~3 分鐘 | WebSearch |
| 撰寫 Markdown 分析報告 | ~2 分鐘 | Write |
| 轉換 PDF（安裝 puppeteer-core + 執行）| ~5 分鐘 | Node.js + Edge |
| 閱讀 PGY Dashboard 原始碼（分析設計語言）| ~2 分鐘 | Read |
| 撰寫 ONDS Dashboard HTML（完整客製化）| ~5 分鐘 | Write |
| **全程合計** | **~17 分鐘** | — |

---

*本樣板由 Claude AI 根據 ONDS Dashboard 製作過程整理，版本 1.0（2026-05-16）*
