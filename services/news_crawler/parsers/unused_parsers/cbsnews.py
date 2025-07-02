from config import CBSNEWS_CATEGORY
from parsers.rss_parser import RSSParser

class CBSNewsParser(RSSParser):
    sys_name = "CBS NEWS"
    categories = CBSNEWS_CATEGORY
    guid = False
    article_main_object_value = "article" # tag

