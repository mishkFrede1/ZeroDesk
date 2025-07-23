import requests
import os

from logger import get_logger

ANALYZER_API = os.environ["ANALYZER_API"]
logger = get_logger()

def send_to_analyzer(article_data):
    try:
        response = requests.post(ANALYZER_API, json=article_data)
        response.raise_for_status()
        logger.info(f"[MAIN PARSER] {response}")
        return True

    except Exception as e:
        print("[ERROR]:", e)
        return False
