from bs4 import BeautifulSoup

from config import FOXNEWS_CATEGORIES
from parsers.rss_parser import RSSParser

class FoxNewsParser(RSSParser):
    def parse_article_html(self, soup: BeautifulSoup, guid: str):
        article_html = ""

        article = soup.find(attrs={"class": "article-body"})
        if not article:
            print("ERROR:", guid)
            raise ValueError(f"Не удалось найти article-body")

        for element in article.descendants:
            if element.name == "p":
                if list(element.children) and any(child.name for child in element.children):
                    continue
                article_html += f"<p>{element.get_text(strip=True)}</p>\n"
            if element.name == "img":
                high_quality_src = self._get_max_quality_srcset(element)
                if "default" in high_quality_src:
                    continue
                alt = element.get("alt", "")
                if high_quality_src:
                    article_html += f'<img src="{high_quality_src}" alt="{alt}" />'
        return article_html

def get_foxnews_parser():
    return FoxNewsParser(
        sys_name="FOX NEWS",
        categories=FOXNEWS_CATEGORIES,
        guid=True
    )