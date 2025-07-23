from parsers import bbc, foxnews, booooooom, menshealth, artnews

def general_parsers_assert(articles_list):
    assert isinstance(articles_list, list)
    assert len(articles_list) > 0
    for article in articles_list:
        assert isinstance(article, dict)
        assert 'guid' in article
        assert 'html' in article
        assert 'category' in article
        assert 'source' in article

def test_bbc_parser_returns():
    general_parsers_assert(bbc.BBCParser().parse_all(0, False))

def test_foxnews_parser_returns():
    general_parsers_assert(foxnews.FoxNewsParser().parse_all(0, False))

def test_menshealth_parser_returns():
    general_parsers_assert(menshealth.MenshealthParser().parse_all(0, False))

def test_booooooom_parser_returns():
    general_parsers_assert(booooooom.BooooooomParser().parse_all(0, False))

def test_artnews_parser_returns():
    general_parsers_assert(artnews.ArtNewsParser().parse_all(0, False))


