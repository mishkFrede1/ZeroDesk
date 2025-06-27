# from parsers.cnn import parse_all_cnn
from parsers.bbc import get_bbc_parser
from parsers.pcgamer import get_pcgamer_parser


def parse_all_sources(articles_count: int):
    print("[MAIN PARSER] Started parsing...")
    articles = []
    # articles += parse_all_cnn(articles_count)
    articles += get_bbc_parser().parse_all(articles_count)
    articles += get_pcgamer_parser().parse_all(articles_count)
    return articles

