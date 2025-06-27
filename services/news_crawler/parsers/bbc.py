from bs4 import BeautifulSoup

from config import BBC_CATEGORIES

# def get_max_quality_image_url(img_tag):
#     # 1. Получаем srcset
#     srcset = img_tag.get("srcset")
#     if not srcset:
#         return img_tag.get("src")  # fallback
#
#     # 2. Парсим все варианты
#     candidates = []
#     for item in srcset.split(","):
#         parts = item.strip().split(" ")
#         if len(parts) == 2:
#             url, width = parts
#             try:
#                 width = int(width.rstrip("w"))
#                 candidates.append((width, url))
#             except ValueError:
#                 continue
#
#     # 3. Берем URL с максимальной шириной
#     if candidates:
#         candidates.sort(reverse=True)  # по ширине
#         return candidates[0][1]
#     return img_tag.get("src")
#
# def parse_article(guid, category):
#     response = requests.get(guid, headers=HEADERS)
#     soup = BeautifulSoup(response.content, "html.parser")
#
#     article_html = ""
#
#     # Заголовок <h1>
#     title_tag = soup.find("h1")
#     if title_tag:
#         title = f"<h1>{title_tag.get_text(strip=True)}</h1>\n"
#         article_html += title
#
#     main_article = soup.find("article")
#     if not main_article:
#         print("ERROR:", "Не удалось найти тег <article> -", guid)
#         return None
#
#     # Сбор всех нужных элементов по порядку
#     for element in main_article.descendants:
#         if element.name == 'h2':
#             if element.get("class")[0] not in ["sc-9d830f2a-3", "fWzToZ"]:
#                 article_html += f"<h2>{element.get_text(strip=True)}</h2>\n"
#
#         elif element.name == 'p':
#             article_html += f"<p>{element.get_text(strip=True)}</p>\n"
#
#         elif element.name == 'img':
#             high_quality_src = get_max_quality_image_url(element)
#             # src = element.get("src") or element.get("data-src")
#             alt = element.get("alt", "")
#             if high_quality_src:
#                 if "grey-placeholder" in high_quality_src: continue
#                 img_tag = f'<img src="{high_quality_src}" alt="{alt}">\n'
#                 article_html += img_tag
#
#
#     # CREATE HTML DEBUG FILE
#     # with open(f"content_{category}_{randint(0, 100)}.html", "w", encoding="utf-8") as f:
#     #     f.write(article_html.strip())
#
#     save_article(guid, title, datetime.now())
#     html = article_html.strip()
#     return {
#         "guid": guid,
#         "html": html,
#         "category": category,
#         "source": "bbc"
#     }
#
# def parse_bbc_news(url, category, articles_count):
#     feed = feedparser.parse(url)
#     print("[BBC PARSER]: Start parsing", category)
#
#     articles = []
#     index = 0
#     for entry in feed.entries:
#         print("[BBC PARSER]", entry.guid, is_article_exists(entry.guid))
#         if "live-news" in entry.guid or "videos" in entry.guid or is_article_exists(entry.guid):
#             continue
#         parsed_article = parse_article(entry.guid, category)
#         if parsed_article is not None: articles.append(parsed_article)
#         if index >= articles_count: break
#         index += 1
#     return articles
#
# def parse_all_bbc(articles_count: int):
#     print("[BBC PARSER]: Started parsing bbc...")
#     articles = []
#     for category in BBC_CATEGORIES:
#         articles += parse_bbc_news(category["url"], category["category"], articles_count)
#     return articles

from parsers.rss_parser import RSSParser

class BBCParser(RSSParser):
    def parse_article_html(self, soup: BeautifulSoup, guid: str):
        article_html = ""

        main_article = soup.find("article")
        if not main_article:
            print("ERROR:", "Не удалось найти тег <article> -", guid)
            return None

        for element in main_article.descendants:
            if element.name == 'h2':
                if element.get("class")[0] not in ["sc-9d830f2a-3", "fWzToZ"]:
                    article_html += f"<h2>{element.get_text(strip=True)}</h2>\n"

            elif element.name == 'p':
                article_html += f"<p>{element.get_text(strip=True)}</p>\n"

            elif element.name == 'img':
                high_quality_src = self._get_max_quality_srcset(element)
                alt = element.get("alt", "")
                if high_quality_src:
                    if "grey-placeholder" in high_quality_src: continue
                    img_tag = f'<img src="{high_quality_src}" alt="{alt}">\n'
                    article_html += img_tag

        return article_html

def get_bbc_parser():
    return BBCParser(
        sys_name="BBC",
        categories=BBC_CATEGORIES,
        guid=True
    )