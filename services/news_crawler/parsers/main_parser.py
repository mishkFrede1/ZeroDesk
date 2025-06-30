from logger import get_logger
# from parsers.cnn import parse_all_cnn
from parsers.bbc import get_bbc_parser
from parsers.pcgamer import get_pcgamer_parser
from parsers.foxnews import get_foxnews_parser
from parsers.menshealth import get_menshealth_parser


logger = get_logger()
def parse_all_sources(articles_count: int):
    logger.info("[MAIN PARSER] Started parsing...")
    articles = []
    parsers = [get_bbc_parser, get_pcgamer_parser, get_foxnews_parser, get_menshealth_parser]
    for parser in parsers:
        articles += parser().parse_all(articles_count)
    return articles

