from parsers.main_parser import parse_all_sources
from send_to_analyzer import send_to_analyzer
from scheduler import start_scheduler
import time


def run():
    try:
        articles = parse_all_sources(0)
        for article in articles:
            print("[INFO] Sent article to analyzer:", article["guid"])
            send_to_analyzer(article)
            print("[INFO] Analyzer article:", article["guid"])
            time.sleep(1)
        print(f"[MAIN_PARSER] Parsed: {len(articles)} articles")

    except Exception as e:
        print("[ERROR]:", e)


if __name__ == "__main__":
    print("[SCHEDULER] Scheduler started. Press Ctrl+C to exit.")
    start_scheduler(run)

    try:
        while True:
            time.sleep(1)  # Держим процесс живым
    except KeyboardInterrupt:
        print("[SCHEDULER] Scheduler stopped, KeyboardInterrupt.")