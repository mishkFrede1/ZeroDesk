from sqlalchemy.exc import IntegrityError
from database.db import SessionLocal, ParsedArticle
from datetime import datetime

def is_article_exists(url: str) -> bool:
    with SessionLocal() as session:
        return session.query(ParsedArticle).filter(ParsedArticle.url == url).first() is not None

def save_article(url: str, title: str, published_at: datetime):
    with SessionLocal() as session:
        article = ParsedArticle(url=url, title=title, published_at=published_at)
        session.add(article)

        try:
            session.commit()
        except IntegrityError:
            session.rollback() # Article already exists

