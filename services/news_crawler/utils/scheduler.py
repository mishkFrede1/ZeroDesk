from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

scheduler = BackgroundScheduler()

def start_scheduler(function, hours, minutes=0, seconds=0):
    scheduler.add_job(
        func=function,
        trigger=IntervalTrigger(hours=hours, minutes=minutes, seconds=seconds),
        id="parsers_id",
        name="parsers_name",
        replace_existing=True
    )

    scheduler.start()
    function()

    # Автоматическая остановка при завершении работы приложения
    atexit.register(lambda: scheduler.shutdown())