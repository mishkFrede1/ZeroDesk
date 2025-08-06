from config import RBCNEWS_CATEGORIES
from parsers.rss_parser import RSSParser


class RbcNewsParser(RSSParser):
    sys_name = "RBC NEWS"
    categories = RBCNEWS_CATEGORIES
    article_main_object_find_type = "class"
    article_main_object = "l-col-center-590 article__content"
    bad_blocks = [".item-blocks-wrapper", ".article__inline-item, .js-material-card-with-rotation", ".article__special_container", ".article__footer-share", ".article__tabs-wrapper, .js-article-tabs-wrapper", ".social-networks, .js-social-networks, .js-yandex-counter"]
    articles_per_category = 3
    guid = False
