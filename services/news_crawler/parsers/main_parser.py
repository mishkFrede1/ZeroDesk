# from parsers.cnn import parse_all_cnn
from parsers.bbc import parse_all_bbc
from parsers.pcgamer import parse_all_pcgamer


def parse_all_sources(articles_count: int):
    print("[MAIN PARSER] Started parsing...")
    articles = []
    # articles += parse_all_cnn(articles_count)
    # articles += parse_all_bbc(articles_count)
    articles += parse_all_pcgamer(articles_count)
    return articles