HEADERS = {"User-Agent": "Mozilla/5.0"}

CATEGORIES = {
    "health": "Health",
    "business": "Business",
    "entertainment": "Entertainment",
    "video_games": "Video Games",
    "world": "World",
    "culture_and_art": "Culture and art",
    "sport": "Sport",
    "science": "Science",
    "technology": "Technology",
    "society": "Society",
    "politics": "Politics",
    "none": "None",
}

RBCNEWS_CATEGORIES = [
    {
        "url": "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",
        "category": CATEGORIES["none"],
    }
]

NURKZ_CATEGORIES = [
    {
        "url": "https://www.nur.kz/rss/all.rss",
        "category": CATEGORIES["none"],
    }
]

RIANEWS_CATEGORIES = [
    {
        "url": "https://ria.ru/export/rss2/archive/index.xml",
        "category": CATEGORIES["none"],
    }
]

BOOOOOOOM_CATEGORY = [
    {
        "url": "https://www.booooooom.com/feed/",
        "category": CATEGORIES["culture_and_art"],
    }
]

FOXNEWS_CATEGORIES = [
    {
        "url": "https://moxie.foxnews.com/google-publisher/world.xml",
        "category": CATEGORIES["world"]
    },
    {
        "url": "https://moxie.foxnews.com/google-publisher/politics.xml",
        "category": CATEGORIES["politics"]
    },
    {
        "url": "https://moxie.foxnews.com/google-publisher/science.xml",
        "category": CATEGORIES["science"]
    },
    {
        "url": "https://moxie.foxnews.com/google-publisher/health.xml",
        "category": CATEGORIES["health"]
    },
    {
        "url": "https://moxie.foxnews.com/google-publisher/travel.xml",
        "category": CATEGORIES["world"]
    },
    {
        "url": "https://moxie.foxnews.com/google-publisher/sports.xml",
        "category": CATEGORIES["sport"]
    },
    {
        "url": "https://moxie.foxnews.com/google-publisher/tech.xml",
        "category": CATEGORIES["technology"]
    }
]

BBC_CATEGORIES = [
    {
        "url": "http://feeds.bbci.co.uk/news/rss.xml",
        "category": CATEGORIES["none"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "category": CATEGORIES["world"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/business/rss.xml",
        "category": CATEGORIES["business"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/politics/rss.xml",
        "category": CATEGORIES["politics"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/health/rss.xml",
        "category": CATEGORIES["health"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/education/rss.xml",
        "category": CATEGORIES["society"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "category": CATEGORIES["science"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "category": CATEGORIES["technology"]
    },
    {
        "url": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        "category": CATEGORIES["none"]
    }
]

# CBSNEWS_CATEGORY = [
#     {
#         "url": "https://www.cbsnews.com/latest/rss/politics",
#         "category": CATEGORIES["politics"],
#     },
#     {
#         "url": "https://www.cbsnews.com/latest/rss/entertainment",
#         "category": CATEGORIES["entertainment"],
#     },
#     {
#         "url": "https://www.cbsnews.com/latest/rss/world",
#         "category": CATEGORIES["world"],
#     },
#     {
#         "url": "https://www.cbsnews.com/latest/rss/technology",
#         "category": CATEGORIES["technology"],
#     },
#     {
#         "url": "https://www.cbsnews.com/latest/rss/science",
#         "category": CATEGORIES["science"],
#     },
#     {
#         "url": "https://www.cbsnews.com/latest/rss/health",
#         "category": CATEGORIES["health"],
#     },
#     {
#         "url": "https://www.cbsnews.com/latest/rss/space",
#         "category": CATEGORIES["none"],
#     },
# ]

# PCGAMER_CATEGORY = [
#     {
#         "url": "https://www.pcgamer.com/rss/",
#         "category": CATEGORIES["video_games"]
#     }
# ]

# MENSHEALTH_CATEGORY = [
#     {
#         "url": "https://www.menshealth.com/rss/all.xml/",
#         "category": CATEGORIES["health"]
#     }
# ]

# IGN_CATEGORY = [
#     {
#         "url": "https://feeds.feedburner.com/ign/news",
#         "category": CATEGORIES["video_games"],
#     }
# ]

# ARTNEWS_CATEGORY = [
#     {
#         "url": "https://www.artnews.com/feed/",
#         "category": CATEGORIES["culture_and_art"],
#     }
# ]

# CNN_CATEGORIES = [
#     {
#         "url": "http://rss.cnn.com/rss/cnn_topstories.rss",
#         "category": "None",
#         "guid": True
#     },
#     {
#         "url": "http://rss.cnn.com/rss/cnn_world.rss",
#         "category": "World",
#         "guid": True
#     },
#     {
#         "url": "http://rss.cnn.com/rss/cnn_showbiz.rss",
#         "category": "World",
#         "guid": True
#     },
#     {
#         "url": "http://rss.cnn.com/rss/cnn_allpolitics.rss",
#         "category": "politics",
#         "guid": True
#     },
#     {
#         "url": "http://rss.cnn.com/rss/cnn_tech.rss",
#         "category": "technology",
#         "guid": False
#     },
#     {
#         "url": "http://rss.cnn.com/rss/cnn_health.rss",
#         "category": "Health",
#         "guid": True
#     },
#     {
#         "url": "http://rss.cnn.com/rss/cnn_showbiz.rss",
#         "category": "Entertainment",
#         "guid": True
#     },
#     {
#         "url": "http://rss.cnn.com/rss/cnn_us.rss",
#         "category": "None",
#         "guid": True
#     }
# ]