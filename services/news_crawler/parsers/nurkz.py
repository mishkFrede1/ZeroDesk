from config import NURKZ_CATEGORIES
from parsers.rss_parser import RSSParser


class NurKzParser(RSSParser):
    sys_name = "NUR KZ"
    categories = NURKZ_CATEGORIES
    article_main_object_find_type = "class"
    article_main_object = "article"
    bad_blocks = [".subscription", ".info-link-container, .astro-snohcbaj"]
    articles_per_category = 3