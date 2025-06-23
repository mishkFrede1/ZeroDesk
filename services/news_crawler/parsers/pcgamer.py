from datetime import datetime
from random import randint

import feedparser
import requests
from bs4 import BeautifulSoup

from config import HEADERS, PCGAMER_LINK
from database import is_article_exists, save_article
from .bbc import get_max_quality_image_url

def check_img_class(class_):
    if class_:
        return class_[0] in ['aspect-[--img-listing-aspect-ratio,16/9]', 'hawk-lazy-image-deal-widget', 'author__avatar', 'image-wrapped__image', 'image__image']
    return False

def parse_article(link, category):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    article_html = ""

    title_tag = soup.find("h1")
    if title_tag:
        title = f"<h1>{title_tag.get_text(strip=True)}</h1>\n"
        article_html += title

    article = soup.find(attrs={"class": "content-wrapper"})
    if not article:
        print("ERROR:", link)
        raise ValueError(f"Не удалось найти article-body")

    for element in article.descendants:
        if element.name == "p":
            article_html += f"<p>{element.get_text(strip=True)}</p>\n"
        if element.name == "h2":
            article_html += f"<h2>{element.get_text(strip=True)}</h2>\n"
        if element.name == "img":
            high_quality_src = get_max_quality_image_url(element)
            if "youtube" in high_quality_src or check_img_class(element.get("class")):
                continue
            alt = element.get("alt", "")
            if high_quality_src:
                article_html += f'<img src="{high_quality_src}" alt="{alt}" />'

    # CREATE HTML DEBUG FILE
    # with open(f"content_{category}_{randint(0, 100)}.html", "w", encoding="utf-8") as f:
    #     f.write(article_html.strip())

    save_article(link, title, datetime.now())

    html = article_html.strip()
    return {
        "guid": link,
        "html": html,
        "category": category,
        "source": "pcgamer"
    }

def parse_pcgamer_news(url, category, articles_count):
    feed = feedparser.parse(url)
    print("[PCGAMER PARSER]: Start parsing", category)

    articles = []
    for index, entry in enumerate(feed.entries):
        print("[PCGAMER PARSER]", entry.link, is_article_exists(entry.link))
        if "live-news" in entry.link or "videos" in entry.link or is_article_exists(entry.link):
            continue
        parsed_article = parse_article(entry.link, category)
        if parsed_article is not None: articles.append(parsed_article)
        if index >= articles_count: break
    return articles

def parse_all_pcgamer(articles_count: int):
    print("[PCGAMER PARSER]: Started parsing pcgamer...")
    articles = parse_pcgamer_news(PCGAMER_LINK["url"], PCGAMER_LINK["category"], articles_count)
    return articles
