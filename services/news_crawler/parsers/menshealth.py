from config import MENSHEALTH_CATEGORY
from parsers.rss_parser import RSSParser

class MenshealthParser(RSSParser):
    article_main_object_find_type = "class"
    article_main_object_value = "standard-container content-container article-container css-1q1kaac et2g3wt3"

    def parse_article_html(self, article, guid: str):
        article_html = ""

        bad_blocks = [".css-1tigmfy, .e94w1mj9", ".css-19m4yzp, .e1jy25xv0"]
        for b in bad_blocks:
            self.delete_block_by_class(article, b)

        for element in article.descendants:
            if element.name == 'p':
                article_html += f"<p>{element.get_text(strip=True)}</p>\n"

            elif element.name == 'img':
                high_quality_src = self._get_max_quality_srcset(element, extra_split=True)
                alt = element.get("alt", "")
                if high_quality_src:
                    img_tag = f'<img src="{high_quality_src}" alt="{alt}">\n'
                    article_html += img_tag

        return article_html

def get_menshealth_parser():
    return MenshealthParser(
        sys_name="MENS HEALTH",
        categories=MENSHEALTH_CATEGORY,
        guid=True
    )