# 專案檔案結構

**最後更新：** 2026-05-16
**專案根目錄：** `C:\Users\User\Desktop\my project`
**GitHub 倉庫：** `https://github.com/oppo123414013-afk/pgy-monitor`
**網站網址：** `https://oppo123414013-afk.github.io/pgy-monitor/pagaya/`

---

## 📁 完整樹狀結構

```
my project/
│
├── 📄 .gitignore                          ← Git 排除規則（.env、.bak、.claude/）
├── 📄 ARCHITECTURE.md                     ← 架構說明文件
├── 📄 README.md                           ← 專案說明
├── 📄 ARCHITECTURE.md                     ← 架構說明
├── 📄 index.html                          ← 網站根頁面
├── 📄 search.html                         ← 搜尋頁面
├── 📄 _redirects                          ← Netlify 路由規則（根目錄）
├── 📄 檔案結構MD.md                        ← 本檔案（結構紀錄）
│
├── 🌐 pagaya/                             ← GitHub Pages 網站目錄（部署用）
│   ├── 📄 pgy_live_dashboard.html         ← PGY 即時監控儀表板
│   ├── 📄 reports.html                    ← PGY 每日報告列表頁（動態載入）
│   ├── 📄 ai_debate.json                  ← AI 辯論數據
│   └── 📄 _redirects                      ← Netlify proxy 規則（/api/quote/ 等）
│
├── 📊 Pagaya_Daily/                       ← PGY 每日報告數據（GitHub API 依賴，勿移動）
│   ├── 📁 reports/                        ← ✅ 最終 MD 報告（網站讀取來源）
│   │   ├── 2026-04-24_report.md
│   │   ├── 2026-04-25_report.md
│   │   ├── 2026-04-30_report.md
│   │   ├── 2026-05-01_report.md
│   │   ├── 2026-05-02_report.md
│   │   ├── 2026-05-03_report.md
│   │   ├── 2026-05-04_report.md
│   │   ├── 2026-05-05_report.md
│   │   ├── 2026-05-06_report.md
│   │   ├── 2026-05-07_report.md
│   │   ├── 2026-05-08_report.md
│   │   ├── 2026-05-09_report.md
│   │   ├── 2026-05-10_report.md
│   │   ├── 2026-05-11_report.md
│   │   ├── 2026-05-12_report.md
│   │   ├── 2026-05-14_report.md
│   │   ├── 2026-05-15_report.md
│   │   └── 2026-05-16_report.md           ← 最新報告（共 18 份）
│   │
│   ├── 📁 pdf/                            ← PDF 版本（與 reports/ 對應）
│   │   ├── 2026-04-24_report.pdf
│   │   ├── 2026-04-25_report.pdf
│   │   ├── 2026-04-30_report.pdf
│   │   ├── 2026-05-01_report.pdf
│   │   ├── 2026-05-02_report.pdf
│   │   ├── 2026-05-03_report.pdf
│   │   ├── 2026-05-04_report.pdf
│   │   ├── 2026-05-05_report.pdf
│   │   ├── 2026-05-06_report.pdf
│   │   ├── 2026-05-07_report.pdf
│   │   ├── 2026-05-08_report.pdf
│   │   ├── 2026-05-09_report.pdf
│   │   ├── 2026-05-10_report.pdf
│   │   ├── 2026-05-11_report.pdf
│   │   ├── 2026-05-12_report.pdf
│   │   ├── 2026-05-14_report.pdf
│   │   ├── 2026-05-15_report.pdf
│   │   └── 2026-05-16_report.pdf          ← 共 18 份
│   │
│   └── 📁 raw/                            ← 原始資料（Claude 產出前的素材）
│       ├── 2026-04-24_raw.md … 2026-05-16_raw.md （共 18 份，缺 05-13）
│
├── 🏛️ Trump_Daily/                        ← 川普每日報告
│   ├── 📁 reports/                        ← MD 報告
│   │   ├── trump_daily_2026-04-22.md
│   │   ├── trump_daily_2026-04-23.md
│   │   ├── trump_daily_2026-04-24.md
│   │   ├── trump_daily_2026-04-25.md
│   │   ├── trump_daily_2026-04-26.md
│   │   ├── trump_daily_2026-04-27.md
│   │   ├── trump_daily_2026-04-28.md
│   │   ├── trump_daily_2026-04-29.md
│   │   ├── trump_daily_2026-04-30.md
│   │   ├── trump_daily_2026-05-01.md
│   │   ├── trump_daily_2026-05-02.md
│   │   ├── trump_daily_2026-05-03.md
│   │   ├── trump_daily_2026-05-04.md
│   │   ├── trump_daily_2026-05-05.md
│   │   ├── trump_daily_2026-05-06.md
│   │   ├── trump_daily_2026-05-07.md
│   │   ├── trump_daily_2026-05-08.md
│   │   ├── trump_daily_2026-05-09.md
│   │   ├── trump_daily_2026-05-10.md
│   │   ├── trump_daily_2026-05-11.md
│   │   ├── trump_daily_2026-05-12.md
│   │   ├── trump_daily_2026-05-13.md
│   │   ├── trump_daily_2026-05-14.md
│   │   ├── trump_daily_2026-05-15.md
│   │   └── trump_daily_2026-05-16.md      ← 最新（共 25 份）
│   │
│   └── 📁 pdf/                            ← PDF 版本
│       ├── trump_daily_2026-04-22.pdf … trump_daily_2026-05-15.pdf （共 24 份）
│
├── 🔬 research/                           ← 公司研究文件
│   ├── 📁 PGY/                            ← Pagaya 公司研究
│   │   ├── 01_company_profile.md          ← 公司概況
│   │   ├── 02_business_model.md           ← 商業模式
│   │   ├── 03_partners.md                 ← 合作夥伴清單
│   │   ├── 04_financials_2026.md          ← 2026 財務數據
│   │   ├── PGY_full_report_2026-05-11.html ← 完整報告（HTML）
│   │   └── README.md
│   │
│   └── 📁 engineering/                    ← 技術研究
│       ├── performance_guide.md           ← 效能指南
│       └── README.md
│
├── 🤖 scripts/                            ← 自動化腳本
│   ├── auto_upload_pgy.ps1                ← 自動上傳 PGY 報告
│   ├── report_generator_naive.py          ← 報告生成器（基礎版）
│   ├── report_generator_optimized.py      ← 報告生成器（優化版）
│   └── setup_task_scheduler.ps1           ← Windows 排程設定
│
├── 🧵 threads_bot/                        ← Threads 自動發文 Bot
│   ├── main.py                            ← 主程式入口
│   ├── analyzer.py                        ← 股票分析模組
│   ├── screener.py                        ← 股票篩選模組
│   ├── threads_api.py                     ← Threads API 封裝
│   ├── database.py                        ← 資料庫操作
│   ├── config.py                          ← 設定檔
│   ├── setup_credentials.py               ← 憑證設定工具
│   ├── test_connection.py                 ← 連線測試
│   ├── requirements.txt                   ← Python 套件清單
│   ├── install.bat                        ← 安裝腳本
│   ├── start_bot.bat                      ← 啟動腳本
│   ├── 取得憑證_點我執行.bat               ← 憑證取得（一鍵執行）
│   ├── .env.template                      ← 環境變數範本
│   └── .env                               ← 環境變數（含密鑰，已列入 .gitignore）
│
└── 📋 templates/                          ← 報告樣板
    ├── 股票樣板.md                         ← 完整版（含當日行情）
    └── 股票樣板(無日報).md                 ← 簡化版（週末/事件快報用）
```

