import time
import logging
import schedule

from database import init_db, save_post, get_recent_posts, is_comment_replied, mark_comment_replied
from screener import screen_us_stocks, screen_tw_stocks
from analyzer import select_best_stock, generate_post, generate_reply
from threads_api import create_post, get_replies, reply_to_comment
from config import POST_TIME, REPLY_CHECK_HOURS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def job_post():
    log.info("=" * 50)
    log.info("開始本週選股發文任務")
    try:
        us = screen_us_stocks()
        tw = screen_tw_stocks()
        all_candidates = us + tw
        log.info(f"共找到 {len(all_candidates)} 支候選（美股 {len(us)}，台股 {len(tw)}）")

        if not all_candidates:
            log.warning("本週無符合條件股票，略過發文")
            return

        selected = select_best_stock(all_candidates)
        if not selected:
            log.warning("無法選出最佳股票")
            return

        log.info(f"本週主角：{selected['ticker']} — {selected['name']}")
        content = generate_post(selected)
        log.info(f"發文內容已生成（{len(content)} 字）")

        post_id = create_post(content)
        save_post(post_id, selected["ticker"], selected["market"], content)
        log.info("任務完成！")

    except Exception as e:
        log.error(f"發文任務失敗：{e}", exc_info=True)


def job_reply():
    log.info("檢查新留言...")
    try:
        posts = get_recent_posts(limit=5)
        if not posts:
            return

        for post_id, ticker, post_content in posts:
            replies = get_replies(post_id)
            for reply in replies:
                cid = reply.get("id")
                text = reply.get("text", "").strip()
                if not cid or not text:
                    continue
                if is_comment_replied(cid):
                    continue

                log.info(f"新留言 [{ticker}]：{text[:60]}...")
                reply_text = generate_reply(post_content, text)
                reply_to_comment(cid, reply_text)
                mark_comment_replied(cid, post_id)
                log.info(f"已回覆：{reply_text[:60]}...")
                time.sleep(5)

    except Exception as e:
        log.error(f"回覆檢查失敗：{e}", exc_info=True)


def main():
    init_db()
    log.info("AI 選股機器人啟動！")

    # 發文排程：每週一/三/五 晚上 8 點
    schedule.every().monday.at(POST_TIME).do(job_post)
    schedule.every().wednesday.at(POST_TIME).do(job_post)
    schedule.every().friday.at(POST_TIME).do(job_post)

    # 回覆排程：每 2 小時
    schedule.every(REPLY_CHECK_HOURS).hours.do(job_reply)

    log.info(f"排程：每週一/三/五 {POST_TIME} 發文 | 每 {REPLY_CHECK_HOURS} 小時檢查留言")
    log.info("按 Ctrl+C 停止")

    # 啟動時立即檢查一次留言
    job_reply()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
