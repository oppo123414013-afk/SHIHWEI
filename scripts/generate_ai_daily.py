#!/usr/bin/env python3
"""
每日 AI 評語自動生成腳本
由 GitHub Actions 於每個交易日盤後自動執行
使用 Gemini API 生成四方評語、前5排行、AI辯論
"""

import os
import json
import re
from datetime import datetime, timezone, timedelta

import google.generativeai as genai
import yfinance as yf

# ── 股票清單 ──────────────────────────────────────────────────
STOCKS = {
    "PGY":  {"name": "Pagaya Technologies",   "sector": "AI信貸基礎設施", "target": 34.50, "color": "#58a6ff"},
    "ONDS": {"name": "Ondas Inc.",             "sector": "國防無人機",     "target": 19.83, "color": "#ffa657"},
    "FIG":  {"name": "Figma Inc.",             "sector": "設計SaaS",       "target": 50.50, "color": "#bc8cff"},
    "UPST": {"name": "Upstart Holdings",       "sector": "AI信貸平台",     "target": 45.84, "color": "#58a6ff"},
    "IREN": {"name": "IREN Limited",           "sector": "BTC挖礦/AI GPU", "target": 66.20, "color": "#ffa657"},
    "AXTI": {"name": "AXT Inc.",               "sector": "化合物半導體",   "target": 87.75, "color": "#3fb950"},
    "COHR": {"name": "Coherent Corp.",         "sector": "光電元件",       "target": 376.00,"color": "#00d4ff"},
    "UI":   {"name": "Ubiquiti Inc.",          "sector": "企業網路設備",   "target": 826.00,"color": "#d29922"},
    "KITT": {"name": "Nauticus Robotics",      "sector": "水下機器人",     "target": 2.55,  "color": "#58a6ff"},
    "INMB": {"name": "INmune Bio",             "sector": "神經炎症生技",   "target": 5.40,  "color": "#f85149"},
    "TTWO": {"name": "Take-Two Interactive",   "sector": "AAA電玩遊戲",    "target": 295.00,"color": "#bc8cff"},
}

# ── 取得即時股價 ──────────────────────────────────────────────
def fetch_prices():
    prices = {}
    for ticker, info in STOCKS.items():
        try:
            tk = yf.Ticker(ticker)
            hist = tk.history(period="2d")
            if not hist.empty:
                close = round(float(hist["Close"].iloc[-1]), 2)
                prev  = round(float(hist["Close"].iloc[-2]), 2) if len(hist) > 1 else close
                chg   = round((close - prev) / prev * 100, 2)
                upside = round((info["target"] - close) / close * 100, 1)
                prices[ticker] = {
                    "price":  close,
                    "prev":   prev,
                    "change": chg,
                    "target": info["target"],
                    "upside": upside,
                }
        except Exception as e:
            print(f"  ⚠️  {ticker} 價格取得失敗：{e}")
    return prices

