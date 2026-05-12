# Engineering 研究索引

> 工程技術參考文件，適用於本專案的自動化腳本開發

---

## 文件清單

| 文件 | 內容摘要 |
|------|---------|
| [performance_guide.md](performance_guide.md) | 報告生成系統性能優化指南（5 大瓶頸 + 優化策略） |

---

## 對應腳本

| 腳本 | 說明 |
|------|------|
| [../../scripts/report_generator_naive.py](../../scripts/report_generator_naive.py) | 優化前版本（標注 5 個性能問題） |
| [../../scripts/report_generator_optimized.py](../../scripts/report_generator_optimized.py) | 優化後版本（asyncio + 快取 + 生成器） |
