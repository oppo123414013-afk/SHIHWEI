"""
執行這個腳本確認所有 API 連線正常，再啟動機器人。
用法：python test_connection.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 50)
print("API 連線測試")
print("=" * 50)

# 1. Claude API
print("\n1. 測試 Claude API...")
try:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{"role": "user", "content": "回傳：連線成功"}]
    )
    print(f"   ✅ Claude API 正常：{resp.content[0].text.strip()}")
except Exception as e:
    print(f"   ❌ Claude API 失敗：{e}")

# 2. Threads API
print("\n2. 測試 Threads API...")
try:
    import requests
    token = os.getenv("THREADS_ACCESS_TOKEN")
    user_id = os.getenv("THREADS_USER_ID")
    resp = requests.get(
        f"https://graph.threads.net/v1.0/{user_id}",
        params={"fields": "id,username,threads_profile_picture_url", "access_token": token}
    )
    if resp.ok:
        data = resp.json()
        print(f"   ✅ Threads API 正常：帳號 @{data.get('username', 'unknown')}")
    else:
        print(f"   ❌ Threads API 失敗：{resp.text}")
except Exception as e:
    print(f"   ❌ Threads API 失敗：{e}")

# 3. yfinance
print("\n3. 測試 yfinance（抓一筆股價）...")
try:
    import yfinance as yf
    s = yf.Ticker("AAPL")
    price = s.info.get("currentPrice") or s.info.get("regularMarketPrice")
    print(f"   ✅ yfinance 正常：AAPL 現價 ${price}")
except Exception as e:
    print(f"   ❌ yfinance 失敗：{e}")

# 4. TWSE API
print("\n4. 測試 TWSE API（台股資料）...")
try:
    import requests
    resp = requests.get(
        "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",
        timeout=10, headers={"User-Agent": "Mozilla/5.0"}
    )
    count = len(resp.json())
    print(f"   ✅ TWSE API 正常：共 {count} 支股票")
except Exception as e:
    print(f"   ❌ TWSE API 失敗：{e}")

print("\n" + "=" * 50)
print("測試完成！如果全部 ✅，執行 python main.py 啟動機器人")
print("=" * 50)
