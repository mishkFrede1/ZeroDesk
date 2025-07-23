from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

scheduler = BackgroundScheduler()

def start_scheduler(function):
    scheduler.add_job(
        func=function,
        trigger=IntervalTrigger(hours=2),
        id="cnn_parser_job",
        name="Парсинг каждый час",
        replace_existing=True
    )

    scheduler.start()
    function()

    # Автоматическая остановка при завершении работы приложения
    atexit.register(lambda: scheduler.shutdown())