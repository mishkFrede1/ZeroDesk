from config import MENSHEALTH_CATEGORY
from parsers.rss_parser import RSSParser

class MenshealthParser(RSSParser):
    def parse_article_html(self, soup, guid: str):
        article_html = ""

        main_article = soup.find(attrs={"class": "standard-container content-container article-container css-1q1kaac et2g3wt3"})
        if not main_article:
            print("ERROR:", "Не удалось найти тег <article> -", guid)
            return None

        # self.delete_block_by_class(main_article, ".css-1tigmfy, .e94w1mj9")

        for element in main_article.descendants:
            if element.name == 'p':
                article_html += f"<p>{element.get_text(strip=True)}</p>\n"

            elif element.name == 'img':
                high_quality_src = self._get_max_quality_srcset(element, "*=")
                alt = element.get("alt", "")
                if high_quality_src:
                    img_tag = f'<img src="{high_quality_src}" alt="{alt}">\n'
                    article_html += img_tag
                # src = element.get("src", None)
                # if src:
                #     alt = element.get("alt", "")
                #     img_tag = f'<img src="{src}" alt="{alt}">\n'
                #     article_html += img_tag

        return article_html

def get_menshealth_parser():
    return MenshealthParser(
        sys_name="MENS HEALTH",
        categories=MENSHEALTH_CATEGORY,
        guid=True
    )