from bs4 import BeautifulSoup

from config import FOXNEWS_CATEGORIES
from parsers.rss_parser import RSSParser

class FoxNewsParser(RSSParser):
    article_main_object_find_type = "class"
    article_main_object_value = "article-body"

    def parse_article_html(self, article, guid: str):
        article_html = ""

        for bad_element in [".author-byline", ".featured, .featured-video, .video-ct", ".video-container", ".collection, .collection-multi"]:
            self.delete_block_by_class(article, bad_element)

        for element in article.descendants:
            if element.name == "p":
                if list(element.children) and any(child.name for child in element.children):
                    continue
                article_html += f"<p>{element.get_text(strip=True)}</p>\n"
            if element.name == "img":
                high_quality_src = self._get_max_quality_srcset(element)
                if "default" in high_quality_src or self.check_class(element.get("class"), ["m"]):
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