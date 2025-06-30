import requests
from dotenv import dotenv_values

from logger import get_logger

ANALYZER_API = dotenv_values('.env')["ANALYZER_API"]
logger = get_logger()

def send_to_analyzer(article_data):
    try:
        response = requests.post(ANALYZER_API, json=article_data)
        response.raise_for_status()
        logger.info(f"{response}")
        return True

    except Exception as e:
        print("[ERROR]:", e)
        return False
