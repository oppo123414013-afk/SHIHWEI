import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "bot.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            post_id TEXT UNIQUE,
            ticker TEXT,
            market TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS replied_comments (
            id INTEGER PRIMARY KEY,
            comment_id TEXT UNIQUE,
            post_id TEXT,
            replied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS posted_tickers (
            ticker TEXT PRIMARY KEY,
            last_posted TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_post(post_id, ticker, market, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO posts (post_id, ticker, market, content) VALUES (?, ?, ?, ?)",
        (post_id, ticker, market, content)
    )
    c.execute(
        "INSERT OR REPLACE INTO posted_tickers (ticker, last_posted) VALUES (?, ?)",
        (ticker, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def is_comment_replied(comment_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM replied_comments WHERE comment_id = ?", (comment_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def mark_comment_replied(comment_id, post_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO replied_comments (comment_id, post_id) VALUES (?, ?)",
        (comment_id, post_id)
    )
    conn.commit()
    conn.close()

def get_recent_posts(limit=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT post_id, ticker, content FROM posts ORDER BY created_at DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def get_recently_posted_tickers(days=60):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT ticker FROM posted_tickers WHERE last_posted > datetime('now', ?)",
        (f'-{days} days',)
    )
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]
