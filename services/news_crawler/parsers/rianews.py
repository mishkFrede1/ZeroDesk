from config import RIANEWS_CATEGORIES
from parsers.rss_parser import RSSParser


class RiaNewsParser(RSSParser):
    sys_name = "RIA NEWS"
    categories = RIANEWS_CATEGORIES
    text_in_div = True
    articles_per_category = 4
    text_in_div_class = 'article__text'
    article_main_object_find_type = "class"
    article_main_object = "layout-article__600-align"
    bad_blocks = [".article__article, .color-font-hover-only, .m-image"]
    bad_img_patterns = ["loader", "tns-counter", "yandex.ru"]

    @staticmethod
    def extra_validation_element(article_html, element):
        try:
            if element.get("class") is not None:
                if element.get("class")[0] == "article__text":
                    article_html += f"<p>{element.get_text(strip=True)}</p>\n"
                    return article_html
            return False
        except:
            return False

    # @staticmethod
    # def extra_validation_p(element):
    #     if list(element.children) and any(child.name for child in element.children):
    #         return False
    #     return True
    #
    # def extra_validation_img(self, element, src):
    #     if self.check_class(element.get("class"), ["m"]):
    #         return False
    #     return True
