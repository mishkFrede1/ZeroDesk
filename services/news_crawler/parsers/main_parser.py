from utils.logger import get_logger
from parsers.bbc import BBCParser
from parsers.foxnews import FoxNewsParser
from parsers.booooooom import BooooooomParser


logger = get_logger()
def parse_all_sources(save_in_db=True):
    logger.info("[MAIN PARSER] Parsing all sources")
    articles = []

    parsers = [
        BBCParser(),
        FoxNewsParser(),
        BooooooomParser()
    ]

    for parser in parsers:
        articles += parser.parse_all(parser.articles_per_category, save_in_db)
    return articles

