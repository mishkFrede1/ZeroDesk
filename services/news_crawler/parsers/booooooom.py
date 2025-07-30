from config import BOOOOOOOM_CATEGORY
from parsers.rss_parser import RSSParser

class BooooooomParser(RSSParser):
    sys_name = "BOOOOOOOM"
    categories = BOOOOOOOM_CATEGORY
    article_main_object_find_type = "class"
    article_main_object_value = "single-post-container"
    bad_blocks = ["#widgetpost", ".yarpp, .yarpp-related, .yarpp-related-website, .yarpp-template-yarpp-template-booooooom"]
    bad_img_patterns = ["loader", "facebook"]
    articles_per_category = 2