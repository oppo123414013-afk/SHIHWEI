import yfinance as yf
import requests
import logging
from database import get_recently_posted_tickers

log = logging.getLogger(__name__)

def _get_stock_info(ticker):
    try:
        s = yf.Ticker(ticker)
        info = s.info
        if not info or info.get('regularMarketPrice') is None:
            return None
        return {
            'ticker': ticker,
            'name': info.get('longName') or info.get('shortName', ticker),
            'price': info.get('currentPrice') or info.get('regularMarketPrice', 0),
            'market_cap': info.get('marketCap', 0),
            'pe': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'ev_ebitda': info.get('enterpriseToEbitda'),
            'revenue_growth': info.get('revenueGrowth'),
            'earnings_growth': info.get('earningsGrowth'),
            'gross_margin': info.get('grossMargins'),
            'operating_margin': info.get('operatingMargins'),
            'sector': info.get('sector', ''),
            'industry': info.get('industry', ''),
            'summary': (info.get('longBusinessSummary', '') or '')[:500],
            'analyst_count': info.get('numberOfAnalystOpinions', 0),
            'target_price': info.get('targetMeanPrice', 0),
            'short_ratio': info.get('shortRatio', 0),
        }
    except Exception as e:
        log.debug(f"無法取得 {ticker} 資料：{e}")
        return None

def screen_us_stocks():
    log.info("篩選美股（Finviz）...")
    recently_posted = get_recently_posted_tickers(days=60)

    try:
        from finvizfinance.screener.overview import Overview
        foverview = Overview()
        foverview.set_filter(filters_dict={
            'Market Cap.': 'Small ($300mln to $2bln)',
            'P/E': 'Under 20',
            'EPS growththis year': 'Over 15%',
            'Sales growthpast 5 years': 'Over 10%',
            'Analyst Recom.': 'Buy or Better',
            'Country': 'USA',
            'Option/Short': 'Optionable',
        })
        df = foverview.screener_view()
    except Exception as e:
        log.warning(f"Finviz 篩選失敗，使用備用清單：{e}")
        df = None

    if df is None or df.empty:
        # Fallback: curated small-cap watchlist
        tickers = ['HIMS', 'AEHR', 'CRCT', 'ELVN', 'ACMR', 'MGNI', 'AMBA', 'LPSN', 'TMDX', 'CLFD']
    else:
        tickers = df['Ticker'].tolist()[:20]

    candidates = []
    for ticker in tickers:
        if ticker in recently_posted:
            continue
        info = _get_stock_info(ticker)
        if info:
            info['market'] = 'US'
            # Filter: low analyst coverage = more undiscovered
            if (info['analyst_count'] or 0) <= 8:
                candidates.append(info)
                log.info(f"  美股候選：{ticker} | 分析師覆蓋：{info['analyst_count']}")

    log.info(f"美股篩選完成，找到 {len(candidates)} 支候選")
    return candidates

def screen_tw_stocks():
    log.info("篩選台股（TWSE）...")
    recently_posted = get_recently_posted_tickers(days=60)

    # Get all TWSE-listed stocks
    try:
        resp = requests.get(
            "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",
            timeout=15,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        all_stocks = resp.json()
    except Exception as e:
        log.warning(f"TWSE API 失敗：{e}")
        # Fallback to known small/mid caps
        all_stocks = [{'Code': c} for c in ['6452', '3037', '6669', '5483', '3042', '6533', '3293', '6510']]

    # Filter stock codes: 4-digit, skip ETFs and special issues
    codes = [s['Code'] for s in all_stocks if len(s.get('Code', '')) == 4 and s['Code'].isdigit()]

    candidates = []
    checked = 0
    for code in codes:
        if checked >= 80:
            break
        ticker = f"{code}.TW"
        if ticker in recently_posted:
            continue

        info = _get_stock_info(ticker)
        checked += 1

        if not info:
            continue

        mc = info['market_cap'] or 0
        pe = info['pe']
        rg = info['revenue_growth']

        # Filter criteria
        if not (3_000_000_000 <= mc <= 100_000_000_000):
            continue
        if pe is None or pe <= 0 or pe > 25:
            continue
        if rg is None or rg < 0.10:
            continue

        info['market'] = 'TW'
        candidates.append(info)
        log.info(f"  台股候選：{ticker} | PE:{pe:.1f} | 營收成長:{rg:.1%}")

    log.info(f"台股篩選完成，找到 {len(candidates)} 支候選")
    return candidates
