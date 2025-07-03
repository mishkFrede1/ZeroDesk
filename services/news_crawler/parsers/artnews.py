from config import ARTNEWS_CATEGORY
from parsers.rss_parser import RSSParser

class ArtNewsParser(RSSParser):
    sys_name = "ART NEWS"
    categories = ARTNEWS_CATEGORY
    article_main_object_value = "article"
    bad_blocks = [".article-related-links", ".o-card, .lrv-u-flex, .lrv-u-flex-direction-column, .lrv-u-height-100p, .u-color-brand-primary:hover"]
    bad_img_patterns = ["scorecardresearch", "quantserve"]