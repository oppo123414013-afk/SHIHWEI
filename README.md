# 仕瑋投資研究工作站

> 架構版本：Clean Architecture v2.0（2026-05-11 重構）
> 維護者：陳仕瑋

---

## 專案用途

個人投資研究與每日市場報告系統，追蹤：
- **Pagaya Technologies (PGY)**：AI 信貸基礎設施公司每日動態
- **Trump 政治動態**：影響市場的政治事件每日追蹤

---

## 資料夾結構

```
my project/
│
├── README.md              ← 本文件
├── ARCHITECTURE.md        ← 架構設計說明
│
├── shared/                ── 共享資源
│   └── styles/
│       └── report-style.css
│
├── research/              ── 靜態研究知識庫
│   └── PGY/               ← Pagaya 深度研究（基本面 / 商模 / 夥伴 / 財務）
│
├── pagaya/                ── PGY 每日報告
│   └── daily/
│       ├── md/            ← Markdown 格式
│       └── pdf/           ← PDF 格式
│
└── trump/                 ── 川普動態每日報告
    └── daily/
        ├── md/
        └── pdf/
```

---

## 模組說明

### `research/` — 知識庫（靜態）
公司基本面、商業模式、合作夥伴名錄、財務數據基準。
不隨日期變動，是撰寫每日報告的「底稿知識層」。

| 子目錄 | 說明 |
|--------|------|
| `research/PGY/` | Pagaya 完整研究（4 份核心文件） |

### `pagaya/daily/` — PGY 每日報告（動態）
每日更新，記錄股價、事件、技術面、資金面。

### `trump/daily/` — 川普動態每日報告（動態）
每日更新，記錄重要政策宣示、市場影響。

---

## 報告命名規則

```
YYYY-MM-DD_report.md     ← Pagaya 日報
trump_daily_YYYY-MM-DD.md ← 川普日報
```

---

## 架構文件

詳細架構設計說明見 [ARCHITECTURE.md](ARCHITECTURE.md)
