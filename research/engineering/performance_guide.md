# 性能優化指南 — 每日報告生成系統

> 建立時間：2026-05-11
> 適用場景：Python 自動化報告生成（抓取資料 → 處理 → 輸出 MD/PDF）

---

## 性能工程師的思考框架

```
測量 → 找瓶頸 → 優化 → 再測量
       （不要猜測，要量化）
```

---

## 一、已識別的瓶頸類型

### 瓶頸 1：串行 I/O（最常見、影響最大）

**問題**：逐一呼叫外部 API / 抓取網頁，等一個完成再做下一個

```python
# ❌ 慢：串行，總時間 = sum(每個請求時間)
for source in sources:
    data = requests.get(source)   # 每個等 2~5 秒
    results.append(data.json())
# 10 個來源 × 3 秒 = 30 秒
```

**優化方向**：改用 async/await 並行處理

```
串行：[→→→][→→→][→→→]  總共 30 秒
並行：[→→→]
      [→→→]             總共 3~5 秒
      [→→→]
```

---

### 瓶頸 2：重複讀寫相同檔案

```python
# ❌ 低效：每次迭代都開檔案
for item in data_list:
    with open("output.md", "a") as f:
        f.write(item)   # 每次都 flush + seek
```

**優化方向**：批次寫入，一次 I/O

---

### 瓶頸 3：PDF 生成記憶體洩漏

```python
# ❌ 危險：大量生成 PDF 時物件未釋放
pdfs = []
for report in reports:
    pdf = generate_pdf(report)   # 每個 PDF 佔 50~200MB
    pdfs.append(pdf)             # 全部留在記憶體
```

**優化方向**：逐一生成並立即寫入磁碟，不在記憶體堆積

---

### 瓶頸 4：無快取的重複請求

```python
# ❌ 浪費：每次執行都重新抓相同靜態資料
company_info = fetch_company_profile("PGY")   # 每天都一樣
```

**優化方向**：對不常變動的資料加 TTL 快取

---

## 二、優化策略對照表

| 問題 | 策略 | 預期加速 |
|------|------|---------|
| 串行 API 請求 | `asyncio` + `aiohttp` 並行 | **5–10x** |
| 重複讀檔 | 一次讀入記憶體，複用 | **2–5x** |
| 無快取 | `functools.lru_cache` / 檔案快取 | **∞**（避免重複工作） |
| 同步 PDF 生成 | `concurrent.futures.ProcessPoolExecutor` | **2–4x** |
| 記憶體堆積 | 生成器（Generator）模式 | 記憶體降 **60–80%** |
| 字串拼接 | `list.join()` 替代 `+=` | 小量但明顯 |

---

## 三、核心優化技術速查

### 技術 1：asyncio 並行 I/O

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)   # 全部並行
```

### 技術 2：生成器省記憶體

```python
# ❌ 全部載入記憶體
def get_all_reports():
    return [load_report(f) for f in files]   # 100 個 × 5MB = 500MB

# ✅ 用到才載入
def get_all_reports():
    for f in files:
        yield load_report(f)                 # 任何時刻只有 1 個在記憶體
```

### 技術 3：TTL 檔案快取

```python
import json, time
from pathlib import Path

def cached_fetch(key, fetch_fn, ttl=3600):
    cache_file = Path(f".cache/{key}.json")
    if cache_file.exists():
        data = json.loads(cache_file.read_text())
        if time.time() - data["_ts"] < ttl:
            return data["value"]             # 快取命中
    result = fetch_fn()
    cache_file.write_text(json.dumps({"value": result, "_ts": time.time()}))
    return result
```

### 技術 4：進程池 CPU 密集工作

```python
from concurrent.futures import ProcessPoolExecutor

def generate_pdfs_parallel(reports):
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(render_pdf, r) for r in reports]
        return [f.result() for f in futures]
```

---

## 四、性能量測工具

```python
import time
import tracemalloc

# 時間量測
start = time.perf_counter()
your_function()
print(f"耗時: {time.perf_counter() - start:.3f}s")

# 記憶體量測
tracemalloc.start()
your_function()
current, peak = tracemalloc.get_traced_memory()
print(f"峰值記憶體: {peak / 1024 / 1024:.1f} MB")
tracemalloc.stop()
```

---

## 五、報告生成系統性能目標

| 指標 | 優化前（估計） | 優化目標 |
|------|-------------|---------|
| 10 個來源並行抓取 | ~30 秒 | < 5 秒 |
| 峰值記憶體 | ~500MB | < 100MB |
| 每日完整執行時間 | ~5 分鐘 | < 60 秒 |
| 相同資料重複抓取 | 每次都抓 | 快取 1 小時內複用 |

---

## 相關文件

- 優化前完整範例：[`../../scripts/report_generator_naive.py`](../../scripts/report_generator_naive.py)
- 優化後完整範例：[`../../scripts/report_generator_optimized.py`](../../scripts/report_generator_optimized.py)