# ── 建立 Gemini 提示 ───────────────────────────────────────────
def build_prompt(prices):
    tw = datetime.now(timezone(timedelta(hours=8)))
    date_str = tw.strftime("%Y-%m-%d")

    stock_lines = []
    for t, info in STOCKS.items():
        p = prices.get(t, {})
        price  = p.get("price",  "N/A")
        change = p.get("change", 0)
        upside = p.get("upside", 0)
        stock_lines.append(
            f"  {t} ({info['name']}, {info['sector']}): "
            f"現價${price} 漲跌{change:+.2f}% 分析師目標${info['target']} 上行空間{upside:+.1f}%"
        )
    stock_block = "\n".join(stock_lines)

    return f"""你是一個專業股票分析AI，今天是 {date_str}（美股盤後）。

以下是我追蹤的11支股票今日數據：
{stock_block}

請以繁體中文，生成一份嚴格符合以下 JSON 格式的每日報告。
只輸出 JSON，不要有任何其他文字、markdown 符號或說明。

JSON 格式要求：
{{
  "date": "{date_str}",
  "updateTime": "盤後 自動更新",
  "aiOpinions": {{
    "gpt": {{
      "name": "ChatGPT", "model": "GPT-4o", "icon": "🤖",
      "color": "#10a37f", "rating": "偏多或中性或審慎", "ratingColor": "g或bl或y",
      "summary": "100-120字的整體投資組合評語，提及具體股票代號",
      "highlight": "30-40字的核心觀點一句話"
    }},
    "grok": {{
      "name": "Grok", "model": "Grok 3", "icon": "⚡",
      "color": "#1da1f2", "rating": "偏多或中性或審慎", "ratingColor": "g或bl或y",
      "summary": "100-120字，Grok風格更激進看重動能",
      "highlight": "30-40字核心觀點"
    }},
    "gemini": {{
      "name": "Gemini", "model": "Gemini 1.5 Pro", "icon": "💎",
      "color": "#4285f4", "rating": "偏多或中性或審慎", "ratingColor": "g或bl或y",
      "summary": "100-120字，Gemini風格更重品質與風險",
      "highlight": "30-40字核心觀點"
    }},
    "claude": {{
      "name": "Claude", "model": "Sonnet 4.6", "icon": "🧬",
      "color": "#d4a054", "rating": "偏多或中性或審慎", "ratingColor": "g或bl或y",
      "summary": "100-120字，Claude風格審慎、重風險調整後報酬",
      "highlight": "30-40字核心觀點"
    }}
  }},
  "top5": [
    {{
      "rank": 1, "ticker": "股票代號", "name": "公司名稱",
      "price": 數字, "target": 數字, "upside": "+XX%",
      "consensus": "Buy/Strong Buy等", "stars": 1到5的整數,
      "aiScore": 60到99的整數, "color": "十六進位色碼",
      "reason": "60-80字說明為何此刻值得買入"
    }},
    {{ "rank": 2, ... }},
    {{ "rank": 3, ... }},
    {{ "rank": 4, ... }},
    {{ "rank": 5, ... }}
  ],
  "debate": {{
    "topic": "今日最具爭議的一支股票的辯題，20-30字",
    "positions": {{
      "gpt": {{ "stance": "立場標籤4-8字", "icon": "🤖", "stanceColor": "#10a37f或#d29922", "argument": "60-80字論點" }},
      "grok": {{ "stance": "立場標籤4-8字", "icon": "⚡", "stanceColor": "#3fb950或#ffa657", "argument": "60-80字論點" }},
      "gemini": {{ "stance": "立場標籤4-8字", "icon": "💎", "stanceColor": "#4285f4或#d29922", "argument": "60-80字論點" }},
      "claude": {{ "stance": "立場標籤4-8字", "icon": "🧬", "stanceColor": "#58a6ff或#d29922", "argument": "60-80字論點" }}
    }},
    "conclusion": "40-60字AI共識總結"
  }}
}}
"""

# ── 呼叫 Gemini 生成 ──────────────────────────────────────────
def generate_with_gemini(prompt):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(temperature=0.7),
        request_options={"timeout": 120},
    )
    return response.text.strip()

# ── 解析並驗證 JSON ───────────────────────────────────────────
def parse_json(raw):
    # 移除可能的 markdown code block
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    return json.loads(cleaned.strip())

# ── 主程式 ────────────────────────────────────────────────────
def main():
    print("📈 取得即時股價...")
    prices = fetch_prices()
    for t, p in prices.items():
        print(f"  {t}: ${p['price']} ({p['change']:+.2f}%)")

    print("\n🤖 呼叫 Gemini API 生成評語...")
    prompt = build_prompt(prices)
    raw = generate_with_gemini(prompt)

    print("\n📝 解析 JSON...")
    data = parse_json(raw)

    out_path = os.path.join(os.path.dirname(__file__), "..", "custom-stocks", "ai-daily.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 已寫入 ai-daily.json（{data['date']}）")

if __name__ == "__main__":
    main()