---

## 📌 重要路徑說明

### 🌐 網站相關（GitHub Pages）

| 路徑 | 說明 | 注意 |
|------|------|------|
| `pagaya/pgy_live_dashboard.html` | 即時監控頁面 | WebSocket 連接 Yahoo Finance |
| `pagaya/reports.html` | 報告列表（動態） | 由 GitHub API 自動讀取 Pagaya_Daily/reports/ |
| `pagaya/_redirects` | API Proxy 規則 | Netlify 用，GitHub Pages 無效 |
| `index.html` | 網站根目錄 | |

### 📊 報告數據（GitHub API 依賴，路徑不可更動）

| 路徑 | 說明 | 命名規則 |
|------|------|----------|
| `Pagaya_Daily/reports/` | PGY MD 報告 | `YYYY-MM-DD_report.md` |
| `Pagaya_Daily/pdf/` | PGY PDF | `YYYY-MM-DD_report.pdf` |
| `Pagaya_Daily/raw/` | PGY 原始資料 | `YYYY-MM-DD_raw.md` |
| `Trump_Daily/reports/` | 川普 MD 報告 | `trump_daily_YYYY-MM-DD.md` |
| `Trump_Daily/pdf/` | 川普 PDF | `trump_daily_YYYY-MM-DD.pdf` |

### 🤖 Bot 憑證設定

`threads_bot/.env` 存放 Threads 帳號 Token，**不進入 git**。
初次使用需執行 `threads_bot/取得憑證_點我執行.bat`。

---

## 📅 更新記錄

| 日期 | 更新內容 |
|------|----------|
| 2026-05-16 | 初始版本：整理後的完整結構記錄 |

---

## 🔄 新增報告時的更新說明

每次新增日報後，請同步更新本檔案：

**PGY 新增一份報告（例如 2026-05-17）：**
1. `Pagaya_Daily/reports/` 新增 `2026-05-17_report.md`
2. `Pagaya_Daily/pdf/` 新增 `2026-05-17_report.pdf`
3. `Pagaya_Daily/raw/` 新增 `2026-05-17_raw.md`（選填）
4. 更新本檔案：在樹狀圖 reports/、pdf/、raw/ 各加一行，修改「最新報告」日期與數量

**川普新增一份報告（例如 2026-05-17）：**
1. `Trump_Daily/reports/` 新增 `trump_daily_2026-05-17.md`
2. `Trump_Daily/pdf/` 新增 `trump_daily_2026-05-17.pdf`
3. 更新本檔案：在樹狀圖 Trump_Daily/ 各加一行，修改數量

**新增資料夾或功能：**
在本檔案對應區塊加入新項目，並在「更新記錄」表格補上日期和說明。
