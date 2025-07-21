from parsers.rss_parser import RSSParser
from config import IGN_CATEGORY

class IGNParser(RSSParser):
    sys_name = "IGN"
    categories = IGN_CATEGORY
    guid = False
    images_from_content = True

    article_main_object_find_type = "class"
    article_main_object_value = "jsx-1779429293"
    bad_blocks = [".card, .jsx-1339469126, .jsx-1355461925, .box, .jsx-2627838217, .object-box"]
    bad_img_patterns = ["adchoices.png"]