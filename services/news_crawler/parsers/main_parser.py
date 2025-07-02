from logger import get_logger
# from parsers.cnn import parse_all_cnn
# from parsers.pcgamer import PcgamerParser
from parsers.bbc import BBCParser
from parsers.foxnews import FoxNewsParser
from parsers.menshealth import MenshealthParser


logger = get_logger()
def parse_all_sources(articles_count: int):
    logger.info("[MAIN PARSER] Started parsing...")
    articles = []
    parsers = [MenshealthParser, BBCParser, FoxNewsParser]
    for parser in parsers:
        articles += parser().parse_all(articles_count)
    return articles

