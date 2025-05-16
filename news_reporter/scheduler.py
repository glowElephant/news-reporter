from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import TIMEZONE
from .main import fetch_and_send  # 아래에서 구현할 fetch_and_send 함수

def start_scheduler():
    """백그라운드 스케줄러 기동 (매일 09:00)"""
    sched = BackgroundScheduler(timezone=TIMEZONE)
    sched.add_job(fetch_and_send, CronTrigger(hour=9, minute=0))
    sched.start()
