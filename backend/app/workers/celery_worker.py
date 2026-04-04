from celery import Celery
from app.config import settings

celery_app = Celery(
    "gigshield",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,
    beat_schedule={
        "monitor-triggers-every-5-min": {
            "task": "app.workers.tasks.monitor_all_city_triggers",
            "schedule": 300.0,  # every 5 minutes
        },
        "update-fraud-scores-hourly": {
            "task": "app.workers.tasks.refresh_fraud_scores",
            "schedule": 3600.0,
        },
    },
)
