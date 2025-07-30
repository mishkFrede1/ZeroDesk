from config import BBC_CATEGORIES
from parsers.rss_parser import RSSParser


class BBCParser(RSSParser):
    sys_name = "BBC"
    categories = BBC_CATEGORIES
    article_main_object = "article"
    bad_blocks = [".sc-464f550b-2, .iEUdAz"]
    bad_url_patterns = ["live-news", "videos", "iplayer", "sounds"]
    bad_img_patterns = ["grey-placeholder"]
    guid = False

    @staticmethod
    def extra_validation_h2(element):
        if element.get("class")[0] not in ["sc-9d830f2a-3", "fWzToZ"]:
            return True
        return False

    # @staticmethod
    # def extra_validation_img(element, src):
    #     if "grey-placeholder" not in src:
    #         return True
    #     return False