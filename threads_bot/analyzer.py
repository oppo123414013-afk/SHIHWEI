import anthropic
import json
import logging
from config import CLAUDE_API_KEY, ANALYSIS_MODEL, REPLY_MODEL, ANALYST_PERSONA

log = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def select_best_stock(candidates):
    if not candidates:
        return None

    summary = []
    for c in candidates:
        summary.append({
            'ticker': c['ticker'],
            'name': c['name'],
            'market': c['market'],
            'pe': c['pe'],
            'ev_ebitda': c['ev_ebitda'],
            'revenue_growth': c['revenue_growth'],
            'earnings_growth': c['earnings_growth'],
            'analyst_count': c['analyst_count'],
            'market_cap_m': round((c['market_cap'] or 0) / 1_000_000, 0),
        })

    response = client.messages.create(
        model=ANALYSIS_MODEL,
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""以下是本週篩選出的股票候選清單（美股+台股）：

{json.dumps(summary, ensure_ascii=False, indent=2)}

請選出最值得本週深入分析的 1 支股票，選擇標準優先順序：
1. 估值最低估（EV/EBITDA 或 P/E 相對同業有明顯折價）
2. 成長確定性高（營收+獲利雙升）
3. 市場關注度最低（分析師覆蓋少）
4. 市值適中（不要太大，機構難以忽視才有催化劑）

只回傳 JSON，不要任何其他文字：
{{"selected_ticker": "XXXX", "reason": "30字以內理由"}}"""
        }]
    )

    try:
        text = response.content[0].text.strip()
        # Extract JSON if wrapped in markdown
        if '```' in text:
            text = text.split('```')[1].replace('json', '').strip()
        result = json.loads(text)
        selected_ticker = result['selected_ticker']
        log.info(f"Claude 選出：{selected_ticker} — {result['reason']}")

        for c in candidates:
            if c['ticker'] == selected_ticker or c['ticker'].startswith(selected_ticker):
                return c
        return candidates[0]
    except Exception as e:
        log.warning(f"解析選股結果失敗：{e}，使用第一候選")
        return candidates[0]

def generate_post(stock):
    market_label = "美股" if stock['market'] == 'US' else "台股"
    ticker_display = stock['ticker'].replace('.TW', '')

    response = client.messages.create(
        model=ANALYSIS_MODEL,
        max_tokens=2000,
        system=ANALYST_PERSONA,
        messages=[{
            "role": "user",
            "content": f"""請針對以下{market_label}股票撰寫一篇 Threads 分析發文（繁體中文）：

股票資料：
- 代號：{ticker_display}（{market_label}）
- 公司名稱：{stock['name']}
- 現價：{stock['price']}
- 市值：{round((stock['market_cap'] or 0) / 1_000_000, 0):,.0f} 百萬
- 本益比 P/E：{stock['pe']}
- EV/EBITDA：{stock['ev_ebitda']}
- 營收成長：{f"{stock['revenue_growth']:.1%}" if stock['revenue_growth'] else 'N/A'}
- 獲利成長：{f"{stock['earnings_growth']:.1%}" if stock['earnings_growth'] else 'N/A'}
- 毛利率：{f"{stock['gross_margin']:.1%}" if stock['gross_margin'] else 'N/A'}
- 分析師覆蓋數：{stock['analyst_count']} 家
- 分析師目標價：{stock['target_price']}
- 產業：{stock['industry']}
- 業務說明：{stock['summary']}

發文格式要求：
- 第一行：吸引人的標題（用 emoji，點出核心論點）
- 第二段：這支股票為什麼現在被低估？（具體數字）
- 第三段：成長飛輪在哪裡？未來 12 個月的催化劑？
- 第四段：主要風險（誠實列出 2-3 點）
- 第五段：目標區間與操作邏輯
- 結尾：2-3 個 hashtag（#低估值 #成長股 #價值投資 等）
- 總長度：400-550 字
- 語氣：像朋友分享研究心得，不是報告

直接輸出發文內容，不要有說明文字。"""
        }]
    )

    return response.content[0].text.strip()

def generate_reply(post_content, comment_text):
    response = client.messages.create(
        model=REPLY_MODEL,
        max_tokens=400,
        system=ANALYST_PERSONA,
        messages=[{
            "role": "user",
            "content": f"""你剛在 Threads 發了這篇股票分析文：
---
{post_content[:800]}
---

有人留言說：「{comment_text}」

請用繁體中文回覆這則留言。規則：
- 如果是問題 → 認真回答，可引用數據
- 如果是質疑 → 用邏輯或數據回應，承認合理的點
- 如果是讚美 → 簡短感謝，補充一個額外的觀察點
- 如果是無關留言 → 禮貌簡短回應
- 長度：50-150 字
- 不要說「作為AI」或任何暴露機器人身份的話
- 自然、有深度、像真人回覆

直接輸出回覆內容。"""
        }]
    )

    return response.content[0].text.strip()
