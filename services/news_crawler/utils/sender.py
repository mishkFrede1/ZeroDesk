import requests
import os
from utils.logger import get_logger

ANALYZER_API = os.getenv('ANALYZER_API')
logger = get_logger()

def send_to_analyzer(article_data):
    try:
        response = requests.post(ANALYZER_API, json=article_data)
        response.raise_for_status()
        logger.info(f"[MAIN PARSER] {response}")
        return True, response

    except Exception as e:
        logger.error(f"[ERROR]: {e}")
        return False, e
