"""
report_generator_naive.py — 優化前版本

問題清單（性能工程師視角）：
  [P1] 串行 HTTP 請求 — 10 個來源需 ~30 秒
  [P2] 無快取 — 每次執行重複抓相同靜態資料
  [P3] 字串 += 拼接 — O(n²) 記憶體操作
  [P4] 全部 PDF 堆在記憶體 — 峰值記憶體 ~500MB
  [P5] 每次迭代都重新開檔案 — 無謂的系統呼叫
"""

import requests
import json
import time
from pathlib import Path
from datetime import date


# ── 資料來源設定 ──────────────────────────────────────────────
DATA_SOURCES = {
    "stock_price":    "https://api.example.com/stock/PGY/price",
    "news_feed":      "https://api.example.com/news/PGY",
    "earnings":       "https://api.example.com/earnings/PGY",
    "partners":       "https://api.example.com/partners/PGY",
    "sec_filings":    "https://api.example.com/sec/PGY",
    "analyst_rating": "https://api.example.com/ratings/PGY",
    "short_interest": "https://api.example.com/short/PGY",
    "options_flow":   "https://api.example.com/options/PGY",
    "macro_data":     "https://api.example.com/macro",
    "trump_news":     "https://api.example.com/trump/news",
}


# ── [P1] 串行 HTTP 請求（最大瓶頸）──────────────────────────────
def fetch_all_data():
    results = {}
    for name, url in DATA_SOURCES.items():
        print(f"Fetching {name}...")
        response = requests.get(url, timeout=10)   # 每個等 2~5 秒，無並行
        results[name] = response.json()
        time.sleep(0.5)                            # 無意義的等待
    return results
    # 總時間：~30 秒


# ── [P2] 無快取，每次重新抓靜態資料 ──────────────────────────────
def get_company_profile():
    response = requests.get("https://api.example.com/company/PGY")  # 每天結果一樣
    return response.json()


# ── [P3] 字串 += 拼接 O(n²) ──────────────────────────────────
def build_markdown_report(data):
    report = ""
    report += f"# PGY 每日報告 {date.today()}\n\n"
    report += "## 股價\n"
    report += f"收盤：${data['stock_price']['close']}\n"
    report += f"漲跌：{data['stock_price']['change']}%\n\n"

    report += "## 新聞\n"
    for news_item in data["news_feed"]["items"]:
        report += f"- {news_item['title']}\n"         # 每次 += 都複製整個字串
        report += f"  來源：{news_item['source']}\n"
        report += f"  時間：{news_item['time']}\n"

    report += "## 分析師評級\n"
    for rating in data["analyst_rating"]["ratings"]:
        report += f"- {rating['firm']}: {rating['rating']} PT ${rating['target']}\n"

    return report


# ── [P4] 全部 PDF 堆在記憶體 ──────────────────────────────────
def generate_all_pdfs(report_texts):
    pdf_objects = []
    for text in report_texts:
        pdf = render_to_pdf(text)          # 假設每個 ~100MB
        pdf_objects.append(pdf)            # 全部留在記憶體，峰值 = N × 100MB

    for i, pdf in enumerate(pdf_objects):
        with open(f"output_{i}.pdf", "wb") as f:
            f.write(pdf)
    return pdf_objects


# ── [P5] 每次迭代都重新開檔案 ─────────────────────────────────
def save_news_items(news_items):
    for item in news_items:
        with open("news_log.txt", "a") as f:   # 每次都 open/close
            f.write(f"{item['title']}\n")


# ── 主程序 ─────────────────────────────────────────────────
def main():
    start = time.time()

    # 串行抓取所有資料（~30 秒）
    all_data = fetch_all_data()

    # 每次都重新抓公司資料（無快取）
    company = get_company_profile()

    # 低效字串拼接
    report_md = build_markdown_report(all_data)

    # 全部 PDF 塞進記憶體
    generate_all_pdfs([report_md])

    # 每次都重新開檔案
    save_news_items(all_data.get("news_feed", {}).get("items", []))

    print(f"完成，耗時：{time.time() - start:.1f}s")


def render_to_pdf(text):
    """模擬 PDF 渲染（實際實作依套件而定）"""
    return text.encode("utf-8")


if __name__ == "__main__":
    main()
