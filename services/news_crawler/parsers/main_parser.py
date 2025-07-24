from utils.logger import get_logger
from parsers.bbc import BBCParser
from parsers.foxnews import FoxNewsParser
from parsers.menshealth import MenshealthParser
from parsers.artnews import ArtNewsParser
from parsers.booooooom import BooooooomParser


logger = get_logger()
def parse_all_sources(articles_count: int, save_in_db=True):
    logger.info("[MAIN PARSER] Started parsing...")
    articles = []
    parsers = [BBCParser, FoxNewsParser, MenshealthParser, BooooooomParser, ArtNewsParser]
    for parser in parsers:
        articles += parser().parse_all(articles_count, save_in_db)
    return articles

