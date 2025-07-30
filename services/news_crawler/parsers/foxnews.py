from config import FOXNEWS_CATEGORIES
from parsers.rss_parser import RSSParser


class FoxNewsParser(RSSParser):
    sys_name = "FOX NEWS"
    categories = FOXNEWS_CATEGORIES
    article_main_object_find_type = "class"
    article_main_object = "article-body"
    bad_blocks = [".author-byline", ".featured, .featured-video, .video-ct", ".video-container", ".collection, .collection-multi", ".slider-wrapper, .list-items", ".related-topics", ".video-container"]
    bad_img_patterns = ["default"]

    @staticmethod
    def extra_validation_p(element):
        if list(element.children) and any(child.name for child in element.children):
            return False
        return True

    def extra_validation_img(self, element, src):
        if self.check_class(element.get("class"), ["m"]):
            return False
        return True