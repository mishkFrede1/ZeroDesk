from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup

from database.db import is_article_exists, save_article
from config import CNN_CATEGORIES


def parse_cnn_news(url: str, category: str, articles_count: int, guid=True):
    feed = feedparser.parse(url)
    print("[CNN PARSER]: Start parsing", category)

    articles = []
    if not guid:
        for index, entry in enumerate(feed.entries):
            if "live-news" in entry.link or is_article_exists(entry.link):
                continue

            parsed_article = parse_article(entry.link, category)
            if parsed_article is not None: articles.append(parsed_article)
            if index >= articles_count: break
    else:
        for index, entry in enumerate(feed.entries):
            if "live-news" in entry.guid or is_article_exists(entry.link):
                continue

            parsed_article = parse_article(entry.guid, category)
            if parsed_article is not None: articles.append(parsed_article)
            if index >= articles_count: break
    return articles

def parse_article(guid, category):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(guid, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # TITLE
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # CONTENT
    content_blocks = []
    container = soup.select_one("div.article__content-container")
    if container:
        for element in container.find_all(["p", "h2"]):
            if element.name == "p":
                content_blocks.append(f"<p>{element.get_text(strip=True)}</p>")
            elif element.name == "h2":
                content_blocks.append(f"<h2>{element.get_text(strip=True)}</h2>")
    if len(content_blocks) < 1: return None

    # IMAGES
    images = []
    for img in soup.find_all("img"):
        if img.get("class")[0] in ['byline__image', 'vossi-byline__image', 'personalized-recirc__image']:
            continue

        src = img.get("src")
        alt = img.get("alt", "")
        height = img.get("height", "")
        width = img.get("width", "")

        if height < 1000 or width < 1000:
            continue

        if src and "data:image" not in src:
            images.append(f'<img src="{src}" alt="{alt} | height={height}, width={width}"/>')

    # IN HTML
    html_content = f"<h1>{title}</h1>"
    html_content += "\n".join(content_blocks)
    html_content += "\n".join(images)

    # CREATE HTML DEBUG FILE
    # with open(f"content_{category}_{randint(0, 100)}.html", "w", encoding="utf-8") as f:
    #     f.write(html_content)

    save_article(guid, title, datetime.now())

    return {
        "guid": guid,
        "html": html_content,
        "category": category,
        "source": "cnn"
    }

def parse_all_cnn(articles_count: int):
    print("[CNN PARSER]: Started parsing cnn...")
    articles = []
    for category in CNN_CATEGORIES:
        articles += parse_cnn_news(category["url"], category["category"], articles_count, category["guid"])
    return articles

# all_cnn = parse_all_cnn(1)
# print(all_cnn, "\n", type(all_cnn), len(all_cnn))
#
# for article in all_cnn:
#     print(article["guid"], "\n", article["category"], "\n\n")