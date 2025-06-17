import sqlite3
from datetime import datetime
from dotenv import dotenv_values

DB_PATH = dotenv_values('.env')["DB_PATH"]


def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS parsed_articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                published_at TEXT
            )
        ''')
        conn.commit()

def is_article_exists(url: str) -> bool:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM parsed_articles WHERE url = ?", (url,))
        return cur.fetchone() is not None

def save_article(url: str, title: str, published_at: datetime):
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO parsed_articles (url, title, published_at) VALUES (?, ?, ?)",
                (url, title, published_at.isoformat())
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # Уже существует — можно игнорировать или логировать
            pass