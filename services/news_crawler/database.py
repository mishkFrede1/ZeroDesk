# import sqlite3
# from datetime import datetime
# import os
#
# # DB_PATH = os.environ["DB_PATH"]
# DB_PATH = os.path.join(os.path.dirname(__file__), os.environ.get("DB_PATH", "data/articles.db"))
#
#
# def get_connection():
#     return sqlite3.connect(DB_PATH)
#
# def init_db():
#     with sqlite3.connect(DB_PATH) as conn:
#         cur = conn.cursor()
#         cur.execute('''
#             CREATE TABLE IF NOT EXISTS parsed_articles (
#                 url TEXT PRIMARY KEY,
#                 title TEXT,
#                 published_at TEXT
#             )
#         ''')
#         conn.commit()
#
# def is_article_exists(url: str) -> bool:
#     with get_connection() as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT 1 FROM parsed_articles WHERE url = ?", (url,))
#         return cur.fetchone() is not None
#
# def save_article(url: str, title: str, published_at: datetime):
#     with get_connection() as conn:
#         cur = conn.cursor()
#         try:
#             cur.execute(
#                 "INSERT INTO parsed_articles (url, title, published_at) VALUES (?, ?, ?)",
#                 (url, title, published_at.isoformat())
#             )
#             conn.commit()
#         except sqlite3.IntegrityError:
#             # Уже существует — можно игнорировать или логировать
#             pass

from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_URL = os.getenv('POSTGRES_URL')

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

class ParsedArticle(Base):
    __tablename__ = 'parsed_article'

    url = Column(String, primary_key=True)
    title = Column(String)
    published_at = Column(DateTime)

def init_db():
    Base.metadata.create_all(bind=engine)