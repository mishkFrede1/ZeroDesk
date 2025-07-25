import time

from utils.logger import get_logger
from parsers.main_parser import parse_all_sources
from utils.sender import send_to_analyzer
from utils.scheduler import start_scheduler
from database.db import init_db

logger = get_logger()
init_db()

def run():
    try:
        articles = parse_all_sources(0)
        length = len(articles)
        logger.info(f"[MAIN PARSER] Start sending: {length} articles")
        for article in articles:
            logger.info(f"[MAIN PARSER] Sent article to analyzer: {article['guid']}")
            r = send_to_analyzer(article)
            if not r[0]: length -= 1
            else:
                logger.info(f"[MAIN PARSER] Analyzed article: {article['guid']}")
            time.sleep(1)
        logger.info(f"[MAIN PARSER] Parsed and sent: {length} articles")

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    logger.info("[SCHEDULER] Scheduler started. Press Ctrl+C to exit.")
    start_scheduler(run, 2)

    try:
        while True:
            time.sleep(1)  # Держим процесс живым
    except KeyboardInterrupt:
        logger.info("[SCHEDULER] Scheduler stopped, KeyboardInterrupt.")