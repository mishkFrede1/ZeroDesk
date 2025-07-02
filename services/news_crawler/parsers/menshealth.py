from config import MENSHEALTH_CATEGORY
from parsers.rss_parser import RSSParser

class MenshealthParser(RSSParser):
    sys_name = "MEN'S HEALTH"
    categories = MENSHEALTH_CATEGORY
    article_main_object_find_type = "class"
    article_main_object_value = "standard-container content-container article-container css-1q1kaac et2g3wt3"
    bad_blocks = [".css-1tigmfy, .e94w1mj9", ".css-19m4yzp, .e1jy25xv0", ".css-15qxeah, .e9dgbgx0", ".css-1ss7lvu, .eluqz9n10", ".css-65ak0v, .e1kgjrvy4", ".size-large, .align-center, .embed, .css-1mm65na, .e1ydkxnk0"]
    img_extra_split = True

    def extra_validation_img(self, element, src):
        for el in ["icons", "logos", "vidthumb"]:
            if el in src:
                return False
        return True