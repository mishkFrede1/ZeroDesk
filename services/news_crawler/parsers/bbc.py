from bs4 import BeautifulSoup

from config import BBC_CATEGORIES
from parsers.rss_parser import RSSParser


class BBCParser(RSSParser):
    article_main_object_find_type = ""
    article_main_object_value = "article"

    def parse_article_html(self, article, guid: str):
        article_html = ""

        self.delete_block_by_class(article, ".sc-464f550b-2, .iEUdAz")

        for element in article.descendants:
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