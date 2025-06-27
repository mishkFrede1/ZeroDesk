from types import NoneType

from bs4 import BeautifulSoup
from config import PCGAMER_CATEGORY
from parsers.rss_parser import RSSParser

bad_img_classes = ['aspect-[--img-listing-aspect-ratio,16/9]', 'hawk-lazy-image-deal-widget',
                   'author__avatar', 'image-wrapped__image', 'image__image',
                   "grid", "grid-cols-1", "gap-4", "mt-4", "mb-5",
                   "object-cover", "w-[--article-river-thumbnail-width,100px]", "flex-shrink-0"]

class PcgamerParser(RSSParser):
    def parse_article_html(self, soup: BeautifulSoup, guid: str):
        article_html = ""

        article = soup.find(attrs={"class": "content-wrapper"})
        if not article:
            print("ERROR:", guid)
            raise ValueError(f"Не удалось найти article-body")

        for element in article.descendants:
            if element.name == "p":
                article_html += f"<p>{element.get_text(strip=True)}</p>\n"
            if element.name == "h2":
                article_html += f"<h2>{element.get_text(strip=True)}</h2>\n"
            if element.name == "div" and self.check_class(element.get("class"), bad_img_classes):
                break
            if element.name == "img":
                high_quality_src = self._get_max_quality_srcset(element)
                if "youtube" in high_quality_src or self.check_class(element.get("class"), bad_img_classes):
                    continue
                alt = element.get("alt", "")
                if high_quality_src:
                    article_html += f'<img src="{high_quality_src}" alt="{alt}" />'
        return article_html

def get_pcgamer_parser():
    return PcgamerParser(
        sys_name="PCGAMER",
        categories=PCGAMER_CATEGORY,
        guid=False
    )


# def parse_article(link, category):
#     response = requests.get(link, headers=HEADERS)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     article_html = ""
#
#     title_tag = soup.find("h1")
#     if title_tag:
#         title = f"<h1>{title_tag.get_text(strip=True)}</h1>\n"
#         article_html += title
#
#     article = soup.find(attrs={"class": "content-wrapper"})
#     if not article:
#         print("ERROR:", link)
#         raise ValueError(f"Не удалось найти article-body")
#
#     for element in article.descendants:
#         if element.name == "p":
#             article_html += f"<p>{element.get_text(strip=True)}</p>\n"
#         if element.name == "h2":
#             article_html += f"<h2>{element.get_text(strip=True)}</h2>\n"
#         if element.name == "img":
#             high_quality_src = get_max_quality_image_url(element)
#             if "youtube" in high_quality_src or check_img_class(element.get("class")):
#                 continue
#             alt = element.get("alt", "")
#             if high_quality_src:
#                 article_html += f'<img src="{high_quality_src}" alt="{alt}" />'
#
#     # CREATE HTML DEBUG FILE
#     # with open(f"content_{category}_{randint(0, 100)}.html", "w", encoding="utf-8") as f:
#     #     f.write(article_html.strip())
#
#     save_article(link, title, datetime.now())
#
#     html = article_html.strip()
#     return {
#         "guid": link,
#         "html": html,
#         "category": category,
#         "source": "pcgamer"
#     }
#
# def parse_pcgamer_news(url, category, articles_count):
#     feed = feedparser.parse(url)
#     print("[PCGAMER PARSER]: Start parsing", category)
#
#     articles = []
#     index = 0
#     for entry in feed.entries:
#         print("[PCGAMER PARSER]", entry.link, is_article_exists(entry.link))
#         if "live-news" in entry.link or "videos" in entry.link or is_article_exists(entry.link):
#             continue
#         parsed_article = parse_article(entry.link, category)
#         if parsed_article is not None: articles.append(parsed_article)
#         if index >= articles_count: break
#         index += 1
#     return articles
#
# def parse_all_pcgamer(articles_count: int):
#     print("[PCGAMER PARSER]: Started parsing pcgamer...")
#     articles = parse_pcgamer_news(PCGAMER_LINK["url"], PCGAMER_LINK["category"], articles_count)
#     return articles
