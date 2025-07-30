from parsers import bbc, foxnews, booooooom
from parsers.main_parser import parse_all_sources

def general_parsers_assert(articles_list):
    assert isinstance(articles_list, list)
    assert len(articles_list) > 0
    for article in articles_list:
        assert isinstance(article, dict)
        assert 'guid' in article
        assert 'html' in article
        assert 'category' in article
        assert 'source' in article

def test_bbc_parser():
    general_parsers_assert(bbc.BBCParser().parse_all(0, False))

def test_foxnews_parser():
    general_parsers_assert(foxnews.FoxNewsParser().parse_all(0, False))

def test_booooooom_parser():
    general_parsers_assert(booooooom.BooooooomParser().parse_all(0, False))

def test_parse_all_sources():
    general_parsers_assert(parse_all_sources(0, False))

