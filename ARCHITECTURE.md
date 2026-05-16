# 專案架構說明 — Clean Architecture

> 重構日期：2026-05-11
> 架構原則：關注點分離 · 模組化 · 低耦合

---

## 設計理念

本專案採用**分層清潔架構**，將「靜態研究知識」與「動態日報輸出」明確分離，確保：

- 研究資料可獨立更新，不影響報告格式
- 各領域模組（PGY、Trump）互不依賴
- 共享資源集中管理，避免重複

---

## 資料夾結構

```
my project/
│
├── ARCHITECTURE.md          ← 本文件
├── README.md                ← 專案總覽
│
├── shared/                  ── 共享資源層（Infrastructure）
│   └── styles/
│       └── report-style.css
│
├── research/                ── 研究資料層（Domain - Static Knowledge）
│   └── PGY/                 ← 每家公司一個子目錄
│       ├── README.md        ← 該公司研究索引
│       ├── 01_company_profile.md
│       ├── 02_business_model.md
│       ├── 03_partners.md
│       └── 04_financials_2026.md
│
├── pagaya/                  ── PGY 報告模組（Application）
│   └── daily/
│       ├── md/              ← Markdown 日報
│       └── pdf/             ← PDF 日報
│
└── trump/                   ── Trump 報告模組（Application）
    └── daily/
        ├── md/
        └── pdf/
```

---

## 三層架構說明

### Layer 1 — Domain（研究資料層）`research/`
- **職責**：儲存不隨時間快速變動的「基礎知識」
- **特性**：純文字、版本控制友好、可獨立閱讀
- **範例**：公司基本面、商業模式、合作夥伴名錄、年度財務基準

### Layer 2 — Application（報告輸出層）`pagaya/` `trump/`
- **職責**：依據 Domain 知識產生每日動態報告
- **特性**：按日期命名、同時提供 md 和 pdf 格式
- **命名規則**：`YYYY-MM-DD_report.md`

### Layer 3 — Infrastructure（共享資源層）`shared/`
- **職責**：跨模組共用的樣式、模板、工具
- **特性**：修改此層不影響任何業務邏輯

---

## 新增公司模組 SOP

1. 在 `research/` 下建立新公司子目錄（如 `research/TSLA/`）
2. 依序建立四份核心文件（01~04）
3. 在對應應用層建立日報資料夾（如 `tesla/daily/md/`）
4. 更新根目錄 `README.md` 的模組清單

---

## 舊結構 → 新結構 對照

| 舊路徑 | 新路徑 |
|--------|--------|
| `Pagaya_Daily/md/` | `pagaya/daily/md/` |
| `Pagaya_Daily/pdf_reports/` | `pagaya/daily/pdf/` |
| `Trump_Daily/md/` | `trump/daily/md/` |
| `Trump_Daily/pdf_reports/` | `trump/daily/pdf/` |
| `reports/trump/` | `trump/daily/` |
| `.report-style.css` | `shared/styles/report-style.css` |
| _(無)_ | `research/PGY/` ← **新增** |
